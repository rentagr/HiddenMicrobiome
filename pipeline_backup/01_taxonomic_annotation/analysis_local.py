#!/usr/bin/env python
"""
Complete analysis for Step 1:
- PCA, t-SNE, alpha diversity, differential abundance, mean relative abundance.
- For both Kraken2 and MetaPhlAn, for fracture and BMD groups.
Generates all figures into images/ directory.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
import os

# ========================
# 1. Load metadata
# ========================
metadata = pd.read_csv("SraRunTable.csv")
metadata.rename(columns={"Run": "sample"}, inplace=True)
metadata["fracture_group"] = metadata["Fracture"].apply(
    lambda x: "healthy" if x == 0 else "case"
)

# BMD groups (from Step0)
bmd_dict = {
    "SRR25006867": "normal",
    "SRR25006868": "normal",
    "SRR25006869": "low",
    "SRR25006870": "low",
    "SRR25006871": "low",
    "SRR25006872": "low",
    "SRR25006873": "normal",
    "SRR25006874": "normal",
    "SRR25006875": "low",
    "SRR25006876": "normal",
    "SRR25006877": "normal",
    "SRR25006878": "normal",
    "SRR25006879": "low",
    "SRR25006880": "normal",
    "SRR25006881": "normal",
    "SRR25006882": "normal",
    "SRR25006883": "normal",
    "SRR25006884": "low",
    "SRR25006885": "normal",
    "SRR25006886": "normal",
    "SRR25006887": "low",
    "SRR25006888": "normal",
    "SRR25006889": "normal",
    "SRR25006890": "normal",
    "SRR25006891": "low",
    "SRR25006892": "low",
    "SRR25006893": "low",
    "SRR25006894": "normal",
    "SRR25006895": "low",
    "SRR25006896": "normal",
    "SRR25006897": "normal",
    "SRR25006898": "normal",
    "SRR25006899": "normal",
    "SRR25006900": "low",
    "SRR25006901": "normal",
    "SRR25006902": "normal",
    "SRR25006903": "normal",
    "SRR25006904": "normal",
    "SRR25006905": "low",
    "SRR25006906": "normal",
    "SRR25006907": "normal",
    "SRR25006908": "normal",
    "SRR25006909": "low",
    "SRR25006910": "normal",
    "SRR25006911": "normal",
    "SRR25006912": "normal",
    "SRR25006913": "normal",
    "SRR25006914": "low",
    "SRR25006915": "normal",
    "SRR25006916": "low",
    "SRR25006917": "low",
    "SRR25006918": "normal",
    "SRR25006919": "normal",
    "SRR25006920": "normal",
    "SRR25006921": "low",
    "SRR25006922": "low",
    "SRR25006923": "normal",
    "SRR25006924": "normal",
    "SRR25006925": "low",
}
metadata["bmd_group"] = metadata["sample"].map(bmd_dict)


# ========================
# 2. Helper functions
# ========================
def shannon_index(df, taxa_cols):
    abundances = df[taxa_cols].values
    row_sums = abundances.sum(axis=1, keepdims=True)
    abundances = abundances / row_sums
    abundances = np.where(abundances == 0, 1e-12, abundances)
    return -np.sum(abundances * np.log(abundances), axis=1)


def run_pca_tsne(
    df, taxa_cols, group_col, group_order, colors, title_prefix, out_dir, outliers=None
):
    X = df[taxa_cols].values
    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X_scaled)

    # PCA with all
    plt.figure(figsize=(8, 6))
    for g, col in zip(group_order, colors):
        idx = df[group_col] == g
        plt.scatter(pca_result[idx, 0], pca_result[idx, 1], label=g, c=col, alpha=0.7)
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%})")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%})")
    plt.title(f"{title_prefix} PCA")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{out_dir}/PCA_o.png", dpi=150)
    plt.close()

    # PCA without outliers if provided
    if outliers is not None:
        mask = ~df.index.isin(outliers)
        X_clean = X_scaled[mask]
        df_clean = df[mask]
        pca2 = PCA(n_components=2)
        pca_result2 = pca2.fit_transform(X_clean)
        plt.figure(figsize=(8, 6))
        for g, col in zip(group_order, colors):
            idx = df_clean[group_col] == g
            plt.scatter(
                pca_result2[idx, 0], pca_result2[idx, 1], label=g, c=col, alpha=0.7
            )
        plt.xlabel(f"PC1 ({pca2.explained_variance_ratio_[0]:.2%})")
        plt.ylabel(f"PC2 ({pca2.explained_variance_ratio_[1]:.2%})")
        plt.title(f"{title_prefix} PCA (outliers removed)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{out_dir}/PCA_wo.png", dpi=150)
        plt.close()

    # t-SNE (outliers removed)
    if outliers is not None:
        mask = ~df.index.isin(outliers)
        X_clean = X_scaled[mask]
        df_clean = df[mask]
        perplexity = min(6, len(df_clean) - 1)
        tsne = TSNE(
            n_components=2, perplexity=perplexity, random_state=42, max_iter=1000
        )
        tsne_result = tsne.fit_transform(X_clean)
        plt.figure(figsize=(8, 6))
        for g, col in zip(group_order, colors):
            idx = df_clean[group_col] == g
            plt.scatter(
                tsne_result[idx, 0], tsne_result[idx, 1], label=g, c=col, alpha=0.7
            )
        plt.xlabel("t-SNE 1")
        plt.ylabel("t-SNE 2")
        plt.title(f"{title_prefix} t-SNE (outliers removed)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{out_dir}/t_SNE.png", dpi=150)
        plt.close()


def plot_alpha_diversity(df, group_col, group_order, colors, title, out_file):
    plt.figure(figsize=(6, 5))
    sns.boxplot(x=group_col, y="shannon", data=df, order=group_order, palette=colors)
    plt.title(title)
    plt.ylabel("Shannon index")
    plt.tight_layout()
    plt.savefig(out_file, dpi=150)
    plt.close()


def differential_abundance(df, taxa_cols, group_col, group_a, group_b, out_csv):
    results = []
    for taxon in taxa_cols:
        vals_a = df[df[group_col] == group_a][taxon]
        vals_b = df[df[group_col] == group_b][taxon]
        stat, p = mannwhitneyu(vals_a, vals_b, alternative="two-sided")
        results.append({"taxon": taxon, "p_value": p})
    res_df = pd.DataFrame(results).sort_values("p_value")
    # FDR correction
    pvals = res_df["p_value"].values
    _, corrected, _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")
    res_df["q_value"] = corrected
    res_df.to_csv(out_csv, index=False)
    return res_df


def mean_relative_abundance(df, taxa_cols, group_col, groups, out_plot, top_n=20):
    # Normalize each sample to relative abundance
    df_norm = df[taxa_cols].div(df[taxa_cols].sum(axis=1), axis=0).fillna(0)
    means = pd.DataFrame()
    for g in groups:
        means[g] = df_norm[df[group_col] == g].mean()
    means["total"] = means.mean(axis=1)
    top_taxa = means.sort_values("total", ascending=False).head(top_n).index
    plot_df = means.loc[top_taxa, groups].copy()
    plot_df.loc["Others"] = means.drop(top_taxa)[groups].sum()
    plot_df_norm = plot_df / plot_df.sum()
    plot_df_norm.T.plot(
        kind="bar", stacked=True, figsize=(8, 6), colormap="tab20", edgecolor="black"
    )
    plt.ylabel("Mean relative abundance")
    plt.title("Mean relative abundance")
    plt.legend(title="Taxa", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(out_plot, dpi=150)
    plt.close()


# ========================
# 3. Load data
# ========================
kraken_df = pd.read_csv("kraken_step1.csv", index_col=0).T  # samples x species
metaphlan_df = pd.read_csv("metaphlan_step1.csv", index_col=0).T

# Align samples with metadata
common_samples = (
    set(kraken_df.index) & set(metaphlan_df.index) & set(metadata["sample"])
)
kraken_df = kraken_df.loc[list(common_samples)]
metaphlan_df = metaphlan_df.loc[list(common_samples)]
metadata = metadata[metadata["sample"].isin(common_samples)].set_index("sample")

# ========================
# 4. Kraken2 analysis
# ========================
out_kra = "images/Step1_kraken"
os.makedirs(out_kra, exist_ok=True)

taxa_kra = kraken_df.columns
# Alpha diversity
kraken_df["shannon"] = shannon_index(kraken_df, taxa_kra)
kraken_df["bmd_group"] = metadata["bmd_group"]
kraken_df["fracture_group"] = metadata["fracture_group"]

# Fracture alpha
plot_alpha_diversity(
    kraken_df,
    "fracture_group",
    ["healthy", "case"],
    ["green", "red"],
    "Kraken2: Alpha diversity by fracture",
    "../images/Fracture/Fracture_alpha_diversity.png",
)
# BMD alpha
plot_alpha_diversity(
    kraken_df,
    "bmd_group",
    ["normal", "low"],
    ["blue", "orange"],
    "Kraken2: Alpha diversity by BMD",
    "../images/BMD/BMD_alpha_diversity.png",
)

# PCA/t-SNE (outliers from original analysis)
outliers_kra = [
    "SRR25006870",
    "SRR25006887",
    "SRR25006895",
    "SRR25006907",
    "SRR25006917",
    "SRR25006925",
]
run_pca_tsne(
    kraken_df,
    taxa_kra,
    "fracture_group",
    ["healthy", "case"],
    ["green", "red"],
    "Kraken2",
    out_kra,
    outliers=outliers_kra,
)

# Differential abundance
diff_kra = differential_abundance(
    kraken_df,
    taxa_kra,
    "fracture_group",
    "healthy",
    "case",
    f"{out_kra}/diff_abundance.csv",
)
# (top results can be printed or saved)

# Mean relative abundance (fracture and BMD)
mean_relative_abundance(
    kraken_df,
    taxa_kra,
    "fracture_group",
    ["case", "healthy"],
    "../images/Fracture/Fracture_MRA.png",
)
mean_relative_abundance(
    kraken_df, taxa_kra, "bmd_group", ["low", "normal"], "../images/BMD/BMD_MRA.png"
)

# ========================
# 5. MetaPhlAn analysis
# ========================
out_met = "images/Step1_metaphlan"
os.makedirs(out_met, exist_ok=True)

taxa_met = metaphlan_df.columns
metaphlan_df["shannon"] = shannon_index(metaphlan_df, taxa_met)
metaphlan_df["bmd_group"] = metadata["bmd_group"]
metaphlan_df["fracture_group"] = metadata["fracture_group"]

# Fracture alpha
plot_alpha_diversity(
    metaphlan_df,
    "fracture_group",
    ["healthy", "case"],
    ["green", "red"],
    "MetaPhlAn: Alpha diversity by fracture",
    "../images/Fracture/Fracture_alpha_diversity.png",
)
# BMD alpha
plot_alpha_diversity(
    metaphlan_df,
    "bmd_group",
    ["normal", "low"],
    ["blue", "orange"],
    "MetaPhlAn: Alpha diversity by BMD",
    "../images/BMD/BMD_alpha_diversity.png",
)

# PCA/t-SNE
run_pca_tsne(
    metaphlan_df,
    taxa_met,
    "fracture_group",
    ["healthy", "case"],
    ["green", "red"],
    "MetaPhlAn",
    out_met,
    outliers=outliers_kra,
)

# Differential abundance
diff_met = differential_abundance(
    metaphlan_df,
    taxa_met,
    "fracture_group",
    "healthy",
    "case",
    f"{out_met}/diff_abundance.csv",
)

# Mean relative abundance for MetaPhlAn (if needed)
# (optional, but can be done similarly)


# ========================
# 6. Heatmaps (top20)
# ========================
def plot_top20_heatmap(
    df, taxa_cols, group_col, title, out_file, group_order=None, colors=None
):
    top_taxa = df[taxa_cols].mean().sort_values(ascending=False).head(20).index
    df_top = df[top_taxa].copy()
    df_top[group_col] = df[group_col]
    if group_order:
        df_top[group_col] = pd.Categorical(
            df_top[group_col], categories=group_order, ordered=True
        )
    df_top = df_top.sort_values(group_col)
    data = df_top.drop(columns=[group_col]).T
    plt.figure(figsize=(12, 8))
    sns.heatmap(data, cmap="viridis", cbar_kws={"label": "Abundance"})
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_file, dpi=150)
    plt.close()


plot_top20_heatmap(
    kraken_df,
    taxa_kra,
    "fracture_group",
    "Kraken2 top20 species by fracture",
    f"{out_kra}/top20_heatmap.png",
    group_order=["healthy", "case"],
)
plot_top20_heatmap(
    metaphlan_df,
    taxa_met,
    "fracture_group",
    "MetaPhlAn top20 species by fracture",
    f"{out_met}/top20_heatmap.png",
    group_order=["healthy", "case"],
)

print("All analyses completed. Figures saved in images/")
