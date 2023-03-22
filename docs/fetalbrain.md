Example run on Fetal Brain dataset 
----------------------------------
These samples are from  (La Manno et al., 2018) and you can download them here:

Put them into a folder, lets say data/ and they will look like this:

```
10X_17_029 10X_17_028
```

or more detailed
```
data/10X_17_029
data/10X_17_029/outs
data/10X_17_029/outs/filtered_feature_bc_matrix
data/10X_17_029/outs/filtered_feature_bc_matrix/features.tsv.gz
data/10X_17_029/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
data/10X_17_029/outs/filtered_feature_bc_matrix/matrix.mtx.gz
data/10X_17_028
data/10X_17_028/outs
data/10X_17_028/outs/filtered_feature_bc_matrix
data/10X_17_028/outs/filtered_feature_bc_matrix/features.tsv.gz
data/10X_17_028/outs/filtered_feature_bc_matrix/barcodes.tsv.gz
data/10X_17_028/outs/filtered_feature_bc_matrix/matrix.mtx.gz
```

So, the data folder contains two samples called, 10X_17_028 and 10X_17_029, these will be our samples names during the analyses and the results will be generated for two separate samples. You may change the sample names by simply changing the directory names if you like. 

We can start run a __cellsnake__ minimal workflow which will generate the most basic outputs such as dimension reduction (PCA, UMAP and tSNE) and __ClusTree__ plots for these two samples. We can inspect the outputs and if we are happy with the parameters, we can do a full run.

Run this command for a __dry run__, you will see the IDs of the detected samples under data folder and the outputs which will be created by __cellsnake__.
```
cellsnake data --option minimal --dry
```
Looks fine, then trigger a minimal workflow run.
```
cellsnake data --option minimal
```