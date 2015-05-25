 #!/usr/bin/env python

# Copyright (C) 2011 by Xueqiao Xu <xueqiaoxu@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys
import time
import datetime
import cPickle
import threading
import random
import pygame
import uuid

from pygame.locals import *
from const.constants import * 
from algo.astar import *

from ui.ui import *
from lib.robot import *
from lib.pedido import *
from lib.control import *
from threading import Timer
 
posicionRobot = [(5, 1), (7, 2), (3, 0), (7, 45), (3, 43), (5, 44)]
#posicionRobot = [(1, 1), (1, 1)]
FONT_NAME = 'freesansbold.ttf'
cur_path = os.path.abspath(os.path.dirname(__file__))
ui_path = os.path.join(cur_path, 'ui')
pygame.font.init()

texto_choque = 'Choque robots'
texto_se_van_chocar = 'Se van a chocar'
font = pygame.font.Font(os.path.join(ui_path, FONT_NAME),40)
txt_choque = font.render(texto_choque,True,(0,0,0))
txt_se_van_chocar = font.render(texto_se_van_chocar,True,(0,0,0))



def CrearRobots(robots):
    '''Creamos una lista de robots. Parametro robot indica cuantos robots creamos'''
    listaRobots = [] 
    for n in range(robots):
        posicionRobotRandom = random.choice(posicionRobot)      
        index_posicionRobotRandom = posicionRobot.index(posicionRobotRandom)
        posicionRobot.pop(index_posicionRobotRandom)
        robot = Robot(posicionRobotRandom, uuid.uuid4())
        listaRobots.append(robot)
    return listaRobots

def CrearRobot():
    '''Creamos un robot dinamicamente'''
    try: 
        posicionRobotRandom = random.choice(posicionRobot) 
        index_posicionRobotRandom = posicionRobot.index(posicionRobotRandom)
        posicionRobot.pop(index_posicionRobotRandom)
        robot = Robot(posicionRobotRandom, uuid.uuid4())
        return robot 
    except:
        return False




class Client(object):
    
    def __init__(self, ui_path):

        self.ui = UI(ui_path)

        # Creamos robots
        self.robots = CrearRobots(2)
             
        # Creacion del control del sistema
        self.control = Control(self.ui.nodes)
        
        # Agragamos robots al control
        for robot in self.robots:
            self.control.agregarRobot(robot)
                

        # general status
        self.status = ''
        self.flag = 1
        self.estadoChoqueCruzado = 0
        self.estadoChoqueDiagonal = 0

        #borrar despues de pruebas
        self.temp_choque = 0

        

    def run(self):
        """
        Iniciamos el bucle principal
        """
        while self.status != EXIT:
            # manejamos eventos de la apliacion
            for event in pygame.event.get():
                if event.type == QUIT:
                    self._quit()
                elif event.type == KEYDOWN:
                    self._handle_keyboard(event)


            
            # Dibujamos el color de fondo para el mapa
            self.ui._draw_background()

            # Dibujamos el mapa inicial
            self.ui._draw_map_init()

            # Dibujamos las lineas separadoras de cada nodo
            self.ui._draw_grid_lines()

            # Dibujamos todos los pedidos pendientes de entrega
            self.control.dibujarPedidos(self.ui.screen)


           

            for robot in self.robots:
                if len(robot.coordenadas_producto) > 0:
                    if robot.posicion_actual == robot.coordenadas_producto[0]:
                        robot.esperando_producto = True
                        robot.coordenadas_producto.pop(0)
                        Timer(2,robot.estadoEsperandoProducto).start()   #Hace que el robot se detenga 3 segundos para recoger roductos


            
            # Dibuajamos la animacion del robot            
            for robot in self.robots:
                robot.dibujarRuta(self.ui.screen, self.ui.nodes)
                if robot.play_animation:
                    robot.Mover()    
                robot.dibujarRobot(self.ui.screen)
                if robot.posicion_actual == (robot.source[0]+1,robot.source[1]):
                    # al finalizar el recorrido imprime los puntos de la trayectoria
                    #print robot.path
                    self.control.quitarPedidoConcluido(robot.pedido_actual)                    
                    robot.notificacion_libre(self.control)

                            
            self.robots_movimiento = []
            self.robots_temporal = []
            for robot in self.robots:
                if robot.play_animation:
                    self.robots_movimiento.append(robot)
            self.robots_temporal = self.robots_movimiento[1:]            
            for robot0 in self.robots_movimiento:
                for robot1 in self.robots_temporal:
                    if robot0.tipo_choque == 1 and robot1.tipo_choque == 1:
                        if robot0.robot_choque == robot1.nombre:
                            if robot0.esperando_robot == False:
                                robot0.esperando_robot = True
                            if DistanciaEntrePuntos(robot0.posicion_actual, robot1.posicion_actual) > 3:
                                robot0.esperando_robot = False
                                robot0.tipo_choque = None
                                robot0.robot_choque = None
                                robot1.esperando_robot = False
                                robot1.tipo_choque = None
                                robot1.robot_choque = None
                    elif robot0.tipo_choque == 20 and robot1.tipo_choque == 20:
                        print 'entra 20'
                        if robot1.robot_choque == robot0.nombre:
                            print '20 20'
                            if robot1.esperando_robot == False:
                                print '20 20 20'
                                robot1.esperando_robot = True
                            if DistanciaEntrePuntos(robot1.posicion_actual, robot0.posicion_actual) > 3:
                                print '20 20 20 20'
                                robot0.esperando_robot = False
                                robot0.tipo_choque = None
                                robot0.robot_choque = None
                                robot1.esperando_robot = False
                                robot1.tipo_choque = None
                                robot1.robot_choque = None
                    elif robot0.tipo_choque == 21 and robot1.tipo_choque == 21:
                        print 'entra 21'
                        if robot0.robot_choque == robot1.nombre:
                            print  '21 21'
                            if robot0.esperando_robot == False:
                                print '21 21 21'
                                robot0.esperando_robot = True
                            if DistanciaEntrePuntos(robot0.posicion_actual, robot1.posicion_actual) > 3:
                                print '21 21 21 21'
                                robot0.esperando_robot = False
                                robot0.tipo_choque = None
                                robot0.robot_choque = None
                                robot1.esperando_robot = False
                                robot1.tipo_choque = None
                                robot1.robot_choque = None






            self.robots_movimiento = []
            self.robots_temporal = []
            self.probabilidad_desvio = []
            for robot in self.robots:
                if robot.play_animation:
                    self.robots_movimiento.append(robot)
            self.robots_temporal = self.robots_movimiento[1:]
            for robot0 in self.robots_movimiento:
                for robot1 in self.robots_temporal:
                    if (robot0.tipo_choque == None and robot1.tipo_choque == None) and not robot0.esperando_producto and not robot1.esperando_producto:
                        if robot0.rec_colision.colliderect(robot1.rec_colision):  
                            if robot0.path_restante[1]==robot1.path_restante[1]:
                                #Se para en el momento del choque
                                #robot0.play_animation = False
                                #robot1.play_animation = False
                                self.ui.screen.blit(txt_se_van_chocar,(170,30)) # Pone texto en pantalla
                                print 'Se van a chocar'   
                                robot0.tipo_choque = 1
                                robot0.robot_choque = robot1.nombre 
                                robot1.tipo_choque = 1
                                robot1.robot_choque = robot0.nombre 
                                self.probabilidad_desvio = [(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0], robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1),(robot0.posicion_actual[0], robot0.posicion_actual[1]-1),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1)]
                                self.probabilidad_desvio.remove(robot1.path_restante[1])
                                if robot0.posicion_actual[0] in pared_izq:
                                    #Antes de borrar el elemto revizamos si esta en el vector. Cuando el choque se produce en la parte sup. o infe. que no hay pared a la izq o der y el punto de choque esta en la posicion de la pared.El codigo primero quitaba el punto de  choque pero este punto tambien pertenece a los puntos que hay q quitar por la pared, entonces se queria quitar un punto que ya no existia
                                    if (robot0.posicion_actual[0]-1, robot0.posicion_actual[1]) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]))
                                    if (robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                                    if (robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                elif robot0.posicion_actual[0] in pared_der:
                                    if (robot0.posicion_actual[0]+1, robot0.posicion_actual[1]) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]))
                                    if (robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1))
                                    if (robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                                elif robot0.posicion_actual[1] == pared_arriba:
                                    if (robot0.posicion_actual[0], robot0.posicion_actual[1]-1) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]-1))
                                    if (robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                    if (robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                                elif robot0.posicion_actual[1] == pared_abajo:
                                    if (robot0.posicion_actual[0], robot0.posicion_actual[1]+1) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]+1))
                                    if (robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                                    if (robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1) in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1))
                                if robot1.path_restante[2] in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove(robot1.path_restante[2])
                                elif robot1.path_restante[3] in self.probabilidad_desvio:
                                        self.probabilidad_desvio.remove(robot1.path_restante[3])                          
                                self.coordenada_desvio = random.choice(self.probabilidad_desvio)                 
                                robot0.path_restante.insert(1, self.coordenada_desvio)
                                robot0.path_restante.insert(2, robot0.path_restante[0])
                            elif (robot0.path_restante[1]==robot1.path_restante[0])and(robot0.path_restante[0]==robot1.path_restante[1]):
                                #robot0.play_animation = False
                                #robot1.play_animation = False
                                self.ui.screen.blit(txt_choque,(170,30))
                                print 'choque'
                                robot0.tipo_choque = 2
                                robot0.robot_choque = robot1.nombre 
                                robot1.tipo_choque = 2
                                robot1.robot_choque = robot0.nombre
                                self.probabilidad_desvio = [(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0], robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1),(robot0.posicion_actual[0], robot0.posicion_actual[1]-1),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1)]
                                
                                if robot0.posicion_actual[0] in pared_izq:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]))
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                                elif robot0.posicion_actual[0] in pared_der:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]))
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1)) 
                                elif robot0.posicion_actual[1] == pared_arriba:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]-1))
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                                elif robot0.posicion_actual[1] == pared_abajo:
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]+1))
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                                    self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1))
                                self.probabilidad_desvio.remove(robot1.path_restante[0])
                                if robot1.path_restante[1] in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove(robot1.path_restante[1])
                                elif robot1.path_restante[2] in self.probabilidad_desvio:
                                    self.probabilidad_desvio.remove(robot1.path_restante[2])                                                     
                                self.coordenada_desvio = random.choice(self.probabilidad_desvio)                                
                                robot0.path_restante.insert(1, self.coordenada_desvio)
                                robot0.path_restante.insert(2, robot0.path_restante[0])



                    elif robot0.esperando_producto and robot1.play_animation and not robot1.esperando_robot:
                        if (DistanciaEntrePuntos(robot0.posicion_actual, robot1.posicion_actual) == 1 ) or (DistanciaEntrePuntos(robot0.posicion_actual, robot1.posicion_actual) == sqrt(2)):
                            #robot0.play_animation = False
                            #robot1.play_animation = False
                            print 'colision, rob0-esperando, rob1-mov'                                                        
                            robot0.robot_choque = robot1.nombre
                            robot1.robot_choque = robot0.nombre
                            robot0.tipo_choque = 20
                            robot1.tipo_choque = 20
                            
                            print robot0.posicion_actual
                            print robot1.posicion_actual
                            print robot1.path_restante[1]
                            print robot0.path_restante[1]
                            #if robot1.path_restante[1][0] == robot0.posicion_actual[0]:                      
                            print 'Gina'
                            self.probabilidad_desvio = [(robot1.posicion_actual[0]+1, robot1.posicion_actual[1]),(robot1.posicion_actual[0]+1, robot1.posicion_actual[1]+1),(robot1.posicion_actual[0], robot1.posicion_actual[1]+1),(robot1.posicion_actual[0]-1, robot1.posicion_actual[1]+1),(robot1.posicion_actual[0]-1, robot1.posicion_actual[1]),(robot1.posicion_actual[0]-1, robot1.posicion_actual[1]-1),(robot1.posicion_actual[0], robot1.posicion_actual[1]-1),(robot1.posicion_actual[0]+1, robot1.posicion_actual[1]-1)]
                            
                            if robot1.posicion_actual[0] in pared_izq:
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0]-1, robot1.posicion_actual[1]))
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0]-1, robot1.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0]-1, robot1.posicion_actual[1]+1))
                            elif robot1.posicion_actual[0] in pared_der:
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0]+1, robot1.posicion_actual[1]))
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0]+1, robot1.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0]+1, robot1.posicion_actual[1]+1)) 
                            elif robot1.posicion_actual[1] == pared_arriba:
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0], robot1.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0]-1, robot1.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0]+1, robot1.posicion_actual[1]-1))
                            elif robot1.posicion_actual[1] == pared_abajo:
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0], robot1.posicion_actual[1]+1))
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0]-1, robot1.posicion_actual[1]+1))
                                self.probabilidad_desvio.remove((robot1.posicion_actual[0]+1, robot1.posicion_actual[1]+1))
                            self.probabilidad_desvio.remove(robot0.posicion_actual)
                            if robot0.path_restante[1] in self.probabilidad_desvio:
                                self.probabilidad_desvio.remove(robot0.path_restante[1])
                            elif robot0.path_restante[2] in self.probabilidad_desvio:
                                self.probabilidad_desvio.remove(robot0.path_restante[2])                                                     
                            self.coordenada_desvio = random.choice(self.probabilidad_desvio)
                            #self.coordenada_desvio = (robot1.posicion_actual[0]+1, robot1.posicion_actual[1])                             
                            robot1.path_restante.insert(1, self.coordenada_desvio)
                            robot1.path_restante.insert(2, robot1.path_restante[0])




                              
                    elif robot1.esperando_producto and robot0.play_animation and not robot0.esperando_robot:
                        if (DistanciaEntrePuntos(robot1.posicion_actual, robot0.posicion_actual) == 1) or (DistanciaEntrePuntos(robot1.posicion_actual, robot0.posicion_actual) == sqrt(2)):
                            #robot0.play_animation = False
                            #robot1.play_animation = False
                            print 'colision, rob1-esperando, rob0-mov'                            
                            robot0.robot_choque = robot1.nombre
                            robot1.robot_choque = robot0.nombre
                            robot0.tipo_choque = 21
                            robot1.tipo_choque = 21
                           
                            print robot1.posicion_actual
                            print robot0.posicion_actual
                            print robot0.path_restante[1]
                            print robot1.path_restante[1]
                            #if robot0.path_restante[1][0] == robot1.posicion_actual[0]:
                            print 'Gina1'
                            self.probabilidad_desvio = [(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0], robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1),(robot0.posicion_actual[0], robot0.posicion_actual[1]-1),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1)]                            
                            if robot0.posicion_actual[0] in pared_izq:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                            elif robot0.posicion_actual[0] in pared_der:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1)) 
                            elif robot0.posicion_actual[1] == pared_arriba:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                            elif robot0.posicion_actual[1] == pared_abajo:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]+1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1))
                            self.probabilidad_desvio.remove(robot1.posicion_actual)
                            if robot1.path_restante[1] in self.probabilidad_desvio:
                                self.probabilidad_desvio.remove(robot1.path_restante[1])
                            elif robot1.path_restante[2] in self.probabilidad_desvio:
                                self.probabilidad_desvio.remove(robot1.path_restante[2])                                                     
                            self.coordenada_desvio = random.choice(self.probabilidad_desvio)
                            #self.coordenada_desvio = (robot0.posicion_actual[0]+1, robot0.posicion_actual[1])                              
                            robot0.path_restante.insert(1, self.coordenada_desvio)
                            robot0.path_restante.insert(2, robot0.path_restante[0])
                            

                    elif robot1.esperando_producto and robot0.esperando_producto: 
                        robot0.play_animation = False
                        robot1.play_animation = False                        
                        if (robot0.path_restante[1]==robot1.path_restante[0])and(robot0.path_restante[0]==robot1.path_restante[1]):
                            robot0.tipo_choque = 3
                            robot0.robot_choque = robot1.nombre 
                            robot1.tipo_choque = 3
                            robot1.robot_choque = robot0.nombre
                            self.probabilidad_desvio = [(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0], robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]),(robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1),(robot0.posicion_actual[0], robot0.posicion_actual[1]-1),(robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1)]
                            
                            if robot0.posicion_actual[0] in pared_izq:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                            elif robot0.posicion_actual[0] in pared_der:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1)) 
                            elif robot0.posicion_actual[1] == pared_arriba:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]-1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]-1))
                            elif robot0.posicion_actual[1] == pared_abajo:
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0], robot0.posicion_actual[1]+1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]-1, robot0.posicion_actual[1]+1))
                                self.probabilidad_desvio.remove((robot0.posicion_actual[0]+1, robot0.posicion_actual[1]+1))
                            self.probabilidad_desvio.remove(robot1.path_restante[0])
                            if robot1.path_restante[1] in self.probabilidad_desvio:
                                self.probabilidad_desvio.remove(robot1.path_restante[1])
                            elif robot1.path_restante[2] in self.probabilidad_desvio:
                                self.probabilidad_desvio.remove(robot1.path_restante[2])                                                     
                            self.coordenada_desvio = random.choice(self.probabilidad_desvio)                                
                            robot0.path_restante.insert(1, self.coordenada_desvio)
                            robot0.path_restante.insert(2, robot0.path_restante[0])
                            print 'Gina3'

                                

                try: 
                    self.robots_temporal.pop(0)
                except:
                    pass

                                                 
            # update screen
            pygame.display.update()

            # control frame rate
            self.ui.clock.tick(FPS_LIMIT)



    def _quit(self):
        """Initiate termination
        """
        pygame.quit()
        raise SystemExit


    def _handle_keyboard(self, event):
        """Handle keyboard events
     cd   """
        #Agragar pedidos
        if event.key == K_SPACE:
            nombre = uuid.uuid4()
            if self.flag == 1:
                self.pedido = Pedido(nombre,'1')
            elif self.flag == 2:
                self.pedido = Pedido(nombre,'2')
            self.flag = 2
            self.control.agregarPedido(self.pedido)
            print self.pedido.nombre
            file = open("robotgina.txt", "w")
            for c in self.robots[0].path:
                file.write(str(c[0]) + ' ' + str(c[1]) + '\n')
            file.close()

        #Tecla para agregar robots en el punto de partida
        elif event.key == K_s:
            self.robotNuevo = CrearRobot()
            if self.robotNuevo:
                self.robots.append(self.robotNuevo)
                self.control.agregarRobot(self.robotNuevo)

        #Tecla para quitar robots en el punto de partida
        elif event.key == K_a:
            for robot in self.robots:
                if robot.state == 'libre':
                    indexRobot = self.robots.index(robot)
                    self.robots.pop(indexRobot)
                    posicionRobot.append(robot.source)
                    self.control.quitarRobot(robot)
                    colorRobot.append(robot.color)
                    return


        elif event.key == K_e:
            print "INFORMACION"
            print '-------------------------------------------------'            
            for robot in self.robots:
                print "INFORMACION robot"
                print '-------------------------------------------------'                
                print 'play_animation: ' + str (robot.play_animation)
                print 'esperando_producto: ' + str (robot.esperando_producto)
                print 'esperando_robot: ' + str (robot.esperando_robot)                
                print 'source: ' + str (robot.source)
                print 'state: ' + robot.state                 
                print 'robot_choque: ' + str (robot.robot_choque) 
                print 'tipo_choque: ' + str (robot.tipo_choque) 
                print 'nombre: ' + str (robot.nombre)     
                print 'path: ' + str (robot.path) 
                print 'path_restante: ' + str (robot.path_restante) 
                print 'coordenadas_producto: ' + str (robot.coordenadas_producto)
                print 'color: ' + str (robot.color) 
                print 'init: ' + str (robot.init) 
                print 'pos: ' + str (robot.pos) 
                print 'mov_pos: ' + str (robot.mov_pos) 
                print 'pedido_actual: ' + str (robot.pedido_actual)                
                print 'posicion_actual: ' + str (robot.posicion_actual) 
                print '-------------------------------------------------'

               
        elif event.key == K_o:
            self.robots[0].play_animation = False
            self.robots[1].play_animation = False
           

        elif event.key == K_p:
            self.robots[0].play_animation = True
            self.robots[1].play_animation = True 

        
                        
             

        

        elif event.key == K_ESCAPE:
            self._quit()



       
if __name__ == '__main__':
   
    
    cur_path = os.path.abspath(os.path.dirname(__file__))
    ui_path = os.path.join(cur_path, 'ui')
    

    client = Client(ui_path)
    client.run()
