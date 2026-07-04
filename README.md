# Thornoise2: Noise Generation Library

## Overview
Thornoise2 is a library designed for generating noise in both Python and C. The library leverages a mathematical model built on the fractal combination of splines. For an in-depth look at the underlying algorithm, refer to the paper https://arxiv.org/abs/1610.03525.

## Features
- Noise generation in Python and C
- Efficient algorithms based on advanced mathematical models
- Supports both NumPy and pure Python implementations
- Examples included to help get you started

## Installation
Simply clone this repository or download the source code to get started. Not published on pip for the moment.

## Quick Start

### Running the NumPy Example
To run the NumPy-based example, navigate to the parent folder of Thornoise2 and execute the following command:
```bash
python -m thornoise2.examples.example_numpygen
```

### Running the Pure Python Example
A more pedagogical but slower implementation is available in pure Python. To run this example, use:
```bash
python -m thornoise2.examples.example_purepython
```
