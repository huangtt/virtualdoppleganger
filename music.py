# Music file for game: named background.wav. Loops when finished.

scene.createDoubleAttribute("songLength", 348, True, "", 1, False, False, False, "Length of background music")

maxTime = scene.getDouble("maxTime")

loop = 1
newSongLength = scene.getDouble("songLength")

class Music (SBScript):
	# plays music at start
	def start(self):
		scene.command("PlaySound " + scene.getLastScriptDirectory() + "/sounds/background.wav ChrBrad")

	def update(self, time):
		global loop, newSongLength

		# loops if song is over
		if time > newSongLength:
			scene.command("PlaySound " + scene.getLastScriptDirectory() + "/sounds/background.wav ChrBrad")
			loop += 1

			songLength = scene.getDouble("songLength")
			newSongLength = songLength * loop

music = Music()
scene.addScript("music", music)

#scene.removeScript("music")