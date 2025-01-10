from gimpfu import *
import gtk 
import webbrowser  

def show_styled_message_dialog_with_link():
    dialog = gtk.Dialog(
        "My account", 
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        (gtk.STOCK_OK, gtk.RESPONSE_OK)
    )
    
    label = gtk.Label()
    label.set_markup("<span font='12' >To manage your API key, click the button below or visit:</span> \n\n")
    
    label.set_padding(10, 10)
    
    button = gtk.Button("Go to Console")
    
    button.set_size_request(100, 40)  
    button.set_property("can-default", True)
    
    button.connect("clicked", lambda w: webbrowser.open("https://console.picsart.io/?source=[gimp]utm_medium=app&utmcamping=plugins"))
    
    dialog.vbox.pack_start(label, True, True, 10)
    dialog.vbox.pack_start(button, True, True, 10)
    
    label.show()
    button.show()

    dialog.run()
    dialog.destroy()  

def goToConsole(i, d):
    show_styled_message_dialog_with_link()
register(
    "python_fu_console_picsart",
    "Console Picsart Io",
    "Show API key balance.",
    "Picsart",
    "API",
    "2024",
    "<Image>/Picsart/My Account", 
    "*",  
    [],
    [],
    goToConsole 
)

main()