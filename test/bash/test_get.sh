#!/bin/bash

# bash file to test getting a file
curl 127.0.0.1:5000 -G -d "file_id=9cd6013fb76843b1b625153c6b77f89a" --output test.txt

