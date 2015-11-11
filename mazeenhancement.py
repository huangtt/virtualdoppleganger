# covert collision shape to a mesh 
# for better lighting effects
names = scene.getPawnNames()
for n in range(0, len(names)):
	if names[n] != "Finish":
		p = scene.getPawn(names[n])
		p.createMeshFromCollisionSurface("Maze" + names[n], SrVec(1.0, 1.0, 0.0))
		p.setStringAttribute("mesh", "Maze" + names[n])
		p.setBoolAttribute("showCollisionShape", False)