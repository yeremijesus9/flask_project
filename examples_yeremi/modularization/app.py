try:
    from . import create_app
except ImportError:
    import os
    import sys

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))

    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

    from examples_yeremi.modularization import create_app


app = create_app()


if __name__ == "__main__":
    print("\n✅ Panel de ejemplos arrancado en http://127.0.0.1:5002")
    print("Puedes ejecutarlo con:")
    print("  python examples_yeremi/modularization/app.py")
    print("  python -m examples_yeremi.modularization.app")
    app.run(debug=True, port=5002)
