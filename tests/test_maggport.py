"""
This file unittests maggport.py file
"""
import pathlib
import pytest
from unittest import mock

import click
from click.testing import CliRunner

from maggport import maggport


PIPELINE = ('['
            '{"$match": { "_id" : { "$ne" : "null"}}},'
            '{"$limit": 10}'
            ']')

def mock_get(pipeline, allowDiskUse):  # pylint: disable=W0613,C0103
    """
    mock_get
    """
    return [
        {'_id': 'dummy_id_A', 'value': 'dummy_value_A'},
        {'_id': 'dummy_id_B', 'value': 'dummy_value_B'},
    ]


@mock.patch('pymongo.MongoClient')
def test_connect_to_db(mock_db):
    """
    test_connect_to_db
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


@mock.patch('pandas.DataFrame.to_csv')
@mock.patch('pymongo.collection.Collection.aggregate', side_effect=mock_get)
def test_print_results(mock_agg, mock_to_csv):
    """
    test_print_results
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
    mock_to_csv.assert_called_with(sep=',', index=False)


@mock.patch('pandas.DataFrame.to_csv')
@mock.patch('pymongo.collection.Collection.aggregate', side_effect=mock_get)
def test_export_results_to_csv(mock_agg, mock_to_csv):
    """
    test_print_results
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


@mock.patch('pandas.DataFrame.to_csv')
@mock.patch('pymongo.collection.Collection.aggregate', side_effect=mock_get)
def test_pass_pipeline_as_file(mock_agg, mock_to_csv):
    """
    test_pass_pipeline_as_file
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
    mock_to_csv.assert_called_with(sep=',', index=False)


def test_no_pipeline_error():
    """
    test_pass_pipeline_as_file
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
    test_pass_pipeline_as_file
    """
    runner = CliRunner()

    # with pytest.raises(AttributeError) as excinfo:
    result = runner.invoke(maggport.maggport, [
        '--host', 'test_host',
        '--collection', 'test_collection',
        '--db', 'test_db',
        '--port', '8080',
        '--pipeline', 'dummyPipeline'
    ])

    assert result.exit_code == 1
    assert isinstance(result.exception, ValueError)
