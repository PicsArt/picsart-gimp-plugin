from gimpfu import *
import urllib2
import json
import os

def get_balance(i, d):
    home_directory = os.path.expanduser("~")
    file_name = ".picsart_api_key.txt"
    file_path = os.path.join(home_directory, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            api_key = f.read().strip()
            if api_key:
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

                    if data and 'credits' in data:
                        gimp.message("\nCredits Available: You have {} credits\n\nChange API Key: Enter a new API key if you have one.\n\nBuy More Credits: Visit Picsart.io to purchase additional credits for uninterupted use.".format(data['credits']))
                    else:
                        gimp.message("\nThere is an issue with the API key. Please use the 'Set API Key' button to update it, or click the 'My Account' button to retrieve your API key.\n")
                
                except urllib2.HTTPError as e:
                    gimp.message("\nHTTP Error: {}\n".format(e.code))
                except urllib2.URLError as e:
                    gimp.message("\nURL Error: {}\n".format(e.reason))
                except Exception as e:
                    gimp.message("\nAn error occurred: {}\n".format(str(e)))
            else:
                gimp.message("\nThere is an issue with the API key. Please use the 'Set API Key' button to update it, or click the 'My Account' button to retrieve your API key.\n")
    else:
        gimp.message("\nThere is an issue with the API key. Please use the 'Set API Key' button to update it, or click the 'My Account' button to retrieve your API key.\n")

register(
    "python_fu_get_balance",
    "Get Balance",
    "Show API key balance.",
    "Erik",
    "Torosyan",
    "2024",
    "<Image>/Picsart/Get Balance", 
    "*",
    [],
    [],
    get_balance 
)

main()