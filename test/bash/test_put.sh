#!/bin/bash

# bash file to test getting a file

curl -v -X PUT -H "Content-Type: multipart/form-data" -F "file=@test.txt" http://localhost:5000
