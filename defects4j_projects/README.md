# Defects4J Project Checkout

The script in this directory, [`checkout_d4j.py`](checkout_d4j.py), automates the process of fetching and checking out the required Defects4J projects and bug versions for use by the patch overfitting detection tools in the [`tools/`](../tools/README.md) directory of this repository.

## Usage

Run the script from the [`defects4j_projects/`](.) directory:
   > **Note:** This requires Defects4J to be installed and configured. Defects4J depends on Java 11. You must update the `JAVA_11_PATH` constant in `checkout_d4j.py` to point to a valid Java 11 installation.  
   > For setup instructions, refer to the [Defects4J GitHub repository](https://github.com/rjust/defects4j).

```sh
python checkout_d4j.py --dataset <repairllama|petke>
```

After processing, the resulting Defects4J projects can be found under `./{dataset}/buggy` and `./{dataset}/fixed`.

Backups of relevant projects which required manual tweaking since they did not behave as intended, either when checking out or when running the patch overfitting detectors, are already provided. 
