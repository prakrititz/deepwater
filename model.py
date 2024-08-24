from ultralytics import YOLO
import os
import shutil

def predict_image(image_path, save_dir='static'):
    # Get absolute paths
    abs_image_path = os.path.abspath(image_path)
    model_path = os.path.abspath("./weights/weights/best.pt")
    
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # # Load the model
    model = YOLO(model_path, task='detect')
    image_generated_path = "runs/detect/predict"
    # # Define the output path
    image_name = os.path.basename(image_path)
    # save_path = os.path.join(save_dir, image_name)
    
    # # If the file already exists, delete it to avoid duplicates
    # if os.path.exists(save_path):
    #     os.remove(save_path)
    
    # # Perform the prediction and save the result in the specified directory
    model.predict(source=abs_image_path, save=True, save_dir=save_dir, save_txt=False)
    
    # # Move the predicted image to the desired location (if necessary)
    # predicted_image_path = os.path.join(save_dir, 'predict', image_name)
    if os.path.exists(image_generated_path):
        to_move = os.path.join(image_generated_path, image_name)
        shutil.move(image_generated_path, save_dir)
    
    # # Remove the 'predict' folder if it was created
    # predict_folder = os.path.join(save_dir, 'predict')
    if os.path.exists("./runs"):
        shutil.rmtree("./runs")

    print(f"Predicted image saved at: {save_dir}")
