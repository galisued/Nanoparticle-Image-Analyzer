import cv2
import numpy as np
import os

def analyze_single_image(image_path, pixel_to_nm_ratio, output_folder):
    """Processes one image, draws verification circles, and returns diameters."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0, []

    # Shrink to 25% for speed
    scale_factor = 0.25
    new_width = int(img.shape[1] * scale_factor)
    new_height = int(img.shape[0] * scale_factor)
    img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # --- NEW: Flatten the dark core to remove the false internal edge ---
    # We create a copy so we don't mess up the original image data
    img_flattened = img_resized.copy()
    
    # Any pixel darker than 80 is clamped to 80 (turning the black core gray).
    # You might need to tweak this number between 50 and 110 based on the specific image.
    img_flattened[img_flattened < 80] = 80
    
    # Now apply the blur to your NEW flattened image
    img_blurred = cv2.GaussianBlur(img_flattened, (27, 27), 0)

    # Detect circles
    circles = cv2.HoughCircles(
        img_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=140,
        param1=17, param2=22, minRadius=80, maxRadius=200
    )

    # --- NEW: Create a color copy of the original high-res image for drawing ---
    verification_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    diameters = []
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            # Extract coordinates from the shrunk image
            shrunk_x = circle[0]
            shrunk_y = circle[1]
            shrunk_radius_pixels = circle[2]
            
            # Scale coordinates back up to 100% for the original high-res image
            true_x = int(shrunk_x / scale_factor)
            true_y = int(shrunk_y / scale_factor)
            
            # --- UPDATED: Added a buffer to the radius ---
            true_radius_pixels = (shrunk_radius_pixels / scale_factor) * 1.02
            
            # --- NEW: Draw the verification circles ---
            # Outer ring in Green (B=0, G=255, R=0), thickness 4
            cv2.circle(verification_img, (true_x, true_y), int(true_radius_pixels), (0, 255, 0), 4)
            # Center dot in Red (B=0, G=0, R=255), thickness -1 (filled)
            cv2.circle(verification_img, (true_x, true_y), 5, (0, 0, 255), -1)
            
            diameter_pixels = true_radius_pixels * 2
            diameter_nm = diameter_pixels * pixel_to_nm_ratio
            diameters.append(diameter_nm)

    # --- NEW: Save the verification image ---
    base_file_name = os.path.basename(image_path) # Gets just 'image01.tiff'
    save_path = os.path.join(output_folder, f"Checked_{base_file_name}")
    cv2.imwrite(save_path, verification_img)
    
    return len(diameters), diameters 
