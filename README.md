# First-term-exam---Practical
CRUD de Usuarios + Prueba controlada de fuerza bruta contra tu propia API

## Descripción
Este proyecto implementa una **API REST con FastAPI** que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre usuarios.  
Adicionalmente, se incluye un **script de fuerza bruta controlado** para demostrar vulnerabilidades asociadas a contraseñas débiles y medir los efectos de este tipo de ataques.

⚠️ **Aviso Importante:**  
Todas las pruebas deben realizarse únicamente en **entornos de desarrollo/laboratorio** y con cuentas creadas expresamente para la práctica.  
No se debe ejecutar este código contra sistemas externos a menos que se desee tener una sentencia penal.

---

## Estructura del proyecto

├── main.py # API con FastAPI (CRUD + login)

├── Brute_Force.py # Script de ataque de fuerza bruta

├── requirements1.txt # Dependencias necesarias

├── bruteforce.sh #Executable desde bash.

└── README.md # Este archivo

-------------------------------------------------------------------

## Instalación

## 1. Crear y activar un entorno virtual (opcional pero recomendado):

# In Bash:
python3 -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows

## 2. Instalar las dependencias:

#In Bash:
pip install -r requirements1.txt

-----------------------------------------------------------------

## Ejecución de la API

Para levantar la API, desde la carpeta del proyecto ejecutar:

fastapi dev main.py

- Esto iniciará un servidor en http://127.0.0.1:8000.

- Podrás acceder a la documentación automática en:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

Endpoints principales

/ POST /Users → Crear usuario

/ GET /Users → Listar usuarios

/ GET /Users/{id} → Obtener un usuario por ID

/ PUT /Users/{id} → Actualizar usuario

/ DELETE /Users/{id} → Eliminar usuario

/ POST /login → Autenticar usuario

/ Ejecución del ataque de fuerza bruta

- La API debe estar corriendo en una terminal (ejecutada con fastapi dev main.py).

# PD: Esa terminal solo mostrará logs de la API, no puede usarse para ejecutar otros comandos.
-----------------------------------------------------------------------------------------------------
Abrir otra terminal, preferentemente en WSL (Windows Subsystem for Linux) o una consola aparte.

Desde esa segunda terminal, ejecutar el executable de fuerza bruta en bash:

#In Bash:
./bruteforce.sh


El script probará credenciales contra el endpoint /login de la API y mostrará los intentos exitosos/fallidos.

-----------------------------------------------------------------------------------------------------------

## Ejemplos:

## No.1:

Ingresa el usuario objetivo: admin
=== ATAQUE DE FUERZA BRUTA CLÁSICA (VERSIÓN SIMPLE) ===
Objetivo: Usuario 'admin'
Charset: 0123456789 (tamaño: 10)
Espacio total estimado (hasta 4 chars): ~11110 combinaciones
API: http://127.0.0.1:8000/login
----------------------------------------

--- Probando longitud 1 (10 combinaciones posibles) ---
[!] Longitud 1 agotada sin éxito

--- Probando longitud 2 (100 combinaciones posibles) ---
[!] Longitud 2 agotada sin éxito

--- Probando longitud 3 (1000 combinaciones posibles) ---
[!] Longitud 3 agotada sin éxito

--- Probando longitud 4 (10000 combinaciones posibles) ---

[+] ¡ÉXITO! Contraseña encontrada: '1234' (longitud 4)
[+] Intentos totales: 2345
[+] Tiempo total: 138.44 segundos
[+] Tasa promedio: 16.94 intentos/segundo
=== FIN DEL ATAQUE ===

## No.2:

Ingresa el usuario objetivo: Matias
=== ATAQUE DE FUERZA BRUTA CLÁSICA (VERSIÓN SIMPLE) ===
Objetivo: Usuario 'Matias'
Charset: 0123456789 (tamaño: 10)
Espacio total estimado (hasta 4 chars): ~11110 combinaciones
API: http://127.0.0.1:8000/login
----------------------------------------

--- Probando longitud 1 (10 combinaciones posibles) ---
[!] Longitud 1 agotada sin éxito

--- Probando longitud 2 (100 combinaciones posibles) ---
[!] Longitud 2 agotada sin éxito

--- Probando longitud 3 (1000 combinaciones posibles) ---
[!] Longitud 3 agotada sin éxito

--- Probando longitud 4 (10000 combinaciones posibles) ---
[!] Longitud 4 agotada sin éxito

[!] Ataque finalizado sin éxito (agotó 11110 combinaciones).
[!] Intentos totales: 11110
[!] Tiempo total: 8.81 segundos
[!] Tasa: 1261.5 intentos/segundo
=== FIN DEL ATAQUE ===
