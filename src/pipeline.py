import json
import sys
from typing import Any, Protocol

from src.constraints import NEUTRAL_VALUES, Segment, Slot, build_skeleton
from src.decoding import Encoder, LogitsProvider, fill_skeleton
from src.models import (
    CallMeMaybeError,
    DecodingError,
    FunctionCall,
    FunctionDefinition,
    ModelError,
)
from src.vocab import Vocab

_SYSTEM = (
    "You translate a user request into a single function call. "
    "You answer with one JSON object and nothing else: the key \"name\" "
    "holds the function to call, the key \"parameters\" holds its "
    "arguments. Argument values are copied verbatim from the request, "
    "never invented and never computed: you provide the call, not the "
    "result."
)

_CHAT_TEMPLATE = (
    "<|im_start|>system\n{system}<|im_end|>\n"
    "<|im_start|>user\n{user}<|im_end|>\n"
    "<|im_start|>assistant\n<think>\n\n</think>\n\n"
)

NAME_OPENING = '{"name": "'


class SdkModel(LogitsProvider, Protocol):
    """The part of ``Small_LLM_Model`` this project relies on."""

    def encode(self, text: str) -> Any:
        """Return the token ids of a text, as a 2-D tensor."""
        ...

    def get_path_to_vocab_file(self) -> str:
        """Return the local path of the vocabulary file."""
        ...


def load_model(model_name: str) -> SdkModel:
    """Instantiate the SDK wrapper.

    Raises ModelError if the package is missing or the model fails.
    """
    try:
        from llm_sdk import Small_LLM_Model
    except ImportError as err:
        raise ModelError(
            "package 'llm_sdk' is not importable, run 'uv sync' first"
        ) from err
    try:
        return Small_LLM_Model(model_name=model_name)
    except Exception as err:
        raise ModelError(f"cannot load model '{model_name}': {err}") from err


def build_encoder(model: SdkModel) -> Encoder:
    """Return the text-to-ids function used for prompts and literals."""
    return lambda text: [int(token_id) for token_id in model.encode(text)[0]]


def describe_function(function: FunctionDefinition) -> str:
    """Render one function as a single readable signature line."""
    arguments = ", ".join(
        f"{name}: {spec.type}" for name, spec in function.parameters.items()
    )
    description = f": {function.description}" if function.description else ""
    return f"- {function.name}({arguments}){description}"


def build_prompt(question: str, functions: list[FunctionDefinition]) -> str:
    """Build the full text the model reads, up to the assistant turn."""
    catalogue = "\n".join(describe_function(fn) for fn in functions)
    user = (
        f"Available functions:\n{catalogue}\n\n"
        f"Request: {question}\n\n"
        "Pick the one function that answers this request and fill its "
        "arguments with the values taken from the request."
    )
    return _CHAT_TEMPLATE.format(system=_SYSTEM, user=user)


def parameters_opening(name: str) -> str:
    """Return the assistant prefix leading straight to the arguments."""
    return f'{NAME_OPENING}{name}", "parameters": '


def choose_function(
    model: LogitsProvider,
    vocab: Vocab,
    functions: list[FunctionDefinition],
    encode: Encoder,
    prompt_text: str,
) -> FunctionDefinition:
    """Pick the function name, constrained to the declared ones."""
    names = [fn.name for fn in functions]
    skeleton: list[Segment] = [Slot(kind="enum", choices=names), '"']
    input_ids = encode(prompt_text + NAME_OPENING)
    produced = fill_skeleton(model, vocab, input_ids, skeleton, encode)
    return functions[names.index(produced[:-1])]


def extract_parameters(
    model: LogitsProvider,
    vocab: Vocab,
    function: FunctionDefinition,
    encode: Encoder,
    prompt_text: str,
) -> dict[str, Any]:
    """Fill the arguments of the chosen function and parse them.

    Raises DecodingError if the produced object cannot be parsed.
    """
    input_ids = encode(prompt_text + parameters_opening(function.name))
    skeleton = build_skeleton(function)
    body = fill_skeleton(model, vocab, input_ids, skeleton, encode)
    try:
        parameters = json.loads(body)
    except json.JSONDecodeError as err:
        raise DecodingError(
            f"produced arguments are not JSON: {body}"
        ) from err
    if not isinstance(parameters, dict):
        raise DecodingError(f"produced arguments are not an object: {body}")
    for name, spec in function.parameters.items():
        if spec.type == "number" and type(parameters.get(name)) is int:
            parameters[name] = float(parameters[name])
    return parameters


def fallback_call(question: str, function: FunctionDefinition) -> FunctionCall:
    """Build a schema-valid call with neutral values, for a failed prompt."""
    parameters = {
        name: NEUTRAL_VALUES.get(spec.type, "")
        for name, spec in function.parameters.items()
    }
    return FunctionCall(prompt=question, name=function.name,
                        parameters=parameters)


def process_prompt(
    model: LogitsProvider,
    vocab: Vocab,
    functions: list[FunctionDefinition],
    encode: Encoder,
    question: str,
) -> FunctionCall:
    """Turn one request into one call, falling back instead of raising."""
    prompt_text = build_prompt(question, functions)
    chosen = functions[0]
    try:
        chosen = choose_function(model, vocab, functions, encode, prompt_text)
        parameters = extract_parameters(
            model, vocab, chosen, encode, prompt_text
        )
        return FunctionCall(prompt=question, name=chosen.name,
                            parameters=parameters)
    except CallMeMaybeError as err:
        print(f"  warning: {err}", file=sys.stderr)
        return fallback_call(question, chosen)
