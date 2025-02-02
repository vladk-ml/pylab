import argparse
from osgeo import gdal
import rasterio


def convert_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = ((decimal_degrees - degrees) * 60 - minutes) * 60
    return f"{degrees}°{minutes}'{seconds:.2f}\""


def main():
    parser = argparse.ArgumentParser(description='Extract the top-left coordinate from a GeoTIFF file.')
    parser.add_argument('tiff_file', help='Path to the .tiff file.')
    args = parser.parse_args()

    try:
        print(f"GDAL version: {gdal.__version__}\n")
        print(f"Rasterio version: {rasterio.__version__}\n")

        with rasterio.open(args.tiff_file) as src:
            # Get the coordinates (top-left corner)
            top_left = src.transform * (0, 0)
            
            print(f"Coordinate Reference System (CRS):")
            print(f"{src.crs}\n")
            print(f"CRS Axis Order: {src.crs.axis_info if hasattr(src.crs, 'axis_info') else 'Unknown'}\n")
            
            print(f"Coordinates as (x,y) / (longitude,latitude):")
            print(f"Decimal degrees: ({top_left[1]}, {top_left[0]})")  # Swapped to match DMS format
            print(f"DMS format: {convert_to_dms(abs(top_left[0]))}{'E' if top_left[0] >= 0 else 'W'}, "
                  f"{convert_to_dms(abs(top_left[1]))}{'N' if top_left[1] >= 0 else 'S'}\n")
            
            print(f"Coordinates as (y,x) / (latitude,longitude):")
            print(f"Decimal degrees: ({top_left[1]}, {top_left[0]})")
            print(f"DMS format: {convert_to_dms(abs(top_left[1]))}{'N' if top_left[1] >= 0 else 'S'}, "
                  f"{convert_to_dms(abs(top_left[0]))}{'E' if top_left[0] >= 0 else 'W'}\n")
            
            print(f"Image Bounds:")
            print(f"Left: {src.bounds.left}")
            print(f"Right: {src.bounds.right}")
            print(f"Top: {src.bounds.top}")
            print(f"Bottom: {src.bounds.bottom}\n")
            
            print(f"Image Size:")
            print(f"Width: {src.width} pixels")
            print(f"Height: {src.height} pixels\n")
            
            print(f"Pixel Size:")
            print(f"X resolution: {src.transform[0]}")
            print(f"Y resolution: {src.transform[4]}")

    except Exception as e:
        print(f'Error processing file: {str(e)}')


if __name__ == '__main__':
    main() 