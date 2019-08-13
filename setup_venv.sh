#!/bin/bash

python -m venv pvenv
source pvenv/bin/activate
python -m pip install --upgrade pip
python -m pip install setuptools
python -m pip install requests
python -m pip install SQLAlchemy
python -m pip install appdirs
