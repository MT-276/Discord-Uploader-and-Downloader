import json
from discord_webhook import DiscordWebhook
import os
import zipfile


webhook_url = "https://discord.com/api/webhooks/1217386966065090590/ZHy6_elF8KG_n2jKWIPYOOhno3K16tvGEhoNlPCxSbRvB4dV6xlmgUwn0zVS27gI6qZl"

thread_id = "1217536611211022487"


def send_message(webhook_url,thread_id,message):
    webhook = DiscordWebhook(url=webhook_url, thread_id=thread_id, content=message)
    response = webhook.execute()
    #print(f"Message sent to Discord: {message}")

def send_file(webhook_url,thread_id,file_name):
    global file_dict
    
    webhook = DiscordWebhook(url=webhook_url, thread_id=thread_id)
    
    with open(f"{folder_path}/{file_name}", "rb") as f:
        webhook.add_file(file=f.read(), filename=file)
    
    response = webhook.execute()
    
    webhook_data = webhook.json['attachments'][0]

    file_dict[webhook_data['filename']] = webhook_data['url']
    
    print(f"File {file_name} sent to Discord.")
        

# file webhook
folder_path = "/workspaces/Discord-Uploader-and-Downloader/Zipped/"
files = os.listdir(folder_path)
files.sort()

file_dict = {}

for file in files:
    send_file(webhook_url,thread_id,file)

Str = json.dumps(file_dict)

send_message(webhook_url,thread_id,Str)


