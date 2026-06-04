import pytest
import cv2
import numpy as np
import os

from vision_engine import analyze_single_image

@pytest.fixture
def synthetic_image_env(tmp_path):
    """
    Pytest fixture to create a temporary directory and a synthetic test image.
    The tmp_path fixture automatically handles cleanup after the test runs.
    """
    image_path = tmp_path / "synthetic_particle.png"
    
    # Create a 1200x1200 light gray background
    img = np.ones((1200, 1200), dtype=np.uint8) * 200
    
    # Draw a dark circle in the middle (mimicking the dense core)
    # Center at (600, 600), radius 400 pixels
    cv2.circle(img, (600, 600), 400, 50, -1)
    
    # Save the synthetic image
    cv2.imwrite(str(image_path), img)
    
    # Yield the image path and the temporary directory string
    yield str(image_path), str(tmp_path)


def test_analyze_single_image(synthetic_image_env):
    """Test if the vision engine can detect a clear, synthetic particle."""
    image_path, output_dir = synthetic_image_env
    trusted_calibration = 0.439
    
    count, diameters = analyze_single_image(image_path, trusted_calibration, output_dir)
    
    # Check that it found the particle
    assert count >= 1, "Failed to detect the synthetic particle."
    assert len(diameters) == count
    
    if count > 0:
        # Check if the calculated diameter is accurate.
        # Radius of 400px -> diameter of 800px.
        # 800px * 0.439 nm/px = 351.2 nm.
        calculated_diameter = diameters[0]
        
        assert 330 < calculated_diameter < 370, f"Diameter {calculated_diameter:.2f} nm is outside expected range (330-370 nm)."
        
        # Verify it saved the checked output image
        checked_path = os.path.join(output_dir, "Checked_synthetic_particle.png")
        assert os.path.exists(checked_path), "Verification image was not saved."