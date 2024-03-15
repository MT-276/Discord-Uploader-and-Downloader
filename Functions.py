#-------------------------------------------------------------------------------
# Name:        Functions.py
# Purpose:     Functions for Discord Uploader and Downloader
#
# Author:      Meit Sant
#
# Created:     13 03 2024
#
# Lead Dev : Meit Sant
# Testing  : Roshan Boby
#-------------------------------------------------------------------------------
import os, sys
import json, requests
from zipfile import ZipFile, ZIP_DEFLATED
from discord_webhook import DiscordWebhook
from tkinter.filedialog import askopenfilename

def send_message(webhook_url,thread_id,message):
    webhook = DiscordWebhook(url=webhook_url, thread_id=thread_id, content=message)
    response = webhook.execute()
    #print(f"Message sent to Discord: {message}")

def send_file(webhook_url,thread_id,folder_path,file_name,file_dict):
    
    webhook = DiscordWebhook(url=webhook_url, thread_id=thread_id)
    
    with open(f"{folder_path}/{file_name}", "rb") as f:
        # Get the size on disk of the file
        file_size = os.path.getsize(f"{folder_path}/{file_name}")
        if file_size > 26109544:
            print(f"File {file_name} is too large to send [Over 25 MB]. Skipping...")
            return file_dict
        webhook.add_file(file=f.read(), filename=file_name)
    
    webhook.execute()
    
    webhook_data = webhook.json['attachments'][0]

    file_dict[webhook_data['filename']] = webhook_data['url']
    
    print(f"File {file_name} sent to Discord.")
    
    return file_dict
 
def upload_files(webhook_url,thread_id,folder_path):
    files = os.listdir(folder_path)
    files.sort()
    
    file_dict = {}
    
    for file in files:
        file_dict = send_file(webhook_url,thread_id,folder_path,file,file_dict)
    
    # Generating the Key string
    Str = json.dumps(file_dict)
    file_dict = eval(Str)
    New_dict = {}
    for i in file_dict:
        New_dict['File_Name'] = i[:-8]
        break

    for i in file_dict:
        New_dict[i[-3:]] = file_dict[i][39:]
    
    send_message(webhook_url,thread_id,f"  **   **")

    
    str_dict = str(New_dict)
    
    if len(str_dict) > 2000:
        # Write the key to a file
        with open(f"Key_{New_dict['File_Name']}.txt", "w") as f:
            f.write(str_dict)
        send_message(webhook_url,thread_id,f"Key too large. Key was saved in uploader's pc.")
        return
    send_message(webhook_url,thread_id,f"Key for Downloading. Please Copy-Paste this key in the program to download the files.")
    send_message(webhook_url,thread_id,f"```{str_dict}```")
    
def download_files(webhook_url,thread_id,string):
    folder_path = "./Downloads/RAW/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_dict = eval(string)
    #print(file_dict)
    
    new_file_dict = {}
    
    for i in file_dict:
        if i == 'File_Name':
            continue
        new_file_dict[f"{file_dict['File_Name']}.zip.{i}"] = f"https://cdn.discordapp.com/attachments/{file_dict[i]}"
    
    file_dict = new_file_dict
    
    for num,i in enumerate(file_dict):
        url = file_dict[i]
        print(f"{num+1}. Downloading {i}...")
        r = requests.get(url, allow_redirects=True)
        if ".zip." in i:
            open(f"{folder_path}{i}", 'wb').write(r.content)
        else:
            open(f"{folder_path[:-4]}{i}", 'wb').write(r.content)
        print(f"Downloaded.")
        
def zip_and_split(file_path):
    
    # If the path is of a folder, then zip the folder
    if os.path.isdir(file_path):
        # Get the base folder name
        folder_name = os.path.basename(file_path)
        # Creating a new folder "Zipped" to store the zipped and split files
        folder_path = "./Zipped/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # Zip the folder
        with ZipFile(f'{folder_path}/{folder_name}.zip', 'w') as zip_archive:
            for foldername, subfolders, filenames in os.walk(file_path):
                for filename in filenames:
                    # Create a complete filepath
                    file_path = os.path.join(foldername, filename)
                    # Add file to zip
                    zip_archive.write(file_path, os.path.relpath(file_path, file_path))
        file_path = f"{folder_path}/{folder_name}.zip"
        path_of_zip_file = file_path
    else:
        # Creating a new folder "Zipped" to store the zipped and split files
        folder_path = "./Zipped/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        filename = os.path.basename(file_path)
        # Open the archive in write mode
        with ZipFile(f'{folder_path}/{filename}.zip', 'w') as zip_archive:
            # Add only the file (not the parent directory)
            zip_archive.write(file_path, filename)  # Specify filename within the archive
        path_of_zip_file = f"{folder_path}/{filename}.zip"
        
    filename = os.path.basename(file_path)
    base_file_name = filename
    
    # Split the zip file into chunks
    with open(path_of_zip_file, "rb") as f_in:
        byte = f_in.read(1)
        chunk_count = 1
        while byte:
            chunk_file_name = f"{folder_path}/{base_file_name}.{str(chunk_count).zfill(3)}"
            with open(chunk_file_name, "wb") as f_out:
                f_out.write(byte)
                Chunk = int(24.9 * 1024.0 * 1024.0) +1
                #print(type(Chunk), f"{Chunk}")
                for _ in range(Chunk - 1):  # -1 for the byte already read
                    byte = f_in.read(1)
                    if not byte: break
                    f_out.write(byte)
            chunk_count += 1
            byte = f_in.read(1)

    os.remove(path_of_zip_file)

def Choose_File(Type):
    '''
    Get the file path from user by opening an Explorer window
    '''
    try:
        # Open a Explorer window to choose a file
        filename = askopenfilename()
    except :
        print("[ERROR] Could not open explorer window.")
        filename = input("\nPlease enter the path of the image manually: ")
    if filename == '':
        return # If the user closes the window without choosing a file, then do nothing.
    return filename

def zip_merge():
    '''
    Merge the split files and unzip them
    '''
    folder_path = "./Downloads/RAW/"
    
    # Arrange files in ascended order
    file_names_list = os.listdir(folder_path)
    file_names_list.sort()

    # Unzip the files
    base_file_name = file_names_list[0][:-8]

    # Concatenate
    with open(f"{folder_path[:-4]}{base_file_name}.zip", "wb") as outfile:
        for i in file_names_list:
            with open(f"{folder_path}{i}", "rb") as infile:
                outfile.write(infile.read())

    print(f"\nFile {base_file_name}.zip merged successfully.")
    print(f"Unzipping {base_file_name}.zip...")
    
    with ZipFile(f"{folder_path[:-4]}{base_file_name}.zip", "r") as zip_ref:
        try:
            zip_ref.extractall(folder_path[:-4])
            os.remove(f"{folder_path[:-4]}{base_file_name}.zip")

        except IsADirectoryError:
            # Checking if a folder with the same name as the base file name already exists
            if os.path.exists(f"./{base_file_name}"):
                print(f"[ERROR] A folder with the name {base_file_name} already exists.")
                zip_ref.extractall(f"./{base_file_name}_New")
            else:
                zip_ref.extractall(f"./{base_file_name}")
            
        
        except:
            print(f"[ERROR] Could not extract {base_file_name}.zip")
            sys.exit()
    
