## Requirements

### Production

```sh
$ uv -V
uv 0.4.30 (61ed2a236 2024-11-04)
```

### Development

In addition to the requirements for production,

```sh
$ protoc --version
libprotoc 28.3
```

## Running in production

```sh
$ uv run src/run.py
```

## Running in development

### For web server

Start the web server in development, stubbing communication from the local app.

```sh
$ uv run src/run_dev.py
```
