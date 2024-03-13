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

import os
import sys
from Functions import *

webhook_url = "https://discord.com/api/webhooks/1217386966065090590/ZHy6_elF8KG_n2jKWIPYOOhno3K16tvGEhoNlPCxSbRvB4dV6xlmgUwn0zVS27gI6qZl"

thread_id = "1217543005926326382"

folder_path = "/workspaces/Discord-Uploader-and-Downloader/Zipped/"

upload_files(webhook_url,thread_id,folder_path)
