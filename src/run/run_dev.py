from src.run.app import *


def main():
    app = build_app(env=ENV_DEV)
    app.run(host="0.0.0.0", debug=True)


if __name__ == '__main__':
    main()
