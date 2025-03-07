path = "../urban-tree-detection-data/test.txt"
# Read all lines from the file
with open(path, 'r') as file:
    lines = file.readlines()

# Remove duplicates while preserving order
deduplicated = list(dict.fromkeys(lines))

# Write the deduplicated lines back to the file
with open(path, 'w') as file:
    file.writelines(deduplicated)

print("Deduplication complete!")
