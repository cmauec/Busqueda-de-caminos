import random
from const.constants import * 
import pygame
from pygame.locals import *
import random


coloresProductos = [(207,23,23),(168,19,19),(133,15,15),(94,10,10),(59,6,6),(230,39,39),(237,111,111),(235,75,75),(242,148,148)]

class Pedido(object):

    def __init__(self, nombre, robot = 0):
        #estado del pedido
        self.state = 'por_entregar'
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
            products_in_wall1.append(self.gen_element(7,8,38))
        target_wall2_products = random.randrange(0,6)
        for p in range(0,target_wall2_products):
            products_in_wall2.append(self.gen_element(13,8,38))
        target_wall3_products = random.randrange(0,6)
        for p in range(0,target_wall3_products):
            products_in_wall3.append(self.gen_element(19,8,38))
        target_wall4_products = random.randrange(0,6)
        for p in range(0,target_wall4_products):
            products_in_wall4.append(self.gen_element(25,8,38))
        target_wall5_products = random.randrange(0,6)
        for p in range(0,target_wall5_products):
            products_in_wall5.append(self.gen_element(31,8,38))
        target_wall6_products = random.randrange(0,6)
        for p in range(0,target_wall6_products):
            products_in_wall6.append(self.gen_element(37,8,38))
        target_wall7_products = random.randrange(0,6)
        for p in range(0,target_wall7_products):
            products_in_wall7.append(self.gen_element(43,8,38))
        target_wall8_products = random.randrange(0,6)
        for p in range(0,target_wall8_products):
            products_in_wall8.append(self.gen_element(49,8,38))
        target_wall9_products = random.randrange(0,6)
        for p in range(0,target_wall9_products):
            products_in_wall9.append(self.gen_element(55,8,38))
        target_wall10_products = random.randrange(0,6)
        for p in range(0,target_wall10_products):
            products_in_wall10.append(self.gen_element(61,8,38))
        target_wall11_products = random.randrange(0,6)
        for p in range(0,target_wall11_products):
            products_in_wall11.append(self.gen_element(67,8,38))
        target_wall12_products = random.randrange(0,6)
        for p in range(0,target_wall12_products):
            products_in_wall12.append(self.gen_element(73,8,38))
        target_wall13_products = random.randrange(0,6)
        for p in range(0,target_wall13_products):
            products_in_wall13.append(self.gen_element(79,8,38))
        target_wall14_products = random.randrange(0,6)
        for p in range(0,target_wall14_products):
            products_in_wall14.append(self.gen_element1(1,8,38))
        target_wall15_products = random.randrange(0,6)
        for p in range(0,target_wall15_products):
            products_in_wall15.append(self.gen_element2(4,7,81))
        target_wall16_products = random.randrange(0,6)
        for p in range(0,target_wall16_products):
            products_in_wall16.append(self.gen_element2(41,7,81))

        #self.productos = products_in_wall1+products_in_wall2+products_in_wall3+products_in_wall4+products_in_wall5+products_in_wall6+products_in_wall7+products_in_wall8+products_in_wall9+products_in_wall10+products_in_wall11+products_in_wall12+products_in_wall13+products_in_wall14+products_in_wall15+products_in_wall16
        #generamos pedidos verticales
        self.productos = []
        '''for a in range(20,30):   
            self.productos.append((4,a))'''
        #genetamos pedidos diagonal inferior izquierda
        '''if robot == '1':
            self.productos = [(6,20), (1,25)]            
        elif robot == '2':
            self.productos = [(1,25),(6,20)]'''
        #genetamos pedidos diagonal inferior derecha
        '''if robot == '1':
            self.productos = [(5,19), (11,25)]            
        elif robot == '2':
            self.productos = [(11,25),(5,19)]'''
        #genetamos pedidos diagonal superior izquierda
        '''if robot == '1':
            self.productos = [(11,25), (7,21)]            
        elif robot == '2':
            self.productos = [(7,21),(11,25)]'''
        #genetamos pedidos diagonal superior derecha
        '''if robot == '1':
            self.productos = [(10,26), (16,20)]            
        elif robot == '2':
            self.productos = [(16,20),(10,26)]'''
        #generamos pedidos horizontales
        '''if robot == '1':
            self.productos = [(10,22), (17,22)]            
        elif robot == '2':
            self.productos = [(17,22),(10,22)]'''

        #generamos pedidos Cruzados(robot0-horiz)Viene de izq a der
        '''if robot == '1':
            self.productos = [(4,10), (9,10)]            
        elif robot == '2':
            self.productos = [(7,10),(5,15)]'''

        #generamos pedidos Cruzados(robot0-horiz)Viene de der a izq######Indicar a Mauro2
        '''if robot == '1':
            self.productos = [(9,10), (4,10)]            
        elif robot == '2':
            self.productos = [(5,10),(5,15)]'''
        #generamos pedidos Cruzados(robot0-ver)Viene de arrib a abaj
        if robot == '1':
            self.productos = [(5,10),(5,15)]            
        elif robot == '2':
            self.productos = [(7,10),(4,10)]
        #generamos pedidos Cruzados(robot0-ver)Viene de abaj a arrib
        '''if robot == '1':
            self.productos = [(5,19),(5,12)]            
        elif robot == '2':
            self.productos = [(17,14),(4,14)]'''
        #generamos pedidos Cruzados Diagonal  ##### Indicar Mauro
        '''if robot == '1':
            self.productos = [(4,10), (11,17)]            
        elif robot == '2':
            self.productos = [(11,17), (4,10)]'''
        #generamos pedidos Cruzados Diagonal (dia - vert)
        '''if robot == '1':
            self.productos = [(4,16), (7,13)]            
        elif robot == '2':
            self.productos = [(7,16), (7,13)]'''
        #generamos pedidos Cruzados Diagonal (vert - diag)
        '''if robot == '1':
            self.productos = [(7,16), (7,13)]            
        elif robot == '2':
            self.productos = [(4,16), (7,13)]'''
        #generamos pedidos Cruzados Diagonal (vert - diag)
        '''if robot == '1':
            self.productos = [(10,16), (7,13)]            
        elif robot == '2':
            self.productos = [(4,16), (7,13)]'''
        #generamos pedidos Combinados
        '''if robot == '1':
            self.productos = [(4,13), (6,13), (6,9)]            
        elif robot == '2':
            self.productos = [(7,6), (3,6), (6,9), (9, 9), (6,9),(6,13), ]'''


            
        

        self.color = random.choice(coloresProductos)
        self.nombre = nombre

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