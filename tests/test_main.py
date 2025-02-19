import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import ImageProcessingApp

def test_app_creation():
    """Test that the application can be created without errors"""
    app = ImageProcessingApp()
    assert app.title() == "PyLab Image Processing"
    assert app.geometry().split('+')[0] == "1024x768"
    app.destroy()

def test_initial_widgets():
    """Test that all initial widgets are created"""
    app = ImageProcessingApp()
    
    # Check main components exist
    assert hasattr(app, 'main_frame')
    assert hasattr(app, 'image_frame')
    assert hasattr(app, 'button_frame')
    assert hasattr(app, 'load_button')
    
    app.destroy() 