# Unveiling Practical Shortcomings of Patch Overfitting Detection Techniques
This is the replication package for "Unveiling Practical Shortcomings of Patch Overfitting Detection Techniques". We will add a permissive open-source license upon acceptance.

## Structure

The following is the overall structure for our repository. Please find below the paths to information/figures we reference in our submission.

### Figures Referenced in Submission

These links will take you to the figures referenced in the paper.

- Tool-specific data preprocessing and other requirements can be found in [`tools/README.md`](./tools/README.md)
- UpSet plots for the repairllama dataset - [correct](./figure_replication/repairllama_figures/visualisations/rq1/correctly_classified_correct_patches.png) & [overfitting](./figure_replication/repairllama_figures/visualisations/rq1/correctly_classified_overfitting_patches.png) patches.
- Project-level MCC box plots for the [classical dataset](./figure_replication/petke_8h_figures/visualisations/rq1/project_boxplot.png) and [repairllama dataset](./figure_replication/repairllama_figures/visualisations/rq1/project_boxplot.png).
- Complete tables for bug-level number of patches to inspect using each overfitting tool and our baselines for the [classical dataset](./figure_replication/petke_8h_figures/tables/rq3/rs-combined.tex) and [repairllama dataset](./figure_replication/repairllama_figures/tables/rq3/rs-combined.tex).
- Complete tables for bug-level number of inspections for the [classical (1st hour subset) dataset](./figure_replication/petke_1h_figures/tables/rq3/rs-combined.tex).
- [Metrics grid of each tool's performance against the WPC baseline for the repairllama dataset](./figure_replication/repairllama_figures/visualisations/rq3/tools_vs_wbc.png)

### Repository Directories

```
apr-overfitting-benchmark/
├── datasets/
│   ├── petke/ # classical dataset
│   │   ├── all_patches/ # All classical dataset patches before deduplication
│   │   └── patches_by_time/ # Classical dataset patches grouped by discovery time.
│   └── repairllama/ # repairllama dataset
│       ├── context_size_3_evaluation_defects4j_repairllama_ir4_or2_martin/ # Original dataset
│       ├── context_size_3_filtered/ # Filtered dataset
│       ├── final_dataset/ # Deduplicated filtered dataset for our experiments
│       ├── repairllama_filtering.py # Filtering script
│       ├── identify_repairllama_duplicate_patches.py # Deduplication script
│       └── README.md # Explaining the source of the patches and filtering script
│── defects4j_projects/ # Defects4J projects required to replicate experiments for each dataset
│   ├── petke/ 
│   ├── repairllama/
│   ├── checkout_d4j.py # Script to download all necessary buggy and fixed Defects4J projects (see below)
│   └── README.md # Explaining the usage of checkout_d4j.py
│── figure_replication/
│   ├── combined_figures/ # Raw data, tables and visualisations for classical and repairllama datasets combined 
│   ├── petke_1h_figures/ # Raw data, tables and visualisations for classical (1h APR tool runtime)
│   ├── petke_8h_figures/ # Raw data, tables and visualisations for classical dataset
│   ├── repairllama_dedup_figures/ # Raw data, tables and visualisations for deduplicated repairllama dataset (presented in our paper)
│   ├── repairllama_figures/ # Raw data, tables and visualisations for repairllama dataset
│   ├── scripts/ # Scripts used to analyse the classifications in results/
│   ├── figure-replication-requirements.txt # Requirements for analysis replication
│   └── README.md # Instructions to replicate data analysis
│── results/
│   └── ... # Sub-directories for each overfitting detector containing classification results on all datasets
│── tools/
│   ├── ... # Sub-directories for each overfitting detector with modified source code used for benchmarking
│   └── README.md # Detailed instructions for each tool on how to replicate experiments
└── README.md # You are here!
```

## Study Replication

1. **Checkout Defects4J Projects**  
   Use the provided script [`defects4j_projects/checkout_d4j.py`](defects4j_projects/checkout_d4j.py) to automatically download all necessary buggy and fixed project versions. See the README in [`defects4j_projects/`](defects4j_projects/) for more information.

   > **Note:** This requires Defects4J to be installed and configured. Defects4J depends on Java 11. You must update the `JAVA_11_PATH` constant in `checkout_d4j.py` to point to a valid Java 11 installation.  
   > For setup instructions, refer to the [Defects4J GitHub repository](https://github.com/rjust/defects4j).

2. **Run Evaluation Tools**  
   Follow the setup and usage instructions provided in [`tools/README.md`](tools/README.md) to run the evaluation tools and move outputs to the `results/` directory as described.

3. **Replicate Figures**  
   After obtaining all experimental outputs, replicate the figures and tables by following the instructions in [`figure_replication/README.md`](figure_replication/README.md).
