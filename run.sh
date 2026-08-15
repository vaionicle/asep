#!/bin/bash

./scripts/2ge_2023.sh | while read list_2023; do
    bash -c "$line" < /dev/null
done