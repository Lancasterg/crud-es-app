# crud-filesystem-elasticsearch

Simple CRUD application that uses ElasticSearch as a lookup for a filesystem.

Containerised and deployed using docker-compose.

## Requirements

* Python == 3.8
* Docker
* docker-compose

## How to run
 
```bash
# Create a virtual environment, activate and install requirements
$ python -m virtualenv crud-es-venv
$ source crud-es-venv/bin/activate

# Install requirements
$ pip install -r requirements-dev.txt
```

### Quick start
```bash
# Run the application! 
$ docker-compose up --build
```

### For development
```bash
# Install the package in development mode
$ pip install 
```

### For testing

#### Option 1:
Apologies for the crude testing...
```bash
docker-compose up --build

cd test/bash

# Upload a file and check it's on the filesystem
bash test_put.sh
less /var/www/test_put.sh

# Edit the test_get file to point to your file id
bash test_get.sh
less test.sh

# Edit the test_delete file to point to your file id
bash test_delete.sh
less /var/www/test_put.sh
```

#### Option 2: 
WIP
```bash
# First run unit tests
$ cd test
$ ./run_pytests.sh

# Then run integration tests
$ ./run_integration_tests.sh
```


#### Option 3
WIP
```bash
cd test/features
behave
```