import numpy as np 
import pandas as pd
from math import log2

# Generating example data for humidity, temperature, and weather prediction
# Here, 'Tiempo' is the target variable to predict based on 'Humedad' and 'Temperatura'
data = pd.DataFrame({
    'Humedad': [ 'Baja', 'Baja', 'Alta', 'Alta', 'Alta'],
    'Temperatura': ['Templado', 'Caluroso', 'Caluroso', 'Templado', 'Frio'],
    'Tiempo': ['Soleado',  'Soleado', 'Soleado','Lluvia', 'Lluvia']})

# Calculating entropy
def entropy(target_col):
    elements, counts = np.unique(target_col, return_counts=True)
    entropy_value = -sum((counts[i]/np.sum(counts)) * log2(counts[i]/np.sum(counts)) for i in range(len(elements)))
    return entropy_value

# Calculating Information Gain
def info_gain(data, split_attribute_name, target_name="Tiempo"):
    total_entropy = entropy(data[target_name])
    vals, counts = np.unique(data[split_attribute_name], return_counts=True)
    weighted_entropy = sum((counts[i]/np.sum(counts)) * entropy(data.where(data[split_attribute_name]==vals[i]).dropna()[target_name]) 
for i in range(len(vals)))
    information_gain = total_entropy - weighted_entropy
    return information_gain

# Implementing the ID3 algorithm
def id3(data, original_data, features, target_attribute_name="Tiempo", parent_node_class=None):
    # Base cases
    if len(np.unique(data[target_attribute_name])) <= 1:
        return np.unique(data[target_attribute_name])[0]
    elif len(data) == 0:
        return np.unique(original_data[target_attribute_name])[np.argmax(np.unique(original_data[target_attribute_name], return_counts=True)[1])]
    elif len(features) == 0:
        return parent_node_class
    else:
        parent_node_class = np.unique(data[target_attribute_name])[np.argmax(np.unique(data[target_attribute_name], return_counts=True)[1])]
        item_values = [info_gain(data, feature, target_attribute_name) for feature in features]
        best_feature_index = np.argmax(item_values)
        best_feature = features[best_feature_index]
        
        tree = {best_feature: {}}
        features = [i for i in features if i != best_feature]
        
        for value in np.unique(data[best_feature]):
            sub_data = data.where(data[best_feature] == value).dropna()
            subtree = id3(sub_data, original_data, features, target_attribute_name, parent_node_class)
            tree[best_feature][value] = subtree
            
        return tree

# Applying ID3 on the example data
features = data.columns[:-1]  # All columns except target
tree = id3(data, data, features)

tree

# Función para hacer una predicción basada en el árbol de decisión y la entrada del usuario
def predict(tree, input_data):
    # Comienza en la raíz del árbol
    for attribute, branches in tree.items():
        value = input_data.get(attribute)
        if value in branches:
            result = branches[value]
            # Si el resultado es todavía un diccionario, continuar la navegación
            if isinstance(result, dict):
                return predict(result, input_data)
            else:
                return result
        else:
            return "Valor no encontrado en el árbol de decisión"

# Ejemplo de interacción con la entrada del usuario
print("Por favor ingrese los siguientes valores para hacer una predicción sobre el Tiempo.")
humedad = input("Humedad (Alta/Baja): ").capitalize()
temperatura = input("Temperatura (Caluroso/Frio/Templado): ").capitalize()

# Construir el diccionario de datos de entrada para la predicción
input_data = {'Humedad': humedad, 'Temperatura': temperatura}
prediction = predict(tree, input_data)

print("\nPredicción del Tiempo:", prediction)

