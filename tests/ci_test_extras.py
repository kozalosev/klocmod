#!/usr/bin/env python3
import sys
from klocmod import LocalizationsContainer

if sys.argv[1] == "installed":
    installed = True
elif sys.argv[1] == "not" and sys.argv[2] == "installed":
    installed = False
else:
    sys.exit(-1)

try:
    LocalizationsContainer.from_file('language-phrases.yml')
except ImportError:
    if installed:
        sys.exit(1)
else:
    if not installed:
        sys.exit(2)
