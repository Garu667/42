import argparse
import sys
import time

from pydantic import BaseModel, ValidationError, field_validator

from src.io import load_functions, load_tests, write_results
from src.models import CallMeMaybeError, FunctionCall, InputError
from src.pipeline import build_encoder, load_model, process_prompt
from src.vocab import load_vocab

DEFAULT_FUNCTIONS = "data/input/functions_definition.json"
DEFAULT_INPUT = "data/input/function_calling_tests.json"
DEFAULT_OUTPUT = "data/output/function_calling_results.json"
DEFAULT_MODEL = "Qwen/Qwen3-0.6B"


class Options(BaseModel):
    """The command line options, once validated."""

    functions_definition: str = DEFAULT_FUNCTIONS
    input: str = DEFAULT_INPUT
    output: str = DEFAULT_OUTPUT
    model: str = DEFAULT_MODEL

    @field_validator("functions_definition", "input", "output", "model")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        """Reject an option given as an empty or blank string."""
        if not value.strip():
            raise ValueError("must not be empty")
        return value


def parse_arguments(argv: list[str] | None = None) -> Options:
    """Parse the command line into validated options.

    Raises InputError if an option holds an unusable value.
    """
    parser = argparse.ArgumentParser(
        prog="python -m src",
        description="Translate natural language prompts into function calls.",
    )
    parser.add_argument("--functions_definition", default=DEFAULT_FUNCTIONS,
                        help="JSON file describing the callable functions")
    parser.add_argument("--input", default=DEFAULT_INPUT,
                        help="JSON file holding the prompts to process")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="where the resulting calls are written")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="model identifier passed to the SDK")
    namespace = parser.parse_args(argv)
    try:
        return Options.model_validate(vars(namespace))
    except ValidationError as err:
        first = err.errors()[0]
        raise InputError(
            f"option '--{first['loc'][0]}' is invalid: {first['msg']}"
        ) from err


def run(argv: list[str] | None = None) -> int:
    """Load the inputs, process every prompt, write the results."""
    try:
        arguments = parse_arguments(argv)
        functions = load_functions(arguments.functions_definition)
        tests = load_tests(arguments.input)
        model = load_model(arguments.model)
        vocab = load_vocab(model.get_path_to_vocab_file())
        encode = build_encoder(model)

        started = time.monotonic()
        results: list[FunctionCall] = []
        for index, test in enumerate(tests, start=1):
            call = process_prompt(model, vocab, functions, encode, test.prompt)
            results.append(call)
            print(f"[{index}/{len(tests)}] {call.name} {call.parameters}")

        write_results(arguments.output, results)
    except CallMeMaybeError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1

    elapsed = time.monotonic() - started
    print(f"{len(results)} call(s) written to '{arguments.output}' "
          f"in {elapsed:.1f}s")
    return 0


def main() -> int:
    """Run the program, turning any escaping failure into an exit code."""
    try:
        return run()
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        return 130
    except Exception as err:
        print(f"error: unexpected failure: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
