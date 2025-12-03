import json
import time
import random

def lambda_handler(event, context):
    print("Iniciando procesamiento de pedido...")
    
    # 1. Simular latencia (tiempo de espera)
    # El código espera entre 0.1 y 1 segundo aleatoriamente.
    # Esto hará que en X-Ray veas tiempos de respuesta variados.
    sleep_time = random.uniform(0.1, 1.0)
    time.sleep(sleep_time)
    
    # 2. Simular un error del 10%
    # 1 de cada 10 veces, la función fallará a propósito.
    # Esto es para que veas círculos rojos/naranjas en el mapa de trazas.
    if random.random() < 0.1:
        raise Exception("Error simulado: Fallo en la base de datos de pedidos")

    print(f"Pedido procesado exitosamente en {sleep_time} segundos.")
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Pedido completado. Tiempo: {sleep_time}')
    }
