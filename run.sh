#!/bin/bash

while read -r -u 3 list_2023; do
    echo "$list_2023";
    eval "$list_2023";
done 3< <(./scripts/2ge_2023.sh)

while read -r -u 3 list_2023; do
    echo "$list_2023";
    eval "$list_2023";
done 3< <(./scripts/2ge_2026.sh)

# Hires go last: they are matched to the teachers created from the ranking lists above.
while read -r -u 3 hire; do
    echo "$hire";
    eval "$hire";
done 3< <(./scripts/hires_de.sh)
