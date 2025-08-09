import importlib

REQUIRED = [
    "flask",
    "dotenv",
    "openai",
    "pypdf",
    "requests",
    "tiktoken",
    "numpy",
    "trafilatura",
    "docx",
]

def test_imports():
    for mod in REQUIRED:
        importlib.import_module(mod)

if __name__ == "__main__":
    test_imports()
    print("All imports OK")
