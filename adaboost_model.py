import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
import os
# Load the saved model
with open('model_ada.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the dataset
data = pd.read_csv(os.path.abspath('./dataset.csv'))

def get_user_input():
    ph = float(input("Enter pH value: "))
    hardness = float(input("Enter Hardness value: "))
    solids = float(input("Enter Solids value: "))
    chloramines = float(input("Enter Chloramines value: "))
    sulfate = float(input("Enter Sulfate value: "))
    conductivity = float(input("Enter Conductivity value: "))
    organic_carbon = float(input("Enter Organic Carbon value: "))
    trihalomethanes = float(input("Enter Trihalomethanes value: "))
    turbidity = float(input("Enter Turbidity value: "))
    
    # Return as a DataFrame for compatibility with the model
    user_data = pd.DataFrame({
        'ph': [ph],
        'Hardness': [hardness],
        'Solids': [solids],
        'Chloramines': [chloramines],
        'Sulfate': [sulfate],
        'Conductivity': [conductivity],
        'Organic_carbon': [organic_carbon],
        'Trihalomethanes': [trihalomethanes],
        'Turbidity': [turbidity]
    })
    
    return user_data

# Preprocessing - assuming StandardScaler was used during model training
scaler = StandardScaler()
scaler.fit(data.drop('Potability', axis=1))  # Fit on the dataset

def preprocess_data(user_data):
    scaled_data = scaler.transform(user_data)
    return scaled_data

def make_prediction(model, user_data):
    preprocessed_data = preprocess_data(user_data)
    prediction = model.predict(preprocessed_data)
    return prediction[0]

def main():
    print("Welcome to the Water Potability Prediction Tool")
    user_data = get_user_input()
    result = make_prediction(model, user_data)
    
    if result == 1:
        print("The water is potable.")
    else:
        print("The water is not potable.")

if __name__ == "__main__":
    main()
