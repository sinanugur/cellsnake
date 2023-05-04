Example run on Fetal Liver dataset 
----------------------------------
Cellsnake can be run directly using the snakemake workflow. We recommend the wrapper but the snakemake workflow give more control in some use cases.

Lets try workflow on Fetal Liver dataset. You can download the dataset here:



Since this dataset have 6 samples, rather than one MT percentage, make it automatic so that each sample. A minimal run is also enough, we do not want to analyze samples seperately.

```shell
snakemake -j 10 --config option=minimal percent_mt=auto
```

Then we can run integration.
```shell
snakemake -j 10 --config option=integration
```

Now it is time to work on the integrated sample. We can run full advanced run on the integrated object which is always generates at the same location.
```shell
snakemake -j 10 --config  datafolder=analyses_integrated/seurat/integrated.rds resolution=0.3 option=advanced is_integrated_sample=True --rerun-incomplete
```



