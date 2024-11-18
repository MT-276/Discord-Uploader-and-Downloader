#-------------------------------------------------------------------------------
# Name:             Functions.py
# Purpose:          Functions for Discord Uploader and Downloader
#
# Created:          13 03 2024
# License:          Apache License Version 2.0
#
# Developed by:     Meit Sant [Github:MT_276]
#-------------------------------------------------------------------------------

# File version - 2.0

import os, sys, json
from zipfile import ZipFile, BadZipFile
from tkinter.filedialog import askopenfilename,askdirectory

from logging import basicConfig, CRITICAL
basicConfig(level=CRITICAL)

# Trying to import requests
try:
    import requests
except ModuleNotFoundError:
    print("[ERROR] requests not found. Installing...\n")
    
    exit_code = os.system("python -m pip install requests")
    
    if exit_code != 0:
        print("\n[ERROR] Error Code : ",exit_code)
        print("[ERROR] Could not install requests. Exiting...")
        exit()
    else:
        print("\n[INFO] requests installed successfully.\n")
        import requests

# Trying to import discord-webhook
try:
    from discord_webhook import DiscordWebhook  
except ModuleNotFoundError:
    print("[ERROR] discord-webhook not found. Installing...\n")
    
    exit_code = os.system("python -m pip install discord-webhook")
    
    if exit_code != 0:
        print("\n[ERROR] Error Code : ",exit_code)
        print("[ERROR] Could not install discord-webhook. Exiting...")
        exit()
    else:
        print("\n[INFO] discord-webhook installed successfully.\n")
        from discord_webhook import DiscordWebhook

def send_message(webhook_url,thread_id,message):
    webhook = DiscordWebhook(url=webhook_url, thread_id=thread_id, content=message)
    webhook.execute()

def send_file(webhook_url,thread_id,folder_path,file_name,file_dict):
    print(f"Uploading file {file_name} to Discord...")
    
    webhook = DiscordWebhook(url=webhook_url, thread_id=thread_id)
    
    with open(f"{folder_path}/{file_name}", "rb") as f:
        # Get the size on disk of the file
        file_size = os.path.getsize(f"{folder_path}/{file_name}")
        
        if file_size > 26203915:
            print(f"File {file_name} is too large to send [Over 25 MB]. Skipping...\n")
            return file_dict
        
        webhook.add_file(file=f.read(), filename=file_name)
    
    try:
        webhook.execute()
    except requests.exceptions.SSLError:
        print(f"\n[ERROR] Internet connection lost.\n[ERROR] Please check your internet connection and try again.")
        print(f"[INFO] Your upload progress is saved and will resume once you select the same file for uploading.")
        sys.exit()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit()
    
    try:
        webhook_data = webhook.json['attachments'][0]
    except IndexError:
        print(f"\n[ERROR] Could not find thread with thread id : {thread_id}\n[ERROR] Please check the thread id and try again.")
        sys.exit()

    file_dict[webhook_data['filename']] = webhook_data['url']
    
    print(f"Uploaded.")
    
    return file_dict
 
def upload_files(webhook_url,thread_id,folder_path,Anonymous_download=True,Key=None):
    '''
    Uploads the files to Discord
    '''
    
    files = os.listdir(folder_path)
    files.sort()
    
    # Checking if the key already exists
    if Key != None:
        file_dict = decode_Dict(Key)
        
    else:
        file_dict = {}

    for file in files:
        file_dict = send_file(webhook_url,thread_id,folder_path,file,file_dict)
        
        # Encode the dictionary
        if not Anonymous_download:
            files_dict = encode_Dict(file_dict,webhook_url,thread_id)
        else:
            files_dict = encode_Dict(file_dict)
        
        # If not present already, creating a folder "Keys" to store the keys
        if not os.path.exists("Keys"):
            os.makedirs("Keys")
        
        # Write the key to a file
        with open(f"Keys/Key_{files_dict['File_Name']}.txt", "w") as f:
                f.write(str(files_dict))
    
    send_message(webhook_url,thread_id,f"  **   **")

    if len(str(files_dict)) > 2000:
        send_message(webhook_url,thread_id,f"Key too large. Key was saved in uploader's pc.")
        return
    send_message(webhook_url,thread_id,f"Key for Downloading. Please Copy-Paste this key in the program to download the files.")
    send_message(webhook_url,thread_id,f"```{str(files_dict)}```")
    
def download_files(string):
    folder_path = "./Downloads/RAW/"
    
    # Changes the folder name if already exists
    c = 0
    while True:
        # break loop if the folder does not exist
        if not os.path.exists(folder_path):
            break
        c += 1
        folder_path = f"./Downloads/RAW_{c}/"
    
    os.makedirs(folder_path)
    file_dict = eval(string)
    
    file_dict = decode_Dict(file_dict)
    
    for num,file_name in enumerate(file_dict):
        
        if file_name == 'Webhook_URL':
            
            # Finding the windows username
            user = os.getlogin()
            # Fetching file name
            file_name = eval(string)['File_Name']
            
            message = f"# File : `{file_name}`\n# Downloaded by `{user}`"
            send_message(file_dict['Webhook_URL'],file_dict['Thread_ID'],message)
            break
        
        url = file_dict[file_name]
        print(f"{num+1}. Downloading {file_name}")
        
        r = requests.get(url, allow_redirects=True)
        
        if ".zip." in file_name:
            open(f"{folder_path}{file_name}", 'wb').write(r.content)
        else:
            open(f"./Downloads/{file_name}", 'wb').write(r.content)
        print(f"Downloaded.")
    return folder_path
        
def zip_and_split(file_path,max_upload_size):
    '''
    Zips the file and splits it into chunks of 25 MB
    '''
    
    # If the path is of a folder, then zip the folder
    if os.path.isdir(file_path):
        
        # Get the base folder name
        folder_name = os.path.basename(file_path)
        
        # Creating a new folder "Zipped" to store the zipped and split files
        folder_path = "./Zipped/"
        c = 0
        while True:
            # break loop if the folder does not exist
            if not os.path.exists(folder_path):
                break
            c += 1
            folder_path = f"./Zipped_{c}/"
            
        os.makedirs(folder_path)
        
        # Zip the folder
        with ZipFile(f'{folder_path}{folder_name}.zip', 'w') as zip_archive:
            for foldername, subfolders, filenames in os.walk(file_path):
                for filename in filenames:
                    # Create a complete filepath
                    file_path = os.path.join(foldername, filename)
                    # Add file to zip
                    zip_archive.write(file_path, os.path.relpath(file_path, file_path))
        file_path = f"{folder_path}{folder_name}.zip"
        path_of_zip_file = file_path
        
        
    else:
        # Else if the path if of a file.
        
        # Creating a new folder "Zipped" to store the zipped and split files
        folder_path = "./Zipped/"
        
        # Check if the folder already exists so as to create a new folder in order to avoid overwriting.
        c = 0
        while True:
            # break loop if the folder does not exist
            if not os.path.exists(folder_path):
                break
            c += 1
            folder_path = f"./Zipped_{c}/"
        
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
            chunk_file_name = f"{folder_path}{base_file_name}.zip.{str(chunk_count).zfill(3)}"
            with open(chunk_file_name, "wb") as f_out:
                f_out.write(byte)
                Chunk = max_upload_size +1

                for _ in range(Chunk - 1):  # -1 for the byte already read
                    byte = f_in.read(1)
                    if not byte: break
                    f_out.write(byte)
            chunk_count += 1
            byte = f_in.read(1)

    os.remove(path_of_zip_file)
    return folder_path

def Choose_File(Type):
    '''
    Get the file/folder path from user by opening an Explorer window
    '''
    try:
        # Open a Explorer window to choose a file
        if Type == 'file':
            print(f"\n[INFO] Please choose the {Type} to upload : ")
            filename = askopenfilename()
        elif Type == 'folder':
            print(f"\n[INFO] Please choose the {Type} to upload :")
            filename = askdirectory()
    except :
        print("[ERROR] Could not open explorer window.")
        filename = input(f"\nPlease enter the path of the {Type} manually : ")
    return filename

def zip_merge(folder_path):
    '''
    Merge the split files and unzip them
    '''
    
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

    if '.zip' in base_file_name :
        extension = ''
    else:
        extension = '.zip'
    print(f"\n[INFO] File {base_file_name}{extension} merged successfully.")
    print(f"[INFO] Unzipping {base_file_name}{extension}...")

    try:
        # Unzip the file
        with ZipFile(f"{folder_path[:-4]}{base_file_name}{extension}", "r") as zip_ref:
            try:
                zip_ref.extractall(folder_path[:-4])

            except IsADirectoryError:
                # Checking if a folder with the same name as the base file name already exists
                if os.path.exists(f"./{base_file_name}"):
                    print(f"[ERROR] A folder with the name {base_file_name} already exists.")
                    zip_ref.extractall(f"./{base_file_name}_New")
                else:
                    zip_ref.extractall(f"./{base_file_name}")
            
            except Exception as e:
                print(f"[ERROR] Could not extract {base_file_name}.zip")
                print(f"[ERROR] System : {e}")
                sys.exit()
        os.remove(f"{folder_path[:-4]}{base_file_name}{extension}")
                
    except BadZipFile:
        print(f"\n[ERROR] {base_file_name}{extension} is corrupted.")
        sys.exit()
    except Exception as e:
        print(f"\n[ERROR] An unknown error occured.\n[ERROR] {e}")
        sys.exit()
        
def update_webhook(webhook_url,Version,mode):
    '''
    Update the name of the webhook
    '''
    
    new_name = f"[{mode}] Database Bot V{Version}"

    headers = { "Content-Type": "application/json",}
    data = {"name": new_name,}

    try:
        response = requests.patch(webhook_url, headers=headers, data=json.dumps(data))
    except requests.exceptions.MissingSchema:
        print(f"\n[ERROR] Invalid Webhook URL. Please try again.")
        sys.exit()
    except requests.exceptions.ConnectionError:
        print(f'\n[ERROR] Could not connect to discord.com.\n[ERROR] Please check your internet connection.')
        sys.exit()
    
    if response.status_code != 200:
        print(f"[ERROR] Could not update the webhook. Error Code: {response.status_code}")
        sys.exit()
    else:
        return
        
def encode_Dict(file_dict,webhook_url=None,thread_id=None):
    '''
    Encoding the original dictionary into a dictrionary that is smaller in size.
    '''
    New_dict = {}
    for i in file_dict:
        New_dict['File_Name'] = i[:-4]
        break

    for i in file_dict:
        New_dict[i[-3:]] = file_dict[i][39:]

    if webhook_url != None:
        New_dict['Webhook_URL'] = webhook_url
        New_dict['Thread_ID'] = thread_id
    
    return New_dict
    
def decode_Dict(file_dict):
    '''
    Decoding the dictionary to the original dictionary.
    '''
    
    newFileDict = {}
    
    # Iterate through each key in the input dictionary
    for i in file_dict:
        # Skip processing if the current key is 'File_Name'
        if i == 'File_Name':
            continue
        # Directly copy 'Webhook_URL' key-value pair to the new dictionary
        if i == 'Webhook_URL':
            newFileDict[i] = file_dict[i]
            continue
        # Directly copy 'Thread_ID' key-value pair to the new dictionary
        if i == 'Thread_ID':
            newFileDict[i] = file_dict[i]
            continue
        # For other keys, generate a new key by appending the 'File_Name'
        # value as a prefix, and create a URL using the value of the current key
        newFileDict[f"{file_dict['File_Name']}.{i}"] = f"https://cdn.discordapp.com/attachments/{file_dict[i]}"
    
    return newFileDict



