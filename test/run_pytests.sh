#!/bin/bash

# Run tests
coverage run -m pytest test_utils

# Report results
coverage report