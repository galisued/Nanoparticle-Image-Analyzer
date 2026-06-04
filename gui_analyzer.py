import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import csv
from PIL import Image, ImageTk

# Import your core analysis functions from main.py
from main import process_sample_batch, plot_diameter_and_volume, generate_report

class ResultsWindow(tk.Toplevel):
    """A new window that displays the CSV results and the plots."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Analysis Results")
        self.geometry("900x700")
        
        # Create a notebook (tabs) for organizing the results
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # --- Tab 1: CSV Data Table ---
        tab_data = ttk.Frame(notebook)
        notebook.add(tab_data, text="Summary Data")
        self.setup_data_table(tab_data)
        
        # --- Tab 2: Kinetics Plots ---
        tab_plots = ttk.Frame(notebook)
        notebook.add(tab_plots, text="Kinetics Plots")
        self.setup_plots(tab_plots)

    def setup_data_table(self, parent):
        """Reads the CSV and displays it in a Treeview table."""
        columns = ('sample_name', 'synthesis_time', 'total_particles', 'average_diameter_nm', 'standard_deviation_nm')
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        
        # Define the column headings
        tree.heading('sample_name', text='Sample Name')
        tree.heading('synthesis_time', text='Synthesis Time')
        tree.heading('total_particles', text='Particles')
        tree.heading('average_diameter_nm', text='Avg Diameter (nm)')
        tree.heading('standard_deviation_nm', text='Std Dev (nm)')
        
        tree.pack(fill='both', expand=True)
        
        # Read the generated CSV
        csv_path = os.path.join('Verification_Output', 'results_summary.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tree.insert('', tk.END, values=(
                        row.get('sample_name', ''),
                        row.get('synthesis_time', ''),
                        row.get('total_particles', ''),
                        row.get('average_diameter_nm', ''),
                        row.get('standard_deviation_nm', '')
                    ))
        else:
            messagebox.showwarning("Missing File", f"Could not find {csv_path}")

    def setup_plots(self, parent):
        """Loads and displays the generated PNG plots in a scrollable frame."""
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.photo_images = [] # Prevent garbage collection of images
        plot_names = ['diameter_vs_time.png', 'volume_vs_time.png']
        
        for plot_name in plot_names:
            plot_path = os.path.join('Verification_Output', plot_name)
            if os.path.exists(plot_path):
                img = Image.open(plot_path)
                img.thumbnail((800, 600)) # Resize to fit comfortably
                photo = ImageTk.PhotoImage(img)
                self.photo_images.append(photo)
                
                lbl = ttk.Label(scrollable_frame, image=photo)
                lbl.pack(pady=10)
                
                title_lbl = ttk.Label(scrollable_frame, text=plot_name, font=("Arial", 12, "bold"))
                title_lbl.pack()


class AnalyzerApp(tk.Tk):
    """The main input GUI replacing the CLI data collection."""
    def __init__(self):
        super().__init__()
        self.title("DMSN Analyzer - Data Setup")
        self.geometry("600x500")
        
        self.master_dataset = []
        self.current_timepoints = []
        
        self.setup_ui()

    def setup_ui(self):
        # --- Sample Entry Frame ---
        frame_sample = ttk.LabelFrame(self, text="1. Sample Information", padding=10)
        frame_sample.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame_sample, text="Sample Name:").grid(row=0, column=0, sticky="w")
        self.entry_sample_name = ttk.Entry(frame_sample, width=30)
        self.entry_sample_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_sample, text="Pixel Ratio (nm/px):").grid(row=1, column=0, sticky="w")
        self.entry_pixel_ratio = ttk.Entry(frame_sample, width=30)
        self.entry_pixel_ratio.insert(0, "1.4")
        self.entry_pixel_ratio.grid(row=1, column=1, padx=5, pady=5)
        
        # --- Timepoint Entry Frame ---
        frame_time = ttk.LabelFrame(self, text="2. Add Timepoints for Current Sample", padding=10)
        frame_time.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame_time, text="Synthesis Time (e.g. '24 hours'):").grid(row=0, column=0, sticky="w")
        self.entry_synth_time = ttk.Entry(frame_time, width=20)
        self.entry_synth_time.grid(row=0, column=1, padx=5, pady=5)
        
        self.btn_select_imgs = ttk.Button(frame_time, text="Select TEM Images", command=self.select_images)
        self.btn_select_imgs.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.lbl_img_count = ttk.Label(frame_time, text="0 images selected")
        self.lbl_img_count.grid(row=2, column=0, columnspan=2)
        
        self.btn_add_timepoint = ttk.Button(frame_time, text="Add Timepoint", command=self.add_timepoint)
        self.btn_add_timepoint.grid(row=3, column=0, columnspan=2, pady=10)
        
        # --- Dataset Overview Frame ---
        frame_dataset = ttk.LabelFrame(self, text="3. Dataset Overview", padding=10)
        frame_dataset.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.list_dataset = tk.Listbox(frame_dataset, height=5)
        self.list_dataset.pack(fill="both", expand=True)
        
        self.btn_save_sample = ttk.Button(frame_dataset, text="Save Sample to Dataset", command=self.save_sample)
        self.btn_save_sample.pack(pady=5)
        
        # --- Run Frame ---
        frame_run = ttk.Frame(self, padding=10)
        frame_run.pack(fill="x")
        
        self.btn_run = ttk.Button(frame_run, text="Run Analysis", command=self.run_analysis)
        self.btn_run.pack(fill="x")
        
        self.temp_image_paths = []

    def select_images(self):
        paths = filedialog.askopenfilenames(
            title="Select TEM Images",
            filetypes=[("Image files", "*.tif *.tiff *.jpg *.jpeg *.png")]
        )
        self.temp_image_paths = list(paths)
        self.lbl_img_count.config(text=f"{len(self.temp_image_paths)} images selected")

    def add_timepoint(self):
        synth_time = self.entry_synth_time.get()
        if not synth_time or not self.temp_image_paths:
            messagebox.showerror("Error", "Please provide a synthesis time and select images.")
            return
            
        self.current_timepoints.append({
            "synthesis_time": synth_time,
            "image_paths": self.temp_image_paths
        })
        
        messagebox.showinfo("Success", f"Added timepoint '{synth_time}' with {len(self.temp_image_paths)} images.")
        
        # Reset for next timepoint
        self.entry_synth_time.delete(0, tk.END)
        self.temp_image_paths = []
        self.lbl_img_count.config(text="0 images selected")

    def save_sample(self):
        sample_name = self.entry_sample_name.get()
        if not sample_name or not self.current_timepoints:
            messagebox.showerror("Error", "Please provide a sample name and add at least one timepoint.")
            return
            
        try:
            pixel_ratio = float(self.entry_pixel_ratio.get())
        except ValueError:
            messagebox.showerror("Error", "Pixel ratio must be a valid number.")
            return
            
        self.master_dataset.append({
            "sample_name": sample_name,
            "pixel_ratio": pixel_ratio,
            "timepoints": self.current_timepoints
        })
        
        self.list_dataset.insert(tk.END, f"{sample_name} ({len(self.current_timepoints)} timepoints)")
        
        # Reset for next sample
        self.entry_sample_name.delete(0, tk.END)
        self.current_timepoints = []

    def run_analysis(self):
        if not self.master_dataset:
            messagebox.showerror("Error", "The dataset is empty. Please save at least one sample.")
            return
            
        print("Starting analysis from GUI...")
        self.btn_run.config(text="Processing... Please wait", state="disabled")
        self.update()
        
        final_statistics = []
        for sample in self.master_dataset:
            stats = process_sample_batch(sample)
            final_statistics.extend(stats)
            
        if final_statistics:
            plot_diameter_and_volume(final_statistics)
            generate_report(final_statistics)
            
            # Open the new results window
            ResultsWindow(self)
            
        self.btn_run.config(text="Run Analysis", state="normal")

if __name__ == "__main__":
    app = AnalyzerApp()
    app.mainloop()