#!/usr/bin/env python
import pytest
from unittest.mock import patch

from sv_c1.celery_main import celery_app as celeryapp
from sv_c1.task_process import process_execute


@pytest.fixture(scope='module')
def celery_app(request):
    celeryapp.conf.update(CELERY_ALWAYS_EAGER=True)
    return celeryapp


def test_process(celery_app):
    retval = process_execute('hello')
    assert retval == True 
