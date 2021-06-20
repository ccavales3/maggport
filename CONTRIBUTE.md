# Local Development

## Prerequisites

Utilize [pip-tools](https://github.com/jazzband/pip-tools) to generate development and production dependencies.

```sh
pip install pip-tools
```

## Testing

A `__main__` file is available to test your code while developing.

```sh
python -m maggport --host <host> --port <port> --db <db> --collection <collection> --pipeline <pipeline>
```

### Building local package

Build your package locally.

```sh
python install setup.py
```

Test by calling the module.

```sh
maggport --host <host> --port <port> --db <db> --collection <collection> --pipeline <pipeline>
```
