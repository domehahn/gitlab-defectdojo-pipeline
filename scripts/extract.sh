#!/bin/bash

if [ -f defectdojo-infrastructure.env ]; then
  export $(grep -v '^#' defectdojo-infrastructure.env | xargs)
fi

run_command() {
  ls -lisa
  pwd
  command=$1
  key=$2
  echo "Running command: $command"
  response=$(eval "$command")
  echo "Eval response: $response"
  status_code=$(echo "$response" | grep -o "HTTP/1.1 [0-9]\{3\}" | awk '{print $2}')
  echo "Http Status code: $status_code"
  if [ "$status_code" -eq 201 ]; then
    id=$(echo "$response" | grep -o '"id":[0-9]*' | awk -F':' '{print $2}' | tr -d '"')
    echo "HTTP status code 201 received. ID: $id"
    echo "$key=$id" >> defectdojo-infrastructure.env
  else
    echo "Error: HTTP status code $status_code received."
    exit 1
  fi
}

print_command() {
  command=$1
  key=$2
  echo "Running command: $command"
}