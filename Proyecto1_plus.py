# -------------------------------------------------
# Proyecto 1 - Cuestionario Interactivo Mejorado (sin límite de tiempo)
# Alumno: [Tu Nombre]
# Módulo: MPO - ASIR
# -------------------------------------------------
# Funcionalidades:
# 1. Menú con 3 opciones: Cuestionario, Ranking, Salir.
# 2. Preguntas cargadas desde archivo JSON.
# 3. Soporte para niveles de dificultad ("fácil" y "difícil").
# 4. Guardar resultados en ranking.json para consultarlos después.
# -------------------------------------------------

import json      # Leer y guardar datos en formato JSON
import os        # Comprobar si archivos existen

# Archivos del proyecto
PREGUNTAS_FILE = "preguntas.json"
RANKING_FILE = "ranking.json"

# -------------------------------------------------
# Función: cargar_preguntas
# -------------------------------------------------
def cargar_preguntas(nivel):
    try:
        with open(PREGUNTAS_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return datos[nivel]
    except FileNotFoundError:
        print("❌ No se encontró el archivo de preguntas.")
        return []
    except KeyError:
        print("❌ No hay preguntas para este nivel.")
        return []


# -------------------------------------------------
# Función: mostrar_pregunta
# -------------------------------------------------
def mostrar_pregunta(pregunta):
    print("\n" + pregunta["pregunta"])
    for opcion in pregunta["opciones"]:
        print(opcion)

# -------------------------------------------------
# Función: obtener_respuesta
# -------------------------------------------------
def obtener_respuesta():
    while True:
        r = input("Tu respuesta (A/B/C/D): ").upper()
        if r in ["A", "B", "C", "D"]:
            return r
        else:
            print("❌ Opción no válida.")


# -------------------------------------------------
# Función: corregir_respuesta
# -------------------------------------------------
def corregir_respuesta(respuesta, correcta):
    if respuesta == correcta:
        print("✅ Correcto!")
        return True
    else:
        print(f"❌ Incorrecto. La respuesta correcta era {correcta}.")
        return False

# -------------------------------------------------
# Función: mostrar_resultados
# -------------------------------------------------
def mostrar_resultados(aciertos, total):
    print("\n--- RESULTADOS ---")
    print(f"Preguntas totales: {total}")
    print(f"Aciertos: {aciertos}")
    porcentaje = (aciertos / total) * 100
    print(f"Porcentaje: {porcentaje:.2f}%")
    if porcentaje >= 80:
        print("¡Muy bien!")
    elif porcentaje >= 50:
        print("Nada mal, pero puedes mejorar.")
    else:
        print("Necesitas practicar más.")

# -------------------------------------------------
# Función: guardar_resultado
# -------------------------------------------------
def guardar_resultado(nombre, aciertos, total):
    resultado = {
        "nombre": nombre,
        "aciertos": aciertos,
        "total": total,
        "porcentaje": round((aciertos / total) * 100, 2)
    }
    ranking = []
    if os.path.exists(RANKING_FILE):
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            try:
                ranking = json.load(f)
            except json.JSONDecodeError:
                pass
    ranking.append(resultado)
    with open(RANKING_FILE, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=4)

# -------------------------------------------------
# Función: mostrar_ranking
# -------------------------------------------------
def mostrar_ranking():
    if not os.path.exists(RANKING_FILE):
        print("📂 No hay ranking disponible todavía.")
        return
    with open(RANKING_FILE, "r", encoding="utf-8") as f:
        ranking = json.load(f)
    if not ranking:
        print("📂 No hay resultados para mostrar.")
        return
    print("\n--- RANKING ---")
    ranking_ordenado = sorted(ranking, key=lambda x: x["porcentaje"], reverse=True)
    for i, r in enumerate(ranking_ordenado[:10], 1):
        print(f"{i}. {r['nombre']} - {r['aciertos']}/{r['total']} ({r['porcentaje']}%)")


# -------------------------------------------------
# Función: empezar_cuestionario
# -------------------------------------------------
def empezar_cuestionario():
    nombre = input("Introduce tu nombre: ").strip()
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
    preguntas = cargar_preguntas(nivel)
    if not preguntas:
        return
    aciertos = 0
    for p in preguntas:
        mostrar_pregunta(p)
        resp = obtener_respuesta()
        if corregir_respuesta(resp, p["respuesta_correcta"]):
            aciertos += 1
    mostrar_resultados(aciertos, len(preguntas))
    guardar_resultado(nombre, aciertos, len(preguntas))

# -------------------------------------------------
# Función: menu
# -------------------------------------------------
def menu():
    while True:
        print("\n### MENÚ ###")
        print("1 - Empezar cuestionario")
        print("2 - Ranking")
        print("3 - Salir")
        opcion = input("Elige una opción: ")
        if opcion == "1":
            empezar_cuestionario()
        elif opcion == "2":
            mostrar_ranking()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

# -------------------------------------------------
# Programa principal
# -------------------------------------------------
if __name__ == "__main__":
    menu()