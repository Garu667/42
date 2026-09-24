import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from src import io as files
from src.__main__ import DEFAULT_MODEL, parse_arguments, run
from src.models import FunctionCall, InputError, OutputError


class InputFilesTest(unittest.TestCase):
    """Every bad input file is rejected with an InputError."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, content: Any, raw: bool = False) -> Path:
        path = self.dir / "input.json"
        path.write_text(content if raw else json.dumps(content))
        return path

    def assert_rejected(self, loader: Any, path: Path, message: str) -> None:
        with self.assertRaises(InputError) as caught:
            loader(path)
        self.assertIn(message, str(caught.exception))

    def test_missing_file(self) -> None:
        self.assert_rejected(files.load_functions, self.dir / "nope.json",
                             "does not exist")

    def test_invalid_json(self) -> None:
        self.assert_rejected(files.load_tests, self.write("[{", raw=True),
                             "is not valid JSON")

    def test_functions_not_an_array(self) -> None:
        self.assert_rejected(files.load_functions, self.write({"name": "f"}),
                             "non-empty JSON array")

    def test_functions_empty(self) -> None:
        self.assert_rejected(files.load_functions, self.write([]),
                             "non-empty JSON array")

    def test_function_without_name(self) -> None:
        self.assert_rejected(files.load_functions,
                             self.write([{"parameters": {}}]),
                             "is not a valid function")

    def test_duplicate_function(self) -> None:
        self.assert_rejected(files.load_functions,
                             self.write([{"name": "f"}, {"name": "f"}]),
                             "declares 'f' twice")

    def test_prompt_missing(self) -> None:
        self.assert_rejected(files.load_tests, self.write([{"text": "hi"}]),
                             "no usable 'prompt'")

    def test_valid_files(self) -> None:
        functions = files.load_functions(self.write([{"name": "f"}]))
        self.assertEqual(functions[0].parameters, {})
        tests = files.load_tests(self.write([{"prompt": "hi"}]))
        self.assertEqual(tests[0].prompt, "hi")

    def test_write_round_trip(self) -> None:
        path = self.dir / "out" / "results.json"
        call = FunctionCall(prompt="p", name="f", parameters={"a": 1.0})
        files.write_results(path, [call])
        self.assertEqual(json.loads(path.read_text()), [call.model_dump()])

    def test_unwritable_output(self) -> None:
        blocker = self.write([])
        with self.assertRaises(OutputError):
            files.write_results(blocker / "results.json", [])


class CommandLineTest(unittest.TestCase):
    """Options and the early exit on a bad input."""

    def test_defaults(self) -> None:
        self.assertEqual(parse_arguments([]).model, DEFAULT_MODEL)

    def test_blank_option(self) -> None:
        with self.assertRaises(InputError):
            parse_arguments(["--input", "  "])

    def test_bad_input_exits_before_loading_the_model(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = run(["--input", "missing.json"])
        self.assertEqual(code, 1)
        self.assertIn("does not exist", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
