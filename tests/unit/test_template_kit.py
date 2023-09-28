# -*- coding: utf-8 -*-

# standard imports
import os

# lib imports
import pytest

# local imports
from plexhints import template_kit


@pytest.fixture(scope="function")
def serializable():
    return template_kit._Serializable()


def test_serializable_serialize(serializable):
    with pytest.raises(Exception):
        serializable._serialize(path='foo')


def test_serializable_deserialize(serializable):
    with pytest.raises(Exception):
        serializable._deserialize(path='foo', el='bar')


@pytest.mark.xfail(reason="Incomplete implementation")
def test_serializable_writedata(serializable, temp_dir):
    element = serializable._writedata(path=os.path.join(temp_dir, 'test_serializable'), data='bar')
    assert element.text == 'bar'


@pytest.mark.xfail(reason="Incomplete implementation")
def test_serializable_readdata(serializable, data_dir):
    data = serializable._readdata(path=os.path.join(data_dir, 'dummy-data.txt'))
    assert data == 'Hello, World!\n'


@pytest.mark.xfail(reason="Incomplete implementation")
def test_serializable_deletedata(serializable, temp_dir):
    serializable._deletedata(path=os.path.join(temp_dir, 'test_serializable'))
    assert not os.path.exists(os.path.join(temp_dir, 'test_serializable'))


@pytest.fixture(scope="function")
def attribute_set():
    return template_kit._AttributeSet()


def test_attribute_set_getattribute(attribute_set):
    with pytest.raises(Exception):
        attribute_set.__getattribute__('foo')


def test_attribute_set_setattr(attribute_set):
    with pytest.raises(Exception):
        attribute_set.__setattr__(name='foo', value='bar')

    attribute_set.__setattr__(name='_foo', value='bar')
    assert attribute_set.__getattribute__('_foo') == 'bar'


@pytest.mark.xfail(reason="Incomplete implementation")
def test_attribute_set_has_synthetic_attr(attribute_set):
    assert not attribute_set._has_synthetic_attr(name='foo')


@pytest.mark.xfail(reason="Incomplete implementation")
def test_attribute_set_get_synthetic_attr(attribute_set):
    attribute_set._get_synthetic_attr(name='foo')


@pytest.mark.xfail(reason="Incomplete implementation")
def test_attribute_set_set_synthetic_attr(attribute_set):
    attribute_set._set_synthetic_attr(name='foo', value='bar')


# todo - finish template kit tests
