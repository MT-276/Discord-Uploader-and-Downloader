#-------------------------------------------------------------------------------
# Name:             Main.py
# Purpose:          Upload files to Discord
#
# Author:           MS Productions
#
# Created:          13 03 2024
# License:          Apache License Version 2.0
#
# Developed by:     Meit Sant [Github:MT_276]
#-------------------------------------------------------------------------------

Program_version = "1.8"
mode = "Stable"

from Functions import *

print(f'Discord Uploader and Downloader V{Program_version}')
print('Developed by     : Meit Sant')
print('Licence          : Apache License Version 2.0')

option = input('\nUpload [U] or Download [D] : ')


if option in ['U','u','Upload','upload']:
    
    webhook_url = input('\nEnter the webhook URL : ')
    thread_id = input('Enter the thread ID : ')
    
    update_webhook(webhook_url,Program_version,mode)

    option = input('\nUpload a file [A] or a folder [B] : ')

    if option in ['A','a','File','file']:
        file_path = input('\nEnter the file path : ')

        # Checking if the entered string is empty.
        if file_path == "":
            print('\n[ERROR] Invalid file path. Exiting...')
            sys.exit()

        file_path = file_path.replace('"','')

        #Check if file exists
        if not os.path.isfile(file_path):
            print(f"\n[ERROR] Could not find {file_path}. Exiting...")
            sys.exit()

        # Checking size of file
        file_size = os.path.getsize(file_path)

        # If file size is greater than 25 MB, zip and split the file
        if file_size > 26203915:
            
            # Getting base name of the file
            file_name = os.path.basename(file_path)
            
            print(f"\n[WARN] File {file_name} is too large to send independently [Over 25 MB].")
            print('\n[INFO] Zipping and splitting file...')
            
            # Calculating the number of files to be zipped
            num = file_size//26203915
            if file_size%26203915 != 0:
                num += 1
            print(f'[INFO] The file will be zipped in chunks of {num} files.')
            if num > 10:
                print(f'[INFO] This may take a while...')

            folder_path = zip_and_split(file_path)

            print('[INFO] Zipped.\n\n[INFO] Uploading files...\n')

            # Uploading the files
            upload_files(webhook_url,thread_id,folder_path)

            # Delete the zipped folder
            for i in os.listdir(folder_path):
                os.remove(f"{folder_path}{i}")
            os.rmdir(folder_path)

            print('\n[INFO] Files uploaded. Exiting...')
            sys.exit()
        else:
            # If the file size is less than 25 MB, send the file directly
            
            print('\n[INFO] Uploading file...\n')
            # Getting base name of the file
            file_name = os.path.basename(file_path)
            # Getting the directory of the file
            folder_path = os.path.dirname(file_path)
            # Sending the file
            file_dict = send_file(webhook_url,thread_id,folder_path,file_name,{})
            # Sending the sharing link
            send_message(webhook_url,thread_id,f"File - `{file_name}` sharing link : {file_dict[file_name]}```{file_dict[file_name]}```")
            sys.exit()

    if option in ['B','b','Folder','folder']:
        
        # Getting folder path
        folder_path = input('\nEnter the folder path : ')
        folder_path = folder_path.replace('"','')

        #Check if folder exists
        if not os.path.isdir(folder_path):
            print(f"\n[ERROR] Could not find {folder_path}. Exiting...")
            sys.exit()

        print('\n[INFO] Uploading files...\n')
        
        # Uploading the files
        upload_files(webhook_url,thread_id,folder_path)
        
    else:
        print('\n[ERROR] Invalid option. Exiting...')
        sys.exit()

if option in ['D','d','Download','download']:
    string = input('\nEnter the key or or directly the path of the file containing the Key \n->')

    # Checking if the entered string is empty.
    if string == "":
        print('\n[ERROR] Invalid key. Exiting...')
        sys.exit()

    # Checking if the entered string is a path to the file containing the key.
    if string[0] != "{":
        string = string.replace('"','')
        if os.path.isfile(string):
            # Checking if the file is a txt.
            if string[-4:] != ".txt":
                print('\n[ERROR] Invalid file. It needs to be a .txt file. Exiting...')
                sys.exit()

            with open(string, "r") as f:
                string = f.read()
        else:
            print('\n[ERROR] Could not find the file. Exiting...')
            sys.exit()

    print('\n[INFO] Downloading files...\n')
    folder_path=download_files(string)

    try:
        # Checks if the RAW folder is empty
        os.rmdir(folder_path)
        print("\n[INFO] Files downloaded. Exiting...")
    except:
        print("\n[INFO] Files downloaded. Merging files...")
        zip_merge()
        print("\n[INFO] Original reconstructed successfully. Exiting...")

        # Delete the RAW folder
        for file in os.listdir(folder_path):
            os.remove(f"./Downloads/RAW/{file}")
        os.rmdir(folder_path)

else:
    print('\n[ERROR] Invalid option. Exiting...')
    sys.exit()
