# Tracking camera during the Virtual Doppelganger game. Camera takes in position and orientation of character and assumes 
# third-person point of view.

characterOrientationList = []
speedList = []
timePositionList = []
velocityList = []
pointList = VecArray()

scene.createDoubleAttribute("windowFrame", 20, True, "", 1, False, False, False, "Updating rate of camera")
scene.createDoubleAttribute("maxTime", 900, True, "", 1, False, False, False, "Updating rate of camera")
scene.createDoubleAttribute("averageSpeed", 0, True, "", 1, False, False, False, "Updating rate of camera")
scene.createStringAttribute("timeText", "", True, "", 1, False, False, False, "Updating rate of camera")

# global values
scalar = 1
counter = 0
text = ""
speedSum = 0
averageSpeed = 0
finishTimeElapsed = 0

# return time
def timer():
	return time.clock()

# set the time text
def setTime(timeElapsed):
		# format time
		format(timeElapsed, '.2f')
		stringMilliseconds  = str(int((timeElapsed % 1) * 100))
		newTime = int(timeElapsed)
		minutes = newTime / 60
		seconds = newTime % 60

		# add 0 to tens digit if only units
		if seconds < 10:
			stringSeconds = "0" + str(seconds)
		else:
			stringSeconds = str(seconds)

		# set time text
		timeText = str(minutes) + ":" + stringSeconds + ":" + stringMilliseconds
		scene.setStringAttribute("timeText", timeText)

class TrackingCamera (SBScript):
	# calculate initial offset
	def start(self):
		camera = scene.getPawn("cameraDefault")
		position = scene.getCharacter("ChrBrad").getPosition()
		self.offset = SrVec(position.getData(0) - camera.getEye().getData(0), position.getData(1) - camera.getEye().getData(1), position.getData(2) - camera.getEye().getData(2))
		self.magnitude = self.offset.len()

	def update(self, timing):
		# get parameters
		global scalar, counter, text, speedSum, averageSpeed, finishTimeElapsed
		windowFrame = scene.getDouble("windowFrame")
		camera = scene.getPawn("cameraDefault")
		cameraPosition = camera.getPosition() 
		character = scene.getCharacter("ChrBrad")
		characterPosition = character.getPosition()
		characterOrientation = character.getHPR().getData(0)
		
		timeElapsed = timer()

		# calculate velocity
		i = len(timePositionList)
		if i <= 1:
			velocity = 0
		else:
			velocity = (math.sqrt((characterPosition.getData(0) - timePositionList[i-1][1])**2 + (characterPosition.getData(1) - timePositionList[i-1][2])**2 + (characterPosition.getData(2) - timePositionList[i-1][3])**2)) / (timeElapsed - timePositionList[i-1][0])
		
		# append tuple to list
		timePosition = (timeElapsed, characterPosition.getData(0), characterPosition.getData(1), characterPosition.getData(2), velocity)
		timePositionList.append(timePosition)
		
		maxTime = scene.getDouble("maxTime")
		finish = scene.getBool("finish")

		# if max time exceeded
		if timeElapsed > maxTime and not finish:
			scene.setBoolAttribute("finish", True)
			scene.setStringAttribute("finishTime", str(maxTime))

		# set timer
		setTime(timeElapsed)

		# print out HUD
		hits = scene.getDouble("hitCounter")
		finish = scene.getBool("finish")
			

		# writes to csv file -- happens once
		if finish and counter == 0:
			# get parameters
			timeString = scene.getString("finishTime")
			mineCollisionCounter = scene.getDouble("mineCollisionCounter")
			wallCollisionCounter = scene.getDouble("wallCollisionCounter")

			# set average speed
			averageSpeed = speedSum / len(speedList)
			scene.setDoubleAttribute("averageSpeed", averageSpeed)

			# name of file (date/time)
			now = str(time.strftime("%m-%d-%Y, %H-%M"))

			# static variable for finished time
			finishTimeElapsed = timeElapsed

			# write to csv file
			with __builtins__.open('output.csv', 'ab') as csvfile:
				fieldnames = ['date_and_time', 'time_finished', 'average_speed', 'mine_hits', 'wall_hits', 'total_hits']
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				writer.writerow({'date_and_time': now, 'time_finished': timeElapsed, 'average_speed': str(averageSpeed), 'mine_hits': str(mineCollisionCounter), 'wall_hits': str(wallCollisionCounter), 'total_hits': str(hits)})
			csvfile.close()

			# increase counter to prevent future overwrites
			counter += 1

			# writes time and position to text value 
			with __builtins__.open(now + ".csv", 'ab') as dataFile:
				fieldnames = ['time_elapsed', 'xPos', 'yPos', 'zPos', 'vel']
				writer = csv.DictWriter(dataFile, fieldnames=fieldnames)

				# write to file
				for i in range(len(timePositionList)):
					# split up tuple
					dataText = str(timePositionList[i])
					dataText = dataText[dataText.find("(")+1:dataText.find(")")]
					positionPoints = dataText.split(",")

					# write
					writer.writerow({'time_elapsed': positionPoints[0], 'xPos': positionPoints[1], 'yPos': positionPoints[2], 'zPos': positionPoints[3], 'vel': positionPoints[4]})
	
			dataFile.close()

			
			# reads file and appends to point list
			with __builtins__.open(now + ".csv", 'rb') as parseFile:
				reader = csv.reader(parseFile)
				for row in reader:
					# point in space
					point = SrVec(float(row[1]), float(row[2]), float(row[3]))
					pointList.append(point)
			parseFile.close()

			
			color = SrVec(1,0,0)
			
			GUIInterface.addLine("path", pointList, color, 2)

			'''
			for i in range(len(pointList)):
				GUIInterface.addPoint("path", pointList[i], color, 100)
			'''

			# text for exceeded time limit
			if finishTimeElapsed > maxTime:
				text = "Test Over! \nAvg Speed: %.2f" % averageSpeed + "\nHits: %.0f" % hits + "\nTime: " + timeString
			# text for finished maze
			else:
				text = "Finished! \nAvg Speed: %.2f" % averageSpeed + "\nHits: %.0f" % hits + "\nTime: " + timeString

			# stop moving
			bml.execBML('*', '<blend name="mocapLocomotion" mode="update" x="0"/>')

			# character faces camera
			bradFacing = SrVec(90, 0, 0)
			character.setHPR(bradFacing)

			# camera faces character
			finalCameraPosition = SrVec(characterPosition.getData(0) + 3, cameraPosition.getData(1), characterPosition.getData(2))
	
			# set eye
			camera.setEye(finalCameraPosition.getData(0), finalCameraPosition.getData(1), finalCameraPosition.getData(2))

			# removes the controller
			manager.removeInterfaceListener(controller)
			
		# maintains the finish HUD text
		elif finish and counter != 0:
			# get parameters
			timeString = scene.getString("finishTime")
			averageSpeed = scene.getDouble("averageSpeed")

			# text for exceeded time limit
			if finishTimeElapsed > maxTime:
				text = "Test Over! \nAvg Speed: %.2f" % averageSpeed + "\nHits: %.0f" % hits + "\nTime: " + timeString
			# text for finished maze
			else:
				text = "Finished! \nAvg Speed: %.2f" % averageSpeed + "\nHits: %.0f" % hits + "\nTime: " + timeString
				
			# continue final camera position
			finalCameraPosition = SrVec(characterPosition.getData(0) + 3, cameraPosition.getData(1), characterPosition.getData(2))
			camera.setEye(finalCameraPosition.getData(0) + self.offset.getData(0), finalCameraPosition.getData(1), finalCameraPosition.getData(2))

		# displays frames info when not finished
		else:
			speed = scene.getDouble("curForwardSpeed")
			speedList.append(speed)
			speedSum += speed
			timeString = scene.getString("timeText")
			text = "Speed: " + str(scene.getDouble("curForwardSpeed")) + " m/s" + "\nHits: %.0f" % hits + "\nTime: " + timeString

			# make angle positive
			if characterOrientation < 0:
				characterOrientation += 360

			# not the first item on the list
			if len(characterOrientationList) != 0:
				# previous frame's orientation (possibly adjusted)
				previous = characterOrientationList[len(characterOrientationList) - 1]
			
				# difference between current and previous
				diff = characterOrientation - previous

				# keep track of how many circles
				# counter clockwise (360+ values)
				if previous >= 360:
					# more than full circle exceeded
					if diff < (-300 * (scalar + 1)):
						scalar += 1

					# returning to previous circle
					elif (previous - characterOrientation) < (300 * scalar):
						# stops and mirrors to negative values
						if scalar > 1:
							scalar -= 1

				# clockwise (negative values)
				elif previous < 0:
					# more than full circle exceeded
					if diff > (300 * (scalar + 1)):
						scalar += 1
					# returning to previous circle
					elif (characterOrientation - previous) < (300 * scalar):
						# stops and mirrors to positive values
						if scalar > 1:
							scalar -= 1
		
				# ERROR: cannot exceed + or - 2160 degrees (6 rotations)
				# catches error
				if scalar >= 6:
					scalar = 1
			
				# adjust for counterclock
				if diff < (-300 * scalar):
					characterOrientation += (360 * scalar)
				# adjust for clock
				if diff > (300 * scalar):
					characterOrientation -= (360 * scalar)

			# add the new orientation
			characterOrientationList.append(characterOrientation)
		
			# exceeds time frame
			while len(characterOrientationList) > windowFrame:
				# remove from list
				characterOrientationList.pop(0)

			# find average
			average = 0
			sum = 0

			# find average orientation
			for i in range(len(characterOrientationList)):
				sum += characterOrientationList[i]
				average = sum / len(characterOrientationList)

			# set the final orientation to the average
			finalOrientation = average

			# find corresponding angle
			correspondingAngle = finalOrientation - 180

			# make positive
			if correspondingAngle < 0:
				correspondingAngle += 360

			# adjust from smartbody angles to cartesian
			correspondingAngle = finalOrientation + 90

			# convert to radians
			correspondingAngleRadians = correspondingAngle * 3.14159 / 180.00	

			# find ratio of x and z
			xcomponent = math.cos(correspondingAngleRadians) 
			zcomponent = math.sin(correspondingAngleRadians)

			# find the true x and z values (x is flipped in smartbody)
			finalOffsetX = xcomponent * self.magnitude * -1
			finalOffsetZ = zcomponent * self.magnitude

			# calculate final camera position
			finalCameraPosition = SrVec(characterPosition.getData(0) - finalOffsetX, cameraPosition.getData(1), characterPosition.getData(2) - finalOffsetZ)
	
			# set camera to final position
			camera.setEye(finalCameraPosition.getData(0), finalCameraPosition.getData(1), finalCameraPosition.getData(2))

			# set the camera's focus on the character
			camera.setCenter(characterPosition.getData(0), characterPosition.getData(1), characterPosition.getData(2))

		# set HUD
		myText.setText(text)
		
myscript = TrackingCamera()
scene.addScript("trackingcamera", myscript)

#scene.removeScript("trackingcamera")
