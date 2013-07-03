#!/usr/bin/env python

import os

settings_module = os.environ.get(
    'CLUSTERIT_SETTINGS_MODULE',
    'tests.settings')
os.environ['CLUSTERIT_SETTINGS_MODULE'] = settings_module


from clusterit.app import app

app.run()
