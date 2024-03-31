#!/bin/bash

folder_path="./postgres-data"

if [[ ! -d "$folder_path" ]]; then
    mkdir -p "$folder_path"
fi

docker-compose up -d

