# FalMenu
A simple customizable mod menu for every SINGLEPLAYER game.

## Instructions
1) Open CheatEngine
2) Find an address for a target variable
3) Right click on address -> "Find out what accesses this address"
4) Get offset (it's the value after the +, e.g: ebx + 00004B0 <- this)
5) Now go back to the address, right click -> "Generate pointermap"
6) Back to the address, right click -> "Pointer scan for this address" (Check "Use saved pointermap" and use the one saved in the last step)
7) Check the "Pointers must end with specific offsets" and write offset found on step 4
8) Click ok and save the scan
9) Close the target application
10) Repeat steps 2 to 7 (IMPORTANT) but also check "Compare results with other saved pointermap(s)"
11) Select one or more of the past pointermaps and the address that was found in the past session
12) Click ok and save the scan (the scan should return less and less results with each repetition)
13) One or more pointers should be found at this point, repeat this for each variable you are interested in
14) You will also need the base address, in CheatEngine, right click on a target variable -> "Browse this memory region" -> Tools -> Dissect PE headers
15) Find the target application.exe, and find the "Prefered imagebase"
16) Find the offset added in the pointer (THIS IS A DIFFERENT OFFSET FROM THE OFFSETS FOUND EARLIER)

You are now ready to run the FalMenu, using this method will work with ANY game, please dont cheat online, only losers cheat online.
The program will ask for all of the information you gathered with Cheat Engine, you can manually insert them, or load a .json file with theese variables:
- "process_name" -> The name of the process 
- "base_address" -> The base address
- "base_offset"  -> The base address offset
- "offsets"      -> The offset(s) found for the target variable (IS AN ARRAY)