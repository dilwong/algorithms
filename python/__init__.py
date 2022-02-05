import os
import glob

directory = os.path.dirname(__file__)
modulesList = glob.glob(os.path.join(directory, "*.py"))
__all__ = [os.path.basename(module)[:-3] for module in modulesList if (module != '__init__.py') and os.path.isfile(module)]