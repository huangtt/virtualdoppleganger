# Keyboard controls for character speed and turn. Begins the game when user presses key.

class Controller (GUIInterface.SBInterfaceListener):
	# pressed key
	def onKeyboardPress(self, c):
		# set variables
		maxSpeed = scene.getDouble("maxSpeed")
		minSpeed = scene.getDouble("minSpeed")
		speed = scene.getDouble("curForwardSpeed")
		rate = scene.getDouble("forwardRate")
		turn = scene.getDouble("curTurnAngle")
		turnRate = scene.getDouble("turnRate")
		maxTurnAngle = scene.getDouble("maxTurnAngle")
		minTurnAngle = scene.getDouble("minTurnAngle")

		# speeding up
		if c == "w":
			#increase
			if speed < maxSpeed:
				speed += rate
			# max speed
			else:
				speed = maxSpeed

			#walk
			bml.execBML('*', '<blend name="mocapLocomotion" mode="update" x="' + str(speed) + '"/>')
			scene.setDoubleAttribute("curForwardSpeed", speed)
		# slowing down
		elif c == "s":
			# decrease
			if speed > minSpeed:
				speed -= rate
				scene.setDoubleAttribute("curForwardSpeed", speed)
				bml.execBML('*', '<blend name="mocapLocomotion" mode="update" x="' + str(speed) + '"/>')
			# precision
			if speed < 0.01:
				speed = 0
				scene.setDoubleAttribute("curForwardSpeed", speed)
		# turn left
		elif c == "d":
			if turn >= minTurnAngle and turn <= maxTurnAngle:
				turn -= turnRate
				scene.setDoubleAttribute("turnRate", turnRate)

			bml.execBML('*', '<blend name="mocapLocomotion" mode="update" x="' + str(speed) + '" y = "' + str(turn) + '"/>')

		# turn right	
		elif c == "a":
			if turn >= minTurnAngle and turn <= maxTurnAngle:
				turn += turnRate
				scene.setDoubleAttribute("turnRate", turnRate)

			bml.execBML('*', '<blend name="mocapLocomotion" mode="update" x="' + str(speed) + '" y = "' + str(turn) + '"/>')

		# begin playing
		elif c == "p":
			# stop the tutorial
			scene.removeScript("tutorialcamera")

			# reset the character
			character.setPosition(SrVec(.217, 1, 45.87))

			# reset the speed
			speed = 0
			turn = 0
			scene.setDoubleAttribute("curForwardSpeed", speed)
			bml.execBML('*', '<blend name="mocapLocomotion" mode="update" x="' + str(speed) + '"/>')

			# reset orientation
			bradFacing = SrVec(176, 0, 0)
			character.setHPR(bradFacing)

			# run the tracking camera
			scene.run("trackingcamera.py")

			# take off the wall
			scene.getPawn("Wall").setPosition(SrVec(0,100,0))

		return True

	# released key
	def onKeyboardRelease(self, c):
		speed = scene.getDouble("curForwardSpeed")
		minSpeed = scene.getDouble("minSpeed")

		# sets turn to 0 after turn key is released
		if c == "d" or c == "a":
			scene.setDoubleAttribute("curTurnAngle", 0)
			turn = 0
			bml.execBML('*', '<blend name="mocapLocomotion" mode="update" x="' + str(speed) + '" y = "' + str(turn) + '"/>')

		return True

# create an instance of the interface
controller = Controller()

# get the interface manager
manager = GUIInterface.getInterfaceManager()

# add the interface to the interface manager
manager.addInterfaceListener(controller)

#manager.removeInterfaceListener(controller)

# speed parameters
scene.createDoubleAttribute("maxSpeed", 4.0, True, "", 1, False, False, False, "Maximum speed of character")
scene.createDoubleAttribute("minSpeed", 0.0, True, "", 1, False, False, False, "Minimum speed of character")
scene.createDoubleAttribute("curForwardSpeed", 0.0, True, "", 2, False, False, False, "Speed of character")
scene.createDoubleAttribute("forwardRate", 0.1, True, "", 3, False, False, False, "Rate of increasing speed for character")

# turn parameters
scene.createDoubleAttribute("maxTurnAngle", 360, True, "", 1, False, False, False, "Maximum turn angle")
scene.createDoubleAttribute("minTurnAngle", 0, True, "", 1, False, False, False, "Minimum turn angle")
scene.createDoubleAttribute("curTurnAngle", 0.0, True, "", 1, False, False, False, "Current angle of character")
scene.createDoubleAttribute("turnRate", 180, True, "", 1, False, False, False, "Rate of turning of character")
