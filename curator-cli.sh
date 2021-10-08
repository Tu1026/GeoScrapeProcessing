#!/bin/bash
umask 002
pipenv run python src/cli.py "$@"