import os
import numpy as np

# Import your functions from the other two files
from data_input import collect_sample_data
from vision_engine import analyze_single_image

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