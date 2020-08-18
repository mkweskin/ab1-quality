# ab1-quality

Reads AB1 files in the selected directory and returns: Well, Q20 length and full length.
In this script Q20 length is the number of bases with quality of at least 20, bases <Q20 are omitted regardless of their position in the sequence, that is, it's not just trimming from the ends, but any position.
This script uses Tkinter for a GUI interface, see below for building as a standalone Windows .exe.
Note: this script does not find ab1 in nested directories, only the top level of the directory provided.

![Sample output](quality.jpg)

## Building standalone Windows version

On a Windows system, install miniconda, then create this environment:
```
conda create -n pyinstaller -c conda-forge python=2 biopython pyinstaller
```

and build with this:

```
conda activate pyinstaller
pyinstaller quality.py
```

The standalone program is in the dist\quality directory. Start by opening `quality.exe`. You will need the entire quality directory to run `quality.exe`.
