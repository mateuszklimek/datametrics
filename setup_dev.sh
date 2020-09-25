#!/bin/bash
pip install -r requirments.txt
pip install -e .

export PYTHONPATH=$PYTHONPATH:$PWD
