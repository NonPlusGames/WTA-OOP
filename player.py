import json
import os

class Player:
  def __init__(self):
    self.player = self.handleAccount()
    self.name = self.player["name"]
    self.__password = self.player["password"]
    self.highScore = self.player["score"]

  #Using the current game instance and a task input, will handle account creation and updates.
  #A list of player data is saved to the [playerData.json] file or create one if non exists.
  def handleAccount(self):
    if os.path.exists("playerData.json"): # Check if [playerData] exists
      with open("playerData.json", "r") as file: #read file and save contents to playerList
        playerList = json.load(file)
      print("Please type in your name and password to save your score. If you dont have one a new one will be created.")
      #Return a dict with all of the player's saved info or create a new player.
      while (True): 
        name=input("name :: ")
        password=input("password :: ")
        player={"name":name, "password":password, "score":0}
        for i in range(0,len(playerList)):
          if name == playerList[i]["name"]: #Looks for the player in the database
            if password == playerList[i]["password"]: #Checks they input the correct password
              return playerList[i]
            else:
              print("Incorrect password for that name. Try Again.")
              break
          elif i==len(playerList)-1: #Adds a new player to the database if the [name] does not exist
            playerList.append(player)
            with open("playerData.json", "w") as file:
              json.dump(playerList, file)
            return player
    else: 
      #Execute the same as above but create a [playerData.json] file 
      #with the first entry being the current player
      print("Please type in a name and password to save your score.")
      name=input("name :: ")
      password=input("password :: ")
      player = {"name":name, "password":password, "score":0}
      playerList = [player]
      with open("playerData.json", "w") as file:
        json.dump(playerList, file)
      return player
  
    #perform account update tasks within the [playerData.json] file
  def updateAccount(self, newScore):
    with open("playerData.json", "r") as file:
        playerList = json.load(file)
    #iterate through the database and update the players score if the current score is greater.
    for i in range(0,len(playerList)):
      if(playerList[i]["name"]==self.name):
        if(playerList[i]["score"]<newScore):
          playerList[i]["score"]=newScore
          break
        break
    with open("playerData.json", "w") as file:
        json.dump(playerList, file)