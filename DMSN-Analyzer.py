import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

# ==========================================
# PART 1: DATA INPUT & GUI
# ==========================================

def get_image_files():
    """Opens a GUI file dialog to select multiple images."""
    root = tk.Tk()
    root.withdraw() 
    root.attributes('-topmost', True) 
    
    file_paths = filedialog.askopenfilenames(
        title="Select TEM Images for Current Sample",
        filetypes=[("Tiff files", "*.tif *.tiff"), ("JPEG files", "*.jpg *.jpeg"), ("PNG files", "*.png"), ("All files", "*.*")]
    )
    return list(file_paths)

def collect_sample_data():
    """Loops to ask the user for sample info and image files."""
    master_dataset = []
    
    while True:
        print("\n" + "="*40)
        print("--- New Sample Entry ---")
        
        sample_name = input("Enter Sample Name: ")
        
        try:
            pixel_ratio = float(input("Enter pixel-to-nanometer ratio (e.g., 0.439): "))
        except ValueError:
            print("Invalid number entered. Defaulting ratio to 1.0.")
            pixel_ratio = 1.0
            
        synthesis_time = input("Enter synthesis time (e.g., '24 hours', '3 days'): ")
        
        print(f"\nOpening file dialog for '{sample_name}'...")
        image_paths = get_image_files()
        
        if image_paths:
            print(f"Successfully linked {len(image_paths)} images.")
        else:
            print("Warning: No images selected.")
        
        sample_dictionary = {
            "sample_name": sample_name,
            "pixel_ratio": pixel_ratio,
            "synthesis_time": synthesis_time,
            "image_paths": image_paths
        }
        
        master_dataset.append(sample_dictionary)
        
        another = input("\nAdd another sample? (y/n): ").strip().lower()
        if another != 'y':
            break
            
    return master_dataset

# ==========================================
# PART 2: COMPUTER VISION & MEASUREMENT
# ==========================================

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

    # Blur to melt the internal pores together
    img_blurred = cv2.GaussianBlur(img_resized, (31, 31), 0)

    # Detect circles
    circles = cv2.HoughCircles(
        img_blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=150,     
        param1=40, param2=30, minRadius=80, maxRadius=400    
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
            true_radius_pixels = shrunk_radius_pixels / scale_factor 
            
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

def process_sample_batch(sample_dictionary):
    """Iterates through all images in a sample and calculates statistics."""
    sample_name = sample_dictionary["sample_name"]
    pixel_ratio = sample_dictionary["pixel_ratio"]
    image_paths = sample_dictionary["image_paths"]
    
    print(f"\nProcessing {len(image_paths)} images for {sample_name}...")
    
    # --- NEW: Create a dedicated folder for this sample's verification images ---
    sample_output_folder = f"Verification_Output/{sample_name}"
    os.makedirs(sample_output_folder, exist_ok=True)
    
    all_diameters = []
    total_particles = 0
    
    for path in image_paths:
        file_name = path.split("/")[-1]
        
        # Pass the output folder to the analyzer
        count, diameters = analyze_single_image(path, pixel_ratio, sample_output_folder)
        
        all_diameters.extend(diameters)
        total_particles += count
        print(f"  - {file_name}: {count} particles detected.")
        
    # Calculate final stats
    if total_particles > 0:
        avg_diameter = sum(all_diameters) / total_particles
        std_dev = np.std(all_diameters, ddof=1) if total_particles > 1 else 0.0
    else:
        avg_diameter = 0
        std_dev = 0
        
    return {
        "sample_name": sample_name,
        "total_particles": total_particles,
        "average_diameter_nm": avg_diameter,
        "standard_deviation_nm": std_dev
    }

# ==========================================
# PART 3: MAIN EXECUTION 
# ==========================================

if __name__ == "__main__":
    print("Starting Nanoparticle Image Analyzer...")
    
    raw_dataset = collect_sample_data()
    
    print("\n" + "="*40)
    print("--- Analysis Phase ---")
    
    final_statistics = []
    for sample in raw_dataset:
        stats = process_sample_batch(sample)
        final_statistics.append(stats)
        
    print("\n" + "="*40)
    print("--- Final Results Summary ---")
    for stat in final_statistics:
        name = stat['sample_name']
        count = stat['total_particles']
        if count > 0:
            avg = stat['average_diameter_nm']
            std = stat['standard_deviation_nm']
            print(f"[{name}] {count} particles -> {avg:.2f} ± {std:.2f} nm")
        else:
            print(f"[{name}] 0 particles detected.")
    
    print("\nDone! Check the 'Verification_Output' folder to see the drawn circles.")
    print("========================================\n")