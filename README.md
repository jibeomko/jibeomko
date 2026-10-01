<p align="center">
  <img src="assets/hero.svg" width="100%" alt="Jibeom Ko — computational biology at KIST, Seoul. I build bioinformatics tools that show their evidence.">
</p>

<p align="center">
  <a href="https://orcid.org/0009-0002-8630-1973"><img src="https://img.shields.io/badge/ORCID-0009--0002--8630--1973-A6CE39?style=flat-square&logo=orcid&logoColor=white" alt="ORCID"></a>
  <a href="https://www.kist.re.kr"><img src="https://img.shields.io/badge/KIST-Seoul-0A4DA2?style=flat-square" alt="KIST, Seoul"></a>
  <a href="https://github.com/bioconda/bioconda-recipes/pull/65953"><img src="https://img.shields.io/badge/bioconda-contributor-44A833?style=flat-square&logo=anaconda&logoColor=white" alt="bioconda contributor"></a>
</p>

## About

- **Research:** cancer multi-omics — long-read transcriptomics, single-cell atlases and tissue-to-serum biomarkers.
- **Tools:** when an analysis step keeps being trusted on faith, I turn it into a tool that records its evidence and says when the evidence is not enough.
- **Notes:** before relying on a method, I recompute it by hand and write down where the textbook and the software disagree.

## Tools & packages

<table>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/jibeomko/PanIsoGuard">PanIsoGuard</a></h3>
      <a href="https://anaconda.org/bioconda/panisoguard"><img src="https://img.shields.io/conda/vn/bioconda/panisoguard?style=flat-square&label=bioconda&color=44A833" alt="bioconda"></a>
      <a href="https://github.com/jibeomko/PanIsoGuard/releases"><img src="https://img.shields.io/github/v/release/jibeomko/PanIsoGuard?style=flat-square" alt="release"></a>
      <a href="https://github.com/jibeomko/PanIsoGuard/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/jibeomko/PanIsoGuard/ci.yml?style=flat-square&label=CI" alt="CI"></a>
      <img src="https://img.shields.io/badge/C%2B%2B17-htslib-00599C?style=flat-square&logo=cplusplus&logoColor=white" alt="C++17">
      <p>Decides which <b>novel isoforms</b> from a long-read RNA-seq caller to trust, and records why.</p>
      <p>Runs on SQANTI3 output from any caller (FLAIR, IsoQuant, Bambu, ESPRESSO, TALON …). Each isoform gets one of seven confidence classes, the rule that decided it, and a provenance log of the evidence used.</p>
      <sub>Alpha · <a href="https://github.com/jibeomko/PanIsoGuard#quick-start">Quick start →</a></sub>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/jibeomko/pdactrace">pdactrace</a></h3>
      <a href="https://github.com/jibeomko/pdactrace/tags"><img src="https://img.shields.io/github/v/tag/jibeomko/pdactrace?sort=semver&style=flat-square&label=version" alt="version"></a>
      <a href="https://doi.org/10.5281/zenodo.20068234"><img src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20068234-1682D4?style=flat-square" alt="DOI"></a>
      <img src="https://img.shields.io/badge/R-package-276DC3?style=flat-square&logo=r&logoColor=white" alt="R package">
      <p>Stage-aware <b>PDAC multi-omics atlas</b> with a deterministic claim-audit framework for tissue-to-blood biomarker evidence.</p>
      <p>Keeps "tissue marker", "serum-observed signal" and "serum-concordant biomarker" as separate claim tiers across bulk RNA-seq, tissue and serum proteomics, single-cell origin and pancreatitis context. An audit, not a trained classifier.</p>
      <sub><code>remotes::install_github("jibeomko/pdactrace")</code></sub>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <h3><a href="https://github.com/jibeomko/poisson-to-deseq2">poisson-to-deseq2</a></h3>
      <img src="https://img.shields.io/badge/R-DESeq2_1.50-276DC3?style=flat-square&logo=r&logoColor=white" alt="R">
      <img src="https://img.shields.io/badge/Jupyter-notebooks-F37626?style=flat-square&logo=jupyter&logoColor=white" alt="Jupyter">
      <img src="https://img.shields.io/badge/notes-한국어-555?style=flat-square" alt="Notes in Korean">
      <p>Study notes on <b>DESeq2</b>, from why a Poisson model is not enough to which genes <code>padj</code> is adjusted over.</p>
      <p>One gene is followed through every step; each number is recomputed by hand and checked against DESeq2.</p>
    </td>
  </tr>
</table>

## Publications

- Hwang Y, Kim J, **Ko JB**, Han Y, Kim Y, Lee KH, Jang S. **From affinity to kinetics: SPR as the analytical backbone of AI-driven drug discovery.** *TrAC Trends in Analytical Chemistry* 204, 119089 (2026). [doi:10.1016/j.trac.2026.119089](https://doi.org/10.1016/j.trac.2026.119089)

<sub>Full list on <a href="https://orcid.org/0009-0002-8630-1973">ORCID</a>.</sub>

## Stack

<table>
  <tr>
    <td><b>Languages</b></td>
    <td><img src="https://skillicons.dev/icons?i=py,r,cpp,bash,js,dart" alt="Python, R, C++, Bash, JavaScript, Dart"></td>
  </tr>
  <tr>
    <td><b>Build & ship</b></td>
    <td><img src="https://skillicons.dev/icons?i=cmake,anaconda,docker,githubactions,git,linux" alt="CMake, Anaconda, Docker, GitHub Actions, Git, Linux"></td>
  </tr>
  <tr>
    <td><b>ML</b></td>
    <td><img src="https://skillicons.dev/icons?i=pytorch,sklearn" alt="PyTorch, scikit-learn"></td>
  </tr>
  <tr>
    <td><b>Apps & design</b></td>
    <td><img src="https://skillicons.dev/icons?i=flutter,androidstudio,figma" alt="Flutter, Android Studio, Figma"></td>
  </tr>
</table>

## Research toolkit

| Area | Methods & tools |
|---|---|
| Long-read transcriptomics | PacBio HiFi · ONT · minimap2 · SQANTI3 · IsoQuant · FLAIR · Bambu · ESPRESSO · TALON |
| Expression & single-cell | DESeq2 · DEXSeq · Seurat · scvi-tools · CellChat · BayesPrism |
| Proteomics | FragPipe (DDA / DIA) · DEqMS |
| Statistical genetics | Mendelian randomization (TwoSampleMR) · colocalization (coloc) |
| Structure | AlphaFold 3 · Boltz · Chai-1 · molecular docking |
| Workflows | Snakemake · Nextflow · conda / bioconda · Docker |
