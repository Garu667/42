import contextlib
import io
import unittest
from typing import Any

from src.constraints import Slot, build_skeleton, is_json_string_chunk
from src.models import (
    FunctionDefinition,
    ParameterSpec,
    UnsupportedTypeError,
)
from src.pipeline import (
    NAME_OPENING,
    build_prompt,
    choose_function,
    extract_parameters,
    parameters_opening,
    process_prompt,
)

from tests.fakes import GreedyEncoder, ScriptedModel, make_vocab

VOCAB = make_vocab()
ENCODE = GreedyEncoder(VOCAB)
PROMPT = "Q"


def function(fn_name: str, /, **types: str) -> FunctionDefinition:
    """Build a function whose parameters have the given types."""
    return FunctionDefinition(
        name=fn_name,
        parameters={key: ParameterSpec(type=kind)
                    for key, kind in types.items()},
    )


def decode(fn: FunctionDefinition, body: str) -> dict[str, Any]:
    """Run the argument pass with a model that wants to write ``body``."""
    target = PROMPT + parameters_opening(fn.name) + body
    model = ScriptedModel(VOCAB, target)
    return extract_parameters(model, VOCAB, fn, ENCODE, PROMPT)


class StringSlotTest(unittest.TestCase):
    """String values, written as JSON source by the model."""

    def test_plain_word(self) -> None:
        fn = function("fn_greet", name="string")
        self.assertEqual(decode(fn, '{"name": "shrek"}'), {"name": "shrek"})

    def test_empty(self) -> None:
        fn = function("fn_greet", name="string")
        self.assertEqual(decode(fn, '{"name": ""}'), {"name": ""})

    def test_windows_path(self) -> None:
        fn = function("fn_open", path="string")
        self.assertEqual(decode(fn, r'{"path": "C:\\Users\\x"}'),
                         {"path": "C:\\Users\\x"})

    def test_regex(self) -> None:
        fn = function("fn_sub", regex="string")
        self.assertEqual(decode(fn, r'{"regex": "\\d+"}'),
                         {"regex": "\\d+"})

    def test_escaped_quotes(self) -> None:
        fn = function("fn_say", s="string")
        self.assertEqual(decode(fn, r'{"s": "say \"hi\""}'),
                         {"s": 'say "hi"'})

    def test_unicode(self) -> None:
        fn = function("fn_say", s="string")
        self.assertEqual(decode(fn, '{"s": "héllo €"}'), {"s": "héllo €"})


class ScalarSlotTest(unittest.TestCase):
    """Numbers, integers and booleans."""

    def test_numbers_become_floats(self) -> None:
        fn = function("fn_add", a="number", b="number")
        self.assertEqual(decode(fn, '{"a": 40, "b": -2.5}'),
                         {"a": 40.0, "b": -2.5})
        self.assertIsInstance(decode(fn, '{"a": 40, "b": 1}')["a"], float)

    def test_integer(self) -> None:
        fn = function("fn_count", n="integer")
        self.assertEqual(decode(fn, '{"n": 345}'), {"n": 345})

    def test_booleans(self) -> None:
        fn = function("fn_flag", on="boolean")
        self.assertEqual(decode(fn, '{"on": true}'), {"on": True})
        self.assertEqual(decode(fn, '{"on": false}'), {"on": False})

    def test_mixed_types(self) -> None:
        fn = function("fn_mix", s="string", n="number", b="boolean")
        self.assertEqual(decode(fn, '{"s": "hello", "n": 0.5, "b": true}'),
                         {"s": "hello", "n": 0.5, "b": True})

    def test_no_parameters(self) -> None:
        self.assertEqual(decode(function("fn_now"), "{}"), {})

    def test_endless_number_is_cut(self) -> None:
        fn = function("fn_sqrt", a="number")
        value = decode(fn, '{"a": ' + "1" * 40 + "}")["a"]
        self.assertEqual(value, float("1" * 24))

    def test_model_wanting_garbage_still_gives_a_number(self) -> None:
        fn = function("fn_sqrt", a="number")
        self.assertIsInstance(decode(fn, '{"a": abc}')["a"], float)


class ChooseFunctionTest(unittest.TestCase):
    """The name pass, including names that prefix one another."""

    FUNCTIONS = [function("fn_add", a="number"),
                 function("fn_add_numbers", a="number", b="number")]

    def choose(self, name: str) -> str:
        target = PROMPT + NAME_OPENING + name + '"'
        model = ScriptedModel(VOCAB, target)
        return choose_function(model, VOCAB, self.FUNCTIONS, ENCODE,
                               PROMPT).name

    def test_short_name(self) -> None:
        self.assertEqual(self.choose("fn_add"), "fn_add")

    def test_long_name(self) -> None:
        self.assertEqual(self.choose("fn_add_numbers"), "fn_add_numbers")


class ProcessPromptTest(unittest.TestCase):
    """Both passes chained, and the fallback on failure."""

    def run_prompt(self, fn: FunctionDefinition, body: str) -> Any:
        question = "Greet shrek"
        target = (build_prompt(question, [fn])
                  + parameters_opening(fn.name) + body)
        model = ScriptedModel(VOCAB, target)
        with contextlib.redirect_stderr(io.StringIO()):
            return process_prompt(model, VOCAB, [fn], ENCODE, question)

    def test_full_call(self) -> None:
        call = self.run_prompt(function("fn_greet", name="string"),
                               '{"name": "shrek"}')
        self.assertEqual((call.name, call.parameters),
                         ("fn_greet", {"name": "shrek"}))

    def test_unsupported_type_falls_back(self) -> None:
        call = self.run_prompt(function("fn_sort", items="array"),
                               '{"items": []}')
        self.assertEqual((call.name, call.parameters),
                         ("fn_sort", {"items": ""}))


class GrammarTest(unittest.TestCase):
    """Skeletons and the JSON string rule."""

    def test_skeleton_alternates(self) -> None:
        fn = function("fn_add", a="number", s="string")
        self.assertEqual(build_skeleton(fn), [
            '{"a": ', Slot(kind="number"),
            ', "s":', Slot(kind="string", opening=' "'),
            '"}',
        ])

    def test_unsupported_type(self) -> None:
        with self.assertRaises(UnsupportedTypeError):
            build_skeleton(function("fn_sort", items="array"))

    def test_json_string_chunks(self) -> None:
        for text in ("abc", "", r"\"", r"\\", r"\u00e9", "é"):
            self.assertTrue(is_json_string_chunk(text), text)
        for text in ('"', "\\", r"\u00", r"\x", "\n"):
            self.assertFalse(is_json_string_chunk(text), text)

    def test_vocab_pools(self) -> None:
        texts = {VOCAB.text_of(tid) for tid in VOCAB.numeric}
        self.assertIn("40", texts)
        self.assertIn("-", texts)
        self.assertNotIn("e", texts)
        self.assertNotIn('"', {VOCAB.text_of(t) for t in VOCAB.string_safe})
        self.assertEqual({VOCAB.text_of(t) for t in VOCAB.prefixes_of(' "')},
                         {" ", ' "'})


if __name__ == "__main__":
    unittest.main()
