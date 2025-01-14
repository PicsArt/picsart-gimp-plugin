# -*- coding: utf-8 -*-
from gimpfu import *
import urllib2
import json
import tempfile
import os
def read_api_key():
    file_name = ".picsart_api_key.txt"
    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, file_name)

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            api_key = f.read().strip()
            if api_key:
                return api_key
            else:
                return False
    else:
        return False

def remove_background_from_current_image(image, drawable):
    api_key = read_api_key()

    supported_types = ['.jpg', '.png', '.tiff', '.webp', '.mpo']

    image_filename = pdb.gimp_image_get_filename(image)
    if image_filename:
        file_extension = os.path.splitext(image_filename.lower())[1]
        if file_extension not in supported_types:
            gimp.message("\nUnsupported file type: {}. Supported types are: JPEG, PNG, TIFF, WEBP, MPO.\n".format(file_extension.upper()))
            return
    else:
        gimp.message("\nError: Cannot determine the file type.\n")
        return

    if api_key:
        url = "https://api.picsart.io/tools/1.0/removebg"
        headers = {
            "X-Picsart-API-Key": api_key,
            "accept": "application/json",
            "User-Agent": "Gimp",
            "X-Picsart-Plugin": "Gimp",
        }

        temp_image_path = tempfile.mktemp(suffix=file_extension)
        pdb.gimp_file_save(image, drawable, temp_image_path, temp_image_path)

        with open(temp_image_path, "rb") as image_file:
            file_content = image_file.read()

        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        data = (
            '--' + boundary + '\r\n' +
            'Content-Disposition: form-data; name="image"; filename="image' + file_extension + '"\r\n' +
            'Content-Type: image/' + file_extension[1:] + '\r\n\r\n' +
            file_content +
            '\r\n--' + boundary + '--\r\n'
        )

        request = urllib2.Request(url, data)
        request.add_header('Content-Type', 'multipart/form-data; boundary={}'.format(boundary))
        for key, value in headers.items():
            request.add_header(key, value)

        try:
            response = urllib2.urlopen(request)
            response_data = json.loads(response.read())
            print("Response of API:", response_data)

            if response_data.get("data"):
                image_url = response_data["data"]["url"]

                try:
                    request_image = urllib2.Request(image_url)
                    request_image.add_header('User-Agent', 'Gimp')
                    request_image.add_header('Referer', 'https://www.picsart.com/')

                    response_1 = urllib2.urlopen(request_image)
                    image_data = response_1.read()

                except urllib2.HTTPError as e:
                    gimp.message("HTTP Error: " + str(e.code))
                    print("Error HTTP:", e.code, e.read())
                    return
                except urllib2.URLError as e:
                    gimp.message("URL Error: " + str(e.reason))
                    print("Error URL:", e.reason)
                    return

                temp_file_out = tempfile.NamedTemporaryFile(delete=False, suffix=".png")#this momnt 
                temp_file_out.write(image_data)
                temp_file_out.close()

                new_image = pdb.gimp_file_load(temp_file_out.name, temp_file_out.name)

                if new_image:
                    gimp.Display(new_image)
                    gimp.displays_flush()
                else:
                    gimp.message("\nError loading image in GIMP\n")

                os.remove(temp_file_out.name)
            else:
                gimp.message("\nError in response: " + str(response_data))

        except urllib2.HTTPError as e:
            gimp.message("\nThere is an issue with the API key. Please use the 'Set API Key' button to update it, or click the 'My Account' button to retrieve your API key.\n")

        except urllib2.URLError as e:
            gimp.message("\nURL error: " + str(e.reason)) 
        finally:
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
    else:
        gimp.message("\nThere is an issue with the API key. Please use the 'Set API Key' button to update it, or click the 'My Account' button to retrieve your API key.\n")
        return

register(
    "python_fu_remove_bg",
    "Remove Background from Current Image",
    "Remove the background of the current image using Picsart API",
    "Picsart",
    "API",
    "2025",
    "<Image>/Picsart/Remove Background",  
    "*",  
    [],
    [],
    remove_background_from_current_image
)

main()