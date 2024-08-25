from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from model import predict_image as predict_microplastic  # Import your prediction 
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Load the AdaBoost model for water potability prediction
with open(os.path.abspath('./adaboost_model.pkl'), 'rb') as file:
    model = pickle.load(file)

# Load the dataset to fit the scaler
data = pd.read_csv(os.path.abspath('./water_potability.csv'))

# Initialize and fit the scaler
scaler = StandardScaler()
scaler.fit(data.drop('Potability', axis=1))

@app.route('/')
def home():
    if os.path.exists(os.path.abspath('./static/predict')):
        shutil.rmtree(os.path.abspath('./static/predict'))
    return render_template('index.html')

@app.route('/form') 
def show_form():  
    return render_template('form.html')  

@app.route('/analyze_microplastic', methods=['POST'])
def analyze():
    if os.path.exists(os.path.abspath('./static/predict')):
        shutil.rmtree(os.path.abspath('./static/predict'))
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        # Generate a unique filename
        filename = f"upload_{os.urandom(8).hex()}{os.path.splitext(file.filename)[1]}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Make prediction
        prediction = predict_microplastic(filepath)
        predicted_image_path = os.path.join("./static/predict", filename)
        # Clean up the uploaded file
        #os.remove(filepath)
        for file in os.listdir('./uploads'):
            os.remove(os.path.join(os.path.abspath('./uploads'),file))
        return jsonify({'total_count': prediction['total_count'],'image_path':predicted_image_path,'fiber': prediction['fiber'], 'pallet': prediction['pallet'], 'fragment': prediction['fragment'], 'film': prediction['film']})

@app.route('/check_potability', methods=['POST'])
def predict_potability():
    # Get user input from form
    ph = float(request.form['ph'])
    hardness = float(request.form['hardness'])
    solids = float(request.form['solids'])
    chloramines = float(request.form['chloramines'])
    sulfate = float(request.form['sulfate'])
    conductivity = float(request.form['conductivity'])
    organic_carbon = float(request.form['organic_carbon'])
    trihalomethanes = float(request.form['trihalomethanes'])
    turbidity = float(request.form['turbidity'])
    
    # Create a DataFrame for the input data
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
    
    # Preprocess the data
    preprocessed_data = scaler.transform(user_data)
    
    # Make prediction
    prediction = model.predict(preprocessed_data)
    
    # Determine the result
    result = "potable" if prediction[0] == 1 else "not potable"
    
    # Return the result as a JSON response
    return jsonify({'result': result})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
