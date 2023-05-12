# ___________                                   .__      ___.                  
# \__    ___/___ _____    _____   ____________  |__| ____\_ |__   ______  _  __
#   |    |_/ __ \\__  \  /     \  \_  __ \__  \ |  |/    \| __ \ /  _ \ \/ \/ /
#   |    |\  ___/ / __ \|  Y Y  \  |  | \// __ \|  |   |  \ \_\ (  <_> )     / 
#   |____| \___  >____  /__|_|  /  |__|  (____  /__|___|  /___  /\____/ \/\_/  
#              \/     \/      \/              \/        \/    \/               
# coded by: Rafael Ivan Mota

from termcolor import colored
from pokemon import Pokemon
from player import Player
import json
import random
import sys

class NewGame:
  def __init__(self):
    self.player= Player()
    self.pokemon = Pokemon()
    self.difficulty = 1
    self.hintNumber = 3
    self.score = 0
    self.tries = 3

  # Prompt and set the difficulty for the player.  Checks that they make the correct input.
  def setDiff(self):
    level = input("""
    Please select a difficulty:
    1: Easy
    2: Normal
    3: Hard
    :: """)
    try:
      level = int(level)
    except ValueError:
      print(colored("Please try again. Type 1, 2, or 3.", "red", attrs=["bold"]))
      return self.setDiff()
    if(level>3 or level<=0):
      print(colored("Please try again. Type 1, 2, or 3.", "red", attrs=["bold"]))
      return self.setDiff()
    self.difficulty = level
    return level

  def restartGame(self):
    print(f"Score:{self.score}")
    self.player.updateAccount(self.score)
    print("Type [restart] to play again, [high score] to see the leaderboard, and [exit] to close the game.")
    while(True):
      prompt=input(":: ").lower()
      if(prompt=="restart"): # RESTART GAME
        intro()
        ng=NewGame()
        print("Hello "+ng.player.name)
        ng.pokemon.displayPokemon(ng.setDiff())
        return ng
      elif(prompt=="high score"): # DISPLAY HIGH SCORES
        highScore()
      elif(prompt=="exit"): # END GAME
        print("bye!")
        sys.exit()

def rules():
  print("""
RULES:
1) You have 3 guesses to correctly name the pokemon. The shorter number of guesses the more points.
2) You have access to a total of 3 hints for the whole game.
3) If you ever get all three guesses wrong.  The game will end and save your High Score.

INSTRUCTIONS:
When you encounter this symbol [::] type in your response and press [ENTER].
Type [manual] to read the rules and instructions again.
Type [pokemon] to display the current pokemon.
Type [hint] to use up one of your hints.
Type [score] to show your current score and number of available hints.
Type [end] to start a new game, look at HIGH SCORES, or exit.
  """)

def intro():
  print("""
Thankyou for playing [Who's That Asciimon!].
This game is a riff on 'Who's That Pokemon!', which appeared in-between episodes of the cartoon
adaptation of the widely popular video game series 'Pokemon'.  Much like the series, this game
will show you a silhouette of a random pokemon made out of ascii characters and you have to guess who it is.  
Please refer to the following rules while playing.  Have Fun!

RULES:
1) You have 3 guesses to correctly name the pokemon. The shorter number of guesses the more points.
2) You have access to a total of 3 hints for the whole game.
3) If you ever get all three guesses wrong.  The game will end and save your High Score.

INSTRUCTIONS:
When you encounter this symbol [::] type in your response and press [ENTER].
Type [guess] to make a guess at the pokemon
Type [manual] to read the rules and instructions again.
Type [pokemon] to display the current pokemon.
Type [hint] to use up one of your hints.
Type [score] to show your current score and number of available hints.
Type [end] to start a new game, look at HIGH SCORES, or exit.
  """)


#Display a running list of High Scores saved in the [playerData.json] file
def scoreValue(e):
  return e["score"] #used to sort the list of player scores
def highScore():
  with open("playerData.json", "r") as file:
    playerList = json.load(file)
  playerList.sort(reverse=True,key=scoreValue) #sort the values in reverse order
  #stylize and print the scores to the terminal
  print("----HIGH SCORES----")
  print("|  NAME : SCORE   |")
  for player in playerList: #print the name and score of each player
    #make sure that the name is max 6 letters and fills in the leftover space
    scoreName=""
    count=0
    for letter in player["name"]:
      count+=1
      if count <=6:
        scoreName+=letter
    scoreName+=" "*(6-count)
    #make sure that the score fills in the leftover space 
    #!*[COMEBACK AND FIX FOR VERY HIGH SCORES]*!
    scoreScore=str(player["score"])
    count=0
    for number in scoreScore:
      count+=1
    scoreScore+=" "*(6-count)
    print("|"+scoreName+" :   "+scoreScore+"|")
  print("-"*19)  


  
#GAME START -------------------------------------------------------------------------------------
intro() #intro text displaying rules and instructions
ng=NewGame() #create a new instance of the Game with various initial values
print("Hello "+ng.player.name)
ng.pokemon.displayPokemon(ng.setDiff())

#Loop that always comes back to the input [prompt] after all input checks are made.
#each if statement will run it's code if the player types the correct response.
while(True):
  prompt=input(":: ").lower()
  if(prompt=="manual"):
    rules()
  elif(prompt=="pokemon"):
    ng.pokemon.displayPokemon(ng.difficulty)
  elif(prompt=="hint"): #show a random hint, but decrease the number of available hints.
    if(len(ng.pokemon.hints)>0 and ng.hintNumber>0):
      randomNum = random.randint(0, len(ng.pokemon.hints)-1)
      print(ng.pokemon.hints.pop(randomNum))
      ng.hintNumber=ng.hintNumber-1
    else:
      print("Sorry, you have used up all your hints.")
  elif(prompt=="score"): #print current score and amount of hints available
    print(f"Score: {ng.score} | Hints: {ng.hintNumber}")
  elif(prompt=="end"): #run all of the initializing lines of code from the GAME START
    ng.score-=25
    print("GAME OVER! Forfeit -25pts.")
    ng = ng.restartGame()
    
  #adds a second layer of prompts for the guess so the player doesn't use up a guess by mistake.
  elif(prompt == "guess"): 
    guess= input("Type your guess:: ").lower()
    
    #generate a new pokemon if guessed correctly and add 100 points to the players current score
    if(guess == ng.pokemon.name):
      ng.score+=100
      print(f"You guessed {ng.pokemon.name} correctly! +100p")
      ng.tries=3
      ng.pokemon = Pokemon()
      ng.pokemon.displayPokemon(ng.difficulty)
      
    #Decrease the number of tries if the player guesses wrong 
    #and decrease their current score by 25 points.
    #If the player uses up all of their tries, will update their account and provide ending prompts.
    else: 
      ng.score-=25
      if(ng.tries>1): 
        ng.tries-=1
        print("Sorry incorrect guess. -25p")
      else:
        print("GAME OVER! Sorry, you have used up all your tries.")
        ng = ng.restartGame()


