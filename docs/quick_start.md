Quick start example
-------------------
Run `cellsnake` in a clean directory and `cellsnake` will create the required directories while running.

After downloading the dataset, just point the data folder which contains the two dataset folders, this will trigger a standard cellsnake workflow:
```
cellsnake data
```

After the pipeline finishes, you may also integrate these two samples:
```
cellsnake data --option integration
```

To determine a manual resolution parameter, you can also create only a ClusTree:
```
cellsnake data --option integration --option clustree
```

Let's say you want a resolution of 0.1, then you can trigger a run with this resolution:
```
cellsnake data --option integration --resolution 0.1
```

It is also possible to use automatic resolution selection, however this might be very slow in large datasets:
```
cellsnake data --option integration --resolution auto
```
