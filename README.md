# Poltergust
[![Build](https://github.com/Scutlet/mk8-poltergust/actions/workflows/build.yml/badge.svg)](https://github.com/Scutlet/mk8-poltergust/actions/workflows/build.yml)

Poltergust is a Mario Kart 8 U (Staff) Ghost Data visualization, extraction, and conversion tool. Mario Kart 8 Deluxe is not actively supported.

Documentation on the Mario Kart 8 ghost files format can be found on the [MK8 CT Wiki](https://mk8.tockdom.com/wiki/Ghost_Data_(File_Format)). Alternatively, visit the [MK8Leaderboards repo](https://github.com/Dinostraw/MK8Leaderboards/wiki).

Contributions to code and/or documentation are always welcome.

## DISCLAIMER
This tool supports modification of ghost files, or otherwise aids in describing the file format to allow someone to perform such modifications themselves. **Under no circumstances should you upload any ghost file that was modified by this tool to the Nintendo servers**, nor should you pretend that a modified run was performed legitimately. Doing so will most likely result in a straight up ban. More importantly, there is no pride to take in cheating. Do **not** act like a doofus and ignore this disclaimer.

## Screenshot
![tool-preview](resources/screenshots/tool-preview.png)

## What about Mario Kart 8 Deluxe?
Deluxe uses an almost-identical format to Mario Kart 8 U. It switches up to a Little Endian format, and gets rid of the long filenames (from which Poltergust fetches its information) for player ghosts. There's also a few more snags, such as an additional ghost list file (See [MK8Leaderboards](https://github.com/Dinostraw/MK8Leaderboards/commits/master) for more details). At this point in time I have no intentions of providing support for Deluxe ghosts. However, you are welcome to contribute to provide support for them.

Images for tracks, characters, and vehicle parts from Deluxe are already present in this repository, and have even already been properly mapped (though IDs between Wii U and Deluxe do not always match up directly). Tracks images from Wave I of the Booster Course Pass are the latest ones that are present here.

# How to Run
First, grab the latest source code. To run, you'll need [Python 3.10](https://www.python.org/downloads/) (or later). Open up a terminal of choice, navigate to the place where you extracted the source code, and install the dependencies using `pip install -r requirements.txt` (possibly inside a Virtual Environment if that has your preference). You can then run the tool through `python poltergust.py`.

I will likely provide an executable which packages everything together at a later point in time.

# Features
Poltergust supports staff ghost files, player ghost files, and downloaded ghost files. It does not support MKTV replays, as their file format is significantly different.

## Previewing
The following information can be previewed:
- Player name
- Player flag
- Racecourse
- Total time
- Individual lap times
- Character used
- Vehicle combination used

The race itself cannot be previewed.

## Mii Data
Mii data from ghost files can be extracted.

## Staff Ghosts
Player ghosts and downloaded ghosts can be converted into staff ghosts.

## Downloaded Ghosts
Player ghosts and staff ghosts can be converted into downloaded ghosts for any of the sixteen available "slots". There is a limit of four downloaded ghosts per track per game save (five if no player ghost exists for it), for a total of 16 per game save. No two ghosts can occupy the same ghost slot, even if they were set on different tracks.

## Future Plans
- Additional verification:
    - Filename vs content: Some information is present in both the ghost's filename and its contents. Although in most cases it won't matter if these two don't match up (the filename takes presence mostly), there can sometimes be issues. For example, if the character does not match up, then animations can break when viewing the replay. See the note below.
- Editing: At least the player name and flag should be editable. Runs recorded on the CEMU emulator fail to add the correct flag. It also adds a bogus name (consisting of several types of question mark charaters) if using the default Mii data. Likewise, runs recorded on a real Wii U may use a Mii name that a player may not want to expose elsewhere.
- Character-specific vehicle parts: Some vehicle parts are coloured differently based on the character that drives it. This is not reflected in the current UI.

# A quick note on Mario Kart 8 Ghost Data
Mario Kart 8 Ghost Data functions differently from earlier titles. In Mario Kart Wii, ghosts mimicked controller inputs to create an identical race. This could in rare cases cause desyncs, meaning that the ghost would behave differently than how the player actually raced originally.

This was fixed in Mario Kart 8, as ghost replays are no longer based on controller inputs, but instead (or also?) store the ghost's location. For example, placing ghost data from Toad Harbour over Rainbow Road will show the ghost racing through the air, following the course layout of Toad Harbour and ignoring collisions and the like from Rainbow Road entirely.


The filename of a ghost stores information such as lap times, character played, player name, player flag, etc. The information on the summary screen (i.e., the screen that is seen before watching a ghost replay) is taken directly from here. All this information is _also_ stored inside the ghost file itself. However, this is not actually used in most cases. For example, lap times on the end screen (after racing the ghost) are taken from the file contents, whereas the character and vehicle combination are still taken from the filename.

Mii data is stored inside ghost files, although it is only really used for displaying the player's name during a ghost race and on the end screen.

Ghost files were changed a little in version 4 of the game, where GCN Baby Park was added to the game. This track features seven laps that need to be stored in a ghost file name, whereas previously there was only space for at most five laps (space for two were unused). Hence, the filename of ghost files was extended in version 4 of the game.

# CREDITS
## B_squo
B_squo provided the initial information on Mii data inside ghost files [in a Tweet](https://twitter.com/b_squo/status/1412392477080834056). This proved to be correct, as this data can be opened in [a Mii viewer](https://kazuki-4ys.github.io/web_apps/MiiInfoEditorCTR/).[CRC-16 XMODEM](https://crccalc.com/) checksum is used to ensure Mii data is not corrupted in that game.

It turned out Mario Kart 8 uses the exact same checksum. Directly editing Mii data _without updating this checksum_ causes a crash.

## lonemoonHD and Cole
lonemoonHD and Cole already independently confirmed the filename format for ghosts earlier on [in a GBATemp thread](https://gbatemp.net/threads/post-your-wiiu-cheat-codes-here.395443/page-454#post-8640417). Furthermore, they provided crucial insights in that same GBATemp thread regarding the difference between staff ghost data and player ghost data: the header.

Copying a player ghost into a staff ghost without removing the player ghost header first caused the game to crash, but completely getting rid of this header and _then_ copying file contents over works completely fine. This provided an entrypoint for custom staff ghosts.

## MK8Leaderboards (Dinostraw)
Starting May 17th 2022, Dinostraw started work on [a Leaderboards visualisation tool](https://github.com/Dinostraw/MK8Leaderboards/commits/master). It contains detailed documentation on the filename and file contents format, written independently from this tool. It provided crucial insights for downloaded ghosts as well as character variants (like Blue Yoshi), support for which was integrated into Poltergust only because of those findings.

## Spriters Resource
Character, flag, track, and vehicle part images were taken from the Spriters Resource, and originally ripped by Random Talking Bush and Ink_Larry.
