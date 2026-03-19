import cv2
import numpy as np
import matplotlib.pyplot as plt

# Image load
default_image_path = 'C:\\Users\\ejmp0\\iCloudDrive\\TEC\\ITC\\4to Semestre\\El arte de la progra\\Evidencia de proyecto\\m1.jpeg'
image_path = input(f"Enter image path (press Enter for default: {default_image_path}): ").strip()
if image_path == "":
    image_path = default_image_path

image = cv2.imread(image_path)
if image is None:
    print(f"Error: Could not load image from: {image_path}")
    exit()

# Copy image for drawing results
annotated_image = image.copy()

# Gray scale and blur
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (11, 11), 2)

# Edge detection
edges = cv2.Canny(gray, 100, 200)

# Circle detection
circles = cv2.HoughCircles(
    edges,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=100,
    param1=100,
    param2=32,
    minRadius=30,   
    maxRadius=200
)

total = 0

if circles is not None:
    # Round circle values to integers
    circles = np.round(circles[0, :]).astype("int")

    # Remove overlapping inner circles
    filtered_circles = []

    for (x, y, r) in circles:
        is_inner = False
        
        for (x2, y2, r2) in circles:
            distance = np.sqrt((x - x2)**2 + (y - y2)**2)
            
            if distance < 15 and r < r2:
                is_inner = True
                break
        
        if not is_inner:
            filtered_circles.append((x, y, r))

    # Radius ranges for denomination assignment
    radii = [r for (x, y, r) in filtered_circles]
    r_min = min(radii)
    r_max = max(radii)
    step = (r_max - r_min) / 4

    # Draw circles and assign values
    for (x, y, r) in filtered_circles:
        print("Final radius:", r)

        if r < r_min +step:
            value = 1
        elif r < r_min +2*step:
            value = 2
        elif r< r_min +3*step:
            value = 5
        else:
            value = 10

        total += value

        cv2.circle(annotated_image, (x, y), r, (0, 255, 0), 2)
        cv2.putText(annotated_image, f"{value}", (x - 20, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

cv2.putText(annotated_image, f"Total: ${total}", (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

# Display results
plt.figure(figsize=(10, 8))
plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title(f"Coin Detection - Total: ${total}")
plt.tight_layout()
plt.show()