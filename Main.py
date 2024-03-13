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

folder_path = "/workspaces/Discord-Uploader-and-Downloader/Zipped/"

string = '{"Wholesome_Pic.zip.001": "https://cdn.discordapp.com/attachments/1217536611211022487/1217536727510679632/Wholesome_Pic.zip.001?ex=66046270&is=65f1ed70&hm=1d15244de4d4bf6cc597f7e8395268ab444843be7055d112692bed93b3cfa8ec&", "Wholesome_Pic.zip.002": "https://cdn.discordapp.com/attachments/1217536611211022487/1217536776944484493/Wholesome_Pic.zip.002?ex=6604627c&is=65f1ed7c&hm=3e9dbb12664aedb4f26342f82343bf1cb6f93ea93b34d0baaa9d4880610b66c9&", "Wholesome_Pic.zip.003": "https://cdn.discordapp.com/attachments/1217536611211022487/1217536822553481296/Wholesome_Pic.zip.003?ex=66046287&is=65f1ed87&hm=53b85b9ba4a486296500c3c571f47acb0df38e10d9ae598b554be14d35fd579f&", "Wholesome_Pic.zip.004": "https://cdn.discordapp.com/attachments/1217536611211022487/1217536851737575495/Wholesome_Pic.zip.004?ex=6604628e&is=65f1ed8e&hm=bccc7de668e4daf11e20ac8bd9f0bb634e7d5986ce88bfc6be4271b5375cd61f&"}'


print('Discord Uploader and Downloader V1.0.0')
print('Developed by     : Meit Sant')
print('Licence          : MIT')

option = input('\nUpload file [U] or Download file [D] : ')

if option in ['U','u','Upload','upload']:
    #webhook_url = input('\nEnter the webhook URL : ')
    #thread_id = input('Enter the thread ID : ')
    #folder_path = input('Enter the folder path : ')
    print()
    print('Uploading files...\n')
    upload_files(webhook_url,thread_id,folder_path)

elif option in ['D','d','Download','download']:
    #webhook_url = input('\nEnter the webhook URL : ')
    #thread_id = input('Enter the thread ID : ')
    #string = input('Enter the string : ')
    print()
    print('\nDownloading files...\n')
    download_files(webhook_url,thread_id,string)

else:
    print('Invalid option. Exiting...')
    sys.exit()