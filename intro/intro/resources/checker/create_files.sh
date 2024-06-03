#!/bin/bash

mkdir -p "$1"
cd "$1" || exit

# In case listdiff.txt already exists, do not change the list/ directory.
if [ -f listdiff.txt ]; then
    echo "listdiff.txt already exists. Exiting."
    exit 1
else
    rm -f *
fi

# Generate the random strings and append to the file.
for i in {1..1000}; do
    openssl rand -base64 37 | cut -c1-37 >> "$2"
done

target_file="$2"

# Make a copy of the file.
cp "$target_file" "list2.txt"

# Select a random line number.
total_lines=$(wc -l < "$target_file")
random_line_number=$(shuf -i 1-$total_lines -n 1)

# Extract the random line.
random_line=$(sed -n "${random_line_number}p" "$target_file")

# Extract the first letter and the rest of the line.
first_letter=$(echo "$random_line" | cut -c1)
rest_of_line=$(echo "$random_line" | cut -c2-)

# Generate a new letter that is different from the first letter.
new_letter=$(echo "abcdefghijklmnopqrstuvwxyz" | grep -o . | shuf -n1)
while [[ "$first_letter" == "$new_letter" ]]; do
    new_letter=$(echo "abcdefghijklmnopqrstuvwxyz" | grep -o . | shuf -n1)
done

new_line="${new_letter}${rest_of_line}"

# Use awk to replace the specific line.
awk -v rln="$random_line_number" -v nl="$new_line" 'NR == rln {print nl} NR != rln {print $0}' "$target_file" > temp && mv temp "$target_file"
