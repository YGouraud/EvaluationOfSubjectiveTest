import subprocess
import sys

try:
    import pandas
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pandas'])
finally:
    import pandas

try:
    import tkinter
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'tkinter'])
finally:
    import tkinter

try:
    import matplotlib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'matplotlib'])
finally:
    import matplotlib

try:
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'numpy'])
finally:
    import numpy as np

try:
    import scipy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'scipy'])
finally:
    import scipy


try:
    import xlrd
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'xlrd'])
finally:
    import xlrd

try:
    import pandastable
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pandastable'])
finally:
    import pandastable


