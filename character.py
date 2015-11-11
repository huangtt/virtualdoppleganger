scene.loadAssetsFromPath(scene.getLastScriptDirectory() + "/autorigexport")

scene.addAssetPath("script", "sbm-common/scripts")
scene.addAssetPath("script", "behaviorsets")
scene.addAssetPath('script', 'scripts')
scene.addAssetPath("sound", scene.getLastScriptDirectory() + "/sounds")

# Set up joint map for Brad
print 'Setting up joint map and configuring character skeleton'
scene.run('mixamo-map2.py')
mixamoMap = scene.getJointMapManager().getJointMap('mixamorig')
skeleton = scene.getSkeleton('model_mesh_skin.dae')
mixamoMap.applySkeleton(skeleton)

print 'Adding character into scene'
# Set up character
character = scene.createCharacter('ChrBrad', '')
characterSkeleton = scene.createSkeleton('model_mesh_skin.dae')
character.setSkeleton(characterSkeleton)
# Set position
bradPos = SrVec(.217, 1, 45.87)
character.setPosition(bradPos)
# Set facing direction
bradFacing = SrVec(176, 0, 0)
character.setHPR(bradFacing)
# Set standard controller
character.createStandardControllers()
# Deformable mesh
character.setDoubleAttribute('deformableMeshScale', 1)
character.setStringAttribute('deformableMesh', 'model_mesh_skin.dae')

# setup locomotion
scene.run('BehaviorSetMaleMocapLocomotion.py')
setupBehaviorSet()
retargetBehaviorSet('ChrBrad')

scene.run('BehaviorSetGestures.py')
setupBehaviorSet()
retargetBehaviorSet('ChrBrad')



character.setStringAttribute("displayType", "GPUmesh")

character.setVoice("audiofile")
character.setVoiceCode(".")

# Set up steering
print 'Setting up steering'
steerManager = scene.getSteerManager()
steerManager.setEnable(False)
character.setBoolAttribute('steering.pathFollowingMode', False) # disable path following mode so that obstacles will be respected
steerManager.setEnable(True)

# Start the simulation
print 'Starting the simulation'
sim.start()

bml.execBML('ChrBrad', '<body posture="ChrMarine@Idle01"/>')
bml.execBML('ChrBrad', '<saccade mode="listen"/>')
bml.execBML('*', '<blend name= "mocapLocomotion" x="0"/>')
#Moving at 0 here


#bml.execBML('ChrBrad', '<gaze sbm:handle="brad" target="camera"/>')

sim.resume()
