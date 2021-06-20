# Maintainers

Contains steps on how to publish to PyPI

## Prerequisite

```sh
pip install twine
```

## Build and test package

```sh
python setup.py sdist bdist_wheel
```

Validate locally built package

```sh
twine check dist/*
```

## Publish to TestPyPI for testing

```sh
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Install published package to TestPyPI

```sh
pip install -i https://test.pypi.org/simple/ maggport==1.0.0
```
