from flask import Flask, render_template, request, jsonify
import os
from model import predict_image as predict_microplastic  # Import your prediction 
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    if os.path.exists(os.path.abspath('./static/predict')):
        shutil.rmtree(os.path.abspath('./static/predict'))
    return render_template('index.html')

@app.route('/form') 
def show_form():  
    return render_template('form.html')  

@app.route('/analyze', methods=['POST'])
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


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)