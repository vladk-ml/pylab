# PyLab Image Processing Tool

A Windows-compatible image processing application built with Python and CustomTkinter, packaged using Nuitka.

## Development Setup

1. Install Miniconda or Anaconda
2. Create the environment:
   ```bash
   conda env create -f environment.yml
   conda activate pylab
   ```

## Building with Nuitka

To build the application:
   ```bash
   python -m nuitka --follow-imports --enable-plugin=tk-inter --windows-disable-console --output-dir=dist main.py
   ```

## Project Structure

- `src/` - Source code
- `tests/` - Test files
- `resources/` - Application resources
- `dist/` - Distribution files

## Development Guidelines

1. Use Black for code formatting
2. Run tests with pytest before commits
3. Follow PEP 8 style guidelines

## Features

- Modern GUI with CustomTkinter
- Image processing capabilities
- GDAL/Rasterio integration for geospatial data
- Single-executable deployment
