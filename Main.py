#-------------------------------------------------------------------------------
# Name:        Main.py
# Purpose:     Upload files to Discord
#
# Author:      Meit Sant
#
# Created:     13 03 2024
#
# Lead Dev : Meit Sant
#-------------------------------------------------------------------------------

import os
import sys
from Functions import *

webhook_url = "https://discord.com/api/webhooks/1217386966065090590/ZHy6_elF8KG_n2jKWIPYOOhno3K16tvGEhoNlPCxSbRvB4dV6xlmgUwn0zVS27gI6qZl"

thread_id = "1217543005926326382"


print('Discord Uploader and Downloader V1.2')
print('Developed by     : Meit Sant')
print('Licence          : MIT')

#webhook_url = input('\nEnter the webhook URL : ')
#thread_id = input('Enter the thread ID : ')

option = input('\nUpload [U] or Download [D] : ')

if option in ['U','u','Upload','upload']:
    option = input('\nUpload a file [A] or a folder [B] : ')
    if option in ['A','a','File','file']:
        file_path = input('\nEnter the file path : ')
        if file_path == "":
            print('\n[ERROR] Invalid file path. Exiting...')
            sys.exit()
        #Check if file exists
        if not os.path.isfile(file_path):
            print(f"\n[ERROR] File {file_path} does not exist.")
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
        
    
    elif option in ['B','b','Folder','folder']:
        folder_path = input('\nEnter the folder path : ')
        print('\nUploading files...\n')
        upload_files(webhook_url,thread_id,folder_path)
        print('\nFiles uploaded. Exiting...')
    else:
        print('Invalid option. Exiting...')
        sys.exit()

elif option in ['D','d','Download','download']:
    string = input('\nEnter the key string : ')
    
    print('\nDownloading files...\n')
    download_files(webhook_url,thread_id,string)

    
    try:
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
    print('Invalid option. Exiting...')
    sys.exit()