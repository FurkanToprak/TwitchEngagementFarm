# TwitchEngagementFarm

## Outputs
Bots with invalid tokens are placed in `/output/invalidBots.csv`.

## Configuration
All parameter settings are found in `/src/config.py`.

### numBots
Sets the number of bots used by the program.

### botGeneratorPath
The `BotBank` class creates users by utilizing an executable that can create a list of OAuth tokens. 
This is the path of an executable program that can generate new accounts. Ensure that this program exists on a directory path `botGeneratorPath`, is installed (use `npm install`, etc), and uses `node index.js` to start.

* In order to not violate the Apache 2.0 license of the software that we have used to generate new accounts, we will not mention which *node.js program* to possibly use. This program is not a derivative work. 

### botListPath
A file that contains a list of bots. Each line should have the space-separated format: `username password email userid token`

## Avoiding Bans
* This is an educational tool and is not intended to break any laws.
* Someone who would maliciously use this tool (don't!) would have to use a VPN and/or multiple proxies to avoid being traced and banned.

## Contact the Developer
Furkan Toprak
furkancemaltoprak@gmail.com
