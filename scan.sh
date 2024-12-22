#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Usage: ./scan.sh <github_url or directory_path>"
    exit 1
fi

target_path="$1"
python main.py "$target_path"