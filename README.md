This project was created for USC Institute for Creative Technologies in about a month in collaboration with Ari Shapiro, Evan Szablowski, Jonathan Gratch, and Gale Lucas.

After 3D data is imported (using Microsoft Kinect or Character Animation/Simulation Team's iPad scanning application), the player's virtual doppelganger is imported into SmartBody character animation platform. Each player records "pain sounds" (i.e. "Ow") to be used during the game.  

While being serenaded to some beautiful and funky gameplay music, the player can go through a short tutorial (briefing him/her on how to control direction of movement and alternate speeds) or begin playing immediately. The player navigates through a winding maze while avoiding hitting walls or stepping on mines in a given time limit. Data is written to a csv file at the end (with time, # of mine hits, # of wall hits). Additionally, each player's path along the maze is tracked and recorded on a separate csv file. 

See gameplay here: https://www.youtube.com/watch?v=wc7zz0FLqyk
(see 3:43 for awesome rockout ending)

See my most significant code in files:
trackingcamera.py and
tutorialcamera.py

Because SmartBody is not naturally a game platform, the gameplay (following over-the-shoulder) camera was created from scratch. Other features such as the "bounce-back"/recoil are also coded in these files. Above files also include writing to the data files described above.
