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

Program_version = "1.7"
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
            num = file_size//26203915
            if file_size%26203915 != 0:
                num += 1
            print(f'[INFO] The file will be zipped in chunks of {num} files.')
            if num > 10:
                print(f'[INFO] This may take a while...')

            folder_path = zip_and_split(file_path)

            print('[INFO] Zipped.\n\n[INFO] Uploading files...\n')


            upload_files(webhook_url,thread_id,folder_path)

            # Delete the zipped folder
            for i in os.listdir(folder_path):
                os.remove(f"{folder_path}{i}")
            os.rmdir(folder_path)

            print('\n[INFO] Files uploaded. Exiting...')
            sys.exit()
        else:
            print('\n[INFO] Uploading file...\n')
            # Getting base name of the file
            file_name = os.path.basename(file_path)
            # Getting the directory of the file
            folder_path = os.path.dirname(file_path)
            # Sending the file
            file_dict = send_file(webhook_url,thread_id,folder_path,file_name,{})
            # Sending the sharing link
            send_message(webhook_url,thread_id,f"File `{file_name}` sharing link : {file_dict[file_name]}```{file_dict[file_name]}```")
            sys.exit()

    if option in ['B','b','Folder','folder']:
        folder_path = input('\nEnter the folder path : ')
        folder_path = folder_path.replace('"','')

        #Check if folder exists
        if not os.path.isdir(folder_path):
            print(f"\n[ERROR] Could not find {folder_path}. Exiting...")
            sys.exit()

        option = input('\nDo you want to upload \n- The contents of the folder [A] or \n- Folder as a zip [B] : ')

        if option in ['A','a','Contents','contents']:
            print('\n[INFO] Uploading files...\n')
            list_files = os.listdir(folder_path)
            list_files.sort()
            file_dict = {}
            for i,file in enumerate(list_files):
                print(f"{i+1}. ",end='')
                file_dict = send_file(webhook_url,thread_id,folder_path,file,file_dict)
            send_message(webhook_url,thread_id,f"  **   **")

            # Generating the Key string
            str_dict = str(file_dict)

            if len(str_dict) > 1994:
                # Write the key to a file
                dir_name = os.path.basename(folder_path)
                # Checking if a key with same name exists
                if os.path.isfile(f"Key_Folder-{dir_name}.txt"):
                    if os.path.isfile(f"Key_Folder-{dir_name}_1.txt"):
                        i = 2
                        while os.path.isfile(f"Key_Folder-{dir_name}_{i}.txt"):
                            i += 1
                        dir_name = f"{dir_name}_{i}"
                    else:
                        dir_name = f"{dir_name}_1"
                with open(f"Key_Folder-{dir_name}.txt", "w") as f:
                    f.write(str_dict)
                send_message(webhook_url,thread_id,f"Key too large. Key was saved in uploader's pc.")

            send_message(webhook_url,thread_id,f"Key for Downloading. Please Copy-Paste this key in the program to download the files.")
            send_message(webhook_url,thread_id,f"```{str_dict}```")
            print('\n[INFO] Files uploaded. Exiting...')
            sys.exit()

        if option in ['B','b','Zip','zip']:
            print('\n[INFO] Zipping and splitting folder...')
            zip_and_split(folder_path)
            print('[INFO] Zipped.\n\n[INFO] Uploading files...\n')

            # Checking if "./Zipped/" folder exists
            zipped_folder = "./Zipped"

            if os.path.exists(zipped_folder):
                if os.path.exists(f"{zipped_folder}_1"):
                    i = 2
                    while os.path.exists(f"{zipped_folder}_{i}"):
                        i += 1
                    zipped_folder = f"{zipped_folder}_{i}"
                else:
                    zipped_folder = f"{zipped_folder}_1"
            upload_files(webhook_url,thread_id,f"{zipped_folder}/")

            # Delete the zipped folder
            for i in os.listdir(zipped_folder):
                os.remove(f"{zipped_folder}/{i}")
            os.rmdir(zipped_folder)

            print('\n[INFO] Files uploaded. Exiting...')
            sys.exit()

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
        print("\n[INFO] Files merged.\n[INFO] Original reconstructed successfully. Exiting...")

        # Delete the RAW folder
        for file in os.listdir(folder_path):
            os.remove(f"./Downloads/RAW/{file}")
        os.rmdir(folder_path)

else:
    print('\n[ERROR] Invalid option. Exiting...')
    sys.exit()
