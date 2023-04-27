from map import Map
import time
import os
import json
from helicopter import helicopter as helico
from pynput import keyboard
from clouds import Clouds

TICK_SLEEP = 0.05
TREE_UPDATE = 50
CLOUDS_UPDATE = 100
FIRE_UPDATE = 75
MAP_W, MAP_H = 20, 10

fields = Map(MAP_W, MAP_H)
clouds = Clouds(MAP_W, MAP_H)
helico = helico(MAP_W, MAP_H)
tick = 1

def game_over():
    global helico
    os.system("cls")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("GAME OVER, YOUR SCORE IS", helico.score)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXX")
    exit(0)

MOVES  = {'w': (-1,0), 'd': (0, 1), 's': (1, 0), 'a': (0, -1)}
def process_key(key):
    global helico, tick, clouds, fields
    c = key.char.lower()
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        helico.move(dx, dy)
    elif (c == "f"):
        data = {"licopter": helico.export_data(), 
                "clouds": clouds.export_data(), 
                "field": fields.export_data(),
                "tick": tick}
        with open("level.json", "w") as lvl:
            json.dump(data, lvl)
    elif c == "g":
        with open("level.json", "r") as lvl:
            data = json.load(lvl)
            helico.import_data(data["helicopter"])
            tick = data["tick"] or 1
            fields.import_data(data["fields"])
            clouds.import_data(data["clouds"])


listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()

while True:
    os.system("cls") #cls
    print("TICK", tick)
    helico.print_stats()
    fields.print_map(helico, clouds)
    fields.process_helicopter(helico, clouds)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        fields.generate_tree()
    if(tick % FIRE_UPDATE == 0):
       fields.update_fires()
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update()
           
    
    
