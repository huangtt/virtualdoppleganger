# Keeps track of type of collision (wall, tutorial wall, mine) and plays pain sound at collision. At collision with finish pawn,
# triggers finish events

# sound parameters
scene.createDoubleAttribute("lastSoundTime", 0.0, True, "virtualdoppleganger", 10, False, False, False, "Last time a sound event was played")
scene.createVec3Attribute("lastValidPosition", 0.0, 0.0, 0.0, True, "virtualdoppleganger", 20, False, False, False, "Last collision free position of the character")
scene.createDoubleAttribute("lastCollisionTime", -1.0, True, "virtualdoppleganger", 30, False, False, False, "Time of last collision event")
scene.createBoolAttribute("hasCollision", False, True, "virtualdoppleganger", 40, False, False, False, "Collision during this event.")

# counter parameters
scene.createDoubleAttribute("wallCollisionCounter", 0, True, "", 1, False, False, False, "Number of times collided with wall")
scene.createDoubleAttribute("mineCollisionCounter", 0, True, "", 1, False, False, False, "Number of times collided with mine")
scene.createDoubleAttribute("tutorialWallCounter", 0, True, "", 1, False, False, False, "Number of times collided with tutorial wall")
scene.createDoubleAttribute("hitCounter", 0, True, "", 1, False, False, False, "Total number of hits")

# collision position parameters
scene.createDoubleAttribute("scalar", 0.4, True, "", 1, False, False, False, "Scalar for distance traveled after collision")
scene.createDoubleAttribute("positionWindowFrame", 10, True, "", 1, False, False, False, "Size of position window for collision")

# finish parameters
scene.createBoolAttribute("finish", False, True, "", 1, False, False, False, "Has finished")
scene.createStringAttribute("finishTime", "", True, "", 1, False, False, False, "Finish time displayed on HUD")

scene.setBoolAttribute("internalAudio", True)

characterPositionList = []

class CheckCollisionScript (SBScript):
	def beforeUpdate(self, time):
		scene.setBoolAttribute("hasCollision", False)
		positionWindowFrame = scene.getDouble("positionWindowFrame")

		# keep track of past position
		pos = scene.getCharacter("ChrBrad").getPosition()
		characterPositionList.append(pos)

		# update the window
		while len(characterPositionList) > positionWindowFrame:
			#remove from list
			characterPositionList.pop(0)

	def afterUpdate(self, time):
		wasInCollision = scene.getAttribute("hasCollision").getValue()

		# in collision
		if wasInCollision:
			character = scene.getCharacter("ChrBrad")
			lastValidPosition = scene.getAttribute("lastValidPosition").getValue()
			scalar = scene.getDouble("scalar")

			# set speed to 0
			scene.setDoubleAttribute("curForwardSpeed", 0.0)
			bml.execBML('*', '<blend name="mocapLocomotion" mode="update" x="0"/>')

			# position at beginning of frame
			previousPos = characterPositionList[0]

			# position when hit
			hitPos = scene.getCharacter("ChrBrad").getPosition()

			# calculate vector and magnitude
			hitVec = SrVec(previousPos.getData(0) - hitPos.getData(0), previousPos.getData(1) - hitPos.getData(1), previousPos.getData(2) - hitPos.getData(2))
			magnitude = hitVec.len()
			moveVec = SrVec(hitVec.getData(0) * scalar / magnitude, hitVec.getData(1) * scalar/ magnitude, hitVec.getData(2) * scalar/ magnitude)

			# set new position after collision
			character.setPosition(SrVec(hitPos.getData(0) + moveVec.getData(0), hitPos.getData(1) + moveVec.getData(1), hitPos.getData(2) + moveVec.getData(2)))
		
		# not in collision
		else:
			position = scene.getCharacter("ChrBrad").getPosition()
			scene.setVec3Attribute("lastValidPosition", position.getData(0), position.getData(1), position.getData(2))
			
checkCollisionScript = CheckCollisionScript()
scene.addScript("checkCollision", checkCollisionScript)

class CollisionEvent(SBEventHandler):
	global lastSoundTime

	def executeAction(self, event):
		str = event.getParameters()
		curTime = scene.getSimulationManager().getTime()
		lastCollisionTime = scene.getAttribute("lastCollisionTime").getValue()
		wallCollisionCounter = scene.getDouble("wallCollisionCounter")
		mineCollisionCounter = scene.getDouble("mineCollisionCounter")
		tutorialWallCounter = scene.getDouble("tutorialWallCounter")

		if curTime == lastCollisionTime:
			return

		tokens = str.split("/")

		if len(tokens) >= 2:
			# character in collision
			if tokens[1].startswith("ChrBrad"):
				scene.setDoubleAttribute("lastCollisionTime", curTime)
				lastSoundTime = scene.getAttribute("lastSoundTime").getValue()

				# finish 
				if tokens[0].startswith("Finish"):
					scene.setBoolAttribute("hasCollision", False)
					scene.setBoolAttribute("finish", True)
					
					# set the finish time
					finishTime = scene.getString("finishTime")
					finishTime = scene.setStringAttribute("finishTime", scene.getString("timeText"))

					# delete the finish pawn
					finishPawn = scene.getPawn("Finish")
					finishPawn.setPosition(SrVec(0,1000,0))

					# stop moving
					speed = 0
					scene.setDoubleAttribute("curForwardSpeed", 0)
					bml.execBML('*', '<blend name="mocapLocomotion" mode="update" x="0"/>')

					# play finish sounds
					scene.command("PlaySound " + scene.getLastScriptDirectory() + "/sounds/finish.wav ChrBrad")
					scene.command("PlaySound " + scene.getLastScriptDirectory() + "/sounds/guitar.wav ChrBrad")

					# rock out on imaginary guitar at finish
					bml.execBML('*', '<animation name="ChrBrad@Idle01_Guitar01"/>')

				# check if finished
				finish = scene.getBool("finish")

				# not finished
				if not finish:
					# play random pain sound for collision
					if curTime - lastSoundTime > 1.0:
						randSound = random.randint(1,4)
						scene.setDoubleAttribute("lastSoundTime", curTime)
						scene.command("PlaySound " + scene.getLastScriptDirectory() + "/sounds/ow%d.wav ChrBrad" % randSound) 

					# wall hits
					if tokens[0].startswith("obj"):
						scene.setBoolAttribute("hasCollision", True)
						if curTime - lastSoundTime > 1.0:
							wallCollisionCounter += 1
							scene.setDoubleAttribute("wallCollisionCounter", wallCollisionCounter)

					# tutorial wall hits
					elif tokens[0].startswith("Wall"):
						scene.setBoolAttribute("hasCollision", True)
						if curTime - lastSoundTime > 1.0:
							tutorialWallCounter += 1
							scene.setDoubleAttribute("tutorialWallCounter", tutorialWallCounter)

					# mine hits and removing  mine
					elif tokens[0].startswith("mine"):
						scene.setBoolAttribute("hasCollision", True)
						# add one to mine counter
						mineCollisionCounter += 1
						scene.setDoubleAttribute("mineCollisionCounter", mineCollisionCounter)
						# get mine
						mineTokens = str.split("_")
						hitMine = scene.getPawn(mineTokens[0])
						# remove mine
						hitMine.setPosition(SrVec(0,1000,0))

		# set total hit counter
		scene.setDoubleAttribute("hitCounter", wallCollisionCounter + mineCollisionCounter)

collisionHandler = CollisionEvent()
eventManager = scene.getEventManager()
eventManager.addEventHandler("collision", collisionHandler)

scene.getCollisionManager().setEnable(True)


