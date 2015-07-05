import os
import pygame
from pygame.locals import *
from const.constants import * 

class _Node(object):
    def __init__(self, (x, y)):
        self.pos = x, y
        left = x * NODE_SIZE
        top = y * NODE_SIZE
        self.rect = Rect(left, top, NODE_SIZE, NODE_SIZE)
        self.status = NORMAL
        self.color = BLOCKED_COLOR
        self.parent = None
        self.f = None
        self.g = None
        self.h = None


class UI(object):

    def __init__(self, ui_path):
        
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
                           BLOCKED: BLOCKED_COLOR,
                           OPENED: Color(OPENED_COLOR),
                           CLOSED: Color(CLOSED_COLOR),
                           SOURCE: Color(SOURCE_COLOR),
                           TARGET: Color(TARGET_COLOR),
                           TARGET_PATH_COLOR: Color(TARGET_PATH_COLOR)}

    def _draw_wall(self,wall,direction='vertical'):
            """dibujas las paredes. Se pasa como parametro el punto inicial y el punto final de la pared y la orientacion
            """
            #Dibujo pared vertical
            if direction == 'vertical':
                wall1 = wall
                range_limit_low = (wall1[0][1]+1)
                range_limit_high = (wall1[1][1])
                nodes_wall = range(range_limit_low,range_limit_high)
                for v in nodes_wall:
                    wall1.append((wall1[0][0],v))
                for w in wall1:
                    nx, ny = w
                    self._set_node_status((nx, ny), BLOCKED,BLOCKED_COLOR )
            elif direction == 'horizontal':
                wall1 = wall
                range_limit_low = (wall1[0][0]+1)
                range_limit_high = (wall1[1][0])
                nodes_wall = range(range_limit_low,range_limit_high)
                for v in nodes_wall:
                    wall1.append((v, wall1[0][1]))
                for w in wall1:
                    nx, ny = w
                    self._set_node_status((nx, ny), BLOCKED,BLOCKED_COLOR )

    def _draw_wall1(self,wall,direction='vertical'):
            """dibujas las paredes. Se pasa como parametro el punto inicial y el punto final de la pared y la orientacion
            """
            #Dibujo pared vertical
            if direction == 'vertical':
                wall1 = wall
                range_limit_low = (wall1[0][1]+1)
                range_limit_high = (wall1[1][1])
                nodes_wall = range(range_limit_low,range_limit_high)
                for v in nodes_wall:
                    wall1.append((wall1[0][0],v))
                for w in wall1:
                    nx, ny = w
                    self._set_node_status((nx, ny), BLOCKED, WALLS)
            elif direction == 'horizontal':
                wall1 = wall
                range_limit_low = (wall1[0][0]+1)
                range_limit_high = (wall1[1][0])
                nodes_wall = range(range_limit_low,range_limit_high)
                for v in nodes_wall:
                    wall1.append((v, wall1[0][1]))
                for w in wall1:
                    nx, ny = w
                    self._set_node_status((nx, ny), BLOCKED, WALLS)

    def _set_node_status(self, (x, y), status,color):
            try:
                self.nodes[y][x].status = status
                self.nodes[y][x].color = color
            except LookupError, why:
                print why

    def _draw_nodes(self):
            for row in self.nodes:
                for node in row:
                    self._draw_node_rect(node)

    def _draw_node_rect(self,node):
        try:
            pygame.draw.rect(self.screen, node.color, 
                    node.rect, 0)
        except LookupError:
            pass

    def _draw_grid_lines(self):
        for x in xrange(0, self.map_width, NODE_SIZE):
            pygame.draw.line(self.screen, Color(GRID_LINE_COLOR),
                    (x, 0), (x, self.map_height), 1)
        for y in xrange(0, self.map_height, NODE_SIZE):
            pygame.draw.line(self.screen, Color(GRID_LINE_COLOR),
                    (0, y), (self.map_width, y), 1)

    def _draw_background(self):
        self.screen.fill(Color(BACKGROUND_COLOR))

    #Dibujamos las paredes
    def _draw_map_init(self):
        self._draw_wall1([(3,4),(81,4)],'horizontal')
        self._draw_wall1([(3,3),(81,3)],'horizontal')
        self._draw_wall1([(3,42),(81,42)],'horizontal')
        self._draw_wall1([(3,41),(81,41)],'horizontal')

        # self._draw_wall([(3,7),(81,7)],'horizontal')
        # self._draw_wall([(3,8),(81,8)],'horizontal')
        # self._draw_wall([(3,36),(81,36)],'horizontal')
        # self._draw_wall([(3,35),(81,35)],'horizontal')
        #letra F
        self._draw_wall([(3,15),(3,25)])
        self._draw_wall([(3,15),(7,15)],'horizontal')
        self._draw_wall([(3,20),(5,20)],'horizontal')
        #letra E
        self._draw_wall([(10,15),(10,25)])
        self._draw_wall([(10,15),(14,15)],'horizontal')
        self._draw_wall([(10,20),(12,20)],'horizontal')
        self._draw_wall([(10,25),(14,25)],'horizontal')
        #letra L
        self._draw_wall([(17,15),(17,25)])
        self._draw_wall([(17,25),(21,25)],'horizontal')
        #letra I
        self._draw_wall([(24,15),(24,25)])
        #letra C
        self._draw_wall([(27,15),(27,25)])
        self._draw_wall([(27,15),(31,15)],'horizontal')
        self._draw_wall([(27,25),(31,25)],'horizontal')
        #letra I
        self._draw_wall([(34,15),(34,25)])
        #letra D
        self._draw_wall([(37,15),(37,25)])
        self._draw_wall([(41,16),(41,24)])
        self._draw_wall([(38,15),(40,15)],'horizontal')
        self._draw_wall([(38,25),(40,25)],'horizontal')
        #letra A
        self._draw_wall([(44,16),(44,25)])
        self._draw_wall([(48,16),(48,25)])
        self._draw_wall([(45,15),(47,15)],'horizontal')
        self._draw_wall([(45,20),(47,20)],'horizontal')
        #letra D
        self._draw_wall([(51,15),(51,25)])
        self._draw_wall([(55,16),(55,24)])
        self._draw_wall([(52,15),(54,15)],'horizontal')
        self._draw_wall([(52,25),(54,25)],'horizontal')
        #letra E
        self._draw_wall([(58,15),(58,25)])
        self._draw_wall([(58,15),(62,15)],'horizontal')
        self._draw_wall([(58,20),(60,20)],'horizontal')
        self._draw_wall([(58,25),(62,25)],'horizontal')
        #letra S
        self._draw_wall([(65,15),(65,20)])
        self._draw_wall([(69,20),(69,25)])
        self._draw_wall([(65,15),(69,15)],'horizontal')
        self._draw_wall([(65,20),(69,20)],'horizontal')
        self._draw_wall([(65,25),(69,25)],'horizontal')
        self._draw_nodes()