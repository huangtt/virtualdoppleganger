winManager = WindowManager.getSingleton()
myText = winManager.createWindow('OgreTray/StaticText', 'myTextBox')   
myText.setText("")
System.getSingleton().getDefaultGUIContext().getRootWindow().addChild(myText)
