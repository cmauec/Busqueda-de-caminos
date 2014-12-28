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
                           BLOCKED: Color(BLOCKED_COLOR),
                           OPENED: Color(OPENED_COLOR),
                           CLOSED: Color(CLOSED_COLOR),
                           SOURCE: Color(SOURCE_COLOR),
                           TARGET: Color(TARGET_COLOR),
                           TARGET_PATH_COLOR: Color(TARGET_PATH_COLOR)}

        self.node_font = pygame.font.Font(os.path.join(
            ui_path, FONT_NAME), NODE_INFO_FONT_SIZE)
        self._draw_map_init()

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

    def _set_node_status(self, (x, y), status):
            try:
                self.nodes[y][x].status = status
            except LookupError, why:
                print why

    def _draw_nodes(self):
            for row in self.nodes:
                for node in row:
                    self._draw_node_rect(node)

    def _draw_node_rect(self,node):
        try:
            pygame.draw.rect(self.screen, self.node_color[node.status], 
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
        self._draw_wall([(1,4),(81,4)],'horizontal')
        self._draw_wall([(1,3),(81,3)],'horizontal')
        self._draw_wall([(1,42),(81,42)],'horizontal')
        self._draw_wall([(1,41),(81,41)],'horizontal')
        self._draw_wall([(0,8),(0,37)])
        self._draw_wall([(1,8),(1,37)])
        self._draw_wall([(88,3),(88,4)])
        self._draw_wall([(89,3),(89,4)])
        self._draw_wall([(88,41),(88,42)])
        self._draw_wall([(89,41),(89,42)])
        self._draw_wall([(88,12),(88,13)])
        self._draw_wall([(89,12),(89,13)])
        self._draw_wall([(88,22),(88,23)])
        self._draw_wall([(89,22),(89,23)])
        self._draw_wall([(88,32),(88,33)])
        self._draw_wall([(89,32),(89,33)])
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
        self._draw_nodes()