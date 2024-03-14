#-------------------------------------------------------------------------------
# Name:        Main.py
# Purpose:     Functions for Discord Uploader and Downloader
#
# Author:      Meit Sant
#
# Created:     13 03 2024
#
# Lead Dev : Meit Sant
#-------------------------------------------------------------------------------
import os, sys
import json, zipfile, requests
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
    
    Str = json.dumps(file_dict)
    
    send_message(webhook_url,thread_id,f"  **   **")
    send_message(webhook_url,thread_id,f"Key for Downloading. Please Copy-Paste this key in the program to download the files.```{Str}```")

def download_files(webhook_url,thread_id,string):
    folder_path = "./Downloads/RAW/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_dict = eval(string)

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
    # Get the base file name
    base_file_name = os.path.basename(file_path)
    base_file_name = base_file_name

    # Creating a new folder "Zipped" to store the zipped and split files
    folder_path = "./Zipped/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    # Create a zip file
    with zipfile.ZipFile(f"{folder_path}/{base_file_name}.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path)

    # Split the zip file into chunks
    with open(f"{folder_path}/{base_file_name}.zip", "rb") as f_in:
        byte = f_in.read(1)
        chunk_count = 1
        while byte:
            chunk_file_name = f"{folder_path}/{base_file_name}.zip.{str(chunk_count).zfill(3)}"
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
    os.remove(f"{folder_path}/{base_file_name}.zip")

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
    files = os.listdir(folder_path)
    files.sort()

    # Unzip the files
    with zipfile.ZipFile(f"./Downloads/{files[0][:-8]}", "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(f"{folder_path}/{file}")

