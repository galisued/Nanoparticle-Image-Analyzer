import cv2
import numpy as np
import os

def analyze_single_image(image_path, pixel_to_nm_ratio, output_folder):
    """Processes one image, draws verification circles, and returns diameters."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0, []

    # --- THE TRICK: PRE-NORMALIZE THE IMAGE TO YOUR 0.439 GOLDEN STANDARD ---
    REFERENCE_RATIO = 0.439
    
    # If the uploaded image has a different ratio, this scales it to match your 0.439 standard
    # If you upload an image that is ALREADY 0.439, normalization_scale becomes 1.0 (no change)
    normalization_scale = pixel_to_nm_ratio / REFERENCE_RATIO 
    
    norm_width = int(img.shape[1] * normalization_scale)
    norm_height = int(img.shape[0] * normalization_scale)
    
    # This becomes the standardized image for the rest of the script
    img_normalized = cv2.resize(img, (norm_width, norm_height), interpolation=cv2.INTER_CUBIC)

    # ---------------------------------------------------------
    # FROM HERE DOWN, IT IS YOUR EXACT ORIGINAL UNTOUCHED LOGIC
    # ---------------------------------------------------------

    # Shrink to 25% for speed
    scale_factor = 0.25
    new_width = int(img_normalized.shape[1] * scale_factor)
    new_height = int(img_normalized.shape[0] * scale_factor)
    img_resized = cv2.resize(img_normalized, (new_width, new_height), interpolation=cv2.INTER_AREA)

    img_flattened = img_resized.copy()
    img_flattened[img_flattened < 80] = 80 
    img_blurred = cv2.GaussianBlur(img_flattened, (27, 27), 0)

    # Detect circles using your exact original parameters
    circles = cv2.HoughCircles(
        img_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=80,     
        param1=50, param2=22, minRadius=40, maxRadius=200    
    )

    verification_img = cv2.cvtColor(img_normalized, cv2.COLOR_GRAY2BGR)
    diameters = []
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            shrunk_x = circle[0]
            shrunk_y = circle[1]
            shrunk_radius_pixels = circle[2]
            
            true_x = int(shrunk_x / scale_factor)
            true_y = int(shrunk_y / scale_factor)
            
            true_radius_pixels = (shrunk_radius_pixels / scale_factor) * 1.025
            
            cv2.circle(verification_img, (true_x, true_y), int(true_radius_pixels), (0, 255, 0), 4)
            cv2.circle(verification_img, (true_x, true_y), 5, (0, 0, 255), -1)
            
            diameter_pixels = true_radius_pixels * 2
            
            # Calculate final physical size using your 0.439 REFERENCE_RATIO
            diameter_nm = diameter_pixels * REFERENCE_RATIO
            diameters.append(diameter_nm)

    base_file_name = os.path.basename(image_path)
    save_path = os.path.join(output_folder, f"Checked_{base_file_name}")
    cv2.imwrite(save_path, verification_img)
            
    return len(diameters), diameters