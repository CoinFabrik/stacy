#!/bin/bash

diff_found=false

process_example() {
    local example_path=$1
    local clar_file=$(find "$example_path" -name "*.clar")
    local expected_output_file="$example_path/stdout"

    ./venv/bin/stacy-analyzer lint "$clar_file" > output.tmp

    if ! diff -q output.tmp "$expected_output_file" > /dev/null; then
        diff --color output.tmp "$expected_output_file"
        diff_found=true
    fi

    rm output.tmp
}

base_dir="tests"

for test_case in "$base_dir"/*; do
    for example in "$test_case"/*; do
        process_example "$example"
    done
done

if [[ -t 1 ]]; then
    color_start="\e[32m"
    color_end="\e[0m"
else
    color_start="=== "
    color_end=" ==="
fi

if ! $diff_found; then
    echo -e "${color_start}All tests passed.${color_end}"
fi