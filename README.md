# Mancala
Python project TYPE:A ID:17

# Game Information
Game description:
  Mancala is a generic name for a family of two-player turn-based strategy board games played with small stones, beans, or seeds and rows of holes or pits in the earth, a board or other playing surface. The objective is usually to capture all or some set of the opponent's pieces.

Contents:
 1 Mancala board
 48 pieces (also called “rocks”)
Set Up:
 The Mancala board is made up of two rows of six pockets (also called “holes,” or “pits”) each.
 Four pieces are placed in each of the 12 pockets. The color of the pieces is irrelevant.
 Each player has a “store” (also called a “Mancala”) to his/her right side of the Mancala board.

Object:
 The object of the game is to collect the most pieces by the end of the game.

Game Play:
1. The game begins with one player picking up all of the pieces in any one of the pockets on his/her side.
2. Moving counter-clockwise, the player deposits one of the stones in each pocket until the stones run out.
3. If you run into your own Mancala (store), deposit one piece in it. If you run into your opponent's Mancala, skip it and
 continue moving to the next pocket.
4. If the last piece you drop is in your own Mancala, you take another turn.
5. If the last piece you drop is in an empty pocket on your side, you capture that piece and any pieces in the pocket directly
opposite
6. Always place all captured pieces in your Mancala (store).
7. The game ends when all six pockets on one side of the Mancala board are empty.
8. The player who still has pieces on his/her side of the board when the game ends captures all of those pieces.
9. Count all the pieces in each Mancala. The winner is the player with the most pieces.

# Application flow
  The game starts the menu scene from which you can choose from 4 options.

  - The first option is play which opens the scene of choosing the opponent, in which you can choose if you want to play with another player or with the computer, after choosing the opponent it is necessary to enter the players' names even for AI, after completing this step the scene opens of the game and it starts here the player can choose if he plays another round or returns to the stage where he chooses his opponent again.
  - The second menu option shows the rules of the game
  - The third menu option displays a ranking of the best FIRST_PLAYERS_NB players, FIRST_PLAYERS_NB is set in the configuration file.
  - The fourth menu option closes the game.
  
  # Classes
    Controllers:
      - SceneManager
      Description:
        This class creates the game scenes and manage the transfer between them
        
      - GameController
      Description:
        This class deals with the logic of the game: make a move depending on the type of players,
       decide who the winner is and communicate with the "GameBoard" class to draw the changes.
       It also remembers the score of each player for a certain game and the number of games ended in a draw. 
      
      - RankingManager
      Description:
        This class deals with creating the ranking and send it to Ranking class which draw it
      
    Views(components directory):
      - Scene
      Description:
        This class deals with scenes drawing and add components  
        
      - GameBoard
      Description:
        This class deals with drawing visual components of the game board
      
      - Ranking
      Description:
        This class deals with drawing the ranking
      
      - Button
      Decription:
        This class deals with buttons drawing and functionality
        
      - TextBox
      Desciption:
        This class deals with text box drawing and functionality
        
      - Label
        This class deals with labels drawing

  # Resources 
    Game board img: https://www.google.com/url?sa=i&url=https%3A%2F%2Fapkpure.com%2Fmancala%2Fcom.appon.mancala&psig=AOvVaw0WjUYicMHuUsle36iR8cwT&ust=1610012022360000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCNi-xa2Ah-4CFQAAAAAdAAAAABBA
    Background img: https://i.pinimg.com/736x/b6/83/0d/b6830dab296638ac8600b15cf90ea2b3.jpg
    Pygame doc: https://www.pygame.org/docs/
    Creating button with pygame tutorial: https://www.youtube.com/watch?v=4_9twnEduFA 
