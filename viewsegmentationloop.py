import cv2
import numpy as np
from pathlib import Path

# Define absolute paths for the directories
#images_dir = r'C:\Users\Munazza Zulnoor\PycharmProjects\pythonProject5\Bell\images'
#labels_dir = r'C:\Users\Munazza Zulnoor\PycharmProjects\pythonProject5\Bell\labels'
#output_dir = r'C:\Users\Munazza Zulnoor\PycharmProjects\pythonProject5\Bellresult'
images_dir = r'C:\path\to\images\folder'  # Update this
labels_dir = r'C:\path\to\labels\folder'  # Update this
output_dir = r'C:\path\to\output\folder'  # Update this

print(f"Images directory: {images_dir}")
print(f"Labels directory: {labels_dir}")
print(f"Output directory: {output_dir}")
# Create the output directory if it doesn't exist
Path(output_dir).mkdir(parents=True, exist_ok=True)
print(f"Output directory set to: {output_dir}")

# Function to read label file and extract polygons with floating point coordinates
def read_label_file(label_file_path, img_width, img_height):
    polygons = []
    with open(label_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            class_id = int(parts[0])
            # Convert normalized coordinates to pixel values
            polygon = [int(float(coord) * img_width if i % 2 == 0 else float(coord) * img_height)
                       for i, coord in enumerate(parts[1:])]
            polygons.append((class_id, polygon))
    return polygons

# Function to draw polygons on an image
def draw_polygons_on_image(image, polygons):
    for class_id, polygon in polygons:
        points = np.array(polygon, np.int32).reshape((-1, 1, 2))
        cv2.polylines(image, [points], True, (0, 255, 0), 2)  # Green color for polygons
    return image

# Process each image and its corresponding label file
for image_path in Path(images_dir).glob('*.jpg'):  # Adjust the extension as needed
    print(f"Processing image: {image_path}")

    try:
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"Failed to read image: {image_path}")
            continue

        img_height, img_width = image.shape[:2]

        label_file_path = Path(labels_dir, image_path.stem + '.txt')
        if not label_file_path.exists():
            print(f"No corresponding label file found for {image_path.name}")
            continue

        polygons = read_label_file(str(label_file_path), img_width, img_height)
        image_with_polygons = draw_polygons_on_image(image.copy(), polygons)
        output_path = Path(output_dir, image_path.name)
        print(f"Saving image to: {output_path}")  # This will print the intended save path
        success = cv2.imwrite(str(output_path), image_with_polygons)
        if success:
            print(f"Successfully saved: {output_path}")
        else:
            print(f"Failed to save: {output_path}")
        output_path = Path(output_dir, image_path.name)
        cv2.imwrite(str(output_path), image_with_polygons)
        print(f"Saved: {output_path}")

    except Exception as e:
        print(f"Error processing {image_path.name}: {e}")

print("Processing complete.")