# DMSN-Analyzer: Automated TEM Image Processing for Nanoparticle Growth Kinetics

An automated image processing pipeline written in Python to extract morphological data from Transmission Electron Microscopy (TEM) images of Dendritic Mesoporous Silica Nanoparticles (DMSNs). This tool accelerates nanomaterials research by replacing manual particle sizing with automated segmentation, tracking nanoparticle diameter and volume evolution over synthesis time.

---

## 1. What does this project do?

Characterizing the growth kinetics of porous nanoparticles typically requires researchers to manually measure hundreds of particle diameters across multiple TEM images using software like ImageJ. This process is time-consuming and prone to human bias.

**DMSN-Analyzer** automates this workflow. It performs the following tasks:
* **Image Preprocessing & Noise Reduction:** Cleans TEM images to handle low contrast, varying brightness, and background variations typical in electron microscopy.
* **Particle Detection & Segmentation:** Utilizes computer vision algorithms (via `OpenCV` and `scikit-image`) to isolate individual dendritic nanoparticles, even when minor overlapping occurs.
* **Morphological Measurement:** Calibrates pixel sizes to physical nanometer scales, extracting the exact boundary, diameter, and calculated volume of each detected particle.
* **Kinetic Analysis:** Aggregates statistical data across different sample batches and plots the growth kinetics to map synthesis progression over time.

---

## 2. Input and Output Data

### Expected Inputs
1. **TEM Images:** A directory containing standard image files (`.png`, `.jpg`, or `.tiff`) captured via Transmission Electron Microscopy.
2. **Synthesis Time Metadata:** * A configuration mapping or a structured filename convention (e.g., `sample_t60min_01.png`) providing the specific synthesis duration (in minutes or hours) for each image batch.
   * A user-defined calibration factor (pixel-to-nanometer ratio) to ensure physical accuracy.

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
git clone [https://github.com/YOUR_USERNAME/DMSN-Analyzer.git](https://github.com/YOUR_USERNAME/DMSN-Analyzer.git)
cd DMSN-Analyzer

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt# DMSN-Analyzer: Automated TEM Image Processing for Nanoparticle Growth Kinetics

An automated image processing pipeline written in Python to extract morphological data from Transmission Electron Microscopy (TEM) images of Dendritic Mesoporous Silica Nanoparticles (DMSNs). This tool accelerates nanomaterials research by replacing manual particle sizing with automated segmentation, tracking nanoparticle diameter and volume evolution over synthesis time.

---

## 1. What does this project do?

Characterizing the growth kinetics of porous nanoparticles typically requires researchers to manually measure hundreds of particle diameters across multiple TEM images using software like ImageJ. This process is time-consuming and prone to human bias.

**DMSN-Analyzer** automates this workflow. It performs the following tasks:
* **Image Preprocessing & Noise Reduction:** Cleans TEM images to handle low contrast, varying brightness, and background variations typical in electron microscopy.
* **Particle Detection & Segmentation:** Utilizes computer vision algorithms (via `OpenCV` and `scikit-image`) to isolate individual dendritic nanoparticles, even when minor overlapping occurs.
* **Morphological Measurement:** Calibrates pixel sizes to physical nanometer scales, extracting the exact boundary, diameter, and calculated volume of each detected particle.
* **Kinetic Analysis:** Aggregates statistical data across different sample batches and plots the growth kinetics to map synthesis progression over time.

---

## 2. Input and Output Data

### Expected Inputs
1. **TEM Images:** A directory containing standard image files (`.png`, `.jpg`, or `.tiff`) captured via Transmission Electron Microscopy.
2. **Synthesis Time Metadata:** * A configuration mapping or a structured filename convention (e.g., `sample_t60min_01.png`) providing the specific synthesis duration (in minutes or hours) for each image batch.
   * A user-defined calibration factor (pixel-to-nanometer ratio) to ensure physical accuracy.

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
git clone [https://github.com/YOUR_USERNAME/DMSN-Analyzer.git](https://github.com/YOUR_USERNAME/DMSN-Analyzer.git)
cd DMSN-Analyzer

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt