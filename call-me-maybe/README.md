*This project has been created as part of the 42 curriculum by ramaroud.*

# call me maybe

## Description

Turns a natural-language request into a structured function call, using the
small `Qwen/Qwen3-0.6B` model.

```
"What is the sum of 40 and 2?"  →  {"name": "fn_add_numbers", "parameters": {"a": 40.0, "b": 2.0}}
```

The model is never trusted to write JSON. The program writes the JSON structure
itself and only lets the model fill the values, masking every token that would
break the syntax or the schema. The output is therefore **always** valid JSON.

## Instructions

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

| Command | Effect |
| --- | --- |
| `make install` | `uv sync` (installs pydantic, numpy, the SDK, lint tools) |
| `make run` | `uv run python -m src` |
| `make debug` | Run under `pdb` |
| `make test` | Offline tests (fake model, no download) |
| `make lint` / `make lint-strict` | flake8 + mypy |
| `make clean` | Remove caches and `data/output/` |

```
uv run python -m src [--functions_definition <file>] [--input <file>]
                     [--output <file>] [--model <model-id>]
```

Defaults: inputs in `data/input/`, output in
`data/output/function_calling_results.json`, model `Qwen/Qwen3-0.6B`.

## Example usage

```console
$ make run
[1/11] fn_add_numbers {'a': 2.0, 'b': 3.0}
[2/11] fn_greet {'name': 'shrek'}
...
11 call(s) written to 'data/output/function_calling_results.json' in 81.6s

$ uv run python -m src --input broken.json
error: 'broken.json' is not valid JSON (line 1: Expecting value)
```

## Project structure

| File | Goal |
| --- | --- |
| `src/__main__.py` | Entry point for `python -m src`: parses the options, processes each prompt, writes the output |
| `src/models.py` | pydantic models of the input and output records, and the project exceptions |
| `src/io.py` | Reads the input files and writes the output file |
| `src/pipeline.py` | Loads the SDK model, builds the chat prompt, runs the two passes for each prompt |
| `src/constraints.py` | JSON rules for values; turns a function into a skeleton; says which values are valid |
| `src/decoding.py` | Constrained decoding loop: pick the candidate tokens, mask logits, pick a token, repeat |
| `src/vocab.py` | Loads `vocab.json` and precomputes token pools |
| `tests/` | Offline tests, with a scripted fake model |
| `llm_sdk/` | Provided SDK (uv workspace member, CPU torch) |

## Algorithm explanation

Each prompt goes through **two constrained passes**.

**1. Choose the function.** The assistant answer is pre-filled with
`{"name": "`. The model then writes the name, but a token is only allowed if
the text stays a prefix of a declared function name. It cannot invent one.

**2. Fill the arguments.** The chosen function becomes a *skeleton*: fixed
text written by the program, and *slots* filled by the model.

```python
['{"a": ', Slot('number'), ', "b": ', Slot('number'), '}']
```

**Decoding loop, for each slot:**

1. Take the candidate tokens for this type (54 numeric tokens made of digits,
   `.` and `-`, or ~147k string-safe tokens), plus tokens that can close the
   slot. Exponents such as `1e5` are not supported.
2. Keep only the tokens that leave the value *viable*: `-5.` is still a
   possible number, `-5.x` is not.
3. Set every other logit to `-inf`, take the `argmax`.
4. Stop when a token reaches the text that follows the slot.

The result is parsed with `json.loads`; `number` values are stored as floats.

## Design decisions

- **Two passes**: the argument skeleton depends on the chosen function.
- **Program writes punctuation, model writes values**: keys and braces can
  never be missing or misspelled.
- **String slots include their opening `"`**: the tokenizer naturally merges
  `"shrek`, so the model sees text it knows.
- **Token pools precomputed once**: avoids scanning 151k tokens at every step.
- **pydantic at the boundaries**: bad input is rejected early with a clear
  message.
- **A failed prompt never stops the run**: it logs a warning and writes a
  schema-valid call with neutral values.

## Performance analysis

Qwen3-0.6B on CPU, 11 prompts.

| Metric | Result |
| --- | --- |
| Accuracy (public and private sets) | 10/11 (90.9%) |
| Valid, schema-compliant JSON | 100% (guaranteed by construction) |
| Time | ~82 s on CPU, ~18 s on CUDA (limit: 300 s) |

Decoding is greedy, so runs are deterministic. The one miss is a model choice,
not a format error: on "Replace all numbers…" it swaps `regex` and
`replacement`.

## Challenges faced

- **Token boundaries**: encoding fixed text alone splits tokens unnaturally.
  `append_literal` re-encodes the last token together with the new text.
- **Tokens crossing a slot's edge**: a token like `)",` ends a value and starts
  the next literal. `_advance` tracks where each character lands.
- **JSON escapes**: the model writes JSON source, so `\"` is allowed but a bare
  `"` ends the string. A token must not cut an escape in half.
- **Repetition guard bug**: a first loop guard turned `10000` into `10`. It was
  replaced by a simple length cap.
- **Partial UTF-8 tokens**: cleaned with `to_clean_str`.

## Testing strategy

Points 1 and 2 are automated in `tests/` (`make test`); 3 and 4 are run by hand.

1. **Offline decoder tests** with a fake model (via the `LogitsProvider`
   protocol): empty strings, Windows paths, regexes, quotes, unicode, negative
   and decimal numbers, booleans, overlong numbers, function names that prefix
   one another, and the fallback on an unsupported type.
2. **Error cases**: missing files, invalid JSON, wrong shapes, empty arrays,
   missing `prompt`, duplicate functions, blank options, unwritable output.
3. **Real-model edge cases**: large numbers, empty prompts, no matching
   function.
4. **End-to-end**: the provided moulinette on the public and private sets.

## Resources

- [Efficient Guided Generation for LLMs](https://arxiv.org/abs/2307.09702)
- [Grammar-Constrained Decoding for Structured NLP Tasks](https://arxiv.org/abs/2305.13971)
- [Neural Machine Translation of Rare Words with Subword Units (BPE)](https://arxiv.org/abs/1508.07909)
- [Hugging Face: tokenizers](https://huggingface.co/docs/transformers/tokenizer_summary)
  and [generation strategies](https://huggingface.co/docs/transformers/generation_strategies)
- [RFC 8259 — JSON](https://datatracker.ietf.org/doc/html/rfc8259)
- [pydantic](https://docs.pydantic.dev/) ·
  [uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) ·
  [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B)

### Use of AI

AI was used to understand byte-level BPE and logit masking, to draft
docstrings and this README, and to build the offline test harness and error
tests. The architecture (two passes, skeleton, slots owning their punctuation)
was designed by hand. The one AI fix kept without a test (the repetition
guard) caused the `10000 → 10` bug.
