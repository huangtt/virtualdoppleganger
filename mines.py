scene.loadAssetsFromPath(scene.getLastScriptDirectory() + "/objects/mine.dae")

mines = scene.getPawnNames()
 
for i in range(len(mines)):
	if "mine" in mines[i]:
		scene.getPawn(mines[i]).setStringAttribute("mesh", "mine.dae")
