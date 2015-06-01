# -*- coding: utf-8 -*-
import random
from const.constants import * 
import pygame
from pygame.locals import *
import random


coloresProductos = [(207,23,23),(168,19,19),(133,15,15),(94,10,10),(59,6,6),(230,39,39),(237,111,111),(235,75,75),(242,148,148)]
nombresProductos = [u'Картофель', u'Капуста', u'Морковь', u'Помидоры', u'Огурцы', u'Чеснок', u'Лук', u'Свекла', u'Зелень', u'Рыба', u'Тушенка', u'Горошек', u'Кукуруза', u'Сгущенка', u'Грибы', u'Макароны', u'Спагетти', u'Гречка', u'Перловка',u'Рис', u'Геркулес', u'Кукурузная крупа', u'Горох', u'Мёд', u'Яйца', u'Уксус', u'Маргарин', u'Мука', u'Сахар', u'Кофе', u'чай', u'Какао']


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

        self.productos = products_in_wall1+products_in_wall2+products_in_wall3+products_in_wall4+products_in_wall5+products_in_wall6+products_in_wall7+products_in_wall8+products_in_wall9+products_in_wall10+products_in_wall11+products_in_wall12+products_in_wall13+products_in_wall14+products_in_wall15+products_in_wall16

        self.productos_nom = {}
        for p in self.productos:
            nombresProductosTemporal = nombresProductos[:]
            nombreProducto = random.choice(nombresProductosTemporal)
            self.productos_nom[nombreProducto]  = p
            nombresProductosTemporal.remove(nombreProducto)                          

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