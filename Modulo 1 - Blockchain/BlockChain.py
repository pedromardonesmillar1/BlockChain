# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 22:48:01 2022

@author: pedro
"""

# Módulo 1 - Crear una Cadena de Bloques

# Importar las librerias

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Parte 1 - Crear la Cadena de Bloques

class Blockchain:
    """
    Instancia __init__ para inicializar el constructor
    """
    def __init__(self):
        self.chain = []       # Para agregar la lista de las cadenas del bloque
        self.create_block(proof = 1, previous_hash = '0')  # Esto es el bloque genesis, y no tiene hash previo
    """
    Desarrollo de las funciones para crear bloques
    """
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1,      # Para el largo del hash de la cadena
                 'timestamp' : str(datetime.datetime.now()),  # Para poder generar automaticamente las fechas y horas
                 'proof' : proof,       # Para desarrollar la prueba de que efectivamente ha sido minada la cadena
                 'previous_hash' : previous_hash}   # Para identificar el hash del bloque anterior para continuar con la cadena
        self.chain.append(block)                 # Para añadir el bloque generado a la lista de la cadena
        return block                             # Para devolver el bloque generado previamente
    """
    Obtener el último bloque creado en la cadena anterior
    """
    def get_previous_block(self):
        return self.chain[-1]        # Para obtener el último de los valores de una lista con [-1]
    
# Parte 2 - Minado de un Bloque de la Cadena

