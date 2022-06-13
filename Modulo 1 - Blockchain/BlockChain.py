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
    """
    Función para poder formar los valores objetivos de hash
    """
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()    # Esta línea permite transformar a hexadecimal
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    """
    Función para determinar y construir el hash del bloque
    """
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    """
    Verificar si la cadena es valida
    """
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()      # Ecuación para validar el bloque  
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
        
# Parte 2 - Minado de un Bloque de la Cadena

# Crear una aplicación Web

app = Flask(__name__)       # Se debe consultar a la documentación

# Esta línea es por si ocurre algun error 500
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Crear una BlockChain

blockchain = Blockchain()

# Minar un nuevo bloque

@app.route("/mine_block", methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : '¡Enhorabuena, has minado un nuevo bloque!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200       # Este es el codigo HTTP para codigos correctos

# Obtención de la cadema de bloques al completo

@app.route("/get_chain", methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(response)

# Verificar si es valida la Blockchain

@app.route("/is_valid", methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid == True:
        response = {'message' : 'La cadena es valida'}
    else:
        response = {'message' : 'La cadena NO es valida'}
    return jsonify(response), 200

# Ejecutar la app

app.run(host = '0.0.0.0', port = 5000)









