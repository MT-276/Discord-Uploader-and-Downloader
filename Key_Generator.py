#-------------------------------------------------------------------------------
# Name:             Key_Generator.py
# Purpose:          Upload files to Discord
#
# Created:          16 06 2024
# License:          Apache License Version 2.0
#
# Developed by:     Meit Sant [Github:MT_276]
#-------------------------------------------------------------------------------

print(f'Key generator for Discord Uploader and Downloader')
print('Developed by     : Meit Sant [Github:MT_276]')
print('Licence          : Apache License Version 2.0')

        
def encode_Dict(file_dict):
    '''
    Encoding the original dictionary into a dictrionary that is smaller in size.
    '''
    New_dict = {}
    for i in file_dict:
        New_dict['File_Name'] = i[:-4]
        break

    for i in file_dict:
        New_dict[i[-3:]] = file_dict[i][39:]

    return New_dict
    
key = {}
c = 0

while True:
    c += 1
    file_url = input(f'Enter the file URL [{c:03}]----->')
    
    if file_url == 'exit':
        break
    if file_url == '':
        continue
    if file_url == 'redo':
        continue
    
    file_name = file_url.split('/')[-1].split('?')[0]
    key[file_name] = file_url

if key == {}:
    print(f'\n[INFO] No files were added to the key')
    exit()
print(f'\nKey : {encode_Dict(key)}')

# Saving the key to a file
key = encode_Dict(key)
with open(f'Keys/Key_{file_name.split(".")[0]}.txt', 'w') as file:
    file.write(str(key))