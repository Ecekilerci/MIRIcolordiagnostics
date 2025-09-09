#!/usr/bin/env python3
"""
Plot sources with GMM ellipses used for Mahalanobis classification.
"""

import numpy as np
import glob
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# ------------------------------
# Load ellipse definitions
# ------------------------------
def load_ellipses(folder="ellipses/"):
    ellipses = {}
    for fname in glob.glob(f"{folder}/*.txt"):
        label = fname.split("/")[-1].replace(".txt", "")
        with open(fname) as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                cx, cy, w, h, angle = map(float, line.split())
                ellipses[label] = {"center": (cx, cy),
                                   "width": w,
                                   "height": h,
                                   "angle": angle}
    return ellipses

# ------------------------------
# Load classified sources
# ------------------------------
def load_sources(classified_file):
    ids, xs, ys, labels = [], [], [], []
    with open(classified_file) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            ids.append(parts[0])
            xs.append(float(parts[1]))
            ys.append(float(parts[2]))
            labels.append(parts[3])
    return np.array(ids), np.array(xs), np.array(ys), np.array(labels)

# ------------------------------
# Plot function
# ------------------------------
def plot_results(ellipses, xs, ys, labels, out_png="classified_plot.png"):
    plt.figure(figsize=(7,7))

    # Plot ellipses
    for label, e in ellipses.items():
        ell = Ellipse(xy=e["center"], width=e["width"], height=e["height"],
                      angle=e["angle"], edgecolor="black", facecolor="none",
                      lw=1.5, label=f"Region {label}")
        plt.gca().add_patch(ell)

    # Plot sources
    for label in np.unique(labels):
        sel = labels == label
        plt.scatter(xs[sel], ys[sel], s=30, label=f"Sources {label}", alpha=0.7)

    plt.xlabel(r"log(F12/F07)")
    plt.ylabel(r"log(F12/F10)")
    plt.legend()
    plt.grid(True, ls="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    print(f"✅ Plot saved: {out_png}")
    plt.close()

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    ellipse_dir = "ellipses/"
    classified_file = "classified_sources.txt"
    out_png = "classified_plot.png"

    ellipses = load_ellipses(ellipse_dir)
    ids, xs, ys, labels = load_sources(classified_file)

    plot_results(ellipses, xs, ys, labels, out_png)
