import os
import re
import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from data_input import collect_sample_data
from vision_engine import analyze_single_image

def sanitize_folder_name(name):
    """Convert synthesis time labels into safe folder names."""
    safe_name = "".join(
        c if (c.isalnum() or c in (' ', '_', '-')) else '_'
        for c in name
    )
    return safe_name.strip().replace(' ', '_') or 'timepoint'


def parse_synthesis_time_to_hours(label):
    """Attempt to convert a synthesis time label into hours for plotting."""
    if not isinstance(label, str):
        return None
    matcher = re.search(r"([0-9]+\.?[0-9]*)", label)
    if not matcher:
        return None
    value = float(matcher.group(1))
    if re.search(r"\b(days?|d)\b", label, re.IGNORECASE):
        return value * 24.0
    if re.search(r"\b(hours?|hrs?|h)\b", label, re.IGNORECASE):
        return value
    if re.search(r"\b(minutes?|mins?|m)\b", label, re.IGNORECASE):
        return value / 60.0
    return value


def compute_particle_volume_nm3(diameter_nm):
    """Estimate nanoparticle volume from diameter assuming a sphere."""
    return (np.pi / 6.0) * diameter_nm**3


def plot_diameter_and_volume(final_statistics):
    """Plot diameter and estimated volume for all samples over synthesis time.

    Saves two separate PNG files in the `Verification_Output` folder:
    - `diameter_vs_time.png`
    - `volume_vs_time.png`
    """
    samples = {}
    for stat in final_statistics:
        sample_name = stat["sample_name"]
        samples.setdefault(sample_name, []).append(stat)

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    fig1, ax1 = plt.subplots(figsize=(8, 6))
    fig2, ax2 = plt.subplots(figsize=(8, 6))

    for idx, (sample_name, stats) in enumerate(samples.items()):
        stats_sorted = sorted(
            stats,
            key=lambda item: parse_synthesis_time_to_hours(item["synthesis_time"]) if parse_synthesis_time_to_hours(item["synthesis_time"]) is not None else float('inf')
        )

        x_values = []
        x_labels = []
        y_diameter = []
        y_volume = []

        for timepoint in stats_sorted:
            x_labels.append(timepoint["synthesis_time"])
            xval = parse_synthesis_time_to_hours(timepoint["synthesis_time"])
            x_values.append(xval if xval is not None else len(x_values))
            y_diameter.append(timepoint["average_diameter_nm"])
            y_volume.append(compute_particle_volume_nm3(timepoint["average_diameter_nm"]))

        color = colors[idx % len(colors)]
        ax1.plot(x_values, y_diameter, marker='o', color=color, label=sample_name)
        ax2.plot(x_values, y_volume, marker='o', color=color, label=sample_name)

        if any(parse_synthesis_time_to_hours(lbl) is None for lbl in x_labels):
            ax1.set_xticks(range(len(x_labels)))
            ax1.set_xticklabels(x_labels, rotation=30, ha='right')
            ax2.set_xticks(range(len(x_labels)))
            ax2.set_xticklabels(x_labels, rotation=30, ha='right')
        else:
            ax1.set_xlabel('Synthesis time (hours)')
            ax2.set_xlabel('Synthesis time (hours)')

    # title intentionally removed
    ax1.set_ylabel('Average Diameter (nm)')
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.legend()

    # title intentionally removed
    ax2.set_ylabel('Estimated Volume (nm³)')
    ax2.grid(True, linestyle='--', alpha=0.4)
    ax2.legend()

    fig1.tight_layout()
    fig2.tight_layout()
    os.makedirs('Verification_Output', exist_ok=True)
    diameter_path = os.path.join('Verification_Output', 'diameter_vs_time.png')
    volume_path = os.path.join('Verification_Output', 'volume_vs_time.png')
    fig1.savefig(diameter_path)
    fig2.savefig(volume_path)
    plt.close(fig1)
    plt.close(fig2)
    return {'diameter': diameter_path, 'volume': volume_path}


def generate_report(final_statistics, output_folder='Verification_Output'):
    """Generate CSV and Markdown report summarizing results and reference plots."""
    os.makedirs(output_folder, exist_ok=True)
    csv_path = os.path.join(output_folder, 'results_summary.csv')
    md_path = os.path.join(output_folder, 'results_report.md')
    plot_path = os.path.join(output_folder, 'diameter_vs_time.png')
    plot_path_volume = os.path.join(output_folder, 'volume_vs_time.png')
    
    # Write CSV
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['sample_name', 'synthesis_time', 'total_particles', 'average_diameter_nm', 'standard_deviation_nm']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for stat in final_statistics:
            writer.writerow({
                'sample_name': stat.get('sample_name', ''),
                'synthesis_time': stat.get('synthesis_time', ''),
                'total_particles': stat.get('total_particles', 0),
                'average_diameter_nm': f"{stat.get('average_diameter_nm', 0):.1f}",
                'standard_deviation_nm': f"{stat.get('standard_deviation_nm', 0):.1f}"
            })

    # Write Markdown report
    now = datetime.now().isoformat(sep=' ', timespec='seconds')
    with open(md_path, 'w') as md:
        md.write(f"# Nanoparticle Analysis Report\n\n")
        md.write(f"Generated: {now}\n\n")
        md.write(f"## Summary Table\n\n")
        md.write(f"| Sample | Synthesis Time | Particles | Avg Diameter (nm) | Std Dev (nm) |\n")
        md.write(f"|---|---:|---:|---:|---:|\n")
        for stat in final_statistics:
            md.write(f"| {stat.get('sample_name','')} | {stat.get('synthesis_time','')} | {stat.get('total_particles',0)} | {stat.get('average_diameter_nm',0):.2f} | {stat.get('standard_deviation_nm',0):.2f} |\n")

        md.write('\n')
        md.write(f"## Plots\n\n")
        if os.path.exists(plot_path):
            md.write(f"### Average Diameter vs Time\n\n![Diameter vs Time]({os.path.basename(plot_path)})\n\n")
        if os.path.exists(plot_path_volume):
            md.write(f"### Estimated Volume vs Time\n\n![Volume vs Time]({os.path.basename(plot_path_volume)})\n\n")
        md.write("## Notes\n\n- Verification images are saved in the Verification_Output folder under each sample/timepoint subfolder.\n")

    return {'csv': csv_path, 'markdown': md_path, 'plot': plot_path}


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

    if final_statistics:
        plot_diameter_and_volume(final_statistics)
        print("\nSaved diameter and volume plots to 'Verification_Output/diameter_and_volume_vs_time.png'.")

        report_paths = generate_report(final_statistics)
        print(f"Saved CSV summary to '{report_paths['csv']}' and markdown report to '{report_paths['markdown']}'.")

    print("\nDone! Check the 'Verification_Output' folder to see the drawn circles and reports.")
    print("========================================\n")