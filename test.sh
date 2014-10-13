#!/bin/sh

nosetests \
    --rednose \
    --verbose \
    --with-coverage \
    --cover-package=clusterit \
    --cover-erase \
    --cover-tests \
    tests

