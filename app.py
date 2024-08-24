from flask import Flask, render_template, request, jsonify
import os
from model import predict_image as predict_microplastic  # Import your prediction function

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form') 
def show_form():     
    return render_template('form.html')  

@app.route('/analyze', methods=['POST'])
def analyze():
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
        os.remove(filepath)
        return jsonify({'prediction': prediction,'image_path':predicted_image_path})


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
