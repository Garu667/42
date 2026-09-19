from src.vocab import load_vocab
v = load_vocab(model.get_path_to_vocab_file())
print(len(v.texts), repr(v.text_of(220)))   # ~151k, et un espace
