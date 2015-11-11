class MyScript (SBScript):

	initialOrientation = 0
	offset = SrVec()
	magnitude = 0
	
	def start(self):
		character = scene.getCharacter("ChrBrad")

		self.initialOrientation = character.getHPR().getData(0)
		camera = scene.getPawn("cameraDefault")
		position = scene.getCharacter("ChrBrad").getPosition()
		self.offset = SrVec(position.getData(0) - camera.getEye().getData(0), position.getData(1) - camera.getEye().getData(1), position.getData(2) - camera.getEye().getData(2))
		self.magnitude = self.offset.len()
		cameraUpdate = scene.getDouble("cameraUpdate")

		camera = scene.getPawn("cameraDefault")
		cameraPosition = camera.getPosition() 
		characterPosition = character.getPosition()

		#calculate final camera position
		finalCameraPosition = SrVec(characterPosition.getData(0), cameraPosition.getData(1), characterPosition.getData(2) - self.magnitude)
	
		#set camera to final position
		camera.setEye(finalCameraPosition.getData(0), finalCameraPosition.getData(1), finalCameraPosition.getData(2))
		camera.setPosition(finalCameraPosition)

		#set the camera's focus on the character
		camera.setCenter(characterPosition.getData(0), characterPosition.getData(1), characterPosition.getData(2))

	def myFunction():
		print "myFunction ran!"

	'''
	def update(self, time):
		cameraUpdate = scene.getDouble("cameraUpdate")
		camera = scene.getPawn("cameraDefault")
		cameraPosition = camera.getPosition() 
		character = scene.getCharacter("ChrBrad")
		characterPosition = character.getPosition()
		characterOrientation = character.getHPR().getData(0)

		#make angle positive
		if characterOrientation < 0:
			characterOrientation += 360
		
		#keeps track of position at each time
		timePositionList = []
		timePosition = (time, characterPosition.getData(0), characterPosition.getData(1), characterPosition.getData(2))
		timePositionList.append(timePosition)

		#set timer
		#milliseconds
		format(time, '.2f')
		stringMilliseconds  = str(int((time % 1) * 100))
		#minutes and seconds
		newTime = int(time)
		minutes = newTime / 60
		seconds = newTime % 60

		#get a 0 in front if only units digit seconds
		if seconds < 10:
			stringSeconds = "0" + str(seconds)
		else:
			stringSeconds = str(seconds)

		text = "Speed: " + str(scene.getDouble("curForwardSpeed")) + " m/s" + "\nCollisions: %.0f" % scene.getDouble("wallCollisionCounter") + "\nTime: " + str(minutes) + ":" + stringSeconds + ":" + stringMilliseconds
		myText.setText(text)

		#print time position
		#for i in range(len(timePositionList)):
		#	print timePositionList[i]
		#add the new orientation
		characterOrientationList.append(characterOrientation)

		#time frame
		while len(characterOrientationList) > cameraUpdate:
			characterOrientationList.pop(0)
		
		#find average
		average = 0
		sum = 0

		for i in range(len(characterOrientationList)):
			sum += characterOrientationList[i]
			average = sum / len(characterOrientationList)

		#set the orientation to the average
		characterOrientation = average

		#find corresponding angle
		correspondingAngle = characterOrientation - 180

		if correspondingAngle < 0:
			correspondingAngle += 360

		#adjust from smartbody angles to cartesian
		correspondingAngle = characterOrientation + 90

		#convert to radians
		correspondingAngleRadians = correspondingAngle * 3.14159 / 180.00	

		#find ratio of x and z
		xcomponent = math.cos(correspondingAngleRadians) 
		zcomponent = math.sin(correspondingAngleRadians)

		#find the true x and z values (x is flipped in smartbody)
		finalOffsetX = xcomponent * self.magnitude * -1
		finalOffsetZ = zcomponent * self.magnitude

		
		#calculate final camera position
		finalCameraPosition = SrVec(characterPosition.getData(0) + finalOffsetX, cameraPosition.getData(1), characterPosition.getData(2) + finalOffsetZ)
	
		#set camera to final position
		camera.setEye(finalCameraPosition.getData(0), finalCameraPosition.getData(1), finalCameraPosition.getData(2))
		camera.setPosition(finalCameraPosition)

		#set the camera's focus on the character
		camera.setCenter(characterPosition.getData(0), characterPosition.getData(1), characterPosition.getData(2))
		
	'''
		
myscript = MyScript()
scene.addScript("frontCamera", myscript)

#scene.removeScript("frontCamera")