import numpy as np

def ellipse_to_cov(width, height, angle_deg):
    """
    Convert ellipse (width, height, angle) into a covariance matrix.
    Width, height assumed to be 2σ (so we scale by 0.5).
    """
    angle = np.deg2rad(angle_deg)
    c, s = np.cos(angle), np.sin(angle)
    R = np.array([[c, -s], [s, c]])  # rotation matrix

    # Assume width, height are 2σ (adjust if yours are 1σ)
    D = np.diag([(width/2.0)**2, (height/2.0)**2])
    cov = R @ D @ R.T
    return cov
#!/usr/bin/env python3
"""
Mahalanobis classifier for AGN vs SFG using published GMM ellipse files.

Usage:
    python classify_mahalanobis.py sources.txt ellipse_file.txt output.txt

Inputs:
    sources.txt      - Table of sources with fluxes (F07, F10, F12) and errors
                       Required columns: ID, F07, F07_err, F10, F10_err, F12, F12_err
    ellipse_file.txt - Ellipse definition (mean vector + covariance matrix)
                       Format example:
                           # mean_x mean_y
                           0.12 0.35
                           # covariance matrix (2x2)
                           0.01 0.002
                           0.002 0.015
    output.txt       - Output file with classification results

Outputs:
    output.txt       - Table with: ID, Mahalanobis_Distance, Class, Uncertain
"""

import sys
import numpy as np
import pandas as pd

def load_ellipse(file_path):
    """Load mean and covariance from ellipse file."""
    with open(file_path) as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    # First line = mean vector
    mean = np.array([float(x) for x in lines[0].split()])

    # Next 2 lines = covariance matrix
    cov = np.array([[float(x) for x in lines[1].split()],
                    [float(x) for x in lines[2].split()]])

    cov_inv = np.linalg.inv(cov)
    return mean, cov, cov_inv

def mahalanobis_distance(x, mean, cov_inv):
    """Compute Mahalanobis distance of vector x from mean."""
    diff = x - mean
    return np.sqrt(diff.T @ cov_inv @ diff)

def classify_sources(sources, mean, cov_inv, threshold=3.0):
    """Apply Mahalanobis classification to sources."""
    results = []

    for _, row in sources.iterrows():
        if row['F07'] <= 0 or row['F10'] <= 0 or row['F12'] <= 0:
            continue  # skip invalid fluxes

        x = np.array([
            np.log10(row['F12'] / row['F07']),
            np.log10(row['F12'] / row['F10'])
        ])

        dist = mahalanobis_distance(x, mean, cov_inv)

        if dist <= threshold:
            results.append([row['ID'], dist, "AGN", "No"])
        else:
            results.append([row['ID'], dist, "SFG", "Yes"])

    return pd.DataFrame(results, columns=["ID", "Mahalanobis_Distance", "Class", "Uncertain"])

def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    source_file, ellipse_file, output_file = sys.argv[1:4]

    # Load input data
    sources = pd.read_csv(source_file, delim_whitespace=True, comment='#')

    # Load ellipse definition
    mean, cov, cov_inv = load_ellipse(ellipse_file)

    # Classify
    results = classify_sources(sources, mean, cov_inv)

    # Save results
    results.to_csv(output_file, sep='\t', index=False)
    print(f"✅ Classification done. Results saved to {output_file}")

if __name__ == "__main__":
    main()
