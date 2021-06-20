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

```sh
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

## Pull Request Process

1. Run `make compile-all` if there is any new dependencies added.
1. `make quality` and `make test` should both pass before filing a PR.
1. Increase the version numbers in setup.py. The versioning scheme we use is [SemVer](http://semver.org/).
1. For every changes or new feature added, make sure that it's covered by test(see package json for test framework used or use other components as examples.
1. Update the README.md with details of changes to the interface.
