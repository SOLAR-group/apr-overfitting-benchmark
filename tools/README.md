# Modified Tools for Benchmarking

This directory contains the modified source code of the tools used in our experiments and instructions for how to replicate the experiments using our classical and repairllama datasets.  

---

## Prerequisites

- Each tool has different environment and library requirements. Where a provided README is incomplete, the necessary additional setup instructions are detailed below.
- **It is necessary to set up a separate virtual environment** for each tool to avoid dependency conflicts.
- The tools Invalidator and FIXCHECK require Defects4J to be installed and added to the system `PATH`. Defects4J also requires Java 11. Full setup instructions are available at the [Defects4J GitHub repository](https://github.com/rjust/defects4j).

## Results Files

All tools save their results in CSV format. To generate the figures presented in the report using these CSV files, the following steps must be followed:

- Move the generated CSV files to the `results` directory under the relevant tool subdirectory.
- Note that the tool subdirectories are named according to their GitHub repository names, which may differ from how the tools are referenced in the report.
- The mapping between tool names and directory names is provided below for clarity.
- After moving the CSV files, ensure that they follow a consistent naming convention, for example: `8h_deduplicated.csv`.

Following these instructions ensures compatibility with the provided figure generation scripts.

---

Below are instructions to replicate our benchmarking results.

## MIPI

- **Publication:**  
  Q.-N. Phung, M. Kim, and E. Lee,  
  *"Identifying incorrect patches in program repair based on meaning of source code"*  
  *IEEE Access*, vol. 10, pp. 12012–12030, 2022.

- **Type:** Static
- **Directory:** `mipi`
- **Original Repository:** https://github.com/ngocpq/MIPI

**Preprocessing:**

MIPI required a list for each patch consisting of all patched methods and their original and modified method bodies, along with with developer intentions. Following their methodological guidelines, developer intention was defined explicitly by the names of the methods modified by each patch. To accumulate this information, we applied each patch to the relevant Defects4J project, parsed the resultant code, and extracted method bodies where modifications occurred.

**Instructions:**  
1. Follow setup instructions in `mipi/README.md` to set up the environment and download the model
2. Change your working directory to `src/mipi-code2vec` and run `pip install -r requirements.txt` and `bash build_extractor.sh`
3. We found a missing dependency: `pip install protobuf==3.20.*`
4. To run experiments, ensure your working directory is `src/mipi-code2vec` and run:
  - Classical Dataset: `python mipi_sample.py mipi_patches_8h_deduplicated.json --dataset petke`
  - Repairllama Dataset: `python mipi_sample.py mipi_patches_repairllama.json --dataset repairllama`
5. Results will be saved under:
  - Classical Dataset: `src/mipi-code2vec/mipi_patches_8h_deduplicated_results.csv`
  - Repairllama Dataset: `src/mipi-code2vec/mipi_patches_repairllama_results.csv`

---

## Yang et al.

- **Publication:**  
A. Z. Yang, S. Kolak, V. J. Hellendoorn, R. Martins, and C. L. Goues,
*“Revisiting unnaturalness for automated program repair in the era of large language models”*
*arXiv* preprint arXiv:2404.15236, 2024.

- **Type:** Static
- **Directory:** `entropy-apr-replication`
- **Original Repository:** https://github.com/squaresLab/entropy-apr-replication

**Preprocessing:**

Minimal changes were made to the Yang et al. tool in the way bug information is inferred; the modified version detects the Defects4J project under patch and its version by parsing our structured patch filenames directly.

**Note: The model used by this tool requires substantial GPU power. We were able to complete our experiments using an NVIDIA RTX 3090.**

**Instructions:**  
1. As outlined in the tool's README, `CUDA version >= 11.4` along with the necessary drivers is required, as well as `torch (version 2.0.1)`.
2. Run `bash init_env.sh`
3. We found a missing dependency: `pip install accelerate`
4. To generate entropy scores for each patch, run:
  - Classical Dataset: `python patches/petke_patch_entropy.py`
  - Repairllama Dataset: `python patches/repairllama_patch_entropy.py`
5. To use the entropy scores to classify each patch, run:
  - Classical Dataset: `python analysis_notebooks/analysis_petke.py`
  - RepairLlama Dataset: `python analysis_notebooks/analysis_repairllama.py`
6. Results will be saved under:
  - Classical Dataset: `entropy_analysis_petke_cutoff_-0.55.csv`
  - Repairllama Dataset: `entropy_analysis_repairllama_cutoff_-0.55.csv`

---

## FIXCHECK

- **Publication:**  
F. Molina, J. M. Copia, and A. Gorla,
*“Improving patch correctness analysis via random testing and large language models”*
in 2024 *IEEE Conference on Software Testing, Verification and Validation (ICST)*, pp. 317–328, 2024.

- **Type:** Dynamic
- **Directory:** `fixcheck`
- **Original Repository:** https://github.com/facumolina/fixcheck 

**Preprocessing:**

FIXCHECK Required specific metadata related to each Defects4J project under evaluation. This metadata included the Defects4J project and bug version, main dependencies, build directory, test source directory, test class names exposing the bug, test method names exposing the bug, class names containing the bug. FIXCHECK’s original experiment on a dataset of Defects4J patches provided most of this information; however, three projects lacked this metadata, which were prepared manually to match FIXCHECK’s required format.

**Note: The model used by this tool requires substantial GPU power. We were able to complete our experiments using an NVIDIA RTX 3090.**

**Instructions:**  
1. Follow setup instructions in `fixcheck/README.md`
2. We found an issue setting up llama-cpp which we resolved by installing via URL: `pip install --no-cache-dir llama-cpp-python==0.2.85 --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu122`
3. Once you have installed the dependencies for the replit model, run `pip install transformers==4.33.1`.
4. Configure the scripts for your environment by replacing the five constants at the top as instructed by the comments to include your own java path etc. in the following files for each dataset:
  - Classical Dataset: In `experiments/run-fixcheck-petke.py` 
  - Repairllama Dataset: In `experiments/run-fixcheck-repairllama.py`
5. In one terminal, launch the LLM by running `python llms/replit-code.py` and wait until it is running.
6. In another terminal, launch fixcheck by running:
  - Classical Dataset: `python experiments/run-fixcheck-petke.py`
  - Repairllama Dataset: `python experiments/run-fixcheck-repairllama.py`
7. Once fixcheck is done, this will generate an output folder at `fixcheck-output/`. Rename these as the following:
  - Classical Dataset: `fixcheck-output/` -> `classical-fixcheck-output/`
  - Repairllama Dataset: `fixcheck-output/` -> `repairllama-fixcheck-output/`
8. Get patch classifications by running:
  - Classical Dataset: `python get_results.py --results-dir classical-fixcheck-output/defects-repairing --patches-dir ../../datasets/petke/all_patches --out fixcheck_results_8h.csv`
  - Repairllama Dataset: `python get_results.py --results-dir repairllama-fixcheck-output/defects-repairing --patches-dir ../../datasets/repairllama/context_size_3_filtered --out fixcheck_results_repairllama.csv`
9. Results will be saved under:
  - Classical Dataset: `fixcheck_results_8h.csv`
  - Repairllama Dataset: `fixcheck_results_repairllama.csv`

---

## Invalidator

- **Publication:**  
T. Le-Cong, D.-M. Luong, X. B. D. Le, D. Lo, N.-H. Tran, B. Quang-Huy, and Q.-T. Huynh,
*“Invalidator: Automated patch correctness assessment via semantic and syntactic reasoning”*
*IEEE Transactions on Software Engineering*, vol. 49, no. 6, pp. 3411–3429, 2023.

- **Type:** Dynamic
- **Directory:** `Invalidator`
- **Original Repository:** https://github.com/thanhlecongg/Invalidator 

**Preprocessing:**

The Invalidator paper does not provide publicly available scripts for invariant collection. To replicate their invariant-based semantic reasoning approach, we implemented a comprehensive pipeline that dynamically instruments and analyses Defects4J projects and APR-generated patches using Daikon. Our approach infers invariants for buggy and patched versions of each project by running Daikon on tailored test classes. These test classes are generated by extracting the test methods which expose the bug according to Defects4J records for each project. Our script collects and stores invariants and patch metadata in a structured format compatible with subsequent analysis, thus filling the implementation gap left by the original publication.

**Instructions:**  
1. The Invalidator replication package did not provide details of Daikon setup. This is the procedure we used to install it:
  - `wget https://plse.cs.washington.edu/daikon/download/daikon-5.8.20.tar.gz`
  - `tar -xzf daikon-5.8.20.tar.gz`
  - Then add Daikon relevant values to bashrc: `export DAIKONDIR="/home/user/workspace/daikon-5.8.20"` `export PATH=$DAIKONDIR:$PATH` `export CLASSPATH=$DAIKONDIR/daikon.jar:$CLASSPATH`
  - `make -C $DAIKONDIR rebuild-everything`
2. Install required libraries: `conda env create -f environment.yml`
3. We found a missing dependency: `pip install javalang`.
4. In `petke.py` (for the classical dataset) and `repairllama.py` (for the repairllama dataset) at the top replace the JAVA_11_HOME constant with your path to your java 11 installation and the patches path as instructed by the comments.
5. Generate invariants using Daikon and Defects4J by running:
  - Classical Dataset: `python petke.py`
  - Repairllama Dataset: `python repairllama.py`
6. To analyse invariants and classify patches, run:
  - Classical Dataset: `python petke_experiment.py --c 0`
  - Repairllama Dataset: `python repairllama_experiment.py --c 0`
7. Results will be saved under:
  - Classical Dataset: `petke_results.csv`
  - Repairllama Dataset: `repairllama_results.csv`

---

## LLM4PatchCorrect

- **Publication:**  
X. Zhou, B. Xu, K. Kim, D. Han, H. H. Nguyen, T. Le-Cong, J. He, B. Le, and D. Lo,
*“Leveraging large language model for automatic patch correctness assessment”*
*IEEE Transactions on Software Engineering*, vol. 50, no. 11, pp. 2865–2883, 2024.

- **Type:** Learning
- **Directory:** `LLM4PatchCorrectness`
- **Original Repository:** https://github.com/Xin-Zhou-smu/LLM4PatchCorrectness 

**Preprocessing:**

LLM4PatchCorrect required specific project attributes for each patch in its experimental setup. These included test method names exposing the bug, test method bodies exposing the bug, test coverage information, bug information as provided by Defects4J which is usually a report by a developer explaining the bug, and execution traces of failed tests. These data points were systematically extracted from Defects4J metadata and cross-verified against the original experimental artefact to confirm accuracy in format and content.

**Note: The model used by this tool requires substantial GPU power. We were able to complete our experiments using an NVIDIA RTX 3090.**

**Instructions:**

1. Run `bash install_library.sh`
  - This script is a list of dependencies which allowed us to run the experiments in our environment. If these do not work for you, we recommend starting from the original dependency list provided by the authors, which we include as `original_install_library.sh`.
2. To download the model via terminal:
  - NOTE: The download link in the repository is currently unavailable (404 Error). Thus, we have included in our repository the model we downloaded when the link was available.
  - `pip install gdown`
  - `gdown --folder https://drive.google.com/drive/folders/1MryWp2iqXAVo4UHxnN-bTspQkysM7Fpy?usp=sharing` (link from the original repository)
  - Place it under `pretrained_model/best`
3. We used deepspeed as our GPU was not selected by default: `pip install deepspeed`
4. To start the tool, run `bash run_pipeline.sh`
  - To switch between the classical and repairllama datasets, modify the first line in this script. For the classical dataset, use `'8h-deduplicated'`. For the repairllama dataset, use `'repairllama'`. 
5. To generate classifications from LLM4PatchCorrect run `python read_results_enhanced.py`
  - To switch between the classical and repairllama datasets, modify lines 19 and 20 of this script. For the classical dataset, uncomment line 19 and comment out line 20, and vice versa for the repairllama dataset.
6. Results will be saved under:
  - Classical Dataset: `8h-deduplicated_results.csv`
  - Repairllama Dataset: `repairllama_results.csv`

---

## Tian et al.

- **Publication:**  
H. Tian, K. Liu, A. K. Kabor´e, A. Koyuncu, L. Li, J. Klein, and T. F. Bissyand´e
*“Evaluating representation learning of code changes for predicting patch correctness in program repair”*
in Proceedings of the 35th *IEEE/ACM International Conference on Automated Software Engineering, ASE* ’20, (New York, NY, USA), p. 981–992, Association for Computing Machinery, 2021.

- **Type:** Learning
- **Directory:** `DL4PatchCorrectness`
- **Original Repository:** https://github.com/TruX-DTF/DL4PatchCorrectness

**Preprocessing:**
The Tian et al. tool required no additional input or metadata beyond the patch text itself.

**Instructions:**
1. Setup the server environment: 
  - `mkdir server && cd server`
  - `wget https://storage.googleapis.com/bert_models/2019_05_30/wwm_cased_L-24_H-1024_A-16.zip`
  - `unzip wwm_cased_L-24_H-1024_A-16.zip`
  - The server requires its own environment with these packages: `pip install tensorflow==1.14 && pip install bert-serving-client==1.10.0 && pip install bert-serving-server==1.10.0 && pip install protobuf==3.20.1`
  - Run: `bert-serving-start -model_dir ./wwm_cased_L-24_H-1024_A-16 -num_worker=1 -max_seq_len=360` NOTE this needs to be in a separate terminal, set num_worker to the number of gpus available otherwise the server will fail to start.
2. Setup the tool environment:
  - `pip install bert-serving-client==1.10.0 && pip install scikit-learn && pip install gensim && pip install nltk`
  - `python -m nltk.downloader punkt`
3. To classify patches, first ensure the server is running, then change your working directory to `DL4PatchCorrectness/prediction` and run:
  - `python run.py --dataset <petke|repairllama>`
    - `petke` is for the full classical dataset and `repairllama` is for the repairllama dataset.
4. Results will be saved under:
  - Classical Dataset: `patch_results_petke_dt.csv`
  - Repairllama Dataset: `patch_results_repairllama_dt.csv`

---