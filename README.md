# GULPy

GULPy is a Python interface for the General Utility Lattice Program (GULP). The package provides several functions to:
 - Interface [pymatgen](https://pymatgen.org) structures and molecules and write them as GULP files, including the correct labels, shells etc.
 - Writing input files and launching GULP optimization, single-point and MD jobs
 - Parsing GULP output files

## Installation

This software requires the following packages:
- [numpy](https://numpy.org/)
- [pymatgen](https://pymatgen.org) (>= 2024.3.29)
- [pandas](https://pandas.pydata.org/) (>= 2.1)
- [rdkit](https://rdkit.org/)
- [networkx](https://networkx.github.io/)
- [PyYAML](https://github.com/yaml/pyyaml)

```bash
conda create -n gulpy python=3.14 numpy pandas networkx pyyaml rdkit pymatgen setuptools -c conda-forge
conda activate gulpy
```

Quote any version specifier you add (e.g. `"pymatgen>=2024.3.29"`), or the shell reads `>` as an output redirect.

You can then install GULPy by running

```bash
pip install .
```

## Examples

Examples on how to use the software can be found in the `tests` folders inside each module. A documentation for the package is under development.

