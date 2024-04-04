
import pygame 
import random
import math 
from pygame import mixer
#inicalizar pygame 
pygame.init()


#crear la pantall
pantalla = pygame.display.set_mode((800,600))

#Título e ícono

pygame.display.set_caption('Invasión Espacial')
icono=pygame.image.load("ronaldo.png")
pygame.display.set_icon(icono)

#musica de fonfo
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.4)
mixer.music.play(-1)

#jugador
img_jugador = pygame.image.load('astronave.png')
jugador_x = 368
jugador_y = 536
jugador_x_cambio = 0
#jugador_y_cambio = 0



#enemigo
img_ovni = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 20


#enemigo
for e in range(cantidad_enemigos):
  img_ovni.append(pygame.image.load('ovni.png'))
  enemigo_x.append(random.randint(0,736))
  enemigo_y.append(random.randint(50,200))
  enemigo_x_cambio.append(3)
  enemigo_y_cambio.append(50)

#Bala
balas = []
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio =0
bala_y_cambio = 3
bala_visible= False

#puntaje

puntaje= 0
fuente = pygame.font.Font ('Fastest.ttf', 32)
texto_x=10
texto_y=10

#texto final del jogo
fuente_final = pygame.font.Font ('Fastest.ttf', 40)

def texto_final():
  mi_fuente_final= fuente_final.render('JUEGO TERMINADO', True, (255,255,255))
  pantalla.blit(mi_fuente_final, (60,200))


#puntaje 
def mostrar_puntaje(x,y):
  texto = fuente.render(f'Puntaje : {puntaje}', True, (255,255,255))
  pantalla.blit(texto, (x,y))
#fondo 
img_fondo = pygame.image.load("klipartz.com (1).png")

#funcion crear jugador 
def jugador(x,y):
  pantalla.blit(img_jugador,(x,y))

def enemigo(x,y,ene): 
  pantalla.blit(img_ovni[ene],(x,y))

def disparar_bala(x,y):
  global bala_visible
  bala_visible = True
  pantalla.blit(img_bala,(x + 16, y + 10 ))


def hay_colision(x_1,y_1,x_2,y_2):
  distancia= math.sqrt(math.pow(x_2-x_1,2) + math.pow(y_2-y_1,2))
  if distancia < 27:
    return True 
  else:
    return False

#Loop del juego
se_ejecuta= True
while se_ejecuta:
  pantalla.blit(img_fondo,(0,0)) #LLenamos el color de la patnalla de color morado

#iterar elementos 
  for evento in pygame.event.get():
  # evento cerrar 
    if evento.type == pygame.QUIT:
      se_ejecuta = False
    #presioanr flechas
    if evento.type == pygame.KEYDOWN:
      if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
        jugador_x_cambio= -1.5
      if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
        jugador_x_cambio = 1.5 
      #if evento.key == pygame.K_UP or  evento.key == pygame.K_w:
        #jugador_y_cambio = -1
      #if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
        #jugador_y_cambio = 1
      if evento.key == pygame.K_UP or evento.key == pygame.K_SPACE:
        sonido_bala = mixer.Sound("disparo.mp3")
        sonido_bala.play()
        nueva_bala = {
        "x": jugador_x,
        "y": jugador_y,
        "velocidad": -2
         }
        balas.append(nueva_bala)

  
    if evento.type == pygame.KEYUP:
          jugador_x_cambio=0 
          
          #jugador_y_cambio=0
  
 #modificar ubicacion de jugador
  jugador_x+=jugador_x_cambio
  #jugador_y+= jugador_y_cambio


  #matner dentro de los bordes
  if jugador_x <=0:
    jugador_x = 0
  elif jugador_x >=736:
    jugador_x = 736

  #if jugador_y <=0:
    #jugador_y = 0
  #elif jugador_y >=536:
    #jugador_y = 536
  
  #modificar ubiacion del enemigo

  for e in range(cantidad_enemigos):
    #fin del jogo
    if enemigo_y[e] > 500 :
      for k in range(cantidad_enemigos):
        enemigo_y[k]= 1000
      balas.clear()
      texto_final()
      break

    enemigo_x[e] += enemigo_x_cambio[e]
    if enemigo_x[e] >=736:
        enemigo_x_cambio[e]= -3
        enemigo_y[e]+=enemigo_y_cambio[e]
    elif enemigo_x[e] <=0:
        enemigo_x_cambio[e] = 3
        enemigo_y[e]+=enemigo_y_cambio[e]

    #colision
    for bala in balas:
      colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
      if colision_bala_enemigo:
        sonido_colision = mixer.Sound("Golpe.mp3")
        sonido_colision.play()
        balas.remove(bala)
        puntaje += 1
        enemigo_x[e] = random.randint(0, 736)
        enemigo_y[e] = random.randint(20, 200)
        break
 
    enemigo(enemigo_x[e], enemigo_y[e], e)


    #moviemiento bala
  for bala in balas:
    bala["y"] += bala["velocidad"]
    pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
    if bala["y"] < 0:
        balas.remove(bala)
      
  #mantere dentro de bordes
    
  jugador(jugador_x,jugador_y)

  mostrar_puntaje(texto_x,texto_y)
 
  pygame.display.update()
