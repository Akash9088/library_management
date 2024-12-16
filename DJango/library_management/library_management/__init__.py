# library_management/__init__.py

from __future__ import absolute_import, unicode_literals

# Make sure Celery is loaded when Django starts
from .celery import app as celery_app

import pymysql
pymysql.install_as_MySQLdb()

__all__ = ('celery_app',)

