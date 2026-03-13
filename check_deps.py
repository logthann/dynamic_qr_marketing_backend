import importlib

packages = ["fastapi", "uvicorn", "sqlalchemy", "pydantic", "dotenv"]

for p in packages:
    try:
        m = importlib.import_module(p)
        v = getattr(m, "__version__", getattr(m, "VERSION", "(no __version__)") )
        print(p, v)
    except Exception as e:
        print(p, "IMPORT_ERROR", type(e).__name__, str(e))

