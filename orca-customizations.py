# display Clipboard (Orca + r)

# for Orca Screenreader
# -*- coding: utf-8 -*-


#GTK/GDK
from gi.repository import Gtk, Gdk

# Orca
import orca.orca
import orca.settings
import orca.keybindings
import orca.speech
import orca.braille

#Stuff
import os

##########
Version = "kyle"
##########

#this is need by arch
orca.settings.tty = 1

#Bind Function to key-------------------------
myKeyBindings = orca.keybindings.KeyBindings()

def DefineShortcut(pHandle,pShortcut):
	myKeyBindings.add(orca.keybindings.KeyBinding(
		pShortcut,
		1 << orca.keybindings.MODIFIER_ORCA,
		1 << orca.keybindings.MODIFIER_ORCA,
		pHandle))
	orca.settings.keyBindingsMap["default"] = myKeyBindings
#Bind Function to key+++++++++++

#Display Message ----------------------------
#Speak or Braille
def outputMessage(Message):
	if (orca.settings.enableSpeech):
		orca.speech.speak(Message)
	if (orca.settings.enableBraille):
		orca.braille.displayMessage(Message)
#Display Message +++++++++++++
#Display  Clipboard-------------------------------

def displayClipboard(script, inputEvent=None):
	Message = ""
	FoundClipboardContent = False
	# Get Clipboard
	ClipboardObj = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

	ClipboardText = ClipboardObj.wait_for_text()  
	ClipboardImage = ClipboardObj.wait_for_image()   
   
	if (ClipboardText != None):
		FoundClipboardContent = True
		if (ClipboardObj.wait_is_uris_available()):
			UriList = ClipboardText.split('\n')
			ObjectNo = 0			
			for Uri in UriList:
				ObjectNo += 1
				if (os.path.isdir(Uri)):
					Message = Message + "Folder " #Folder
				if (os.path.isfile(Uri)):
					Message = Message + "File " #File
				if (os.path.ismount(Uri)):
					Message = Message + "Disk " #Mountpoint	 
				if (os.path.islink(Uri)):
					Message = Message + "Link " #Link
				#Message = Message + " " + Uri				
				Message = Message + " " + Uri[Uri.rfind('/') + 1:]
			if (ObjectNo > 1):			
				Message = str(ObjectNo) + " Objects in the clipboard " + Message # X Objects in Clipboard Object Object		
			else:
				Message = str(ObjectNo) + " Objects in the clipboard " + Message # 1 Object in Clipboard Object	
		else:		
			Message = "Text in clipboard " + ClipboardText # Text in Clipboard
	
	if (ClipboardImage != None):
		FoundClipboardContent = True
		Message = "The clipboard contains image data" # Image is in Clipboard

	if (not FoundClipboardContent):
		Message = "The clipboard is empty" #Clipboard is empty
	# Say/braille something.
	outputMessage(Message)
    
	# Consume the event so it will not go to an application.
	return True

# define ClipboardHandler
displayClipboardHandler = orca.input_event.InputEventHandler(
	displayClipboard, "Announce the clipboard content") #Speak Content of the Clipboard
#Display Clipboard++++++++++++++++++++++++++++++

#define shortcuts
DefineShortcut(displayClipboardHandler,"r") # Shortcut Orca + r

