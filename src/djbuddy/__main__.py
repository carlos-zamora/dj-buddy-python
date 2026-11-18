"""Allow ``python -m djbuddy`` as an alternative to the ``djbuddy`` console script."""

from djbuddy.cli import app

if __name__ == "__main__":
    app(prog_name="djbuddy")
