#!/bin/bash

# bash file to test getting a file
curl 127.0.0.1:5000 -G -d "file_id=test" --output test.txt

