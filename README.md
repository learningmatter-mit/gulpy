# GULPy

GULPy is a Python interface for the General Utility Lattice Program (GULP). The package provides several functions to:
 - Interface [pymatgen](https://pymatgen.org) structures and molecules and write them as GULP files, including the correct labels, shells etc.
 - Writing input files and launching GULP optimization, single-point and MD jobs
 - Parsing GULP output files

## Installation

This software requires the following packages:
- [numpy](https://numpy.org/)
- [pymatgen](https://pymatgen.org)
- [pandas](https://pandas.pydata.org/)
- [rdkit](https://rdkit.org/)
- [networkx](https://networkx.github.io/)
- [PyYAML](https://github.com/yaml/pyyaml)

```bash
conda upgrade conda
conda create -n gulpy python=3.7 numpy pandas networkx pymatgen>=2020.3.2 scikit-learn -c conda-forge
conda activate gulpy
conda install rdkit -c rdkit
```

You can then install GULPy by running

```bash
pip install .
```

## Examples

Examples on how to use the software can be found in the `tests` folders inside each module. A documentation for the package is under development.

