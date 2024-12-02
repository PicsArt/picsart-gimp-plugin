
from gimpfu import *
import urllib2
import json
import os

def set_api_key(image, drawable, api_key):
    
    if not api_key:
        gimp.message("API key not entered.")
        return

    
    home_directory = os.path.expanduser("~")
    file_name = ".picsart_api_key.txt"
    file_path = os.path.join(home_directory, file_name)

    
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("")  
    
    url = "https://api.picsart.io/tools/1.0/balance"
    headers = {
        "X-Picsart-API-Key": api_key,
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        data = json.load(response)

        
        if data and 'credits' in data:
            
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
    "<Image>/Picsart/Set API Key",  
    "*",  
    [
        (PF_STRING, "api_key", "Enter API Key", "")  
    ],
    [],
    set_api_key  
)

main()