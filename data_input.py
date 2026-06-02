import tkinter as tk
from tkinter import filedialog

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
    """Loops to ask the user for sample info and multiple synthesis-time image batches."""
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

        timepoints = []
        while True:
            print("\n--- Add Synthesis Time for this Sample ---")
            synthesis_time = input("Enter synthesis time (e.g., '24 hours', '3 days'): ")

            print(f"\nOpening file dialog for synthesis time '{synthesis_time}'...")
            image_paths = get_image_files()

            if image_paths:
                print(f"Successfully linked {len(image_paths)} images for '{synthesis_time}'.")
            else:
                print("Warning: No images selected for this synthesis time.")

            timepoints.append({
                "synthesis_time": synthesis_time,
                "image_paths": image_paths
            })

            another_time = input("\nAdd another synthesis time for this sample? (y/n): ").strip().lower()
            if another_time != 'y':
                break

        sample_dictionary = {
            "sample_name": sample_name,
            "pixel_ratio": pixel_ratio,
            "timepoints": timepoints
        }

        master_dataset.append(sample_dictionary)

        another = input("\nAdd another sample? (y/n): ").strip().lower()
        if another != 'y':
            break

    return master_dataset