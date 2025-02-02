
import os
import sys

# Set GDAL environment variables
os.environ['GDAL_DATA'] = os.path.join(sys._MEIPASS, 'Library', 'share', 'gdal')
os.environ['PROJ_LIB'] = os.path.join(sys._MEIPASS, 'Library', 'share', 'proj')
