# This app creates a web interface for lib-search_sdk
# The app is refactored from the basic tutorial to avoid from pywebio import * construction

import asyncio
import pywebio as pwb
from lib_search_sdk import load_db, get_suggestions, add_to_db

"""
Here I will try to make an async version of my little suggestion engine demo
"""

if __name__ == '__main__':
    main()