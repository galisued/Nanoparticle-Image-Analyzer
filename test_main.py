import pytest
import numpy as np
import os
from unittest.mock import patch

# Import the functions we want to test
from main import (
    sanitize_folder_name, 
    parse_synthesis_time_to_hours, 
    compute_particle_volume_nm3,
    generate_report,
    process_sample_batch
)

def test_sanitize_folder_name():
    """Test that folder names are cleaned of dangerous characters."""
    assert sanitize_folder_name("24 hours") == "24_hours"
    assert sanitize_folder_name("Day 3!") == "Day_3_"
    assert sanitize_folder_name("  messy  name  ") == "messy__name"

def test_parse_synthesis_time_to_hours():
    """Test the regex parser handles different time units correctly."""
    # Standard cases
    assert parse_synthesis_time_to_hours("24 hours") == 24.0
    assert parse_synthesis_time_to_hours("3 days") == 72.0
    assert parse_synthesis_time_to_hours("30 mins") == 0.5
    
    # Edge cases and abbreviations
    assert parse_synthesis_time_to_hours("1.5 h") == 1.5
    assert parse_synthesis_time_to_hours("1 d") == 24.0
    
    # Invalid cases
    assert parse_synthesis_time_to_hours("unknown time") is None
    assert parse_synthesis_time_to_hours(12345) is None

def test_compute_particle_volume_nm3():
    """Test that the spherical volume calculation is mathematically correct."""
    # Volume of sphere = (pi / 6) * diameter^3
    expected_vol = (np.pi / 6.0) * (10 ** 3)
    
    # pytest.approx handles tiny floating-point differences automatically
    assert compute_particle_volume_nm3(10) == pytest.approx(expected_vol, rel=1e-3)
    assert compute_particle_volume_nm3(0) == 0

def test_generate_report(tmp_path):
    """Test that the CSV and Markdown reports are generated with the correct data."""
    # Create fake statistics data mimicking your pipeline's output
    fake_stats = [
        {
            "sample_name": "Silica_Test",
            "synthesis_time": "24 hours",
            "total_particles": 150,
            "average_diameter_nm": 45.5,
            "standard_deviation_nm": 5.2
        }
    ]

    # Run the report generator, saving to the temporary pytest directory
    report_paths = generate_report(fake_stats, output_folder=str(tmp_path))

    # Assert the files were physically created on the hard drive
    assert os.path.exists(report_paths['csv'])
    assert os.path.exists(report_paths['markdown'])

    # Read the CSV and verify the data was written correctly
    with open(report_paths['csv'], 'r') as f:
        content = f.read()
        assert "Silica_Test" in content
        assert "45.5" in content

@patch('main.analyze_single_image')
def test_process_sample_batch(mock_analyze, tmp_path):
    """Test the batch processing logic and statistical aggregation using Mocking."""
    
    # We 'mock' the vision engine. Instead of doing real OpenCV work, 
    # we force it to always return exactly 2 particles with sizes 100nm and 110nm.
    mock_analyze.return_value = (2, [100.0, 110.0])

    # Create a fake sample dictionary that looks like the GUI output
    fake_sample = {
        "sample_name": "Batch_A",
        "pixel_ratio": 1.4,
        "timepoints": [
            {
                "synthesis_time": "12 hours",
                # We give it two fake images.
                "image_paths": ["fake_image1.tif", "fake_image2.tif"] 
            }
        ]
    }

    # Temporarily change the working directory so 'Verification_Output' folders 
    # are created in the safe tmp_path instead of cluttering your real project.
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        # Run the batch process
        result = process_sample_batch(fake_sample)
        
        # Verify the aggregation logic
        assert len(result) == 1
        
        # 2 images * 2 particles each = 4 total particles.
        assert result[0]["total_particles"] == 4
        
        # Diameters: [100, 110] from img1 + [100, 110] from img2. Average should be exactly 105.0.
        assert result[0]["average_diameter_nm"] == 105.0
        
        # Standard deviation of [100, 110, 100, 110] with ddof=1 is approx 5.77
        assert 5.7 < result[0]["standard_deviation_nm"] < 5.8
        
    finally:
        # Always switch back to the original directory so other tests don't break
        os.chdir(original_cwd)