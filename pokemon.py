from ascii_magic import AsciiArt
import requests
import json
import random


class Pokemon:
  def __init__(self):
    self.name = ""
    self.type = ""
    self.ability = ""
    self.hints = []
    self.generatePokemon()


    
  #Generate a pokemon based on the current instance of the game and return a dict [hints] with hints based
  #off of that individual pokemon
  def generatePokemon(self):
    #generate a random pokemonID and save the api data associated with it to a file [data.json]
    random_poke_ID = random.randint(1,151)
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{random_poke_ID}")
    data = response.json()
    with open("data.json", "w") as f:
      json.dump(data, f)
   
    #Grab the sprite from the api data and save it to a file named [pokemon.png]
    image_url = data["sprites"]["front_default"]
    image_response = requests.get(image_url)
    with open('pokemon.png', 'wb') as f:
      f.write(image_response.content)
    
    #iterate through the [type] data and store all of it's types
    for types in data["types"]:
      self.type = self.type+types["type"]["name"]+" "
  
    #iterate through the [ability] data and store all of it's abilities
    for abilities in data["abilities"]:
      self.ability = self.ability+abilities["ability"]["name"]+" "
      
    #iterate through the name and store and create a hint using the first and last letters
    self.name = data["name"]
    nameHint=""
    for i in range(0, len(self.name)):
      if i==0:
        nameHint += self.name[i]
      elif i==(len(self.name)-1):
        nameHint += self.name[i]
      else:
        nameHint += "_"
  
    #Save [name] [type] and [ability] to the [hints] dict
    self.hints.append("name: "+nameHint)
    self.hints.append("type: "+self.type)
    self.hints.append("ability: "+self.ability)
  
  
  
  #Using the set difficulty, reads the pokemon image file and outputs an ascii interpretation.
  #The number of columns used to generate the image will change depending on the difficulty.
  def displayPokemon(self, difficulty):
    my_art = AsciiArt.from_image('pokemon.png')
    columns= 30
    if difficulty == 3:
      columns = 30
    elif difficulty == 2:
      columns = 50
    elif difficulty == 1:
      columns = 75
    elif difficulty == 0:
      columns = 100
    my_art.to_terminal(columns)