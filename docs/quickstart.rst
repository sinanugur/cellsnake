*******************
Quick start example
*******************

Run `cellsnake` in a clean directory and `cellsnake` will create the required directories while running.

After downloading the dataset, just point the data folder which contains the two dataset folders, this will trigger a standard cellsnake workflow:


.. code-block:: bash

    cellsnake standard data


After the pipeline finishes, you may also integrate these two samples:

.. code-block:: bash

    cellsnake integrate data


To determine a manual resolution parameter, you can also create only a ClusTree.

.. code-block:: bash

    cellsnake integrated clustree analyses_integrated/seurat/integrated.rds


Let's say you want a resolution of 0.1, then you can trigger a run with this resolution.

.. code-block:: bash

    cellsnake integrated standard analyses_integrated/seurat/integrated.rds --resolution 0.1


It is also possible to use automatic resolution selection, however this might be very slow in large datasets.

.. code-block:: bash

    cellsnake integrated standard analyses_integrated/seurat/integrated.rds --resolution auto

