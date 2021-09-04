#This is in order to have an import which will always work regardless of installation method
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fastdiff