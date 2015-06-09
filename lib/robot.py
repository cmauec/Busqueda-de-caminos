from const.constants import * 
import pygame
from pygame.locals import *
import random

colorRobot = [(235,56,211),(255,109,5),(59,57,55),(36,90,240),(0,255,4),(49,18,204),(119,5,176)]
colorRobotTemp = []
''' Tipos de choque:
    1 - se van a chocar en la siguiente posicion
    2 - se chocaron
'''
giroCanastaA = {'der': 40, 'izq': -40, 'arriba': 0, 'abajo':180}
giroCanastaB = {'der': 0, 'izq': -180, 'arriba': -90, 'abajo':90}
giroCanastaC = {'der': -180, 'izq': 0, 'arriba': 90, 'abajo':-90}

class CanastaRobot(object):
    def __init__(self, nombreCanasta, posicionCanasta):
        self.nombreCanasta = nombreCanasta
        self.posicionCanasta = posicionCanasta
        self.productosCanasta = [] #producctos que se van recogiendo
        self.productosRecoger = [] #lista de todos los producctos que hay que recoger
        self.estadoCanasta = 0   # 0-vacia, 1- llena

class Robot(object):

    def __init__(self,source,nombre):
        #Punto donde sale el robot
        self.canastas = []
        self.colorRandom = random.choice(colorRobot)
        self.index_colorRandom = colorRobot.index(self.colorRandom)
        colorRobot.pop(self.index_colorRandom)
        self.source = source
        self.state = 'libre'
        self.esperando_producto = False
        self.esperando_robot = False
        self.robot_choque = None       #Es el nombre del robot al que tiene que esperar que pase para poner en accion al robot q esta esperando 
        self.tipo_choque = None      #Almacenamos el tipo de choque 
        self.nombre = nombre    
        self.path = []
        self.path_restante = []
        self.coordenadas_producto = []     #es el punto del camino no el de la pared
        self.color = self.colorRandom 
        self.init = 0
        self.pos = 30
        self.mov_pos = 0
        self.pedido_actual = None
        self.play = False
        self.posicion_actual = source
        self.flagGirar = False
        #self.canastaRecogerProducto = None #Nos da el nombre(A-B-C-D) de la canasta en q hay q poner el producto
        # rectangulo delimitador para colisones
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        self.rec_colision = pygame.Rect(nx, ny, NODE_SIZE, NODE_SIZE)
        #self.salida = None
        

    def dibujarRobot(self,screen, orientacion = None):
        x, y = self.posicion_actual
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        giroHacia = None 
        canastaRecogerProducto = None
        if orientacion:
            canastaRecogerProducto = orientacion[0]
            giroHacia = orientacion[1]

        if not canastaRecogerProducto:  
            b = pygame.sprite.Sprite() # create sprite
            b.image = pygame.image.load("robot.png").convert_alpha() # load ball image
            b.rect = b.image.get_rect() # use image extent values 
            b.rect.topleft = [nx+2, ny+2] # put the ball in the top left corner
            screen.blit(b.image, b.rect)
        elif canastaRecogerProducto == 'A':
            print 'asdasdsad'
            if giroHacia == 'der':
                b = pygame.sprite.Sprite() # create sprite
                b.image = pygame.image.load("robot.png").convert_alpha() # load ball image
                image = pygame.transform.rotate(b.image,45)
                b.rect = image.get_rect() # use image extent values 
                b.rect.topleft = [nx+2, ny+2] # put the ball in the top left corner
                screen.blit(image, b.rect)
            elif giroHacia == 'izq':
                b = pygame.sprite.Sprite() # create sprite
                b.image = pygame.image.load("robot.png").convert_alpha() # load ball image
                image = pygame.transform.rotate(b.image, giroCanastaA['izq'])
                b.rect = image.get_rect() # use image extent values 
                b.rect.topleft = [nx+2, ny+2] # put the ball in the top left corner
                screen.blit(image, b.rect)
            elif giroHacia == 'arriba':
                b = pygame.sprite.Sprite() # create sprite
                b.image = pygame.image.load("robot.png").convert_alpha() # load ball image
                image = pygame.transform.rotate(b.image, giroCanastaA['arriba'])
                b.rect = image.get_rect() # use image extent values 
                b.rect.topleft = [nx+2, ny+2] # put the ball in the top left corner
                screen.blit(image, b.rect)
            elif giroHacia == 'abajo':
                b = pygame.sprite.Sprite() # create sprite
                b.image = pygame.image.load("robot.png").convert_alpha() # load ball image
                image = pygame.transform.rotate(b.image, giroCanastaA['abajo'])
                b.rect = image.get_rect() # use image extent values 
                b.rect.topleft = [nx+2, ny+2] # put the ball in the top left corner
                screen.blit(image, b.rect)

        '''elif self.canastaRecogerProducto == 'B':
            b = pygame.sprite.Sprite() # create sprite
            b.image = pygame.image.load("robot.png").convert_alpha() # load ball image
            image = pygame.transform.rotate(b.image,90)
            b.rect = image.get_rect() # use image extent values 
            b.rect.topleft = [nx+2, ny+2] # put the ball in the top left corner
            screen.blit(image, b.rect)
        elif self.canastaRecogerProducto == 'C':
            b = pygame.sprite.Sprite() # create sprite
            b.image = pygame.image.load("robot.png").convert_alpha() # load ball image
            image = pygame.transform.rotate(b.image,90)
            b.rect = image.get_rect() # use image extent values 
            b.rect.topleft = [nx+2, ny+2] # put the ball in the top left corner
            screen.blit(image, b.rect)
        elif self.canastaRecogerProducto == 'D':
            b = pygame.sprite.Sprite() # create sprite
            b.image = pygame.image.load("robot.png").convert_alpha() # load ball image
            image = pygame.transform.rotate(b.image,90)
            b.rect = image.get_rect() # use image extent values 
            b.rect.topleft = [nx+2, ny+2] # put the ball in the top left corner
            screen.blit(image, b.rect)'''



   
    def agregarRuta(self,ruta,pedido):
        self.path = ruta
        self.path_restante = list(self.path)
        self.pedido_actual = pedido

    def iniciarRecorrido(self):
        self.play = True

    def stop(self):
        self.play = False

    def notificacion_libre(self,control):
        self.path = []
        self.state = 'libre'
        self.posicion_actual = self.source
        self.mov_pos = 0
        self.pedido_actual = None
        self.play = False
        self.robot_choque = None
        self.tipo_choque = None
        #self.stop()
        control.asignarPedidoRobot(self.nombre)


    def dibujarRuta(self, screen, nodes):
        if self.path:
            seg = [nodes[y][x].rect.center 
                    for (x, y) in self.path]
            pygame.draw.lines(screen, self.color, False,
                    seg, PATH_WIDTH)


    def BorrarRuta(self, screen, nodes):
        if self.path:
            seg = [nodes[y][x].rect.center 
                    for (x, y) in self.path]
            pygame.draw.lines(screen,(255,255,255) , False,
                    seg, PATH_WIDTH)


    def Mover(self):
        # Si las dos funciones son verdaderas - el robot camina, si esperando producto es falso (no hay productos para recoger) - el robot no camina (porq una de las condiciones no se cumple).
        if self.play: 
            self.length_path = len(self.path_restante)
            if  self.length_path>0:
                self.mov_pos += 1
                self.path_restante.pop(0)
                try:
                    self.posicion_actual = self.path_restante[0]
                except:
                    self.posicion_actual = self.source
                x, y = self.posicion_actual
                nx, ny = x * NODE_SIZE, y * NODE_SIZE
                self.rec_colision = pygame.Rect(nx, ny, NODE_SIZE, NODE_SIZE).inflate(NODE_SIZE*2,NODE_SIZE*2)

   
    def estadoEsperandoProducto(self):
        self.esperando_producto = False
        self.play = True
        self.flagGirar = False
        '''b = pygame.sprite.Sprite() # create sprite
        b.image = pygame.image.load("robot.png").convert_alpha() # load ball image
        image = pygame.transform.rotate(b.image,-45)
        b.rect = image.get_rect() # use image extent values 
        b.rect.topleft = [nx+3, ny+3] # put the ball in the top left corner
        screen.blit(image, b.rect)'''






        








    