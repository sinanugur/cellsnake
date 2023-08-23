********
Glossary
********

Here we explain some of the terminology related to Cellsnake and Seurat.

**RDS (R Data Serialization)** files are a common format for saving R objects in RStudio, and they allow you to preserve the state of an object between R sessions. Cellsnake generated RDS files for later use, you can access them under analyses folder.

**ClusTree plot** ClusTree package allows you to produce clustering trees, a visualisation for interrogating clusterings as resolution increases. Please refer their publication for more details. You can access this plot under *technicals*.

**nFeature_RNA** is the number of genes detected in each cell. You can access this plot under *technicals*.

**nCount_RNA** is the total number of molecules detected within a cell. You can access this plot under *technicals*.

**mt.percent** Mitochondrial RNA percentage. We use "^[Mm][Tt]-" regex pattern to detect MT genes. Higher percentage of MT genes may suggest death cells.

**rp.percent** Ribosomal RNA percentage. We use "(?i)(^RP[SL])" regex pattern to detect ribosomal genes. Usually no filtering required for ribosomal genes.

**Snakemake** Snakemake is a workflow managament tool to design bioinformatics pipelines. Cellsnake contains a Snakemake workflow based on mostly Seurat which is an R based single-cell analysis tool.

**SingleR** It is an R package for annotation of single-cell RNA-seq data. **plot_annotations** predicted using SingleR package. You can also access additional plots under singler directory related to annotation.