# <img src="Lorem Ipsum" width="500" alt="DUAD Logo">

## Overview

The `Discord Uploader-and-Downloader` is an application designed to upload and download files directly from or into your Discord server using webhooks.

### Features

1. **Upload Files**: Uploads individual files and folders to Discord. If the file is above the upload limit set by Discord (10 MB as of 2025) then the program will zip and split the file into chunks and will upload them.  

2. **Download Files**: You can download files from Discord by using the "Key" provided by the uploader.

>Note: As of 2025, the key will expire after 24 hours, so you will need to download the file(s) within that time frame or you can regenerate a new key using `Key_Generator.py`.

3. **Generate Keys**: If the key expires, you will have to manually copy each link of the uploaded files and paste them in `Key_Generator.py`as directed, to generate a new key.

### Requirements

- Python installed on your machine (`3.x` recommended).
- A Discord account with permission on a server to create webhooks.
- You may enable the "developer mode" in Discord settings to easily copy IDs for channels and webhooks.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/YourUsername/Discord-Uploader-and-Downloader.git
   ```

2. Run the main.py to start uploading/downloading files.

> You don't need to install anything. The program will automatically install the required libraries when you run `Main.py`.

## Usage Guide

### Setting Up Webhook

To use `DUAD`, you need to set up a webhook in your Discord server. Follow these steps:

1. [OPTIONAL] Create a text channel in your Discord server.
2. Go to Server Settings > Integrations > Webhooks > New Webhook.
3. Change the channel to the one you created (or any channel you want to use).
4. Copy the Webhook URL. I recommend, pasting the URL in the channel for easy access.
5. In the channel, create a new thread > Copy the thread ID (you can do this by right-clicking the thread name and selecting "Copy Thread ID" if you have developer mode enabled in Discord settings).
6. Run the `Main.py` file in your terminal:

   ```sh
   python Main.py
   ```

7. When prompted, enter the Webhook URL and the thread ID you copied earlier and follow the prompts to upload or download files.

### Uploading Files

1. To start uploading, type `U` when prompted in the terminal after running the main script file (`Main.py`).

2. You can upload an individual file or folders.

    - Type `A` to upload a file.
    - Type `B` to upload a folder.

3. After selecting the file or folder, an explorer window will open. Navigate to the file or folder you want to upload and select it.

4. You may choose whether to allow users to download the file anonymously or not.
    - Type `Y` to allow anonymous downloads.

    - Type `N` to not allow anonymous downloads (this will send a message in the thread with the window's username of the downloader).

5. The program will then upload the file(s) or folder to the specified Discord channel using the webhook URL and thread ID you provided.

After the upload is complete, a "Key" will be generated and saved in the folder `Keys`. You can share this key with others to allow them to download the file(s) later.

### Downloading Files

1. To start downloading, type `D` when prompted in terminal after running the main script file (`Main.py`).

2. You will be asked "What is the format of the key?".
    - Type `A` if you have the key in text form (e.g., `{'File_Name': ...}`).
    - Type `B` if you have the `.txt` file containing the key.

3. If you selected `A`, paste the key in the terminal when prompted. If you selected `B`, navigate to the `.txt` file containing the key and select it.

The program will then download the file(s) associated with the key from the Discord channel and save them in the `Downloads` folder.

## Contributing

If you wish to contribute to this project, feel free to submit a pull request or open an issue on the GitHub repository. Contributions are welcome!
