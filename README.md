# Mu2e Manifold and Fiber Guide Bar Scanner
Software developed to measure SiPM Mounting Blocks and Fiber Guide Bars for dicounter construction at the University of Virginia for the Mu2e experiment.

Software Requirements:
- [Python 2.7](https://www.python.org/downloads/)
- OpenCV 3.2.0
- Scanning Software. For the Epson Perfection V39 scanner in the lab, [this software](https://ftp.epson.com/drivers/epson17634.exe) is recommended.

Installation Instructions:

The easiest way to install the required software is using Anaconda.
- Download and install Anaconda with Python 2.7 [here](https://www.continuum.io/downloads)
- Open a command prompt and run `conda install -c conda-forge opencv=3.2.0`


Operation Instructions:
1. Fill scanner with either SiPM Mounting Blocks or Fiber Guide Bars.
2. Using a scanner, take a scan at 2400 PPI.
4. Open a command prompt and run: `python scanner.py [path_to_new_image]`.
5. Follow the instructions at the command prompt to complete image analysis.

The directory `python/images` is provided as a place to store the images from the scanner.

It is not required that images be placed here, as long as you have the pathname of the new images. 

Images of the scanned bars and holes are stored in `python/measurements/smb_images` and `python/measurements/fgb_images`. 

Measurements for each of the holes in each of the bars are stored in `python/measurements/smb_measurements.txt` and `python/measurements/smb_measurements.txt`.
