import os 
import zipfile

Directory = '/workspaces/Discord-Uploader-and-Downloader/Downloads/ ' #input("Enter the directory of the file: ")

# Check if the directory exists
if not os.path.isdir(Directory):
    print(f"Directory {Directory} does not exist.")
    exit()

# Arrange files in ascended order
files = os.listdir(Directory)

for file in files:
    if "zip" not in file:
        # delete elements that are not zip files
        files.remove(file)
        
files.sort()


# Unzip the files
with zipfile.ZipFile(f"{files[0][:-8]}", "w", zipfile.ZIP_DEFLATED) as zipf:
    for file in files:
        zipf.write(f"{Directory}/{file}")

print("[INFO] Original reconstructed successfully")