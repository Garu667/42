# call-me-maybe
Introduction to function calling in LLMs

```
src/
├── __init__.py
├── __main__.py      # main() + sys.exit sous if __name__
├── parsing.py       # argparse + pydantic + lecture JSON
├── prompt.py        # construction du prompt (noms + descriptions)
├── constraints.py   # allowed(état) → tokens autorisés
├── decoding.py      # cache vocab + squelette + boucle
└── errors.py        # exceptions + codes de sortie
```
