from gimpfu import *
import gtk  
import webbrowser  

def show_styled_message_dialog_with_link():
    dialog = gtk.Dialog(
        "Support",
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        (gtk.STOCK_OK, gtk.RESPONSE_OK)
    )
    
    label = gtk.Label()
    label.set_markup("<span font='12'>To support, click the button below or visit:</span> \n\n"
                     "<a href='https://help.picsart.io/'>https://help.picsart.io/</a>")
    
    label.set_padding(10, 10)
    
    button = gtk.Button("Go to Console")
    
    button.set_size_request(100, 40) 
    
    button.connect("clicked", lambda w: webbrowser.open("https://help.picsart.io/"))
    
    vbox = gtk.VBox(spacing=10)
    vbox.pack_start(label, True, True, 0)
    vbox.pack_start(button, True, True, 0)

    dialog.vbox.pack_start(vbox)

    label.show()
    button.show()
    vbox.show()

    dialog.run()
    dialog.destroy()

def goToConsole(i, d):
    show_styled_message_dialog_with_link()

register(
    "python_fu_support_picsart",
    "Support Picsart Io",
    "Show API key balance.",
    "Erik",
    "Torosyan",
    "2024",
    "<Image>/Picsart/Support", 
    "*",
    [],
    [],
    goToConsole 
)

main()
