# TwitchEngagementFarm

## Configuration
All parameter settings are found in `/src/config.py`.

### numBots
Sets the number of bots used by the program.

### botGeneratorPath
The `BotBank` class creates users by utilizing an executable that can create a list of OAuth tokens. 
This is the path of an executable program that can generate new accounts. Ensure that this program exists on a directory path `botGeneratorPath`, is installed (use `npm install`, etc), and uses `node index.js` to start.

* In order to not violate the Apache 2.0 license of the software that we have used to generate new accounts, we will not mention which *node.js program* to possibly use. This program is not a derivative work. 

## Contact the Developer
Furkan Toprak
furkancemaltoprak@gmail.com
