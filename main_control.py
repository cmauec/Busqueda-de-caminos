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
import cPickle
import threading
import random
import pygame

from pygame.locals import *
from const.constants import * 
from algo.astar import *


class _Node(object):
    def __init__(self, (x, y)):
        self.pos = x, y
        left = x * NODE_SIZE
        top = y * NODE_SIZE
        self.rect = Rect(left, top, NODE_SIZE, NODE_SIZE)
        self.status = NORMAL
        self.parent = None
        self.f = None
        self.g = None
        self.h = None



class Client(object):
    
    def __init__(self, ui_path):

        self.flag = 0
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        # GUI related stuffs
        pygame.display.set_icon(
                pygame.image.load(os.path.join(ui_path, ICON_NAME)))
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.map_size = MAP_SIZE
        self.map_width, self.map_height = MAP_SIZE
        self.n_col = int(self.map_width / NODE_SIZE)
        self.n_row = int(self.map_height / NODE_SIZE)
        
        # builds nodes map
        self.nodes = [[_Node((x, y)) 
            for x in xrange(self.n_col)] 
                for y in xrange(self.n_row)]

        # color dictionary
        self.node_color = {NORMAL: Color(NORMAL_COLOR),
                           BLOCKED: Color(BLOCKED_COLOR),
                           OPENED: Color(OPENED_COLOR),
                           CLOSED: Color(CLOSED_COLOR),
                           SOURCE: Color(SOURCE_COLOR),
                           TARGET: Color(TARGET_COLOR),
                           TARGET_PATH_COLOR: Color(TARGET_PATH_COLOR)}

        self.node_font = pygame.font.Font(os.path.join(
            ui_path, FONT_NAME), NODE_INFO_FONT_SIZE)
        
        
        # Creamos variables para guardar coordenadas de los productos en las estanterias
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

        # Llenamos las varibles de los productos con coordenadas aleatorias
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

        self.play_animation = False
        self.pos = 30
        self.mov_pos = 0
        self.source = (1, 1)
        self.targets = products_in_wall1+products_in_wall2+products_in_wall3+products_in_wall4+products_in_wall5+products_in_wall6+products_in_wall7+products_in_wall8+products_in_wall9+products_in_wall10+products_in_wall11+products_in_wall12+products_in_wall13+products_in_wall14+products_in_wall15+products_in_wall16
        self.targets_with_source = []
        self.lenght_targets = len(self.targets)
        self.path = []
        self.move_right_wall = (1,9,15,21,27,33,39,45,51,57,63,69,75,81) 
        self.move_left_wall = (7,13,19,25,31,37,43,49,55,61,67,73,79)
        self.move_down_wall = 4
        self.move_up_wall = 41
        #parametro para tomar en cuenta targets solo a lo largo de la pared.
        self.wall_is_vertical = range(8,38)
        #coordenadas para dividir el mapa en secciones verticalmente
        self.sections = [(1,8),(9,14),(15,20),(21,26),(27,32),(33,38),(39,44),(45,50),(51,56),(57,62),(63,68),(69,74),(75,80),(81,82)]
        

        # general status
        self.status = DRAWING
        self.editable = False
        self.erasing = False
        self.drag = None

    def gen_path(self, targets):
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
                path_section.insert(0,path[-1])
            path_section = self.path_order_distance(path_section)
            path = path +path_section
        return path

    def path_order_distance(self, targets):
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
                        v1 = len(a.path)
                    except:
                        v1 = 0
                    t = (v1,t[0],t[1])
                    temp.append(t)
                    temp.sort()
                element_near = (temp[0][1],temp[0][2])
                targets_order.append(element_near)
                targets_temp.remove(element_near)
        return targets_order

       

    def gen_element(self,origin,limit_1_y,limit_2_y):
        mov_right = random.randrange(0,2) 
        if mov_right == 1:
            mov_right = 2
        x = origin+mov_right
        y = random.randrange(limit_1_y,limit_2_y)
        return (x,y)

    def gen_element1(self,origin,limit_1_y,limit_2_y):
        x = origin
        y = random.randrange(limit_1_y,limit_2_y)
        return (x,y)

    def gen_element2(self,origin,limit_1_x,limit_2_x):
        y = origin
        x = random.randrange(limit_1_x,limit_2_x)
        return (x,y)

    def run(self):
        """Starts the main loop
        """
        # handle events
        while self.status != EXIT:

            for event in pygame.event.get():
                if event.type == QUIT:
                    self._quit()
                elif event.type == KEYDOWN:
                    self._handle_keyboard(event)
            
            # draw stuffs
            self._draw_background()
            self._draw_nodes()
            self._draw_source_target()
            self._draw_target_path()
            self._draw_grid_lines()
            self._draw_path()
            self._draw_wall([(7,4),(81,4)],'horizontal')
            self._draw_wall([(7,3),(81,3)],'horizontal')
            self._draw_wall([(7,42),(81,42)],'horizontal')
            self._draw_wall([(7,41),(81,41)],'horizontal')
            self._draw_wall([(0,8),(0,37)])
            self._draw_wall([(1,8),(1,37)])
            self._draw_wall([(88,23),(88,24)])
            self._draw_wall([(89,23),(89,24)])
            self._draw_wall([(88,12),(88,13)])
            self._draw_wall([(89,12),(89,13)])
            self._draw_wall([(88,35),(88,36)])
            self._draw_wall([(89,35),(89,36)])
            self._draw_wall([(7,8),(7,37)])
            self._draw_wall([(8,8),(8,37)])
            self._draw_wall([(9,8),(9,37)])
            self._draw_wall([(13,8),(13,37)])
            self._draw_wall([(14,8),(14,37)])
            self._draw_wall([(15,8),(15,37)])
            self._draw_wall([(19,8),(19,37)])
            self._draw_wall([(20,8),(20,37)])
            self._draw_wall([(21,8),(21,37)])
            self._draw_wall([(25,8),(25,37)])
            self._draw_wall([(26,8),(26,37)])
            self._draw_wall([(27,8),(27,37)])
            self._draw_wall([(31,8),(31,37)])
            self._draw_wall([(32,8),(32,37)])
            self._draw_wall([(33,8),(33,37)])
            self._draw_wall([(37,8),(37,37)])
            self._draw_wall([(38,8),(38,37)])
            self._draw_wall([(39,8),(39,37)])
            self._draw_wall([(43,8),(43,37)])
            self._draw_wall([(44,8),(44,37)])
            self._draw_wall([(45,8),(45,37)])
            self._draw_wall([(49,8),(49,37)])
            self._draw_wall([(50,8),(50,37)])
            self._draw_wall([(51,8),(51,37)])
            self._draw_wall([(55,8),(55,37)])
            self._draw_wall([(56,8),(56,37)])
            self._draw_wall([(57,8),(57,37)])
            self._draw_wall([(61,8),(61,37)])
            self._draw_wall([(62,8),(62,37)])
            self._draw_wall([(63,8),(63,37)])
            self._draw_wall([(67,8),(67,37)])
            self._draw_wall([(68,8),(68,37)])
            self._draw_wall([(69,8),(69,37)])
            self._draw_wall([(73,8),(73,37)])
            self._draw_wall([(74,8),(74,37)])
            self._draw_wall([(75,8),(75,37)])
            self._draw_wall([(79,8),(79,37)])
            self._draw_wall([(80,8),(80,37)])
            self._draw_wall([(81,8),(81,37)])
            self.length_path = len(self.targets_with_source)
            #punto verde dinamico
            if self.play_animation: 
                if self.mov_pos < self.length_path:
                    self.source1 = self.targets_with_source[self.mov_pos]
                    x, y = self.source1
                    nx, ny = x*NODE_SIZE, y*NODE_SIZE
                    pygame.draw.rect(self.screen, self.node_color[SOURCE], Rect(nx, ny, NODE_SIZE, NODE_SIZE))
                    self.mov_pos += 1
            
            # update screen
            pygame.display.update()

            # control frame rate
            self.clock.tick(FPS_LIMIT)



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
            self.targets_with_source =self.targets
            self.targets_with_source.insert(0,self.source)
            self.targets_with_source = self.gen_path(self.targets_with_source)
            self.targets_with_source = self.gen_path_order(self.targets_with_source)
            #self.targets_with_source = self.gen_path_order_distance(self.targets_with_source)
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
        elif event.key == K_r:
            # Creamos variables para guardar coordenadas de los productos en las estanterias
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

            # Llenamos las varibles de los productos con coordenadas aleatorias
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
            self.play_animation = False
            self.pos = 30
            self.mov_pos = 0
            self.source = (1, 1)
            self.play_animation = False
            self.pos = 30
            self.mov_pos = 0
            targets_with_source = []
            self._reset()
            self.flag = 0
        elif event.key == K_ESCAPE:
            self._quit()
        elif event.key == K_s:
            self._reset()
            self.flag = 0

    def _set_node_status(self, (x, y), status):
        try:
            self.nodes[y][x].status = status
        except LookupError, why:
            print why

    def _set_node_value(self, (x, y), which, val):
        try:
            setattr(self.nodes[y][x], which, val)
        except AttributeError, why:
            print why

    def _set_node_parent(self, (x1, y1), (x2, y2)):
        try:
            self.nodes[y1][x1].parent = self.nodes[y2][x2]
        except LookupError, why:
            print why

    def _set_path(self, path):
        if not self.path:
            self.status = DRAWING
            self.path = path
        else:
            self.status = DRAWING
            self.path = self.path+path

    def _draw_background(self):
        self.screen.fill(Color(BACKGROUND_COLOR))

    def _draw_nodes(self):
        for row in self.nodes:
            for node in row:
                self._draw_node_rect(node)
                #self._draw_node_info(node)

    def _draw_node_rect(self, node):
        try:
            pygame.draw.rect(self.screen, self.node_color[node.status], 
                    node.rect, 0)
        except LookupError:
            pass

    def _draw_wall(self,wall,direction='vertical'):
        """draw the room walls.
        """
        if direction == 'vertical':
            wall1 = wall
            range_limit_low = (wall1[0][1]+1)
            range_limit_high = (wall1[1][1])
            nodes_wall = range(range_limit_low,range_limit_high)
            for v in nodes_wall:
                wall1.append((wall1[0][0],v))
            for w in wall1:
                nx, ny = w
                self._set_node_status((nx, ny), BLOCKED)
        elif direction == 'horizontal':
            wall1 = wall
            range_limit_low = (wall1[0][0]+1)
            range_limit_high = (wall1[1][0])
            nodes_wall = range(range_limit_low,range_limit_high)
            for v in nodes_wall:
                wall1.append((v, wall1[0][1]))
            for w in wall1:
                nx, ny = w
                self._set_node_status((nx, ny), BLOCKED)

    def _draw_source_target(self):
        """Source and target nodes are drawed on top of other nodes.
        """
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.screen, self.node_color[SOURCE], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 
        for target in self.targets:
            x, y = target
            nx, ny = x * NODE_SIZE, y * NODE_SIZE
            pygame.draw.rect(self.screen, self.node_color[TARGET], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE))

    def _draw_target_path(self):
        """Source and target nodes are drawed on top of other nodes.
        """
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.screen, self.node_color[SOURCE], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 
        for target in self.targets_with_source:
            x, y = target
            nx, ny = x * NODE_SIZE, y * NODE_SIZE
            pygame.draw.rect(self.screen, self.node_color[TARGET_PATH_COLOR], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE))

    def _draw_source_target1(self):
        """Source and target nodes are drawed on top of other nodes.
        """
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.screen, self.node_color[SOURCE], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 

        x, y = self.target1
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.screen, self.node_color[TARGET], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 

    def _draw_source_target2(self):
        """Source and target nodes are drawed on top of other nodes.
        """
        x, y = self.source
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.screen, self.node_color[SOURCE], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 

        x, y = self.target2
        nx, ny = x * NODE_SIZE, y * NODE_SIZE
        pygame.draw.rect(self.screen, self.node_color[TARGET], 
                Rect(nx, ny, NODE_SIZE, NODE_SIZE)) 

        
    def _draw_node_info(self, node):
        if node.f:
            img = self.node_font.render(str(node.f), True,
                    Color(NODE_INFO_COLOR))
            x = node.rect.left + MARGIN
            y = node.rect.top + MARGIN
            self.screen.blit(img, (x, y))
        if node.g:
            img = self.node_font.render(str(node.g), True,
                    Color(NODE_INFO_COLOR))
            x = node.rect.left + MARGIN
            y = node.rect.bottom - img.get_height() - MARGIN + 1
            self.screen.blit(img, (x, y))
        if node.h:
            img = self.node_font.render(str(node.h), True,
                    Color(NODE_INFO_COLOR))
            x = node.rect.right - img.get_width() - MARGIN + 1
            y = node.rect.bottom - img.get_height() - MARGIN + 1
            self.screen.blit(img, (x, y))
                
    def _draw_parent_lines(self):
        for row in self.nodes:
            for node in row:
                if node.parent:
                    pygame.draw.line(self.screen, 
                        Color(PARENT_LINE_COLOR),
                        node.parent.rect.center, node.rect.center, 1)


    def _draw_grid_lines(self):
        for x in xrange(0, self.map_width, NODE_SIZE):
            pygame.draw.line(self.screen, Color(GRID_LINE_COLOR),
                    (x, 0), (x, self.map_height), 1)
        for y in xrange(0, self.map_height, NODE_SIZE):
            pygame.draw.line(self.screen, Color(GRID_LINE_COLOR),
                    (0, y), (self.map_width, y), 1)

    def _draw_path(self):
        if self.path:
            seg = [self.nodes[y][x].rect.center 
                    for (x, y) in self.path]
            pygame.draw.lines(self.screen, Color(PATH_COLOR), False,
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
        for row in self.nodes:
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
        for row in self.nodes:
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
