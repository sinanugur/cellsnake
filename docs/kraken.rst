*********************
Metagenomics analysis
*********************

Cellsnake releases **Kraken2** for metagenomics analysis. However, you need to download a Kraken2 database before running Cellsnake. 

You can download one from the following link: https://benlangmead.github.io/aws-indexes/k2

Once you have downloaded the database, you need to specify the path to the database in the config file or as a parameter. Cellsnake looks for "inspect.txt" to check if the database is valid.

Only cellranger outputs are supported for this analysis so you need RAW outputs from cellranger as well. If both cellranger outputs and a valid kraken2 database are present, cellsnake will automatically detect them and run the analysis. 
However, if they are absent or not accessible, cellranger may send a warning or skip metagenome results.


.. code-block:: bash

    #kraken_db_folder: /path/to/kraken2_db
    cellsnake minimal data --config config.yaml 
    
    #or as a parameter
    cellsnake minimal data --kraken_db_folder /path/to/kraken2_db
    #we can use the snakemake workflow in a similar way
    snakemake -j 10 --config option=minimal kraken_db_folder=/path/to/kraken2_db


    #since confidence and min_hit_groups are very important parameters to decrease false positives for karaken2 analysis, we can specify them in the config file or as a parameter as well.
    #if you do not specify them, the default values will be used and written into folders accordingly.
    #you can later supply alternative values for these parameters in the config file or as a parameter which create another folder.
    #you can compare the results of different parameters later on.
    #for example, if you want to run the analysis with confidence 0.5 and min_hit_groups 2, you can do the following:

    cellsnake minimal data --config config.yaml --confidence 0.5 --min_hit_groups 2 #assuming config.yaml has the kraken_db_folder parameter.

    #after integration, you if you select the same confidence and min_hit_groups params, the results will be reported under results_integrated folder as expected.

    #for example
    cellsnake integrate data --config config.yaml --confidence 0.5 --min_hit_groups 2 #the results are integrated with this command
    cellsnake integrated minimal analyses_integrated/seurat/integrated.rds --config config.yaml --confidence 0.5 --min_hit_groups 2 #the integrated sample is processed and the metagenome analysis will be reported under results_integrated folder.


.. note::

    When metagenome analyses finish for all the samples in parallel with the main workflow, they will be automatically merged into a single file for later integration. Therefore, you do not need to worry. 
    