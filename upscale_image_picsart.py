
from gimpfu import *
import urllib2
import json
import tempfile
import os

def read_api_key():
    
    home_directory = os.path.expanduser("~")
    file_name = ".picsart_api_key.txt"
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

def upscale_from_current_image(image, drawable, upscale_factor):
    api_key = read_api_key()
    if api_key is False:
        gimp.message("\nThere is an issue with the API key. Please use the 'Set API Key' button to update it, or click the 'My Account' button to retrieve your API key.\n")
        return

    
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

    allowed_factors = ["2", "4", "6", "8"]
    upscale_factor = allowed_factors[upscale_factor]

    url = "https://api.picsart.io/tools/1.0/upscale"
    headers = {
        "X-Picsart-API-Key": api_key,
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Referer": "https://www.picsart.com/",
        "Origin": "https://www.picsart.com"
    }

    
    temp_image_path = tempfile.mktemp(suffix=".jpg")
    pdb.gimp_file_save(image, drawable, temp_image_path, temp_image_path)

    
    with open(temp_image_path, "rb") as image_file:
        file_content = image_file.read()

    
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    data = (
        '--' + boundary + '\r\n' +
        'Content-Disposition: form-data; name="image"; filename="image.jpg"\r\n' +
        'Content-Type: image/jpeg\r\n\r\n' +
        file_content +
        '\r\n--' + boundary + '\r\n' +
        'Content-Disposition: form-data; name="upscale_factor"\r\n\r\n' +
        str(upscale_factor) +
        '\r\n--' + boundary + '--\r\n'
    )

    
    request = urllib2.Request(url, data)
    request.add_header('Content-Type', 'multipart/form-data; boundary={}'.format(boundary))

    for key, value in headers.items():
        request.add_header(key, value)

    try:
        
        response = urllib2.urlopen(request)
        response_data = json.loads(response.read())

        if response_data.get("data"):
            
            image_url = response_data["data"]["url"]

            
            try:
                
                image_request = urllib2.Request(image_url)
                for key, value in headers.items():
                    image_request.add_header(key, value)
                response_1 = urllib2.urlopen(image_request)
                image_data = response_1.read()

                
                temp_file_out = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
                temp_file_out.write(image_data)
                temp_file_out.close()

                
                new_image = pdb.gimp_file_load(temp_file_out.name, temp_file_out.name)
                gimp.Display(new_image)
                gimp.displays_flush()

                
                os.remove(temp_file_out.name)
            except urllib2.HTTPError as e:
                gimp.message("HTTP Error: " + str(e.code))
                return
            except urllib2.URLError as e:
                gimp.message("URL Error: " + str(e.reason))
                return
        else:
            gimp.message("Error in response: " + str(response_data))
    except urllib2.HTTPError as e:
        gimp.message("\nThere is an issue with the API key. Please use the 'Set API Key' button to update it, or click the 'My Account' button to retrieve your API key.\n")
    except urllib2.URLError as e:
        gimp.message("URL error: " + str(e.reason))
    finally:
        
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)


register(
    "python_fu_upscale",
    "Improve your image resolution with ease. Please select your upscale factor:",
    "Upscale of the current image using the Picsart API",
    "Romik",
    "Romik",
    "2024",
    "<Image>/Picsart/Upscale",  
    "*",
    [
        (PF_OPTION, "upscale_factor", "Upscale Factor", 0, ["2", "4", "6", "8"])  
    ],
    [],
    upscale_from_current_image
)


main()