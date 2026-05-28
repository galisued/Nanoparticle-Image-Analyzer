import os
import numpy as np

# Import your functions from the other two files
from data_input import collect_sample_data
from vision_engine import analyze_single_image

def sanitize_folder_name(name):
    """Convert synthesis time labels into safe folder names."""
    safe_name = "".join(
        c if (c.isalnum() or c in (' ', '_', '-')) else '_'
        for c in name
    )
    return safe_name.strip().replace(' ', '_') or 'timepoint'


def process_sample_batch(sample_dictionary):
    """Iterates through all timepoints in a sample and calculates statistics."""
    sample_name = sample_dictionary["sample_name"]
    pixel_ratio = sample_dictionary["pixel_ratio"]
    timepoints = sample_dictionary.get("timepoints", [])

    all_stats = []
    for timepoint in timepoints:
        synthesis_time = timepoint["synthesis_time"]
        image_paths = timepoint["image_paths"]

        print(f"\nProcessing {len(image_paths)} images for {sample_name} at '{synthesis_time}'...")

        sample_output_folder = os.path.join(
            "Verification_Output",
            sample_name,
            sanitize_folder_name(synthesis_time)
        )
        os.makedirs(sample_output_folder, exist_ok=True)

        all_diameters = []
        total_particles = 0

        for path in image_paths:
            file_name = path.split("/")[-1]
            count, diameters = analyze_single_image(path, pixel_ratio, sample_output_folder)
            all_diameters.extend(diameters)
            total_particles += count
            print(f"  - {file_name}: {count} particles detected.")

        if total_particles > 0:
            avg_diameter = sum(all_diameters) / total_particles
            std_dev = np.std(all_diameters, ddof=1) if total_particles > 1 else 0.0
        else:
            avg_diameter = 0
            std_dev = 0

        all_stats.append({
            "sample_name": sample_name,
            "synthesis_time": synthesis_time,
            "total_particles": total_particles,
            "average_diameter_nm": avg_diameter,
            "standard_deviation_nm": std_dev
        })

    return all_stats

if __name__ == "__main__":
    print("Starting Nanoparticle Image Analyzer...")
    
    raw_dataset = collect_sample_data()
    
    print("\n" + "="*40)
    print("--- Analysis Phase ---")
    
    final_statistics = []
    for sample in raw_dataset:
        stats = process_sample_batch(sample)
        final_statistics.extend(stats)

    print("\n" + "="*40)
    print("--- Final Results Summary ---")
    for stat in final_statistics:
        name = stat['sample_name']
        timepoint = stat['synthesis_time']
        count = stat['total_particles']
        if count > 0:
            avg = stat['average_diameter_nm']
            std = stat['standard_deviation_nm']
            print(f"[{name} | {timepoint}] {count} particles -> {avg:.2f} ± {std:.2f} nm")
        else:
            print(f"[{name} | {timepoint}] 0 particles detected.")

    print("\nDone! Check the 'Verification_Output' folder to see the drawn circles.")
    print("========================================\n")