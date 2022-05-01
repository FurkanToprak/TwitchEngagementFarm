# TwitchEngagementFarm

## Outputs
Bots with invalid tokens are placed in `/output/invalidBots.csv`.

## Configuration
All parameter settings are found in `/src/config.py`.

### numBots
Sets the number of bots used by the program.

### minDelay
Sets the minimum amount of time before the bot can chat again. 

### maxDelay
Sets the minimum amount of time before the bot can chat again.

### botGeneratorPath
The `BotBank` class creates users by utilizing an executable that can create a list of OAuth tokens. 
This is the path of an executable program that can generate new accounts. Ensure that this program exists on a directory path `botGeneratorPath`, is installed (use `npm install`, etc), and uses `node index.js` to start.

* In order to not violate the Apache 2.0 license of the software that we have used to generate new accounts, we will not mention which *node.js program* to possibly use. This program is not a derivative work. 

### botListPath
A file that contains a list of bots. Each line should have the space-separated format: `username password email userid token`

## Avoiding Bans
* This is an educational tool and is not intended to break any laws.
* Someone who would maliciously use this tool (don't!) would have to use a VPN and/or multiple proxies to avoid being traced and banned.

## Invalid accounts
If an account stops working, it is output into `/output/invalidBots.csv`.

## Avoiding Frequent Account Creation and the Law
The malicious percent who would exploit this code (don't!) is in an arms race with Twitch. In fact, the only way to feasibly run bot accounts (besides using hacked accounts, which is a crime in many jurisdictions of the law) is to frequently change IP addresses and use proxies. The cautious evil person would also beware to use their script only after being confident that there are TWO layers of proxies. Why?

### The way to get caught
`User -> Proxy -> Twitch.tv`
Twitch.tv can identify the IP address of the Proxy. Twitch can then open a lawsuit, which allows them to communicate with many country's internet service providers (ISPs). Once the ISP identifies the IP address connecting to the Proxy, the proxy can identify you.

### The harder way to get caught
`User -> Proxy 1 -> Proxy 2 -> Twitch.tv`
Twitch.tv can identify the IP address of the Proxy 2. Your ISP only knows that you connected to Proxy 1, and may not be able to know where Proxy 1 communicates with. It would also be wise for the malicious user to ensure that Proxy 1 and Proxy 2 are in different countries. Certain countries have no obligation to communicate with any investigative party. The script would run on Proxy 2 and the user would would communicate with the script through Proxy 1. Additionally, some have the view that VPNs cannot be trusted to not collaborate with law enforcement so mainstream VPNs would have to be investigated.

### How to potentially never raise any flags
If each bot were to use a different proxy, this would be nearly impossible to detect, except from clientIds in the request headers (which can be changed, but they do not seem to be tracking clientId repetitions). It is also unknown how to generate arbitrary valid client IDs that Twitch would consider authentic. Perhaps they never track clientIds?

## Architecture
`Bot`: Represents a bot that will be loaded from a file or created. Bots can join channels, follow/unfollow users, and chat in channels.

`Pool`: A pool of bots concurrently interact with `Channel`s. This is a simple way to group users together.
* Each pool has a master that computes common calculations for the pool in order to avoid excessive rate limits.
* Pools allow for a list of strings to be dumped into chat. The pool automatically assigns a string to each user in the pool. Edge cases are handled, so you can pass in any number of strings you'd like.

`BotBank`: The main interface that creates and loads bots from input files. BotBank and allocates pools of bots. Configuration through `config.py` is essential to make this code work. This is unavoidable, so make sure to keep your input/output directories so that they will not be overwritten. Especially the size of this BotBank is crucial, especially if you are not confident in your abilities to use proxies and consistently refresh OAuth tokens. 
* BotBank is used to generate pools.
* If a pool is not desired, BotBank is capable of dispensing single users as well.

`Channel`: Represents a channel to follow. A channel can only be created by the master of a Pool, due to the Twitch API's OAuth requirements.

## Chatting
https://dev.twitch.tv/docs/irc

### Delay Mechanism 
- Set a random timer from `minDelay` seconds to `maxDelay` seconds. 
- After each chat made by another user in the channel, if the timer is finished, your bot fires a message in the channel chat. 
- The timer resets with another random duration

## Disclaimer
This is for educational purposes ONLY. By downloading this code, you agree to not use this code for any malicious persons and to not abuse Twitch.tv or any other website using this code or its derivatives. Always follow Twitch.tv's Terms of Service and the law.

## TODO: use .env for all API keys.