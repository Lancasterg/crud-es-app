#!/bin/bash

# bash file to test putting a file

curl -v -X PUT -H "Content-Type:multipart/form-data" -F "file=@test_put.txt" http://localhost:5000
