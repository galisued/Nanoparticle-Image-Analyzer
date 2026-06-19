# DMSN-Analyzer: Automated TEM Image Processing for Nanoparticle Growth Kinetics

An automated image processing pipeline written in Python to extract morphological data from Transmission Electron Microscopy (TEM) images of Dendritic Mesoporous Silica Nanoparticles (DMSNs). This tool accelerates nanomaterials research by replacing manual particle sizing with automated segmentation, tracking nanoparticle diameter and volume evolution over synthesis time.

---

## 1. What does this project do?

Dendritic Mesoporous Silica Nanoparticles (DMSNs) are advanced nanomaterials characterized by their unique center-radial, hierarchical pore structures and high surface areas. Because of their unique morphology, they are highly valuable for applications like drug delivery, catalysis, and sensing. However, characterizing their growth kinetics requires researchers to manually measure hundreds of particle diameters across multiple Transmission Electron Microscopy (TEM) images. This process is incredibly time-consuming and prone to human bias.

**DMSN-Analyzer** automates this workflow. It performs the following tasks:
* **Image Preprocessing & Noise Reduction:** Cleans TEM images to handle low contrast, varying brightness, and background variations typical in electron microscopy.
* **Particle Detection & Segmentation:** Utilizes computer vision algorithms to isolate individual dendritic nanoparticles, even when minor overlapping occurs.
* **Morphological Measurement:** Calibrates pixel sizes to physical nanometer scales, extracting the exact boundary, diameter, and calculated volume of each detected particle.
* **Kinetic Analysis:** Aggregates statistical data across different sample batches and plots the growth kinetics to map synthesis progression over time.

---

## 2. Input and Output Data

### Expected Inputs
1. **TEM Images:** A directory containing standard image files (`.png`, `.jpg`, or `.tiff`) captured via Transmission Electron Microscopy.
2. **Image Calibration:** A user-defined calibration factor (pixel-to-nanometer ratio) to ensure physical accuracy.
2. **Synthesis Time:** A specific synthesis duration (in hours or days) for each image batch.

### Expected Outputs
For every processed image directory, the application generates:
* **Statistical Summary:** The exact number of successfully detected particles, their average diameter, and the standard deviation.
* **Annotated Verification Images:** Visual validation outputs highlighting detected particle boundaries so the user can verify segmentation quality.
* **Kinetic Plots:** High-resolution graphs illustrating:
   * Average Particle Diameter vs. Synthesis Time
   * Estimated Particle Volume vs. Synthesis Time
* **Data Export:** A structured CSV or Excel file containing all raw measurements and summary statistics for downstream academic reporting.

---

## 3. Project Structure

The repository is organized into distinct modules to separate the user interface, data handling, and core analysis:

* **`gui_analyzer.py`**: The graphical user interface (GUI) that allows users to easily input sample names, calibration ratios, and browse for TEM images.
* **`data_input.py`**: Handles the data ingestion pipeline. It collects user inputs and maps the selected image file paths to their respective synthesis times.
* **`vision_engine.py`**: The core computer vision module. It normalizes image scales, applies OpenCV algorithms (like `HoughCircles`) to detect the nanoparticles, and calculates their physical dimensions.
* **`main.py`**: The primary orchestration script that links the data input collection with the vision processing engine.
* **`test_main.py` & `test_vision_engine.py`**: Unit tests designed to verify the mathematical accuracy of the vision engine and ensure the overall logic runs without errors.

---

## 4. Technicalities

### Prerequisites & Installation
This project requires Python 3.8+. To clone the repository and install the necessary dependencies, run the following commands in your terminal:

```bash
# Clone the repository
git clone [https://github.com/galisued/Nanoparticle-Image-Analyzer.git](https://github.com/galisued/Nanoparticle-Image-Analyzer.git)
cd Nanoparticle-Image-Analyzer

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```
---

## 5. Usage (How to Run the Code)

### Step 1: Launch the Application
Open your terminal, ensure your virtual environment is activated, and run the GUI script:
```bash
python gui_analyzer.py
```

### Step 2: Configure Your Sample
In the **1. Sample Configuration** section of the GUI:
* **Sample Name:** Enter the identifier for your synthesis batch (e.g., "sample1").
* **Calibration (nm/px):** Set your pixel-to-nanometer scale. This defaults to the standard manual calibration of `0.439`, but can be manually adjusted if needed (for the images in the folder the defult ratio is the right one).

### Step 3: Add Synthesis Timepoints and Images
In the **2. Synthesis Timepoints** section:
* Enter the **Duration** and select the **Unit** from the dropdown menu (e.g., `24` and `Hours`).
* Click the **"Browse..."** button to select all relevant TEM images (`.tif`, `.jpg`, `.png`) for that specific timepoint.
* If you are tracking growth over time, click the **"+ Add Another Timepoint"** button to attach more image batches to the current sample.

### Step 4: Add Sample to Queue
Once your sample's timepoints are configured, click the blue **"Add Sample"** button in the **3. Current Dataset Queue** section. 
* Your configured sample will appear in the queue box. 
* If you want to analyze multiple different samples at once, you can repeat steps 2-4 to add more batches to the queue.

### Step 5: Run Analysis & Review Results
When your queue is ready, click the large green **"Start Analysis Processing"** button at the bottom of the window. The application will process the queued datasets using the core vision engine. 

Once complete, check the automatically generated `Verification_Output` folder in your project directory. Here you will find:
* Visual verification images with detected particles highlighted (to ensure accuracy).
* High-resolution kinetic plots tracking diameter and volume over time (`diameter_vs_time.png` and `volume_vs_time.png`).
* A comprehensive `.csv` summary and markdown report containing all your statistical data ready for publication.

---
**Note:** This project is being developed as a final project for the Advanced Python Programming Course. You can view the course guidelines and core repository here:
[https://github.com/Code-Maven/wis-python-course-2026-03](https://github.com/Code-Maven/wis-python-course-2026-03)