# -*- coding: utf-8 -*-
from gimpfu import *
import urllib2
import json
import tempfile
import os

def read_api_key():
    # Define the path for the API key file
    home_directory = os.path.expanduser("~")
    file_name = ".picsart_api_key.txt"
    file_path = os.path.join(home_directory, file_name)
    # Check if the API key file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            api_key = f.read().strip()  # Read and strip any whitespace
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

    # Supported image types
    supported_types = ['.jpg', '.png', '.tiff', '.webp', '.mpo']
    
    # Get the filename and check the file extension
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
        "User-Agent": "Gimp",
        "X-Picsart-Plugin": "Gimp",
    }

    # Save the current image to a temporary file
    temp_image_path = tempfile.mktemp(suffix=".jpg")
    pdb.gimp_file_save(image, drawable, temp_image_path, temp_image_path)

    # Read the content of the saved image file
    with open(temp_image_path, "rb") as image_file:
        file_content = image_file.read()

    # Prepare the multipart/form-data request body
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

    # Create the POST request
    request = urllib2.Request(url, data)
    request.add_header('Content-Type', 'multipart/form-data; boundary={}'.format(boundary))

    for key, value in headers.items():
        request.add_header(key, value)

    try:
        # Send the request and get the response
        response = urllib2.urlopen(request)
        response_data = json.loads(response.read())

        if response_data.get("data"):
            # Extract the URL of the processed image
            image_url = response_data["data"]["url"]

            # Fetch the processed image with appropriate headers
            try:
                # Set up the request for the processed image with headers
                image_request = urllib2.Request(image_url)
                for key, value in headers.items():
                    image_request.add_header(key, value)
                response_1 = urllib2.urlopen(image_request)
                image_data = response_1.read()

                # Save the processed image to a temporary file
                temp_file_out = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
                temp_file_out.write(image_data)
                temp_file_out.close()

                # Load the processed image in GIMP
                new_image = pdb.gimp_file_load(temp_file_out.name, temp_file_out.name)
                gimp.Display(new_image)
                gimp.displays_flush()

                # Delete the temporary file
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
        # Delete the temporary file created for the image
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

# Register the plugin in GIMP with additional parameters
register(
    "python_fu_upscale",
    "Improve your image resolution with ease. Please select your upscale factor:",
    "Upscale of the current image using the Picsart API",
    "Picsart",
    "API",
    "2025",
    "<Image>/Picsart/Upscale",  # Location in GIMP menu
    "*",
    [
        (PF_OPTION, "upscale_factor", "Upscale Factor", 0, ["2", "4", "6", "8"])  # Dropdown menu for upscale factor
    ],
    [],
    upscale_from_current_image
)

# This runs the script
main()