#!/bin/bash
# High school (ΔΕ) hire files. Folder a_fasi -> round A, b_fasi -> B, ...
# 2023-24 files use the 2023 layout, 2025-26 files the 2025 layout.

cd ./tmp/anaplirotes

for entry in "2023-24:2023" "2025-26:2025"; do
    school_year="${entry%%:*}"
    layout="${entry##*:}"

    for file in "$school_year"/*_fasi/*ΔΕ*.xls; do
        [ -f "$file" ] || continue

        phase=$(basename "$(dirname "$file")")
        round=$(printf '%s' "${phase%%_*}" | tr '[:lower:]' '[:upper:]')

        echo make import.hires LAYOUT="$layout" SCHOOL_YEAR=\"$school_year\" ROUND=\"$round\" FILE=\"anaplirotes/$file\"
    done
done
