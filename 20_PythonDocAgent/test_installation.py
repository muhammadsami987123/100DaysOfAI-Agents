import importlib


def test_imports() -> None:
	for mod in [
		"openai",
		"requests",
		"bs4",
		"rich",
		"pyperclip",
	]:
		importlib.import_module(mod)


if __name__ == "__main__":
	test_imports()
	print("OK")
