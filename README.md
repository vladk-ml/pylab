# pylab Project

This repository contains a basic Python executable that prints "Hello world".

## Setup

1. Create the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate pylab
   ```

2. Run the Python script:
   ```bash
   python main.py
   ```

3. Package the script into an executable using PyInstaller:
   ```bash
   pyinstaller --onefile main.py
   ```

The executable will be available in the `dist` directory after packaging.
