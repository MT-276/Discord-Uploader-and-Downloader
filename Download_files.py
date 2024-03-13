import requests
import discord
import os 

folder_path = "./Downloads/"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

webhook_url = "https://discord.com/api/webhooks/1217386966065090590/ZHy6_elF8KG_n2jKWIPYOOhno3K16tvGEhoNlPCxSbRvB4dV6xlmgUwn0zVS27gI6qZl"
thread_id = "1217536611211022487"
string = '{"Wholesome_Pic.zip.001": "https://cdn.discordapp.com/attachments/1217536611211022487/1217536727510679632/Wholesome_Pic.zip.001?ex=66046270&is=65f1ed70&hm=1d15244de4d4bf6cc597f7e8395268ab444843be7055d112692bed93b3cfa8ec&", "Wholesome_Pic.zip.002": "https://cdn.discordapp.com/attachments/1217536611211022487/1217536776944484493/Wholesome_Pic.zip.002?ex=6604627c&is=65f1ed7c&hm=3e9dbb12664aedb4f26342f82343bf1cb6f93ea93b34d0baaa9d4880610b66c9&", "Wholesome_Pic.zip.003": "https://cdn.discordapp.com/attachments/1217536611211022487/1217536822553481296/Wholesome_Pic.zip.003?ex=66046287&is=65f1ed87&hm=53b85b9ba4a486296500c3c571f47acb0df38e10d9ae598b554be14d35fd579f&", "Wholesome_Pic.zip.004": "https://cdn.discordapp.com/attachments/1217536611211022487/1217536851737575495/Wholesome_Pic.zip.004?ex=6604628e&is=65f1ed8e&hm=bccc7de668e4daf11e20ac8bd9f0bb634e7d5986ce88bfc6be4271b5375cd61f&"}'

file_dict = eval(string)

for i in file_dict:
    url = file_dict[i]
    print(f"Downloading file {i}...")
    r = requests.get(url, allow_redirects=True)
    open(f"{folder_path}{i}", 'wb').write(r.content)
    print(f"File {i} downloaded.")