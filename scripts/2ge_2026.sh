#!/bin/bash

cd ./tmp/pinakes/2GE_2026_PROSORINOI

for file in 1_*.xls; do
    [ -f "$file" ] || continue

    spec=$(printf '%s' "$file" | grep -o 'ΠΕ[0-9]\+\.[0-9]\+')

    if [ -z "$spec" ]; then
        spec=$(printf '%s' "$file" | grep -o 'ΠΕ[0-9]\+' | head -n1)
    fi

    echo make import.qualifications SPEC=\"${spec}\" FILE=\"pinakes/2GE_2026_PROSORINOI/$file\"
done
