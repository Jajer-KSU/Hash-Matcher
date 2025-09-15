# Hash-Matcher
Python script that takes a target file, reads its contents and determines if it is a hash. If not md5 hash, hashes the contents. Takes said targeted hash and compares it to a list of files in a given directory. Hashes each file in directory and compares that hash with the target hash. If a match is found, appends it to a list and displays the list at the end.

# Usage Example
usage: Hash-Matcher.py [-h] [--verbose] [--recursive] [--extensions [EXTENSIONS ...]] directory targetFile

Find files with matching MD5 hash.

positional arguments:
  directory             Target directory that contains files to match hash to.
  targetFile            File that contains md5 string or data to hash.

options:
  -h, --help            show this help message and exit
  --verbose, -v         Enable verbose output. (default: False)
  --recursive, -r       Recursively search through subdirectories. (default: False)
  --extensions, -e [EXTENSIONS ...]
                        Only checks files with these extensions (e.g., .txt .log). (default: None)

# Example using dataset 
```
python3 Hash-Matcher.py Milestone_1_dataset/plain_files Milestone_1_dataset/message_hash.md5
```
# Results
```
Target MD5 Hash: d9643115dc80d566d9b985d287451de3
1 Matches found
Checked 10000 files, found 1 matches:
File: Milestone_1_dataset/plain_files\file1693.txt | MD5: d9643115dc80d566d9b985d287451de3
```
