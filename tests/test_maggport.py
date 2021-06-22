"""
This file unittests maggport.py file
"""
import json
import pathlib
from unittest import mock
from unittest.mock import mock_open

from click.testing import CliRunner

from maggport import maggport

PIPELINE = ('['
            '{"$match": { "_id" : { "$ne" : "null"}}},'
            '{"$limit": 10}'
            ']')


def mock_get(pipeline, allowDiskUse):  # pylint: disable=W0613,C0103
    """
    Return mocked mongodb docs.
    """
    return [
        {'_id': 'dummy_id_A', 'value': 'dummy_value_A'},
        {'_id': 'dummy_id_B', 'value': 'dummy_value_B'},
    ]


@mock.patch('pymongo.MongoClient')
def test_connect_to_db(mock_db):
    """
    Should call create new mongodb instance with mocked data.
    """
    runner = CliRunner()

    result = runner.invoke(maggport.maggport, [
        '--host', 'test_host',
        '--collection', 'test_collection',
        '--db', 'test_db',
        '--port', '8080',
        '--pipeline', PIPELINE
    ])

    assert result.exit_code == 0
    mock_db.assert_called_with('test_host', 8080)


@mock.patch('json.loads')
@mock.patch('json.dumps')
@mock.patch('pymongo.collection.Collection.aggregate', side_effect=mock_get)
def test_print_results(mock_agg, mock_json_dumps, mock_json_loads):  # pylint: disable=W0613
    """
    Should call aggregate pipeline.
    Should output result to console.
    """
    runner = CliRunner()

    result = runner.invoke(maggport.maggport, [
        '--host', 'test_host',
        '--collection', 'test_collection',
        '--db', 'test_db',
        '--port', '8080',
        '--pipeline', PIPELINE
    ])

    assert result.exit_code == 0
    mock_agg.assert_called_with([{'$match': {'_id': {'$ne': 'null'}}}, {'$limit': 10}], allowDiskUse=True)
    mock_json_dumps.assert_called_with(json.loads(), indent=2)  # pylint: disable=E1120


@mock.patch('pandas.DataFrame.to_csv')
@mock.patch('pymongo.collection.Collection.aggregate', side_effect=mock_get)
def test_export_results_to_csv(mock_agg, mock_to_csv):
    """
    Should call pandas export to csv with pipeline passed as parameter.
    """
    runner = CliRunner()

    result = runner.invoke(maggport.maggport, [
        '--host', 'test_host',
        '--collection', 'test_collection',
        '--db', 'test_db',
        '--port', '8080',
        '--pipeline', PIPELINE,
        '--out', 'dummy_file.csv'
    ])

    assert result.exit_code == 0
    mock_agg.assert_called_with([{'$match': {'_id': {'$ne': 'null'}}}, {'$limit': 10}], allowDiskUse=True)
    mock_to_csv.assert_called_with('dummy_file.csv', sep=',', index=False)


@mock.patch('json.dump')
@mock.patch('builtins.open', new_callable=mock_open())
@mock.patch('pymongo.collection.Collection.aggregate', side_effect=mock_get)
def test_export_results_to_json(mock_agg, mock_open_file, mock_json_dump):  # pylint: disable=W0613
    """
    Should call pandas export to csv with pipeline passed as parameter.
    """
    # mock_open = mock.mock_open()
    runner = CliRunner()

    result = runner.invoke(maggport.maggport, [
        '--host', 'test_host',
        '--collection', 'test_collection',
        '--db', 'test_db',
        '--port', '8080',
        '--pipeline', PIPELINE,
        '--out', 'dummy_file.json'
    ])

    assert result.exit_code == 0
    mock_open_file.assert_called_with('dummy_file.json', 'w')
    mock_agg.assert_called_with([{'$match': {'_id': {'$ne': 'null'}}}, {'$limit': 10}], allowDiskUse=True)


@mock.patch('json.loads')
@mock.patch('json.dumps')
@mock.patch('pymongo.collection.Collection.aggregate', side_effect=mock_get)
def test_pass_pipeline_as_file(mock_agg, mock_json_dumps, mock_json_loads):  # pylint: disable=W0613
    """
    Should output result to console with pipeline passed as file.
    """
    runner = CliRunner()

    result = runner.invoke(maggport.maggport, [
        '--host', 'test_host',
        '--collection', 'test_collection',
        '--db', 'test_db',
        '--port', '8080',
        '--pipeline-path', f'{pathlib.Path(__file__).parent.absolute()}/resources/pipeline.txt'
    ])

    assert result.exit_code == 0
    mock_agg.assert_called_with([{'$match': {'_id': {'$ne': 'null'}}}, {'$limit': 10}], allowDiskUse=True)
    mock_json_dumps.assert_called_with(json.loads(), indent=2)  # pylint: disable=E1120


def test_no_pipeline_error():
    """
    Should return error if pipeline not passed.
    """
    runner = CliRunner()

    result = runner.invoke(maggport.maggport, [
        '--host', 'test_host',
        '--collection', 'test_collection',
        '--db', 'test_db',
        '--port', '8080'
    ])

    assert result.exit_code == 1
    assert isinstance(result.exception, AttributeError)
    assert str(result.exception) == 'Expects value in either pipeline or pipeline_path. None given'


def test_bad_pipeline_param_error():
    """
    Should return error if pipeline parameter is not valid.
    """
    runner = CliRunner()

    result = runner.invoke(maggport.maggport, [
        '--host', 'test_host',
        '--collection', 'test_collection',
        '--db', 'test_db',
        '--port', '8080',
        '--pipeline', 'dummyPipeline'
    ])

    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)


def test_ext_not_found_error():
    """
    Should return error if 'out' file extension is not supported
    """
    runner = CliRunner()

    result = runner.invoke(maggport.maggport, [
        '--host', 'test_host',
        '--collection', 'test_collection',
        '--db', 'test_db',
        '--port', '8080',
        '--pipeline', PIPELINE,
        '--out', 'dummyFile.aaa'
    ])

    assert result.exit_code == 1
    assert isinstance(result.exception, AttributeError)
    assert str(result.exception) == 'File extension not supported'
