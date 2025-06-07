#-------------------------------------------------------------------------------
# Name:             Main.py
# Purpose:          Upload files to Discord
#
# Created:          13 03 2024
# License:          Apache License Version 2.0
#
# Developed by:     Meit Sant [Github:MT_276]
#-------------------------------------------------------------------------------

programVersion = "2.1"
mode = "Test"

from Functions import *

print(f'Discord Uploader and Downloader V{programVersion}')
print('Developed by     : Meit Sant [Github : MT_276]')
print('Licence          : Apache License Version 2.0')

max_upload_size = 10 # in MB



option = input('\nChoose an option [U/D] : \n[U] Upload \n[D] Download\n-> ')

if option in ['U','u','Upload','upload']:

    webhook_url = input('\nEnter the webhook URL : ')
    thread_id = input('Enter the thread ID : ')
    
    update_webhook(webhook_url,programVersion,mode)

    option = input('\nWhat do you want to upload [A/B] : \n[A] File \n[B] Folder \n-> ')

    if option in ['A','a','File','file']:

        file_path = Choose_File("file")

        # Checking if the entered string is empty.
        if file_path in [""," ",None]:
            print('\n[ERROR] Invalid file path. ')
            sys.exit()

        file_path = file_path.replace('"','')

        print(f"[INFO] Chosen file's path : {file_path}")

        # Check if file exists
        if not os.path.isfile(file_path):
            print(f"\n[ERROR] Could not find {file_path}. ")
            sys.exit()

        # Checking size of file
        file_size = os.path.getsize(file_path)

        # Anonymous download option
        Anonymous_download = input("\nDo you want to enable anonymous download ? [Y/N] : \n[Y] NO log message will be sent to the channel. \n[N] Log message will be sent to the channel.\n-> ")
        
        if Anonymous_download in ['Y','y','Yes','yes']:
            Anonymous_download = True
        else:
            Anonymous_download = False
        
        # Convert max upload size to decimal
        max_upload_size = int((max_upload_size-0.001) * 1047576 + 1000) # Very complicated mafs
        
        # If file size is greater than Max upload size, zip and split the file
        if file_size > max_upload_size:

            # Getting base name of the file
            file_name = os.path.basename(file_path)

            print(f"\n[WARN] File {file_name} is too large to send independently [Over 25 MB].")
            print('\n[INFO] Zipping and splitting file...')

            # Calculating the number of files to be zipped
            num = file_size//max_upload_size
            if file_size%max_upload_size != 0:
                num += 1
            print(f'[INFO] The file will be zipped in chunks of {num} files.')
            if num > 10:
                print(f'[INFO] This may take a while...')

            # Checking if a key already exists
            if os.path.exists(f"Keys/Key_{file_name}.txt"):
                print(f"\n[INFO] A key already exists for {file_name}.")

                # Checking if there was a crash during the last upload
                with open(f"Keys/Key_{file_name}.txt", "r") as f:
                    key = eval(f.read())

                if len(key) < num+1:
                    print(f"[INFO] A crash was detected during the last upload.")
                    continue_upload = input("\nDo you want to continue uploading from last known file ? [Y/N] : \n[Y] Yes \n[N] No\n-> ")

                    if continue_upload in ['N','n','No','no']:
                        
                        print('\n[INFO] Zipping and splitting file...')
                        
                        folder_path = zip_and_split(file_path)

                        print('[INFO] Zipped.\n\n[INFO] Uploading files...\n')

                        # Uploading the files
                        upload_files(webhook_url,thread_id,folder_path,Anonymous_download)

                    elif continue_upload in ['Y','y','Yes','yes']:

                        # Getting all the names of the subfolders
                        subfolders = []

                        current_path = os.getcwd()
                        for entry in os.listdir():
                            full_path = os.path.join(current_path, entry)
                            if os.path.isdir(full_path):
                                subfolders.append(entry)

                        # Scanning all the subfolders for the zipped files of the specific file
                        for subfolder in subfolders:
                            if "Zipped" in subfolder:
                                files = os.listdir(f"{current_path}\\{subfolder}\\")
                                if file_name in files[0]:
                                    folder_path = f"{current_path}\\{subfolder}\\"
                                    break

                        try:
                            files.sort()
                        except NameError:
                            print("\n[ERROR] The zip files are not present. Falling back to zipping the file again.")
                            print('\n[INFO] Zipping and splitting file...')
                            folder_path = zip_and_split(file_path)

                            print('[INFO] Zipped.\n\n[INFO] Uploading files...\n')

                            # Uploading the files
                            upload_files(webhook_url,thread_id,folder_path,Anonymous_download)
                            
                            # Delete the zipped folder
                            for i in os.listdir(folder_path):
                                os.remove(f"{folder_path}{i}")
                            os.rmdir(folder_path)

                            print('\n[INFO] Files uploaded. ')
                            sys.exit()
                            
                        item_lst = list(key.keys())

                        for num,file in enumerate(files):
                            file_num = file.split(".")[-1]
                            try:
                                if file_num == item_lst[num+1]:
                                    # Create a folder if not present named "Restore" in Zipped
                                    if not os.path.exists("Restore"):
                                        os.mkdir("Restore")
                                    # Move the file to the "Restore" folder
                                    os.rename(f"{folder_path}/{file}",f"Restore/{file}")
                                else:
                                    pass
                            except:
                                pass
                        files = os.listdir(folder_path)
                        files.sort()
                        print(f"\n[INFO] Continuing upload from file {files[0]}...\n")

                        upload_files(webhook_url,thread_id,folder_path,Key=key)

                        # Delete the "Restore" folder
                        for i in os.listdir("Restore"):
                            os.remove(f"Restore/{i}")
                        os.rmdir("Restore")

                        # Delete the zipped folder
                        for i in os.listdir(folder_path):
                            os.remove(f"{folder_path}{i}")
                        os.rmdir(folder_path)
                        
                        # Delete the old Key
                        os.remove(f"Keys/Key_{file_name}.txt")

                        print('\n[INFO] Files uploaded. ')
                        sys.exit()

                    else:
                        print("[ERROR] Invalid option. Defaulting to NO.")
                        print('\n[INFO] Zipping and splitting file...')
                        
                        folder_path = zip_and_split(file_path)

                        print('[INFO] Zipped.\n\n[INFO] Uploading files...\n')

                        # Uploading the files
                        upload_files(webhook_url,thread_id,folder_path,Anonymous_download)
                        
            folder_path = zip_and_split(file_path,max_upload_size)

            print('[INFO] Zipped.\n\n[INFO] Uploading files...\n')

            # Uploading the files
            upload_files(webhook_url,thread_id,folder_path,Anonymous_download)

            # Delete the zipped folder
            for i in os.listdir(folder_path):
                os.remove(f"{folder_path}{i}")
            os.rmdir(folder_path)

            print('\n[INFO] Files uploaded. ')
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

    elif option in ['B','b','Folder','folder']:

        # Getting folder path
        folder_path = Choose_File("folder")
        folder_path = folder_path.replace('"','')
        
        # Check if folder exists
        if not os.path.isdir(folder_path):
            print(f"\n[ERROR] Could not find {folder_path}. ")
            sys.exit()
            
        # Information about the folder
        print(f"\n[INFO] Chosen folder's path : {folder_path}")
        print(f"[INFO] Number of files in the folder : {len(os.listdir(folder_path))}")
        
        # Check if the uploader wants to enable or disable Anonymous download
        Anonymous_download = input("\nDo you want to enable anonymous download ? [Y/N] : \n[Y] NO log message will be sent to the channel. \n[N] Log message will be sent to the channel.\n-> ")
        if Anonymous_download in ['N','n','No','no']:
            Anonymous_download = False

        print('\n[INFO] Uploading files...\n')

        # Uploading the files
        upload_files(webhook_url,thread_id,folder_path,Anonymous_download)
        
        # All files uploaded message
        print('\n[INFO] Files have been uploaded. ')

    else:
        print('\n[ERROR] Invalid option. ')
        sys.exit()

elif option in ['D','d','Download','download']:
    # Option if the user has the file containing the key or the key itself.
    opening_key = input('\nWhat is the format of the key ? [A/B] \n[A] Key itself \n[B] File containing the key \n-> ')

    if opening_key in ['A','a','Key','key']:
        # If the user has the key itself.
        key = input('\nEnter the key \n->')
        key = key.replace('"','')

    elif opening_key in ['B','b','File','file']:
        # If the user has the file containing the key.
        key = Choose_File("file")
        if key == "":
            print('\n[ERROR] Operation cancelled.\n')
            sys.exit()
        print(f'[INFO] Chosen file\'s path : {key}')
    else:
        print('\n[ERROR] Invalid option.\n')
        sys.exit()
    
    # Checking if the entered string is empty.
    if key == "":
        # If the user did not enter anything.
        print('\n[ERROR] No key entered.')
        sys.exit()
    
    if key[0] != '{':
        if os.path.isfile(key):
            # Checking if the file is a txt.
            if key[-4:] != ".txt":
                print('\n[ERROR] Invalid file. It needs to be a .txt file. ')
                sys.exit()

            with open(key, "r") as f:
                key = f.read()
        else:
            print('\n[ERROR] Could not find the file. ')
            sys.exit()

    print('\n[INFO] Downloading files...\n')
    folder_path = download_files(key)

    try:
        # Checks if the RAW folder is empty
        os.rmdir(folder_path)
        print("\n[INFO] Files downloaded. ")
    except:
        print("\n[INFO] Files downloaded. Merging files...")
        zip_merge(folder_path)
        print("\n[INFO] Original reconstructed successfully.")

        # Delete the RAW folder
        for file in os.listdir(folder_path):
            os.remove(f"{folder_path}{file}")
        os.rmdir(folder_path)

else:
    print('\n[ERROR] Invalid option. ')
    sys.exit()
