from ursina import *


from ursina.prefabs.first_person_controller import FirstPersonController
import time
import random

app = Ursina()

Sky()
player = FirstPersonController()
player.speed = 10
player.jump_height = 15
player.gravity = 0.5
camera.fov = 120
camera.z = camera.z -5

coord_cube = 50
last_distance = None
distance1 = None
fall_sound_played = False
nb_max_enti = None

ground = Entity(model = 'plane', texture = 'grass', collider = 'mesh', scale = (50,1,130), position = (0,-20,0))
wall1 = Entity(model = 'cube', collider = 'mesh', scale = (1,100,100), position = (20,0,0), visible = False)
wall2 = Entity(model = 'cube', collider = 'mesh', scale = (1,100,100), position = (-20,0,0),visible = False)
wall3 = Entity(model = 'cube', collider = 'mesh', scale = (100,100,1), position = (-3,0,0),visible = False)
limit = Entity(model = 'cube',color = color.red ,collider = 'mesh', scale = (100,1,1), position = (0,0,15))
old_limit = Entity(model = 'cube',color = color.blue ,collider = 'mesh', scale = (100,1,1), position = (0,0,-35))

image = Entity(model = 'quad', texture = 'game_over.png',scale = (4,4),position =(100,100,100))
coin = Entity(model = 'coin.stl',texture = 'white_cube',position = (20,-40,25))
player_skin = Entity(model = 'cat2.stl', color = color.black,double_sided = True,rotation = (270,0,0),scale = 2,)
distance_text = Text(text='Distance: 0', position=(0.5, 0.4), scale=2, color=color.white)
jump_sound = Audio('maouw_jump.mp3', autoplay=False)
fall_sound = Audio('maouw_fall.mp3',autoplay=False)
jump_secret = Audio('miaou_nours.mp3',autoplay=False)

liste_entite = []

def couleur_aleatoire():
    nb_al = random.randint(1,3)
    if nb_al == 1:
        return color.blue
    elif nb_al == 2:
        return color.white
    elif nb_al == 3:
        return color.red

def enti_random(coord_limit,nb_max_enti):
    nb_enti = random.randint(5,nb_max_enti)
    print("il y a " , nb_enti ," entités sur la nouvelle surface")
    i = 0
    for i in range (nb_enti):
        dim_enti_rand(coord_limit)
    #print("la liste contient ", len(liste_entite))

def dim_enti_rand(coord_limit):
    coord_rand_z = random.randint(10,50)
    coord_scale = (random.randint(5,20),5,random.randint(5,20))
    coord_rand_x = random.randint(-20,20)
    coord_rand_y = random.randint(-25, -20)
    entite = Entity(model = 'cube',collider = 'mesh' ,texture = "brick",color = couleur_aleatoire(), position = (coord_rand_x,coord_rand_y,coord_limit + coord_rand_z+10),scale = coord_scale)
    liste_entite.append(entite)
    

def update():

    global coord_cube
    global last_distance
    global fall_sound_played
    global nb_max_enti

    if player.z > limit.z:
        
        enti_random(coord_cube-10,nb_max_enti)
        limit.z += 40
        old_limit.z += 40
        coord_cube += 50

        entites_a_supprimer = []
        for i in liste_entite:
            if old_limit.z-20 >= i.z:
                entites_a_supprimer.append(i)
        
        for i in entites_a_supprimer:
            destroy(i)
            liste_entite.remove(i)


    if (player.position.y < -60):
        if not fall_sound_played:
            image.visible = True
            player.enabled = False
            camera.position = (100,100,95)
            camera.rotation = (0,0,0)
            fall_sound.play()
            fall_sound_played = True

    if held_keys['shift']:
        player.speed = 20
    else :
        player.speed = 10
    
    if held_keys['space']:
        if not jump_sound.playing and not jump_secret.playing:
            randi = random.randint(1, 20)
            if randi == 1:
                jump_secret.play()
            else:
                jump_sound.play()

    distance1 = round(player.position.z/5,1)

    if last_distance != distance1:
       # print("le joueur a parcouru ", round(distance1,1) , " mètres")
        distance_text.text = f'Distance: {distance1}m'
        last_distance = distance1

    player_skin.position = (player.x,player.y,player.z)

    if distance1 < 50:
        nb_max_enti = 15
    elif distance1 < 100:
        nb_max_enti = 10
    elif distance1 < 200:
        nb_max_enti = 8
    else:
        nb_max_enti = 6

app.run()