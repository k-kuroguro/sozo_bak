from web import create_app


def main():
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)


if __name__ == "__main__":
    main()
