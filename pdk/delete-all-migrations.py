import os

for root, dictionaries, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
    if "venv" not in root and root[-10:] == "migrations":
        for file in files:
            if file != "__init__.py":
                os.remove(os.path.join(root, file))
                print(os.path.join(root, file))
