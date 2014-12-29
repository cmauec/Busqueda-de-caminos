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

from pygame.locals import *
from const.constants import * 
from algo.astar import *

from ui.ui import *
from robot.robot import *


class Client(object):
    
    def __init__(self, ui_path):

        self.ui = UI(ui_path)
        self.flag = 0
        # Creamos variables para guardar coordenadas de los productos en las estanterias(targets)
        products_in_wall1 = []
        products_in_wall2 = []
        products_in_wall3 = []
        products_in_wall4 = []
        products_in_wall5 = []
        products_in_wall6 = []
        products_in_wall7 = []
        products_in_wall8 = []
        products_in_wall9 = []
        products_in_wall10 = []
        products_in_wall11 = []
        products_in_wall12 = []
        products_in_wall13 = []
        products_in_wall14 = []
        products_in_wall15 = []
        products_in_wall16 = []

        # Llenamos las estanterias de los productos con coordenadas aleatorias tomando en cuenta la posicion ( que no este en el centro - self.gen_element)
        target_wall1_products = random.randrange(0,6)
        for p in range(0,target_wall1_products):
            products_in_wall1.append(self.gen_element(7,8,37))
        target_wall2_products = random.randrange(0,6)
        for p in range(0,target_wall2_products):
            products_in_wall2.append(self.gen_element(13,8,37))
        target_wall3_products = random.randrange(0,6)
        for p in range(0,target_wall3_products):
            products_in_wall3.append(self.gen_element(19,8,37))
        target_wall4_products = random.randrange(0,6)
        for p in range(0,target_wall4_products):
            products_in_wall4.append(self.gen_element(25,8,37))
        target_wall5_products = random.randrange(0,6)
        for p in range(0,target_wall5_products):
            products_in_wall5.append(self.gen_element(31,8,37))
        target_wall6_products = random.randrange(0,6)
        for p in range(0,target_wall6_products):
            products_in_wall6.append(self.gen_element(37,8,37))
        target_wall7_products = random.randrange(0,6)
        for p in range(0,target_wall7_products):
            products_in_wall7.append(self.gen_element(43,8,37))
        target_wall8_products = random.randrange(0,6)
        for p in range(0,target_wall8_products):
            products_in_wall8.append(self.gen_element(49,8,37))
        target_wall9_products = random.randrange(0,6)
        for p in range(0,target_wall9_products):
            products_in_wall9.append(self.gen_element(55,8,37))
        target_wall10_products = random.randrange(0,6)
        for p in range(0,target_wall10_products):
            products_in_wall10.append(self.gen_element(61,8,37))
        target_wall11_products = random.randrange(0,6)
        for p in range(0,target_wall11_products):
            products_in_wall11.append(self.gen_element(67,8,37))
        target_wall12_products = random.randrange(0,6)
        for p in range(0,target_wall12_products):
            products_in_wall12.append(self.gen_element(73,8,37))
        target_wall13_products = random.randrange(0,6)
        for p in range(0,target_wall13_products):
            products_in_wall13.append(self.gen_element(79,8,37))
        target_wall14_products = random.randrange(0,6)
        for p in range(0,target_wall14_products):
            products_in_wall14.append(self.gen_element1(1,8,37))
        target_wall15_products = random.randrange(0,6)
        for p in range(0,target_wall15_products):
            products_in_wall15.append(self.gen_element2(4,7,81))
        target_wall16_products = random.randrange(0,6)
        for p in range(0,target_wall16_products):
            products_in_wall16.append(self.gen_element2(41,7,81))



        # Creamos variables para guardar coordenadas de los productos en las estanterias(targets) robot dos
        products_uno_in_wall1 = []
        products_uno_in_wall2 = []
        products_uno_in_wall3 = []
        products_uno_in_wall4 = []
        products_uno_in_wall5 = []
        products_uno_in_wall6 = []
        products_uno_in_wall7 = []
        products_uno_in_wall8 = []
        products_uno_in_wall9 = []
        products_uno_in_wall10 = []
        products_uno_in_wall11 = []
        products_uno_in_wall12 = []
        products_uno_in_wall13 = []
        products_uno_in_wall14 = []
        products_uno_in_wall15 = []
        products_uno_in_wall16 = []

        # Llenamos las estanterias de los productos con coordenadas aleatorias tomando en cuenta la posicion ( que no este en el centro - self.gen_element) robot dos
        target_uno_wall1_products = random.randrange(0,6)
        for p in range(0,target_uno_wall1_products):
            products_uno_in_wall1.append(self.gen_element(7,8,37))
        target_uno_wall2_products = random.randrange(0,6)
        for p in range(0,target_uno_wall2_products):
            products_uno_in_wall2.append(self.gen_element(13,8,37))
        target_uno_wall3_products = random.randrange(0,6)
        for p in range(0,target_uno_wall3_products):
            products_uno_in_wall3.append(self.gen_element(19,8,37))
        target_uno_wall4_products = random.randrange(0,6)
        for p in range(0,target_uno_wall4_products):
            products_uno_in_wall4.append(self.gen_element(25,8,37))
        target_uno_wall5_products = random.randrange(0,6)
        for p in range(0,target_uno_wall5_products):
            products_uno_in_wall5.append(self.gen_element(31,8,37))
        target_uno_wall6_products = random.randrange(0,6)
        for p in range(0,target_uno_wall6_products):
            products_uno_in_wall6.append(self.gen_element(37,8,37))
        target_uno_wall7_products = random.randrange(0,6)
        for p in range(0,target_uno_wall7_products):
            products_uno_in_wall7.append(self.gen_element(43,8,37))
        target_uno_wall8_products = random.randrange(0,6)
        for p in range(0,target_uno_wall8_products):
            products_uno_in_wall8.append(self.gen_element(49,8,37))
        target_uno_wall9_products = random.randrange(0,6)
        for p in range(0,target_uno_wall9_products):
            products_uno_in_wall9.append(self.gen_element(55,8,37))
        target_uno_wall10_products = random.randrange(0,6)
        for p in range(0,target_uno_wall10_products):
            products_uno_in_wall10.append(self.gen_element(61,8,37))
        target_uno_wall11_products = random.randrange(0,6)
        for p in range(0,target_uno_wall11_products):
            products_uno_in_wall11.append(self.gen_element(67,8,37))
        target_uno_wall12_products = random.randrange(0,6)
        for p in range(0,target_uno_wall12_products):
            products_uno_in_wall12.append(self.gen_element(73,8,37))
        target_uno_wall13_products = random.randrange(0,6)
        for p in range(0,target_uno_wall13_products):
            products_uno_in_wall13.append(self.gen_element(79,8,37))
        target_uno_wall14_products = random.randrange(0,6)
        for p in range(0,target_uno_wall14_products):
            products_uno_in_wall14.append(self.gen_element1(1,8,37))
        target_uno_wall15_products = random.randrange(0,6)
        for p in range(0,target_uno_wall15_products):
            products_uno_in_wall15.append(self.gen_element2(4,7,81))
        target_uno_wall16_products = random.randrange(0,6)
        for p in range(0,target_uno_wall16_products):
            products_uno_in_wall16.append(self.gen_element2(41,7,81))


        self.init = 0
        self.init_uno = 0
        self.play_animation = False
        self.pos = 30
        self.mov_pos = 0
        self.mov_pos_uno = 0
        self.source = (4, 1)
        self.source_uno = (4, 45)  #inicio robot dos
        #este punto representa el lugar a donde regresa el robot despues de dejar los productos (self.source_end)
        self.source_end = (4,1)
        self.salida_norte = [(89,6),(89,8),(89,10)]
        self.salida_noreste = [(89,15),(89,17),(89,19)]
        self.salida_sur = [(89,35),(89,37),(89,39)]
        self.salida_suroeste = [(89,25),(89,27),(89,29)]
        #si el robot esta en la parte de arriba tendra como salida al norte o al noreste
        if self.source[1]<8:
            self.salida = self.salida_norte+self.salida_noreste
            self.salida = random.choice(self.salida)
        #si el robot esta en la parte inferior tendra como salida al sur o suroeste
        elif self.source[1]>37:
            self.salida = self.salida_sur+self.salida_suroeste
            self.salida = random.choice(self.salida)
        #genera punto de salida del robot dos    
        if self.source_uno[1]<8:
            self.salida_uno = self.salida_norte+self.salida_noreste
            self.salida_uno = random.choice(self.salida_uno)
        elif self.source_uno[1]>37:
            self.salida_uno = self.salida_sur+self.salida_suroeste
            self.salida_uno = random.choice(self.salida_uno)
        #sumamos todos loas productos que se generan aleatoreamente robot uno    
        self.targets = products_in_wall1+products_in_wall2+products_in_wall3+products_in_wall4+products_in_wall5+products_in_wall6+products_in_wall7+products_in_wall8+products_in_wall9+products_in_wall10+products_in_wall11+products_in_wall12+products_in_wall13+products_in_wall14+products_in_wall15+products_in_wall16
        #producto del robot dos
        self.targets_uno= products_uno_in_wall1+products_uno_in_wall2+products_uno_in_wall3+products_uno_in_wall4+products_uno_in_wall5+products_uno_in_wall6+products_uno_in_wall7+products_uno_in_wall8+products_uno_in_wall9+products_uno_in_wall10+products_uno_in_wall11+products_uno_in_wall12+products_uno_in_wall13+products_uno_in_wall14+products_uno_in_wall15+products_uno_in_wall16
        self.targets_with_source = []
        self.targets_with_source_uno = []
        #self.lenght_targets = len(self.targets)
        self.path = []
        self.path_uno = []
        #nos sirve para crear la sombra de los targets
        self.move_right_wall = (1,9,15,21,27,33,39,45,51,57,63,69,75,81) #aumentamos en x uno
        self.move_left_wall = (7,13,19,25,31,37,43,49,55,61,67,73,79) #disminuimos en x uno
        self.move_down_wall = 4 #aumentamos en y uno
        self.move_up_wall = 41 #disminuimos en Y uno
        #parametro para tomar en cuenta targets solo a lo largo de la pared.
        self.wall_is_vertical = range(8,38)
        #coordenadas para dividir el mapa en secciones verticalmente, son las coordenadas de la pared del centro
        self.sections = [(1,8),(9,14),(15,20),(21,26),(27,32),(33,38),(39,44),(45,50),(51,56),(57,62),(63,68),(69,74),(75,80),(81,82)]
        

        # general status
        self.status = DRAWING
        self.editable = False
        self.erasing = False
        self.drag = None

        

    def gen_path(self, targets):
        #generamos la trayectoria pasando por la sombra de los targets
        path = []
        for t in targets:
            if t[1] in self.wall_is_vertical:
                if t[0] in self.move_right_wall:
                    t = (t[0]+1,t[1])
                elif t[0] in self.move_left_wall:
                    t = (t[0]-1,t[1]) 
            else:
                if t[1] == self.move_down_wall:
                    t = (t[0],t[1]+1)
                elif t[1] == self.move_up_wall:
                    t = (t[0],t[1]-1)
             
            path.append(t)
        return path


    # Para ordenar los targets de menor a mayor (por seccion)    
    def gen_path_order(self, targets):
        path = []
        for s in self.sections:
            path_section = []
            for t in targets:
                if t[0] in range(s[0], s[1]+1):
                    try:
                        #path.append(t)
                        path_section.append(t)
                    except:  
                        pass
            if len(path)>0:
                path_section.insert(0,path[-1]) #hace que el ultimo punto de la seccion sea el primer punto de la siguiente seccion
            path_section = self.path_order_distance(path_section)
            path = path +path_section
        return path

    def path_order_distance(self, targets):
        #haciendo el sol con cada target
        targets_order = []
        temp = []
        targets_temp = []
        for t in targets:
            targets_temp.append(t)
        for t1 in targets:
            if len(targets_order) == 0: 
                element = targets_temp[0]
                targets_order.append(targets_temp[0])
                targets_temp.remove(element)
            else:
                element = targets_order[-1]
            temp = []
            targets_temp_order = []
            for t2 in targets_temp:
                targets_temp_order.append(t2)
            if len(targets_temp_order)>0:
                for t in targets_temp_order:
                    nodes_map_raw = self._get_str_map(element, t)
                    try:
                        a = AStar(nodes_map_raw)
                        for i in a.step():
                            pass
                        v1 = len(a.path) #tomando el tamano de la trayectoria
                    except:
                        v1 = 0
                    t = (v1,t[0],t[1]) # tomando el tamano de la distancia menor y su coordenada para tomar como siguiente punto de inicio (sol)
                    temp.append(t)
                    temp.sort()
                element_near = (temp[0][1],temp[0][2])
                targets_order.append(element_near)
                targets_temp.remove(element_near)
        return targets_order

       
    #cambiando las targets, dependiendo de la posicion en la pared, para que no quede en el centro 
    def gen_element(self,origin,limit_1_y,limit_2_y): #para todas las paredes verticales
        mov_right = random.randrange(0,2) 
        if mov_right == 1:
            mov_right = 2
        x = origin+mov_right
        y = random.randrange(limit_1_y,limit_2_y)
        return (x,y)

    def gen_element1(self,origin,limit_1_y,limit_2_y): #para pared vertical del fondo(2paredes)
        x = origin
        y = random.randrange(limit_1_y,limit_2_y)
        return (x,y)

    def gen_element2(self,origin,limit_1_x,limit_2_x): #cambiando x, para pardes horizontales
        y = origin
        x = random.randrange(limit_1_x,limit_2_x)
        return (x,y)

    def run(self):
        """Iniciamos el bucle principal
        """
        # handle events
        while self.status != EXIT:

            for event in pygame.event.get():
                if event.type == QUIT:
                    self._quit()
                elif event.type == KEYDOWN:
                    self._handle_keyboard(event)
            
            #Dibujamos el color de fondo para el mapa
            self.ui._draw_background()
            #Dibujamos el mapa inicial
            self.ui._draw_map_init()
            #Dibujamos las lineas separadoras de cada nodo
            #self.ui._draw_grid_lines()
            self._draw_source_target()
            self._draw_target_path()
            self._draw_path()
            self.length_path = len(self.targets_with_source)
            self.length_path_uno = len(self.targets_with_source_uno) #ve cuantos targets tiene la trayectoria 
            #punto verde dinamico
            if self.play_animation:
                if self.init == 0:    #para que el retardo en la animacion se ejecute a  partir del segundo ciclo
                    time.sleep(0.5)
                if self.mov_pos < self.length_path:
                        self.source1 = self.targets_with_source[self.mov_pos]
                        x, y = self.source1
                        nx, ny = x*NODE_SIZE, y*NODE_SIZE
                        pygame.draw.rect(self.ui.screen, self.ui.node_color[SOURCE], Rect(nx, ny, NODE_SIZE, NODE_SIZE))
                        self.mov_pos += 1
            self.init += self.init

            #punto dinamico para el robot dos
            if self.play_animation:
                if  self.init_uno == 0:    #para que el retardo en la animacion se ejecute a  partir del segundo ciclo
                    time.sleep(0.5)
                if self.mov_pos_uno < self.length_path_uno:
                        self.source1_uno = self.targets_with_source_uno[self.mov_pos_uno]
                        x, y = self.source1_uno
                        nx, ny = x*NODE_SIZE, y*NODE_SIZE
                        pygame.draw.rect(self.ui.screen, (15,108,125), Rect(nx, ny, NODE_SIZE, NODE_SIZE))
                        self.mov_pos_uno += 1
            self.init_uno += self.init_uno
            
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
        """
        
        if event.key == K_SPACE:
            self.play_animation = True
            #intergrando source,targets, punto de salida y punto de llegada a la estacion principal (self.source_end), para que el punto verde recorra todos los puntos
            self.targets_with_source =self.targets
            self.targets_with_source.insert(0,self.source)
            self.targets_with_source = self.gen_path(self.targets_with_source)
            self.targets_with_source = self.gen_path_order(self.targets_with_source)
            self.targets_with_source.append(self.salida)
            self.targets_with_source.append(self.source_end)

            self.targets_with_source_uno =self.targets_uno 
            self.targets_with_source_uno.insert(0,self.source_uno )
            self.targets_with_source_uno  = self.gen_path(self.targets_with_source_uno )
            self.targets_with_source_uno  = self.gen_path_order(self.targets_with_source_uno )
            self.targets_with_source_uno.append(self.salida_uno)
            self.targets_with_source_uno.append(self.source_uno)
            #self.targets_with_source = self.gen_path_order_distance(self.targets_with_source)
            #codigo para dibujar el camino continuo entre todas las targets
            for t in range(len(self.targets_with_source)):
                if t+1 < len(self.targets_with_source):
                    nodes_map_raw = self._get_str_map(self.targets_with_source[t], self.targets_with_source[t+1])
                    try:
                        a = AStar(nodes_map_raw)
                        for i in a.step():
                            pass
                        self.path += a.path
                    except:
                        pass 

            #dibuja el camino entre las targets del robot dos
            for t in range(len(self.targets_with_source_uno)):
                if t+1 < len(self.targets_with_source_uno):
                    nodes_map_raw = self._get_str_map(self.targets_with_source_uno[t], self.targets_with_source_uno[t+1])
                    try:
                        a = AStar(nodes_map_raw)
                        for i in a.step():
                            pass
                        self.path_uno += a.path
                    except:
                        pass                        
        elif event.key == K_r: #borrando todo
            # Borramos los tagets y las trayectorias creadas robot uno
            if self.source[0]<8:
                self.salida = self.salida_norte+self.salida_noreste
                self.salida = random.choice(self.salida)
            elif self.source[0]>37:
                self.salida = self.salida_sur+self.salida_suroeste
                self.salida = random.choice(self.salida)
            
            products_in_wall1 = []
            products_in_wall2 = []
            products_in_wall3 = []
            products_in_wall4 = []
            products_in_wall5 = []
            products_in_wall6 = []
            products_in_wall7 = []
            products_in_wall8 = []
            products_in_wall9 = []
            products_in_wall10 = []
            products_in_wall11 = []
            products_in_wall12 = []
            products_in_wall13 = []
            products_in_wall14 = []
            products_in_wall15 = []
            products_in_wall16 = []

            
            target_wall1_products = random.randrange(0,6)
            for p in range(0,target_wall1_products):
                products_in_wall1.append(self.gen_element(7,8,37))
            target_wall2_products = random.randrange(0,6)
            for p in range(0,target_wall2_products):
                products_in_wall2.append(self.gen_element(13,8,37))
            target_wall3_products = random.randrange(0,6)
            for p in range(0,target_wall3_products):
                products_in_wall3.append(self.gen_element(19,8,37))
            target_wall4_products = random.randrange(0,6)
            for p in range(0,target_wall4_products):
                products_in_wall4.append(self.gen_element(25,8,37))
            target_wall5_products = random.randrange(0,6)
            for p in range(0,target_wall5_products):
                products_in_wall5.append(self.gen_element(31,8,37))
            target_wall6_products = random.randrange(0,6)
            for p in range(0,target_wall6_products):
                products_in_wall6.append(self.gen_element(37,8,37))
            target_wall7_products = random.randrange(0,6)
            for p in range(0,target_wall7_products):
                products_in_wall7.append(self.gen_element(43,8,37))
            target_wall8_products = random.randrange(0,6)
            for p in range(0,target_wall8_products):
                products_in_wall8.append(self.gen_element(49,8,37))
            target_wall9_products = random.randrange(0,6)
            for p in range(0,target_wall9_products):
                products_in_wall9.append(self.gen_element(55,8,37))
            target_wall10_products = random.randrange(0,6)
            for p in range(0,target_wall10_products):
                products_in_wall10.append(self.gen_element(61,8,37))
            target_wall11_products = random.randrange(0,6)
            for p in range(0,target_wall11_products):
                products_in_wall11.append(self.gen_element(67,8,37))
            target_wall12_products = random.randrange(0,6)
            for p in range(0,target_wall12_products):
                products_in_wall12.append(self.gen_element(73,8,37))
            target_wall13_products = random.randrange(0,6)
            for p in range(0,target_wall13_products):
                products_in_wall13.append(self.gen_element(79,8,37))
            target_wall14_products = random.randrange(0,6)
            for p in range(0,target_wall14_products):
                products_in_wall14.append(self.gen_element1(1,8,37))
            target_wall15_products = random.randrange(0,6)
            for p in range(0,target_wall15_products):
                products_in_wall15.append(self.gen_element2(4,7,81))
            target_wall16_products = random.randrange(0,6)
            for p in range(0,target_wall16_products):
                products_in_wall16.append(self.gen_element2(41,7,81))

            self.targets = products_in_wall1+products_in_wall2+products_in_wall3+products_in_wall4+products_in_wall5+products_in_wall6+products_in_wall7+products_in_wall8+products_in_wall9+products_in_wall10+products_in_wall11+products_in_wall12+products_in_wall13+products_in_wall14+products_in_wall15+products_in_wall16

            self.targets_with_source = self.targets
            self.targets_with_source = self.gen_path(self.targets_with_source)
            self.targets_with_source = self.gen_path_order(self.targets_with_source)
            self.targets_with_source.append(self.salida)
            self.play_animation = False
            self.pos = 30
            self.mov_pos = 0
            self.source = (4, 1)
            self.play_animation = False
            self.pos = 30
            self.mov_pos = 0
            targets_with_source = []
            self._reset()
            self.flag = 0


            #borrando robot dos
            if self.source_uno[1]<8:
                self.salida_uno = self.salida_norte+self.salida_noreste
                self.salida_uno = random.choice(self.salida_uno)
            elif self.source_uno[1]>37:
                self.salida_uno = self.salida_sur+self.salida_suroeste
                self.salida_uno = random.choice(self.salida_uno)
            products_uno_in_wall1 = []
            products_uno_in_wall2 = []
            products_uno_in_wall3 = []
            products_uno_in_wall4 = []
            products_uno_in_wall5 = []
            products_uno_in_wall6 = []
            products_uno_in_wall7 = []
            products_uno_in_wall8 = []
            products_uno_in_wall9 = []
            products_uno_in_wall10 = []
            products_uno_in_wall11 = []
            products_uno_in_wall12 = []
            products_uno_in_wall13 = []
            products_uno_in_wall14 = []
            products_uno_in_wall15 = []
            products_uno_in_wall16 = []

            # Llenamos las estanterias de los productos con coordenadas aleatorias tomando en cuenta la posicion ( que no este en el centro - self.gen_element) robot dos
            target_uno_wall1_products = random.randrange(0,6)
            for p in range(0,target_uno_wall1_products):
                products_uno_in_wall1.append(self.gen_element(7,8,37))
            target_uno_wall2_products = random.randrange(0,6)
            for p in range(0,target_uno_wall2_products):
                products_uno_in_wall2.append(self.gen_element(13,8,37))
            target_uno_wall3_products = random.randrange(0,6)
            for p in range(0,target_uno_wall3_products):
                products_uno_in_wall3.append(self.gen_element(19,8,37))
            target_uno_wall4_products = random.randrange(0,6)
            for p in range(0,target_uno_wall4_products):
                products_uno_in_wall4.append(self.gen_element(25,8,37))
            target_uno_wall5_products = random.randrange(0,6)
            for p in range(0,target_uno_wall5_products):
                products_uno_in_wall5.append(self.gen_element(31,8,37))
            target_uno_wall6_products = random.randrange(0,6)
            for p in range(0,target_uno_wall6_products):
                products_uno_in_wall6.append(self.gen_element(37,8,37))
            target_uno_wall7_products = random.randrange(0,6)
            for p in range(0,target_uno_wall7_products):
                products_uno_in_wall7.append(self.gen_element(43,8,37))
            target_uno_wall8_products = random.randrange(0,6)
            for p in range(0,target_uno_wall8_products):
                products_uno_in_wall8.append(self.gen_element(49,8,37))
            target_uno_wall9_products = random.randrange(0,6)
            for p in range(0,target_uno_wall9_products):
                products_uno_in_wall9.append(self.gen_element(55,8,37))
            target_uno_wall10_products = random.randrange(0,6)
            for p in range(0,target_uno_wall10_products):
                products_uno_in_wall10.append(self.gen_element(61,8,37))
            target_uno_wall11_products = random.randrange(0,6)
            for p in range(0,target_uno_wall11_products):
                products_uno_in_wall11.append(self.gen_element(67,8,37))
            target_uno_wall12_products = random.randrange(0,6)
            for p in range(0,target_uno_wall12_products):
                products_uno_in_wall12.append(self.gen_element(73,8,37))
            target_uno_wall13_products = random.randrange(0,6)
            for p in range(0,target_uno_wall13_products):
                products_uno_in_wall13.append(self.gen_element(79,8,37))
            target_uno_wall14_products = random.randrange(0,6)
            for p in range(0,target_uno_wall14_products):
                products_uno_in_wall14.append(self.gen_element1(1,8,37))
            target_uno_wall15_products = random.randrange(0,6)
            for p in range(0,target_uno_wall15_products):
                products_uno_in_wall15.append(self.gen_element2(4,7,81))
            target_uno_wall16_products = random.randrange(0,6)
            for p in range(0,target_uno_wall16_products):
                products_uno_in_wall16.append(self.gen_element2(41,7,81))

            self.targets_uno= products_uno_in_wall1+products_uno_in_wall2+products_uno_in_wall3+products_uno_in_wall4+products_uno_in_wall5+products_uno_in_wall6+products_uno_in_wall7+products_uno_in_wall8+products_uno_in_wall9+products_uno_in_wall10+products_uno_in_wall11+products_uno_in_wall12+products_uno_in_wall13+products_uno_in_wall14+products_uno_in_wall15+products_uno_in_wall16

            self.targets_with_source_uno = self.targets_uno
            self.targets_with_source_uno = self.gen_path(self.targets_with_source_uno)
            self.targets_with_source_uno = self.gen_path_order(self.targets_with_source_uno)
            self.targets_with_source_uno.append(self.salida_uno)
            self.play_animation = False
            self.pos = 30
            self.mov_pos_uno = 0
            self.source_uno = (4, 1)
            self.play_animation = False
            self.pos = 30
            self.mov_pos_uno = 0
            targets_with_source_uno = []
            self._reset()
            self.flag = 0

        elif event.key == K_ESCAPE:
            self._quit()
        elif event.key == K_s:
            self._reset()
            self.flag = 0

    def _draw_source_target(self):
        """Source and target nodes are drawed on top of other nodes.
        """
        #para dibujar robot uno
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.ui.screen, self.ui.node_color[SOURCE], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 

        #para dibujar robot dos
        x, y = self.source_uno
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.ui.screen,(15, 108, 125), 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 

        #para dibujar punto de salida del robot uno
        x1, y1 = self.salida
        nx1, ny1 = x1 * NODE_SIZE, y1 * NODE_SIZE
        pygame.draw.rect(self.ui.screen, self.ui.node_color[SOURCE], 
                Rect(nx1, ny1, NODE_SIZE, NODE_SIZE)) 

         #para dibujar punto de salida del robot dos
        x1, y1 = self.salida_uno
        nx1, ny1 = x1 * NODE_SIZE, y1 * NODE_SIZE
        pygame.draw.rect(self.ui.screen, (15, 108, 125), 
                Rect(nx1, ny1, NODE_SIZE, NODE_SIZE)) 

        #para dibujar los targets del robot uno
        for target in self.targets:
            x, y = target
            nx, ny = x * NODE_SIZE, y * NODE_SIZE
            pygame.draw.rect(self.ui.screen, self.ui.node_color[TARGET], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE))

        #para dibujar los targets del robot dos
        RED = (250,154,0)
        for target in self.targets_uno:
            x, y = target
            nx, ny = x * NODE_SIZE, y * NODE_SIZE
            pygame.draw.rect(self.ui.screen, RED, 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE))

    def _draw_target_path(self):
        """Source and target nodes are drawed on top of other nodes.
        """
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.ui.screen, self.ui.node_color[SOURCE], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 
        #dibujando la trayectoria del robot uno
        for target in self.targets_with_source:
            x, y = target
            nx, ny = x * NODE_SIZE, y * NODE_SIZE
            pygame.draw.rect(self.ui.screen, self.ui.node_color[TARGET_PATH_COLOR], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE))

        #dibujando la trayectoria del robot dos
        ORANGE = (242,196, 131)
        for target in self.targets_with_source_uno:
            x, y = target
            nx, ny = x * NODE_SIZE, y * NODE_SIZE
            pygame.draw.rect(self.ui.screen, ORANGE, 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE))

    def _draw_path(self):
        if self.path:
            seg = [self.ui.nodes[y][x].rect.center 
                    for (x, y) in self.path]
            pygame.draw.lines(self.ui.screen, Color(PATH_COLOR), False,
                    seg, PATH_WIDTH)

        if self.path_uno:
            seg = [self.ui.nodes[y][x].rect.center 
                    for (x, y) in self.path_uno]
            pygame.draw.lines(self.ui.screen, (204,189,167), False,
                    seg, PATH_WIDTH)

    def _reset(self):
        """Reset all nodes to be NORMAL and clear the node infos
        """
        self.path = []
        for row in self.nodes:
            for node in row:
                node.status = NORMAL
                node.f = None
                node.g = None
                node.h = None
                node.parent = None

    def _reset_except_block(self):
        """Same as _reset, but does not clear the blocked nodes
        """
        self.path = []
        for row in self.ui.nodes:
            for node in row:
                if node.status != BLOCKED:
                    node.status = NORMAL
                node.f = None
                node.g = None
                node.h = None
                node.parent = None

    def _get_str_map(self,sourceA,targetA):
        """Generate a string represented map from the current nodes' status.
        """
        final_str = []
        for row in self.ui.nodes:
            str = []
            for node in row:
                if node.pos == sourceA:
                    str.append(SOURCE)
                elif node.pos == targetA :
                    str.append(TARGET)
                else: 
                    str.append(node.status)
            str.append('\n')
            final_str.append(''.join(str))
        return ''.join(final_str)

    
if __name__ == '__main__':
   
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ha:p:', ['help'])
        for o, a in opts:
            if o in ('-h', '--help'):
                print_help()
                raise SystemExit
           
    except (getopt.GetoptError, ValueError):
        print 'Argumentos invalidos\n'
        print_help()
        raise SystemExit
    cur_path = os.path.abspath(os.path.dirname(__file__))
    ui_path = os.path.join(cur_path, 'ui')
    

    client = Client(ui_path)
    client.run()
