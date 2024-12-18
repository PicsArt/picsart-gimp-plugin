# -*- coding: utf-8 -*-
from gimpfu import *
import urllib2
import json
import os

def set_api_key(image, drawable, api_key):
    # Check if the API key is provided
    if not api_key:
        gimp.message("API key not entered.")
        return

    # Get the current working directory
    home_directory = os.path.expanduser("~")
    file_name = ".picsart_api_key.txt"
    file_path = os.path.join(home_directory, file_name)

    # Check if the file exists; if not, create it
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("")  # Create an empty file
    # Example API request logic 
    url = "https://api.picsart.io/tools/1.0/balance"
    headers = {
        "X-Picsart-API-Key": api_key,
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0",
        "X-Picsart-Plugin": "Gimp"
    }

    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        data = json.load(response)

        # Check if the API key is valid
        if data and 'credits' in data:
            # Save or update the API key in the file
            with open(file_path, "w") as f:
                f.write(api_key)
            gimp.message("API key is valid. Balance: {}".format(data['credits']))
        else:
            gimp.message("Invalid API key or response from server.")
    
    except urllib2.HTTPError as e:
         gimp.message("\nIncorrect API key. You can click the 'My Account' button to retrieve API key.\n")

    except urllib2.URLError as e:
        gimp.message("\nURL Error: {}\n".format(e.reason))
    except Exception as e:
        gimp.message("\nAn error occurred: {}\n".format(str(e)))

register(
    "python_fu_set_api_key",
    "Sign up at picsart.io, copy and put here your API Key.",
    "Prompt for API key input.",
    "Erik",
    "Torosyan",
    "2024",
    "<Image>/Picsart/Set API Key",  # Menu path
    "*",  # Image type
    [
        (PF_STRING, "api_key", "Enter API Key", "")  # Input field for the API key
    ],
    [],
    set_api_key  # Function that handles the API key
)

main()