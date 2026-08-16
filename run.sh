#!/bin/bash

while read -r -u 3 list_2023; do
    echo "$list_2023";
    eval "$list_2023";
done 3< <(./scripts/2ge_2023.sh)

while read -r -u 3 list_2023; do
    echo "$list_2023";
    eval "$list_2023";
done 3< <(./scripts/2ge_2026.sh)
