#!/bin/bash
#
# Check all journey data sets against the schema

cat datasets.txt | xargs -I '{}' python tools/check-all-documents.py {} journey
