# -*- coding: utf-8 -*-

# local imports
from plexhints import log_kit

Log = log_kit.Log

basic_message = 'This is a message.'
format_message_args = 'This is a %s message.'
format_message_kwargs = 'This is a %(message_type)s message.'


def test_debug(caplog):
    Log.Debug(basic_message)

    captured = caplog
    assert basic_message in captured.text


def test_debug_format_args(caplog):
    fmt_args = 'debug'
    Log.Debug(format_message_args, fmt_args)

    captured = caplog
    assert format_message_args % fmt_args in captured.text


def test_debug_format_kwargs(caplog):
    fmt_kwargs = {'message_type': 'debug'}
    Log.Debug(format_message_kwargs, fmt_kwargs)

    captured = caplog
    assert format_message_kwargs % fmt_kwargs in captured.text


def test_info(caplog):
    Log.Info(basic_message)

    captured = caplog
    assert basic_message in captured.text


def test_info_format_args(caplog):
    fmt_args = 'info'
    Log.Debug(format_message_args, fmt_args)

    captured = caplog
    assert format_message_args % fmt_args in captured.text


def test_info_format_kwargs(caplog):
    fmt_kwargs = {'message_type': 'info'}
    Log.Debug(format_message_kwargs, fmt_kwargs)

    captured = caplog
    assert format_message_kwargs % fmt_kwargs in captured.text


def test_warn(caplog):
    Log.Info(basic_message)

    captured = caplog
    assert basic_message in captured.text


def test_warn_format_args(caplog):
    fmt_args = 'warn'
    Log.Debug(format_message_args, fmt_args)

    captured = caplog
    assert format_message_args % fmt_args in captured.text


def test_warn_format_kwargs(caplog):
    fmt_kwargs = {'message_type': 'warn'}
    Log.Debug(format_message_kwargs, fmt_kwargs)

    captured = caplog
    assert format_message_kwargs % fmt_kwargs in captured.text


def test_error(caplog):
    Log.Info(basic_message)

    captured = caplog
    assert basic_message in captured.text


def test_error_format_args(caplog):
    fmt_args = 'error'
    Log.Debug(format_message_args, fmt_args)

    captured = caplog
    assert format_message_args % fmt_args in captured.text


def test_error_format_kwargs(caplog):
    fmt_kwargs = {'message_type': 'error'}
    Log.Debug(format_message_kwargs, fmt_kwargs)

    captured = caplog
    assert format_message_kwargs % fmt_kwargs in captured.text


def test_critical(caplog):
    Log.Info(basic_message)

    captured = caplog
    assert basic_message in captured.text


def test_critical_format_args(caplog):
    fmt_args = 'critical'
    Log.Debug(format_message_args, fmt_args)

    captured = caplog
    assert format_message_args % fmt_args in captured.text


def test_critical_format_kwargs(caplog):
    fmt_kwargs = {'message_type': 'critical'}
    Log.Debug(format_message_kwargs, fmt_kwargs)

    captured = caplog
    assert format_message_kwargs % fmt_kwargs in captured.text


def test_exception(caplog):
    Log.Info(basic_message)

    captured = caplog
    assert basic_message in captured.text


def test_exception_format_args(caplog):
    fmt_args = 'exception'
    Log.Debug(format_message_args, fmt_args)

    captured = caplog
    assert format_message_args % fmt_args in captured.text


def test_exception_format_kwargs(caplog):
    fmt_kwargs = {'message_type': 'exception'}
    Log.Debug(format_message_kwargs, fmt_kwargs)

    captured = caplog
    assert format_message_kwargs % fmt_kwargs in captured.text


def test_stack(caplog):
    Log.Stack()

    captured = caplog
    assert 'Current stack:' in captured.text
