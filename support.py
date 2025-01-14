# -*- coding: utf-8 -*-
from gimpfu import *
import gtk  # GTK is used to create custom dialog windows
import webbrowser  # Import webbrowser to open the URL in the default browser

def show_styled_message_dialog_with_link():
    # Create a dialog window
    dialog = gtk.Dialog(
        "Support",  # Window title
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        (gtk.STOCK_OK, gtk.RESPONSE_OK)
    )
    
    # Create a label with instructions
    label = gtk.Label()
    label.set_markup("<span font='12'>To support, click the button below or visit:</span> \n\n"
                     "<a href='https://help.picsart.io/'>https://help.picsart.io/</a>")
    
    # Set some padding around the label
    label.set_padding(10, 10)
    
    # Create a button that opens the URL
    button = gtk.Button("Help center")
    
    # Style the button with padding
    button.set_size_request(100, 40)  # Set the button size (width, height)
    
    # Connect button click to open the URL
    button.connect("clicked", lambda w: webbrowser.open("https://help.picsart.io/"))
    
    # Create a VBox and add the label and button to it
    vbox = gtk.VBox(spacing=10)
    vbox.pack_start(label, True, True, 0)
    vbox.pack_start(button, True, True, 0)

    # Add the VBox to the dialog
    dialog.vbox.pack_start(vbox)

    # Show the components
    label.show()
    button.show()
    vbox.show()

    # Display the dialog window
    dialog.run()
    dialog.destroy()  # Destroy the dialog after user interaction

def goToConsole(i, d):
    # Show the styled message dialog with a clickable button and link
    show_styled_message_dialog_with_link()

# Register the plugin in GIMP
register(
    "python_fu_support_picsart",
    "Support Picsart Io",
    "Show API key balance.",
    "Picsart",
    "API",
    "2025",
    "<Image>/Picsart/Support",  # Menu path
    "*",  # Image type, leave empty
    [],
    [],
    goToConsole  # Function that handles the API key
)

# This runs the script
main()