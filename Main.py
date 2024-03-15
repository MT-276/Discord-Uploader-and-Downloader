#-------------------------------------------------------------------------------
# Name:        Main.py
# Purpose:     Upload files to Discord
#
# Author:      Meit Sant
#
# Created:     13 03 2024
#
# Lead Dev : Meit Sant
# Testing  : Roshan Boby
#-------------------------------------------------------------------------------
Program_version = "1.5"
mode = "Test"

from Functions import *

webhook_url = "https://discord.com/api/webhooks/1217386966065090590/ZHy6_elF8KG_n2jKWIPYOOhno3K16tvGEhoNlPCxSbRvB4dV6xlmgUwn0zVS27gI6qZl"

thread_id = "1218253959681015900"


print(f'Discord Uploader and Downloader V{Program_version}')
print('Developed by     : Meit Sant')
print('Licence          : MIT')

#webhook_url = input('\nEnter the webhook URL : ')
#thread_id = input('Enter the thread ID : ')

update_webhook(webhook_url,Program_version,mode)

option = input('\nUpload [U] or Download [D] : ')


if option in ['U','u','Upload','upload']:

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
            
        print('\nZipping and splitting file...')
        zip_and_split(file_path)
        
        print('Zipped.\n\nUploading files...\n')
        upload_files(webhook_url,thread_id,"./Zipped/")


        # Delete the zipped folder
        for i in os.listdir("./Zipped/"):
            os.remove(f"./Zipped/{i}")
        os.rmdir("./Zipped/")

        print('\nFiles uploaded. Exiting...')
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
            print('\nUploading files...\n')
            upload_files(webhook_url,thread_id,folder_path)
            print('\nFiles uploaded. Exiting...')
            sys.exit()

        if option in ['B','b','Zip','zip']:
            print('\nZipping and splitting folder...')
            zip_and_split(folder_path)
            print('Zipped.\n\nUploading files...\n')
            upload_files(webhook_url,thread_id,"./Zipped/")

            # Delete the zipped folder
            for i in os.listdir("./Zipped/"):
                os.remove(f"./Zipped/{i}")
            os.rmdir("./Zipped/")

            print('\nFiles uploaded. Exiting...')
            sys.exit()

    else:
        print('[ERROR] Invalid option. Exiting...')
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

    print('\nDownloading files...\n')
    download_files(webhook_url,thread_id,string)

    try:
        # Checks if the RAW folder is empty
        os.rmdir("./Downloads/RAW/")
        print("\nFiles downloaded. Exiting...")
    except:
        print("\nFiles downloaded. Merging files...")
        zip_merge()
        print("\nFiles merged.\nOriginal reconstructed successfully. Exiting...")

        # Delete the RAW folder
        for file in os.listdir("./Downloads/RAW/"):
            os.remove(f"./Downloads/RAW/{file}")
        os.rmdir("./Downloads/RAW/")
else:
    print('\n[ERROR] Invalid option. Exiting...')
    sys.exit()