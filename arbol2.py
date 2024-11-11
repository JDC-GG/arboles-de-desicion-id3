# Árbol de decisión basado en la estructura del diagrama
decision_tree = {
    'Temperatura': {
        'Frio': 'Lluvioso',
        'Caluroso': 'Soleado',
        'Templado': {
            'Humedad': {
                'Baja': 'Soleado',
                'Alta': 'Lluvioso'
            }
        }
    }
}

# Función para hacer una predicción con el árbol de decisión
def predict(tree, input_data):
    attribute = 'Temperatura'
    if attribute in tree:
        temp_value = input_data.get(attribute)
        result = tree[attribute].get(temp_value, None)
        
        # Si el resultado es otro diccionario, navegar más a fondo
        if isinstance(result, dict):
            humidity_value = input_data.get('Humedad')
            return result['Humedad'].get(humidity_value, "Valor no encontrado en el árbol")
        
        return result
    return "Valor no encontrado en el árbol de decisión"

# Interacción de ejemplo con la entrada del usuario
print("Por favor ingrese los siguientes valores para hacer una predicción sobre el Tiempo.")
humedad = input("Humedad (Alta/Baja): ").capitalize()
temperatura = input("Temperatura (Frio/Caluroso/Templado): ").capitalize()

# Construcción de los datos de entrada para la predicción
input_data = {'Humedad': humedad, 'Temperatura': temperatura}
prediction = predict(decision_tree, input_data)

print("\nPredicción del Tiempo:", prediction)
