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

## 3. Technicalities

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

## 4. Usage (How to Run the Code)

### Step 1: Launch the Application
Open your terminal, ensure your virtual environment is activated, and run the GUI script:
`bash
python DMSN_Analyzer.py
`

### Step 2: Enter Sample Parameters
The GUI will prompt you to enter the core details for your current dataset:
* **Sample Name:** The identifier for your synthesis batch (e.g., "Silica_Batch_A").
* **Pixel-to-Nanometer Ratio:** The calibration scale for your TEM images (e.g., `0.439`).
* **Synthesis Time:** You can add multiple synthesis times for a single sample batch. For each specific timepoint, you will upload the TEM images that correspond to that duration.

### Step 3: Select TEM Images
* For each synthesis timepoint (e.g., "24 hours", "3 days"), click the "Browse" button in the GUI.
* Select all the relevant TEM images (`.tif`, `.jpg`, `.png`) for that specific timepoint.
* You can add multiple timepoints for a single sample to track growth over time.

### Step 4: Run Analysis & Review Results
Click the **"Run Analysis"** button. The application will process the images using the core engine. Once complete, check the automatically generated `Verification_Output` folder in your directory. Here you will find:
* Visual verification images with detected particles highlighted (to ensure accuracy).
* High-resolution kinetic plots tracking diameter and volume over time (`diameter_vs_time.png` and `volume_vs_time.png`).
* A comprehensive `.csv` summary and markdown report containing all your statistical data ready for publication.

---
**Note:** This project is being developed as a final project for the Advanced Python Programming Course. You can view the course guidelines and core repository here
https://github.com/Code-Maven/wis-python-course-2026-03