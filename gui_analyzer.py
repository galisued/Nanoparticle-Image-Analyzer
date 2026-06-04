import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import csv
from PIL import Image, ImageTk

# Import your core analysis functions from main.py
from main import process_sample_batch, plot_diameter_and_volume, generate_report

class ResultsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Analysis Results")
        self.geometry("950x750")
        self.configure(bg="#f8fafc")
        
        self.setup_styles()
        
        header = tk.Label(self, text="Analysis Results Dashboard", font=('Segoe UI', 18, 'bold'), bg="#f8fafc", fg="#0f172a")
        header.pack(pady=(15, 10))
        
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        tab_data = ttk.Frame(notebook)
        notebook.add(tab_data, text="  Summary Data  ")
        self.setup_data_table(tab_data)
        
        tab_plots = ttk.Frame(notebook)
        notebook.add(tab_plots, text="  Kinetics Plots  ")
        self.setup_plots(tab_plots)

    def setup_styles(self):
        style = ttk.Style(self)
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=30, background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'), background="#f1f5f9", foreground="#0f172a")
        style.map("Treeview", background=[('selected', '#3b82f6')])

    def setup_data_table(self, parent):
        columns = ('sample_name', 'synthesis_time', 'total_particles', 'average_diameter_nm', 'standard_deviation_nm')
        
        tree_scroll = ttk.Scrollbar(parent)
        tree_scroll.pack(side="right", fill="y")
        
        tree = ttk.Treeview(parent, columns=columns, show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)
        
        tree.heading('sample_name', text='Sample Name')
        tree.heading('synthesis_time', text='Synthesis Time')
        tree.heading('total_particles', text='Particles Count')
        tree.heading('average_diameter_nm', text='Avg Diameter (nm)')
        tree.heading('standard_deviation_nm', text='Std Dev (nm)')
        
        tree.column('sample_name', width=150, anchor='center')
        tree.column('synthesis_time', width=150, anchor='center')
        tree.column('total_particles', width=100, anchor='center')
        tree.column('average_diameter_nm', width=150, anchor='center')
        tree.column('standard_deviation_nm', width=150, anchor='center')
        
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        csv_path = os.path.join('Verification_Output', 'results_summary.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for count, row in enumerate(reader):
                    tag = 'evenrow' if count % 2 == 0 else 'oddrow'
                    tree.insert('', tk.END, values=(
                        row.get('sample_name', ''),
                        row.get('synthesis_time', ''),
                        row.get('total_particles', ''),
                        row.get('average_diameter_nm', ''),
                        row.get('standard_deviation_nm', '')
                    ), tags=(tag,))
            tree.tag_configure('evenrow', background='#f8fafc')
            tree.tag_configure('oddrow', background='#ffffff')
        else:
            messagebox.showwarning("Missing File", f"Could not find {csv_path}")

    def setup_plots(self, parent):
        canvas = tk.Canvas(parent, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.photo_images = [] 
        plot_names = ['diameter_vs_time.png', 'volume_vs_time.png']
        
        for plot_name in plot_names:
            plot_path = os.path.join('Verification_Output', plot_name)
            if os.path.exists(plot_path):
                img = Image.open(plot_path)
                img.thumbnail((800, 600), Image.Resampling.LANCZOS) 
                photo = ImageTk.PhotoImage(img)
                self.photo_images.append(photo)
                
                title_lbl = tk.Label(scrollable_frame, text=plot_name.replace('_', ' ').replace('.png', '').title(), font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#334155")
                title_lbl.pack(pady=(20, 5))
                
                lbl = tk.Label(scrollable_frame, image=photo, bg="#ffffff")
                lbl.pack(pady=(0, 20))


class AnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DMSN Analyzer - Data Setup")
        self.geometry("800x750") # Slightly wider to accommodate columns comfortably
        self.configure(bg="#f8fafc")
        
        self.master_dataset = []
        
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style(self)
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        app_font = ('Segoe UI', 10)
        style.configure('.', font=app_font, background="#f8fafc", foreground="#334155")
        
        style.configure('TLabelframe', background="#ffffff", bordercolor="#e2e8f0", borderwidth=1)
        style.configure('TLabelframe.Label', font=('Segoe UI', 11, 'bold'), background="#ffffff", foreground="#2563eb", padding=(5, 0))
        
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'), background="#3b82f6", foreground="white", borderwidth=0, padding=6)
        style.map('Primary.TButton', background=[('active', '#2563eb')])
        
        style.configure('Success.TButton', font=('Segoe UI', 12, 'bold'), background="#10b981", foreground="white", borderwidth=0, padding=10)
        style.map('Success.TButton', background=[('active', '#059669')])
        
        style.configure('Secondary.TButton', font=('Segoe UI', 10), background="#f1f5f9", foreground="#475569", borderwidth=0, padding=6)
        style.map('Secondary.TButton', background=[('active', '#e2e8f0')])
        
        style.configure('TEntry', padding=6, fieldbackground="#ffffff", bordercolor="#cbd5e1")
        style.configure('TCombobox', padding=6)

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self, bg="#f8fafc")
        header_frame.pack(fill="x", pady=(15, 5))
        tk.Label(header_frame, text="DMSN Growth Kinetics Analyzer", font=('Segoe UI', 18, 'bold'), bg="#f8fafc", fg="#0f172a").pack()

        # Canvas and scrollbar setup for the main window
        canvas_bg = tk.Canvas(self, bg="#f8fafc", highlightthickness=0)
        main_scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas_bg.yview)
        
        self.main_container = ttk.Frame(canvas_bg, padding=20)
        self.main_container.bind("<Configure>", lambda e: canvas_bg.configure(scrollregion=canvas_bg.bbox("all")))
        
        canvas_bg.create_window((0, 0), window=self.main_container, anchor="nw", width=760)
        canvas_bg.configure(yscrollcommand=main_scrollbar.set)
        
        canvas_bg.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")

        # 1. Sample Information
        frame_sample = ttk.LabelFrame(self.main_container, text=" 1. Sample Configuration ", padding=20)
        frame_sample.pack(fill="x", pady=(0, 20))
        
        ttk.Label(frame_sample, text="Sample Name:", background="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_sample_name = ttk.Entry(frame_sample, width=40)
        self.entry_sample_name.grid(row=0, column=1, padx=15, pady=5)
        
        ttk.Label(frame_sample, text="Calibration (nm/px):", background="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_pixel_ratio = ttk.Entry(frame_sample, width=40)
        self.entry_pixel_ratio.insert(0, "0.439") 
        self.entry_pixel_ratio.grid(row=1, column=1, padx=15, pady=5)
        
        # 2. Dynamic Timepoints Rubric
        self.frame_time = ttk.LabelFrame(self.main_container, text=" 2. Synthesis Timepoints ", padding=20)
        self.frame_time.pack(fill="x", pady=(0, 20))
        
        # Header row for the dynamic columns
        headers = tk.Frame(self.frame_time, bg="#ffffff")
        headers.pack(fill="x", pady=(0, 10))
        tk.Label(headers, text="Duration", bg="#ffffff", fg="#64748b", font=('Segoe UI', 9, 'bold'), width=12, anchor="w").pack(side="left")
        tk.Label(headers, text="Unit", bg="#ffffff", fg="#64748b", font=('Segoe UI', 9, 'bold'), width=12, anchor="w").pack(side="left", padx=(10, 0))
        tk.Label(headers, text="Images", bg="#ffffff", fg="#64748b", font=('Segoe UI', 9, 'bold'), anchor="w").pack(side="left", padx=(25, 0))

        # Container for the rows
        self.rows_container = tk.Frame(self.frame_time, bg="#ffffff")
        self.rows_container.pack(fill="x")
        
        self.timepoint_rows = [] 
        self.add_timepoint_row() 
        
        # Add Another Row Button
        self.btn_add_row = ttk.Button(self.frame_time, text="+ Add Another Timepoint", style='Secondary.TButton', command=self.add_timepoint_row)
        self.btn_add_row.pack(anchor="w", pady=(15, 0))
        
        # 3. Dataset Overview
        frame_dataset = ttk.LabelFrame(self.main_container, text=" 3. Current Dataset Queue ", padding=20)
        frame_dataset.pack(fill="both", expand=True, pady=(0, 20))
        
        self.list_dataset = tk.Listbox(frame_dataset, height=4, font=('Segoe UI', 10), bg="#f8fafc", fg="#334155", relief="flat", highlightthickness=1, highlightcolor="#cbd5e1")
        self.list_dataset.pack(fill="both", expand=True, pady=(0, 15))
        
        self.btn_save_sample = ttk.Button(frame_dataset, text="Add Sample", style='Primary.TButton', command=self.save_sample)
        self.btn_save_sample.pack(anchor="e")
        
        # Run Button
        self.btn_run = ttk.Button(self.main_container, text="Start Analysis Processing", style='Success.TButton', command=self.run_analysis)
        self.btn_run.pack(fill="x", pady=(5, 10))

    def add_timepoint_row(self):
        """Creates a neatly gridded row of inputs for a timepoint in the rubric."""
        row_frame = tk.Frame(self.rows_container, bg="#ffffff")
        row_frame.pack(fill="x", pady=6)
        
        # Setup grid columns for perfect alignment
        row_frame.columnconfigure(0, minsize=90)  # Duration entry
        row_frame.columnconfigure(1, minsize=100) # Unit combo
        row_frame.columnconfigure(2, minsize=120) # Browse button
        row_frame.columnconfigure(3, minsize=120) # Text Label
        row_frame.columnconfigure(4, weight=1)    # Spacer
        row_frame.columnconfigure(5, minsize=40)  # Delete icon
        
        row_data = {
            'frame': row_frame,
            'image_paths': []
        }
        
        # Duration Entry
        val_entry = ttk.Entry(row_frame, width=12)
        val_entry.grid(row=0, column=0, sticky="w")
        row_data['val_entry'] = val_entry
        
        # Unit Combo
        unit_combo = ttk.Combobox(row_frame, values=["Hours", "Days"], width=10, state="readonly")
        unit_combo.current(0)
        unit_combo.grid(row=0, column=1, padx=(10, 0), sticky="w")
        row_data['unit_combo'] = unit_combo
        
        # Images queued label
        lbl_count = tk.Label(row_frame, text="0 images linked", font=('Segoe UI', 9, 'italic'), bg="#ffffff", fg="#94a3b8", anchor="w")
        row_data['lbl_count'] = lbl_count
        
        # Image browse function specific to this row
        def browse_imgs():
            paths = filedialog.askopenfilenames(
                title="Select TEM Images",
                filetypes=[("Image files", "*.tif *.tiff *.jpg *.jpeg *.png")]
            )
            if paths:
                row_data['image_paths'] = list(paths)
                lbl_count.config(text=f"{len(paths)} images linked", fg="#10b981", font=('Segoe UI', 9, 'bold'))
                
        btn_browse = ttk.Button(row_frame, text="Browse...", style='Secondary.TButton', width=10, command=browse_imgs)
        btn_browse.grid(row=0, column=2, padx=(15, 0), sticky="w")
        
        lbl_count.grid(row=0, column=3, padx=(10, 0), sticky="w")
        
        # Delete Row 'Button' (Using a label to avoid macOS button styling issues)
        if len(self.timepoint_rows) > 0:
            def remove_this_row(event=None):
                row_frame.destroy()
                self.timepoint_rows.remove(row_data)
                
            lbl_remove = tk.Label(row_frame, text="✕", fg="#ef4444", bg="#ffffff", font=('Segoe UI', 14, 'bold'), cursor="hand2")
            lbl_remove.bind("<Button-1>", remove_this_row)
            lbl_remove.bind("<Enter>", lambda e: lbl_remove.config(fg="#b91c1c")) # Hover dark red
            lbl_remove.bind("<Leave>", lambda e: lbl_remove.config(fg="#ef4444")) # Leave light red
            lbl_remove.grid(row=0, column=5, sticky="e", padx=5)
            
        self.timepoint_rows.append(row_data)

    def save_sample(self):
        sample_name = self.entry_sample_name.get().strip()
        if not sample_name:
            messagebox.showerror("Missing Data", "Please define a sample name.")
            return
            
        try:
            pixel_ratio = float(self.entry_pixel_ratio.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Calibration ratio must be a numeric value.")
            return
            
        valid_timepoints = []
        
        for row in self.timepoint_rows:
            val_str = row['val_entry'].get().strip()
            paths = row['image_paths']
            
            if not val_str and not paths:
                continue
                
            if not val_str or not paths:
                messagebox.showerror("Incomplete Row", "Please ensure all filled timepoint rows have both a duration and selected images.")
                return
                
            try:
                float(val_str)
            except ValueError:
                messagebox.showerror("Invalid Input", f"Synthesis duration '{val_str}' must be a numeric value.")
                return
                
            unit = row['unit_combo'].get()
            valid_timepoints.append({
                "synthesis_time": f"{val_str} {unit}",
                "image_paths": paths
            })
            
        if not valid_timepoints:
            messagebox.showerror("Missing Data", "Please completely fill out at least one timepoint row.")
            return
            
        self.master_dataset.append({
            "sample_name": sample_name,
            "pixel_ratio": pixel_ratio,
            "timepoints": valid_timepoints
        })
        
        self.list_dataset.insert(tk.END, f"  📦 {sample_name}  |  {len(valid_timepoints)} timepoints  |  Ratio: {pixel_ratio}")
        
        self.entry_sample_name.delete(0, tk.END)
        for row in self.timepoint_rows:
            row['frame'].destroy()
        self.timepoint_rows.clear()
        self.add_timepoint_row()

    def run_analysis(self):
        if not self.master_dataset:
            messagebox.showerror("Empty Queue", "Your analysis queue is empty. Save a sample first.")
            return
            
        self.btn_run.config(text="Processing images... Please wait", state="disabled")
        self.update()
        
        final_statistics = []
        for sample in self.master_dataset:
            stats = process_sample_batch(sample)
            final_statistics.extend(stats)
            
        if final_statistics:
            plot_diameter_and_volume(final_statistics)
            generate_report(final_statistics)
            
            ResultsWindow(self)
            
        self.btn_run.config(text="Start Analysis Processing", state="normal")

if __name__ == "__main__":
    app = AnalyzerApp()
    app.mainloop()