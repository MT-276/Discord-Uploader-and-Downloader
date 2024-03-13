import os
import zipfile
import shutil


def zip_and_split(file_path, chunk_size):
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Get the base file name
    base_file_name = os.path.basename(file_path)

    base_file_name = base_file_name[:-4]
    
    # Create a zip file
    with zipfile.ZipFile(f"{base_file_name}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path)

    # Split the zip file into chunks
    with open(f"{base_file_name}.zip", "rb") as f_in:
        byte = f_in.read(1)
        chunk_count = 1
        while byte:
            chunk_file_name = f"{base_file_name}.zip.{str(chunk_count).zfill(3)}"
            with open(chunk_file_name, "wb") as f_out:
                f_out.write(byte)
                Chunk = int(chunk_size * 1024.0 * 1024.0) +1
                print(type(Chunk), f"{Chunk}")
                for _ in range(Chunk - 1):  # -1 for the byte already read
                    byte = f_in.read(1)
                    if not byte:
                        break
                    f_out.write(byte)
            chunk_count += 1
            byte = f_in.read(1)

    # Delete the original zip file
    os.remove(f"{base_file_name}.zip")

# Usage
print(zip_and_split("Original/Wholesome_Pic.txt",24.8))