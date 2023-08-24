************************
How to draw marker plots
************************

As explained for fetal-liver example, it is possible to visualize selected genes.

For this, you need to provide a list of genes in a file or a single gene name. Just save how you run the workflow and rerun it with the same parameters.

You can visuzalize any gene after the workflow completes.



.. code-block:: bash

    
    cellsnake standard data --resolution auto  -j 10
    
    #or on an integrated dataset
    cellsnake integrated standard analyses_integrated/seurat/integrated.rds --gene AHPS --resolution auto  -j 10

    #it is also possible to give a file with a list of genes to visualize
    cellsnake integrated standard analyses_integrated/seurat/integrated.rds --gene markers.tsv --resolution auto  -j 10
    
    
