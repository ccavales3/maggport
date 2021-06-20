# Local Development

## Prerequisites

Utilize [pip-tools](https://github.com/jazzband/pip-tools) to generate development and production dependencies.

```sh
pip install pip-tools
```

Before modifying the code base, make sure to set up your local environment for development. In the root folder, run the below commands:

Generate the full list of dependencies in requirements.txt and dev-requirements.txt needed to develop the package:

```sh
make compile-all
```

Install the dependencies compiled by the previous command:

```sh
make install-dev
```

Setup the git hook scripts:

```
pre-commit install
pre-commit install --hook-type pre-push
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
