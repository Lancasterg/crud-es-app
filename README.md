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
$ docker-compose up
```

### For development
```bash
# Install the package in development mode
$ pip install 
```


### For testing
```bash
# First run unit tests
$ cd test
$ ./run_pytests.sh

# Then run integration tests
$ ./run_integration_tests.sh
```
