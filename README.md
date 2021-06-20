# maggport

![Coverage Report](./badges/coverage.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A mongodb aggregate export CLI tool

## Overview

maggport is a python CLI tool designed to bridge the gap of exporting aggregate pipeline(s) in mongodb. What used to be feat accomplished by writing your own shell script or exporting a custom mongodb collection to csv or JSON generated by running an aggregate pipeline can now be achieved by this tool.

## Installation

```sh
pip install maggport
```

## Usage

| Arguments             | Description                       |
| --------------------- | --------------------------------- |
| -c/--collection       | Collection of database            |
| -d/--db               | Database to connect               |
| -h/--host             | Hostname of mongodb instance      |
| --no-allow-disk-use   | Don\'t allow disk use             |
| -o/--out              | Output file                       |
| -p/--port             | Port of mongodb instance          |
| -q/--pipeline         | Pipeline to run                   |
| -f/--pipeline-path    | Path of pipeline if saved in file |

---
**host**: sample_host  
**port**: 8080  
**db**: food  
**collection**: fruits

```json
[
    {
        "name": "apple",
        "origin":  "usa",
        "price": 5
    },
    {
        "name": "apple",
        "origin":  "italy",
        "price": 3
    },
    {
        "name": "mango",
        "origin":  "malaysia",
        "price": 3
    }
]
```

## Example 1

Passing pipeline as a parameter and output results in terminal.

```sh
maggport --host sample_host --port 8080 --db food --collection fruits --pipeline '[{"$group": {"_id": "$name", "count": {"$sum": 1}}}, {"$match": {"count": {"$gt": 1}}}]'
```

**Output**:

```json
[
    {
        "_id":"apple",
        "count": 3
    }
]
```

## Example 2

Passing pipeline as a file and output results in terminal.

**pipeline.txt**

```txt
[
    {"$group": {"_id": "$name", "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}}
]
```

```sh
maggport --host sample_host --port 8080 --db food --collection fruits --pipeline-path pipeline.txt
```

**Output**:

```json
[
    {
        "_id":"apple",
        "count": 3
    }
]
```

## Example 3

Export results as csv file.

**pipeline.txt**

```txt
[
    {"$group": {"_id": "$name", "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}}
]
```

```sh
maggport --host sample_host --port 8080 --db food --collection fruits --pipeline-path pipeline.txt --out test_results.csv
```

**Output**:

**test_results.csv**

![image](https://user-images.githubusercontent.com/8203778/122682899-0b699580-d1ca-11eb-95e1-5ded3e1228d6.png)

## Bugs/Request

Please submit an issue in [GitHub](https://github.com/ccavales3/maggport/issues/new)

## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue in the [maggport dashboard](https://github.com/ccavales3/maggport/issues/new), or any other method with the owner(s)(info at the bottom of this README) of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

For more information about how to contribute, take a look at [CONTRIBUTE.md](./CONTRIBUTE.md)

## Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/

## Maintainers

[@ccavales3](https://github.com/ccavales3)
