# -*- coding: utf-8 -*-

# standard imports
import os

# lib imports
import pytest

# local imports
from plexhints import core_kit


def create_dirs(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture(scope='session')
def core_kit_fixture():
    return core_kit.Core


@pytest.fixture(scope='session')
def core_storage_fixture(core_kit_fixture):
    return core_kit_fixture.Storage()


@pytest.fixture(scope='function')
def binary_file_content():
    return b'This is a test file.'


@pytest.fixture(scope='function')
def regular_file_content():
    return 'This is a test file.'


def test_load_binary(binary_file_content, core_storage_fixture, temp_dir):
    temp_file_path = os.path.join(temp_dir, 'test_core_kit', 'test_load_binary')
    remove_file(file_path=temp_file_path)
    create_dirs(dir_path=os.path.dirname(temp_file_path))

    with open(temp_file_path, 'wb') as f:
        f.write(binary_file_content)

    assert core_storage_fixture.load(filename=temp_file_path, binary=True) == binary_file_content

    remove_file(file_path=temp_file_path)


def test_load_regular(regular_file_content, core_storage_fixture, temp_dir):
    temp_file_path = os.path.join(temp_dir, 'test_core_kit', 'test_load_regular')
    remove_file(file_path=temp_file_path)
    create_dirs(dir_path=os.path.dirname(temp_file_path))

    with open(temp_file_path, 'w') as f:
        f.write(regular_file_content)

    assert core_storage_fixture.load(filename=temp_file_path, binary=False) == regular_file_content

    remove_file(file_path=temp_file_path)


def test_save_binary(binary_file_content, core_storage_fixture, temp_dir):
    temp_file_path = os.path.join(temp_dir, 'test_core_kit', 'test_save_binary')
    remove_file(file_path=temp_file_path)
    create_dirs(dir_path=os.path.dirname(temp_file_path))

    core_storage_fixture.save(filename=temp_file_path, data=binary_file_content, binary=True)
    assert os.path.exists(temp_file_path)

    with open(temp_file_path, 'rb') as f:
        assert f.read() == binary_file_content

    remove_file(file_path=temp_file_path)


def test_save_regular(regular_file_content, core_storage_fixture, temp_dir):
    temp_file_path = os.path.join(temp_dir, 'test_core_kit', 'test_save_regular')
    remove_file(file_path=temp_file_path)
    create_dirs(dir_path=os.path.dirname(temp_file_path))

    core_storage_fixture.save(filename=temp_file_path, data=regular_file_content, binary=False)
    assert os.path.exists(temp_file_path)

    with open(temp_file_path, 'r') as f:
        assert f.read() == regular_file_content

    remove_file(file_path=temp_file_path)
