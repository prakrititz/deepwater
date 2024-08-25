from ultralytics import YOLO
import os
import shutil

# Define class mappings
class_mapping = {
    0: 'fiber',
    1: 'film',
    2: 'fragment',
    3: 'pallet'
}

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
    model.predict(source=abs_image_path, save=True, save_dir=save_dir, save_txt=True)
    
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

    # Initialize counters
    total_microplastics = 0
    class_counts = {class_name: 0 for class_name in class_mapping.values()}

    # Find the YOLO format label file
    label_file = None
    for file in os.listdir(os.path.abspath('./static/predict/labels/')):
        if file.endswith('.txt') and file != 'classes.txt': # To be changed
            label_file = file
            break

    if label_file:
        with open(os.path.join(os.path.abspath('./static/predict/labels'),label_file), 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    class_id = int(parts[0])
                    if class_id in class_mapping:
                        total_microplastics += 1
                        class_name = class_mapping[class_id]
                        class_counts[class_name] += 1

    # Print results
    # result+=f"Total microplastics detected: {total_microplastics}\n"
    # result+=f"\nMicroplastics by class:\n"
    result = {}
    result['total_count'] = total_microplastics
    for class_name, count in class_counts.items():
        result[class_name] = count
    if result:
        return result