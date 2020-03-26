# chess_engine

A program to play chess against the computer.
To run the program, after downloading the repository, open the terminal (UNIX systems) or the command prompt (Windows) and 
run either

cd ~/path_to_repo/chess (UNIX)

cd Z:\path_to_repo\chess (Windows)

where path_to_repo is the path from your home directory to wherever you downloaded this repository.

Then simply run 

python chess.py (UNIX)

C:\python37\python.exe chess.py (Windows)

A terminal interface will open, asking you for the coordinates of the piece you want to move. You will always have the 
white pieces, so you start the game. Insert the coordinates of the piece you want to move in the form (a,b), where 
a and b are integers between 0 and 7 representing the line number and the column number respectively.

Then insert the coordinates of the destination square where you want the piece to be moved. Once you made your move,
the computer will make its move and the new position will be printed on the screen.

You can press q at any time to leave the game without saving. You can instead press s to save and quit. The position will
be saved in txt format in the saved_games folder.

In the settings.txt file you can find an option to load previously saved games. Simply change the second line to load = y
and when you run the program you will be asked which game you want to load. Your saved games will be numbered 1,2,3,...
in the order in which they were saved; specify a number to load the corresponding game, and start playing from where you 
left off.

Finally in the first line of settings.txt, you can set the computer strength by changing the number. For now only depth = 1
and depth = 2 are available, with 1 being easy and 2 slightly harder. I'm planning to add harder opponents soon (level 2 is
very easy to defeat)

Future updates (and essential missing features to be coded):

1)Need to include castling

2)En-passant capture with the pawn

3)Improving user interaction with the program, and visualization of the chess board

3b)Eventually building a proper GUI

4)Increasing the strength of the computer

5)Including analysis of games

Goal of the project:
This is just a way to pass time while remaining home during the COVID-19 outbreak. To challenge myself I have made a point
out of not reading anything about chess algorithms or coding a chess app in general from the internet. I wanted to try to
build the chess engine (however terrible) independently. 
Therefore the final goal of the project is quite modest: I will consider it complete when the program manages to beat me,
a beginner chess player






