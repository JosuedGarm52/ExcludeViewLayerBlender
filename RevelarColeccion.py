import bpy

# Nombre de la colección principal
folder_name = "ParedIzq"  # Cambia esto al nombre de tu carpeta en el Outliner

def get_layer_collection(collection, view_layer=None):
    '''Devuelve la LayerCollection correspondiente a una colección dentro del View Layer.'''
    if view_layer is None:
        view_layer = bpy.context.view_layer
    
    # Recursivamente busca la LayerCollection que corresponde a la colección dada
    def scan_children(layer_collection):
        if layer_collection.collection == collection:
            return layer_collection
        for child in layer_collection.children:
            result = scan_children(child)
            if result:
                return result
        return None

    # Inicia la búsqueda desde la capa principal
    return scan_children(view_layer.layer_collection)

def set_collection_visibility(collection, exclude_state):
    '''Activa o desactiva la visibilidad de una colección en el View Layer, incluyendo subcolecciones.'''
    layer_collection = get_layer_collection(collection)
    
    if layer_collection:
        # Cambiar visibilidad de la colección principal
        layer_collection.exclude = exclude_state  # Cambia el estado de "Exclude from View Layer"
        print(f"Visibilidad de la colección '{collection.name}' ha sido cambiada a {exclude_state}")

        # Cambiar visibilidad de todas las subcolecciones
        for subcollection in collection.children:
            set_collection_visibility(subcollection, exclude_state)
    else:
        print(f"No se encontró la LayerCollection para la colección '{collection.name}' en el View Layer.")

# Buscar la colección principal
collection = bpy.data.collections.get(folder_name)

if collection:
    # Ejecutar la función para cambiar la visibilidad de la colección y sus subcolecciones
    set_collection_visibility(collection, exclude_state=False)  # False para mostrarla, True para ocultarla
else:
    print(f"No se encontró ninguna carpeta con el nombre '{folder_name}' en las colecciones.")
