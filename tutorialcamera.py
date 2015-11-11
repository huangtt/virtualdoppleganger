# Camera at the beginning of the Virtual Doppelganger game. Camera eye follows character.

def timer():
	return time.clock()

class MyScript (SBScript):

	def start(self):
		camera = scene.getPawn("cameraDefault")
		position = scene.getCharacter("ChrBrad").getPosition()

	def update(self, time):
		camera = scene.getPawn("cameraDefault")
		character = scene.getCharacter("ChrBrad")
		position = character.getPosition()
		#speed = scene.getDouble("curForwardSpeed")

		#set the camera's focus on the character
		camera.setCenter(position.getData(0), position.getData(1), position.getData(2))

		#timeElapsed = timer()

		if time < 8:
			myText.setText("Welcome to the Maze game, listen to the following instructions!")
		elif time >= 8 and time < 20:
			myText.setText("First try turning around! \nA: turn left \nD: turn right")
		elif time >= 20 and time < 30:
			myText.setText("Now try walking forward! \nW: increase speed \nS: decrease speed")
		elif time >= 30 and time < 40:
			myText.setText("Holding W/S rapidly increases/decreases the speed")
		elif time >= 40 and time < 50:
			myText.setText("The maze will require you to move around obstacles, try turning while running!")
		elif time >= 50 and time < 60:
			myText.setText("Hitting a wall or trap sets your speed back to zero. Watch out or they will slow you down!")
		elif time >= 60 and time < 70:
			myText.setText("The maze requires narrow turns, make sure you can slow down and stop \n(Hold S) ")	
		elif time >= 70 and time < 80:
			hits = scene.getDouble("mineCounter") + scene.getDouble("tutorialWallCounter")
			text = "Speed: " + str(scene.getDouble("curForwardSpeed")) + " m/s" + "\nHits: %.0f" % hits + "\nTime: 0:00"
			myText.setText("Track your speed, # of hits, and time here!\n" + text)
		else:
			hits = scene.getDouble("mineCounter") + scene.getDouble("tutorialWallCounter")
			text = "Speed: " + str(scene.getDouble("curForwardSpeed")) + " m/s" + "\nHits: %.0f" % hits + "\nTime: 0:00"
			myText.setText("Press P to play!\n" + text)

myscript = MyScript()
scene.addScript("tutorialcamera", myscript)

#scene.removeScript("tutorialcamera")