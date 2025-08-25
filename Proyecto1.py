# -------------------------------------------------
# Proyecto 1 - Cuestionario Interactivo
# Alumno: Alejandro Jiménez Sánchez
# Módulo: MPO - ASIR
# -------------------------------------------------
# Funcionalidades:
# 1. Menú con 3 opciones: Cuestionario, Ranking, Salir.
# 2. Preguntas cargadas desde archivo JSON.
# 3. Soporte para niveles de dificultad ("fácil" y "difícil").
# 4. Guardar resultados en ranking.json para consultarlos después.
# -------------------------------------------------

import json  # Leer y guardar datos en formato JSON
import os  # Comprobar si archivos existen

# Archivos del proyecto
PREGUNTAS_FILE = "preguntas.json"
RANKING_FILE = "ranking.json"

# -------------------------------------------------
# Función: cargar_preguntas
# Cargar preguntas desde un archivo JSON según el nivel especificado.
# -------------------------------------------------
def cargar_preguntas(nivel):
    """
    Definimos una función llamada cargar_preguntas
    Recibe el parámetro nivel que indica qué preguntas cargar
    """
    try:
        with open(PREGUNTAS_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return datos[nivel] #Accedemos al diccionario datos usando la clave nivel, retorna la lista de preguntas de ese nivel
    except FileNotFoundError:
        print("❌ No se encontró el archivo de preguntas.") #Si el archivo no existe, muestra un mensaje de error
        return [] #Retorna una lista vacía [] para evitar que el programa se detenga
    except KeyError:
        print("❌ No hay preguntas para este nivel.") #Si el nivel especificado no existe en el JSON, muestra un mensaje
        return []


# -------------------------------------------------
# Función: mostrar_pregunta
# Mostrar una pregunta y sus opciones de respuesta en la consola.
# -------------------------------------------------
def mostrar_pregunta(pregunta):
    """
    Definimos una función llamada mostrar_pregunta
    Recibe un parámetro pregunta que es un diccionario
    """
    print("\n" + pregunta["pregunta"]) #pregunta["pregunta"]: Accede al valor de la clave "pregunta" en el diccionario
    for opcion in pregunta["opciones"]: #Itera sobre cada elemento de la lista de opciones, accede a la lista de opciones en el diccionario
        print(opcion) #Imprime cada opción en una línea nueva

# -------------------------------------------------
# Función: obtener_respuesta
# Obtener una respuesta válida del usuario (A, B, C o D) y asegurarse de que sea correcta.
# -------------------------------------------------
def obtener_respuesta():
    """
    Obtener una respuesta válida del usuario (A, B, C o D) y comprobar que sea correcta.
    No recibe parámetros, lo obtiene del usuario
    """
    while True: #Crea un bucle que se repetirá indefinidamente, solo se detendrá cuando encuentre un return
        r = input("Tu respuesta (A/B/C/D): ").upper()#.upper(): Convierte la respuesta a MAYÚSCULAS (ej: "a" → "A"), r: Almacena la respuesta del usuario
        if r in ["A", "B", "C", "D"]:
            return r #Verifica si r está en la lista de opciones válidas, si es válida, retorna la respuesta y termina la función
        else:
            print("❌ Opción no válida.") #El bucle while True se repite automáticamente


# -------------------------------------------------
# Función: corregir_respuesta
# Verificar si la respuesta del usuario es correcta y mostrar el resultado.
# -------------------------------------------------
def corregir_respuesta(respuesta, correcta):
    """
    Definimos una función llamada corregir_respuesta
    Recibe dos parámetros:
    respuesta: La respuesta que dio el usuario
    correcta: La respuesta correcta esperada
    """
    if respuesta == correcta: #Compara si la respuesta del usuario es igual a la respuesta correcta
        print("✅ Correcto!")
        return True #Retorna True (verdadero) indicando que la respuesta fue correcta
    else:
        print(f"❌ Incorrecto. La respuesta correcta era {correcta}.") #{correcta}: Inserta la respuesta correcta en el mensaje
        return False #Retorna False (falso) indicando que la respuesta fue incorrecta

# -------------------------------------------------
# Función: mostrar_resultados
# Mostrar los resultados del test con estadísticas.
# -------------------------------------------------
def mostrar_resultados(aciertos, total):
    """
    Definimos una función llamada mostrar_resultados
    Recibe dos parámetros:
    aciertos: Número de respuestas correctas
    total: Número total de preguntas respondidas
    """

    print("\n--- RESULTADOS ---")
    print(f"Preguntas totales: {total}")
    print(f"Aciertos: {aciertos}")
    porcentaje = (aciertos / total) * 100 #Fórmula: (aciertos ÷ total) × 100
    print(f"Porcentaje: {porcentaje:.2f}%") #:.2f: Formatea el número para mostrar 2 decimales
    if porcentaje >= 80:
        print("¡Muy bien!")
    elif porcentaje >= 50:
        print("Nada mal, pero puedes mejorar.")
    else:
        print("Necesitas practicar más.")

# -------------------------------------------------
# Función: guardar_resultado
# Guardar los resultados del usuario en un archivo JSON para mantener un ranking.
# -------------------------------------------------
def guardar_resultado(nombre, aciertos, total):
    """
    Recibe tres parámetros:
    nombre: Nombre del jugador
    aciertos: Número de respuestas correctas
    total: Número total de preguntas
    """
    resultado = { #Crea un diccionario con toda la información del resultado
        "nombre": nombre,
        "aciertos": aciertos,
        "total": total,
        "porcentaje": round((aciertos / total) * 100, 2) #round(..., 2): Redondea el porcentaje a 2 decimales
    }
    ranking = [] #ranking = []: Inicializa una lista vacía
    if os.path.exists(RANKING_FILE): #os.path.exists(RANKING_FILE): Verifica si el archivo ya existe
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            try:
                ranking = json.load(f) #json.load(f): Intenta cargar el contenido JSON del archivo
            except json.JSONDecodeError: #except json.JSONDecodeError: Si el archivo está corrupto o vacío, ignora el error
                pass
    ranking.append(resultado) #append(resultado): Añade el nuevo resultado a la lista del ranking
    with open(RANKING_FILE, "w", encoding="utf-8") as f: #"w": Modo escritura (sobrescribe el archivo)
        json.dump(ranking, f, ensure_ascii=False, indent=4)
        # json.dump(): Convierte la lista Python a formato JSON,
        # ensure_ascii=False: Permite caracteres especiales (tildes, ñ, etc.)
        # indent=4: Formatea el JSON con sangría para que sea legible


# -------------------------------------------------
# Función: mostrar_ranking
# -------------------------------------------------
def mostrar_ranking():
    if not os.path.exists(RANKING_FILE): #os.path.exists(RANKING_FILE) verifica si el archivo de ranking existe
        print("📂 No hay ranking disponible todavía.")
        return  # Salir de la función si no existe el archivo

    with open(RANKING_FILE, "r", encoding="utf-8") as f: # Abrir y leer el archivo de ranking
        ranking = json.load(f)  # json.load(f) convierte el contenido JSON en una estructura de datos Python (lista)

    if not ranking:    # Comprobar si la lista está vacía
        print("📂 No hay resultados para mostrar.")
        return  # Salir de la función si no hay datos

    print("\n--- RANKING ---") # Encabezado del ranking

    ranking_ordenado = sorted(ranking, key=lambda x: x["porcentaje"], reverse=True)
    #sorted() ordena la lista
    #key = lambda x: x["porcentaje"] indica que debe ordenar por el campo"porcentaje"
    #reverse = True ordena de mayor a menor(los mejores porcentajes primero)

    for i, r in enumerate(ranking_ordenado[:10], 1):  # Mostrar los 10 mejores resultados, enumerate empieza en 1
        print(f"{i}. {r['nombre']} - {r['aciertos']}/{r['total']} ({r['porcentaje']}%)")

# -------------------------------------------------
# Función: empezar_cuestionario
# -------------------------------------------------
def empezar_cuestionario():
    nombre = input("Introduce tu nombre: ").strip() # Solicitar nombre del usuario, .strip() elimina espacios al inicio/final
    print("\nElige nivel de dificultad:")
    print("1 - Fácil")
    print("2 - Difícil")
    nivel_opcion = input("Opción: ")
    if nivel_opcion == "1":
        nivel = "facil"
    elif nivel_opcion == "2":
        nivel = "dificil"
    else:
        print("Nivel no válido.")
        return
    preguntas = cargar_preguntas(nivel) #Cargar las preguntas según el nivel seleccionado
    if not preguntas:
        return
    aciertos = 0 #Inicializar contador de aciertos
    for p in preguntas: #Bucle para recorrer todas las preguntas
        mostrar_pregunta(p)
        resp = obtener_respuesta()
        if corregir_respuesta(resp, p["respuesta_correcta"]): #Verificar si es correcta y actualizar contador
            aciertos += 1
    mostrar_resultados(aciertos, len(preguntas))
    guardar_resultado(nombre, aciertos, len(preguntas))


# -------------------------------------------------
# Función: menu
# -------------------------------------------------
def menu():
    # Bucle infinito: mantiene el programa ejecutándose hasta que el usuario elija salir
    while True:
        #  Mostrar las opciones del menú
        print("\n### MENÚ ###")
        print("1 - Empezar cuestionario")
        print("2 - Ranking")
        print("3 - Salir")

        #  Solicitar una opción al usuario
        opcion = input("Elige una opción: ")

        #  Ejecutar la opción seleccionada
        if opcion == "1":
            empezar_cuestionario()  # Inicia el cuestionario
        elif opcion == "2":
            mostrar_ranking()  # Muestra el ranking de resultados
        elif opcion == "3":
            print("Saliendo...")  # Mensaje de despedida
            break  # Rompe el bucle while True, terminando el programa
        else:
            # Manejar opciones no válidas
            print("Opción no válida.")

# -------------------------------------------------
# Programa principal
# -------------------------------------------------
if __name__ == "__main__":
    menu()