#!/bin/bash

"""
Hay que tener instalado node 18
Hay que tener instalado python 3
Hay que tener instalado pip
Hay que tener instalado yarn
Hay que tener instalado redis y encendido
Hay que tener instalado MySQL y encendio
"""


python3 api/iqoptionapi/setup.py install
pip install -r requirements.txt

npm install --global yarn
cd util && npm install && cd ..
