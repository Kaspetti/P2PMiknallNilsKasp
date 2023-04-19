# Peer-to-Peer filesharing
INF142 Oblig2

## Contents
- A script for the tracker
- A sciprt for the induvidual peers
- Some Files, for testing purposes

## How to use
1. Start the tracker
2. Start one or multiple peers
  - you will be prompted for a port, choose an unique one if on localhost.
  - The files have to be placed within the "Files" folder, or the peer will not find them.
3. In the terminal, the peer will be given a few instructions on how to use the program

## Notes
* If a peer disconnects whilst sending a file, an error might occur, as there are no
hotswitching between who you are receiving data from.
* The user disconnect without calling the unregister command, the user will not be properly removed
from the tracker.
