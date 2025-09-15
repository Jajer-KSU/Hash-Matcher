import hashlib
import os
import argparse

# Function to load a file and return its MD5 hash
# Read each file 1mb at a time to avoid memory issues with larger files. For my purpose, this is not needed since I am dealing with small files, but its a good practice nontheless.
chunkSize = 1024 * 1024  # 1MB
def hashFile(filePath):
    md5Hash = hashlib.md5()
    # Returns the hexdigest of the hash passed into the function. AKA a human readable hash.
    with open(filePath, "rb") as file:
        while True:
            data = file.read(chunkSize)
            if not data:
                break
            md5Hash.update(data)
    return md5Hash.hexdigest()

def iterateFiles(directoryPath, recursive: bool, extensions):
    # Searches recursively through directoryPath for files with specified extensions
    if recursive:
        for root, _, files in os.walk(directoryPath):
            for file in files:
                if extensions:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        yield os.path.join(root, file)
                else:
                    yield os.path.join(root, file)
    # If not recursive, only checks the top level of the directory
    else:
        for file in os.listdir(directoryPath):
            fullPath = os.path.join(directoryPath, file)
            if os.path.isfile(fullPath):
                if extensions:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        yield fullPath
                else:
                    yield fullPath

# Checks if targetFile content is a hash or a file that needs to be to hashed
def getTargetHash(targetFile):
    try:
        with open(targetFile, "r") as file:
            hash = file.read().strip()
            if len(hash) == 32 and all(c in '0123456789abcdef' for c in hash.lower()):
                return hash
            else:
                return hashFile(targetFile)
    except Exception as e:
        raise ValueError(f"Error reading target file {targetFile}: {e}")


# Main function
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Find files with matching MD5 hash.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Example: python3 Hash-Matcher.py /path/to/directory /path/to/targetfile"
    )
    parser.add_argument("directory", type=str, help="Target directory that contains files to match hash to.")
    parser.add_argument("targetFile", type=str, help="File that contains md5 string or data to hash.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output.")
    parser.add_argument("--recursive", "-r", action="store_true", help="Recursively search through subdirectories.")
    parser.add_argument("--extensions", "-e", type=str, nargs='*', help="Only checks files with these extensions (e.g., .txt .log).")
    
    args = parser.parse_args()

    # Check if directory and target file exist
    if not os.path.isdir(args.directory):
        raise FileNotFoundError(f"The target directory {args.directory} does not exist.")
    
    if not os.path.isfile(args.targetFile):
        raise FileNotFoundError(f"The target file {args.targetFile} does not exist.")
    
    # Get the target hash or hash the target file
    try:
        targetHash = getTargetHash(args.targetFile)
    except ValueError as ve:
        print(ve)
        return
    print(f"Target MD5 Hash: {targetHash}")

    checked = 0
    matches = 0
    # Convert extensions to lowercase for case-insensitive comparison
    args.extensions = {ext.lower() for ext in args.extensions} if args.extensions else None

    # List to store match results
    matchResults = []

    for filePath in iterateFiles(args.directory, args.recursive, args.extensions):
        checked += 1
        try:
            fileHash = hashFile(filePath)
            if args.verbose:
                print(f"Checked: {filePath} | MD5: {fileHash}")
            if fileHash == targetHash:
                matches += 1
                # print number of matches found so far
                print(f"{matches} Matches found")
                # add the found hashes along with filepath to matchResults list
                matchResults.append((filePath, fileHash))
        except Exception as e:
            print(f"Error processing file {filePath}: {e}")

    if matches == 0:
        print("No matches found.")
    else:
        print(f"Checked {checked} files, found {matches} matches:")
        # Print each matched file with its hash
        for filePath, fileHash in matchResults:
            print(f"File: {filePath} | MD5: {fileHash}")
    if checked == 0:
        print("No files were checked. Please ensure the directory contains files and the extensions (if provided) are correct.")
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())