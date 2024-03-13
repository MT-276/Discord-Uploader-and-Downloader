#-------------------------------------------------------------------------------
# Name:        Main.py
# Purpose:     Main graphical user interface for SID
#
# Author:      Meit Sant
#
# Created:     13 03 2024
#
# Lead Dev : Meit Sant
#-------------------------------------------------------------------------------

import json
from discord_webhook import DiscordWebhook
import os
import zipfile

def send_message(webhook_url,thread_id,message):
    webhook = DiscordWebhook(url=webhook_url, thread_id=thread_id, content=message)
    response = webhook.execute()
    #print(f"Message sent to Discord: {message}")

def send_file(webhook_url,thread_id,folder_path,file_name,file_dict):
    
    webhook = DiscordWebhook(url=webhook_url, thread_id=thread_id)
    
    with open(f"{folder_path}/{file_name}", "rb") as f:
        webhook.add_file(file=f.read(), filename=file_name)
    
    response = webhook.execute()
    
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
    
    send_message(webhook_url,thread_id,Str)
    