#!/bin/bash

cd ./tmp/pinakes/2GE_2023_PROSORINOI_PINAKES_KATATAXIS_APORRIPTEON

for file in 1_*.xls; do
    [ -f "$file" ] || continue

    spec=$(printf '%s' "$file" | grep -o 'ΠΕ[0-9]\+\.[0-9]\+')

    if [ -z "$spec" ]; then
        spec=$(printf '%s' "$file" | grep -o 'ΠΕ[0-9]\+' | head -n1)
    fi

    echo make import.qualifications YEAR="2023" SPEC=\"${spec}\" FILE=\"pinakes/2GE_2023_PROSORINOI_PINAKES_KATATAXIS_APORRIPTEON/$file\"
done
