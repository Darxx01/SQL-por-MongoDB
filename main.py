from pymongo import MongoClient

def obtener_conexion():
    client = MongoClient('mongodb://localhost:/')
    return client.diccionario_db

def crear_colecciones():
    db = obtener_conexion()
    if "diccionario" not in db.list_collection_names():
        db.create_collection("diccionario")

def principal():
    crear_colecciones()
    menu = """
a) Agregar nueva palabra
b) Editar palabra existente
c) Eliminar palabra existente
d) Ver listado de palabras
e) Buscar significado de palabra
f) Salir
Elige: """
    eleccion = ""
    while eleccion != "f":
        eleccion = input(menu)
        if eleccion == "a":
            palabra = input("Ingresa la palabra: ")
            # Comprueba si no existe
            posible_significado = buscar_significado_palabra(palabra)
            if posible_significado:
                print(f"La palabra '{palabra}' ya existe")
            else:
                significado = input("Ingresa el significado: ")
                agregar_palabra(palabra, significado)
                print("Palabra agregada")
        elif eleccion == "b":
            palabra = input("Ingresa la palabra que quieres editar: ")
            nuevo_significado = input("Ingresa el nuevo significado: ")
            editar_palabra(palabra, nuevo_significado)
            print("Palabra actualizada")
        elif eleccion == "c":
            palabra = input("Ingresa la palabra a eliminar: ")
            eliminar_palabra(palabra)
        elif eleccion == "d":
            palabras = obtener_palabras()
            print("=== Lista de palabras ===")
            for palabra in palabras:
                print(palabra['palabra'])
        elif eleccion == "e":
            palabra = input(
                "Ingresa la palabra de la cual quieres saber el significado: ")
            significado = buscar_significado_palabra(palabra)
            if significado:
                print(f"El significado de '{palabra}' es:\n{significado['significado']}")
            else:
                print(f"Palabra '{palabra}' no encontrada")

def agregar_palabra(palabra, significado):
    db = obtener_conexion()
    db.diccionario.insert_one({'palabra': palabra, 'significado': significado})

def editar_palabra(palabra, nuevo_significado):
    db = obtener_conexion()
    db.diccionario.update_one(
        {'palabra': palabra},
        {'$set': {'significado': nuevo_significado}}
    )

def eliminar_palabra(palabra):
    db = obtener_conexion()
    db.diccionario.delete_one({'palabra': palabra})

def obtener_palabras():
    db = obtener_conexion()
    return list(db.diccionario.find({}, {'_id': 0, 'palabra': 1}))

def buscar_significado_palabra(palabra):
    db = obtener_conexion()
    resultado = db.diccionario.find_one({'palabra': palabra}, {'_id': 0, 'significado': 1})
    return resultado

if __name__ == '__main__':
    principal()
