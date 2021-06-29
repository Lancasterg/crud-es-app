Feature: get
  Integration tests for getting some files from ElasticSearch

  Scenario: File does not exist
    Given The ES server and REST API are online
     When We send a bad get request
     Then We receive a 404 status code

  Scenario: File does exist
    Given The file is found in ElasticSearch
     When We send a get request
     Then We receive the file and a 200 status code