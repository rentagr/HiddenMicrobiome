import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt

samples = []
dist_dict = {}

with open("distances.tab", "r") as f:
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) < 3:
            continue
        s1, s2 = parts[0], parts[1]
        if s1 == s2:
            continue
        try:
            dist = float(parts[2])
        except:
            continue
        dist_dict[(s1, s2)] = dist
        dist_dict[(s2, s1)] = dist
        samples.extend([s1, s2])

unique_samples = sorted(set(samples))
n = len(unique_samples)
print(f"Found {n} unique samples.")

# Build distance matrix
dist_matrix = np.ones((n, n))
for i, s1 in enumerate(unique_samples):
    dist_matrix[i, i] = 0.0
    for j, s2 in enumerate(unique_samples):
        if i == j:
            continue
        if (s1, s2) in dist_dict:
            dist_matrix[i, j] = dist_dict[(s1, s2)]
        else:
            dist_matrix[i, j] = 1.0

dist_matrix = (dist_matrix + dist_matrix.T) / 2
condensed = squareform(dist_matrix, checks=False)

# 2.1 Fracture status from SraRunTable.csv
meta = pd.read_csv("SraRunTable.csv")
meta["has_fracture"] = meta["Fracture"] > 0  # True if fracture present

# Dictionary: sample -> fracture (bool)
fracture_dict = {}
for _, row in meta.iterrows():
    fracture_dict[row["Run"]] = row["has_fracture"]

# normal/low categories (BMD) (according to Step0, substep 0.6; From .txt file, but we can also make it more adorable)))
BMD_cat = """
SRR25006867	normal
SRR25006868	normal
SRR25006869	low
SRR25006870	low
SRR25006871	low
SRR25006872     low
SRR25006873	normal
SRR25006874	normal
SRR25006875	low
SRR25006876	normal
SRR25006877	normal
SRR25006878	normal
SRR25006879	low
SRR25006880	normal
SRR25006881	normal
SRR25006882	normal
SRR25006883	normal
SRR25006884	low
SRR25006885	normal
SRR25006886	normal
SRR25006887	low
SRR25006888	normal
SRR25006889	normal
SRR25006890	normal
SRR25006891	low
SRR25006892	low
SRR25006893	low
SRR25006894	normal
SRR25006895	low
SRR25006896	normal
SRR25006897	normal
SRR25006898	normal
SRR25006899	normal
SRR25006900	low
SRR25006901	normal
SRR25006902	normal
SRR25006903	normal
SRR25006904	normal
SRR25006905     low
SRR25006906	normal
SRR25006907	normal
SRR25006908	normal
SRR25006909	low
SRR25006910     normal
SRR25006911	normal
SRR25006912	normal
SRR25006913	normal
SRR25006914	low
SRR25006915	normal
SRR25006916	low
SRR25006917	low
SRR25006918	normal
SRR25006919	normal
SRR25006920	normal
SRR25006921	low
SRR25006922	low
SRR25006923	normal
SRR25006924	normal
SRR25006925	low
"""

category_dict = {}
for line in BMD_cat.strip().split("\n"):
    if not line.strip():
        continue
    parts = line.split()
    if len(parts) >= 2:
        samp = parts[0].strip().upper()
        cat = parts[1].strip().lower()
        category_dict[samp] = cat

# For each sample, create label: "ID" + "*" if fracture present
labels = []
leaf_colors = []
for s in unique_samples:
    # Basic label
    has_frac = fracture_dict.get(s, False)
    label = s
    if has_frac:
        label += "*"
    labels.append(label)

    # Color by normal/low category
    cat = category_dict.get(s)
    if cat == "normal":
        leaf_colors.append("green")
    elif cat == "low":
        leaf_colors.append("red")
    else:
        leaf_colors.append("gray")

linkage_matrix = linkage(condensed, method="average")  # UPGMA

plt.figure(figsize=(16, 10))
dendrogram(
    linkage_matrix,
    labels=labels,
    leaf_rotation=90,
    leaf_font_size=8,
    color_threshold=0.5,
    above_threshold_color="gray",
)

# Change leaf colors according to category
ax = plt.gca()
for lbl, color in zip(ax.get_xmajorticklabels(), leaf_colors):
    lbl.set_color(color)

# Add legend
from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor="green", label="normal"),
    Patch(facecolor="red", label="low"),
    Patch(facecolor="none", label="* = fracture"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=10)

plt.title("Dendrogram: green=normal, red=low, * = fracture")
plt.xlabel("Sample ID")
plt.ylabel("Distance")
plt.tight_layout()
plt.savefig("dendrogram_combined.png", dpi=150)
plt.show()
