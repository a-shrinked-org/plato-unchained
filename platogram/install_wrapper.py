#!/usr/bin/env python3
"""
Install the plato wrapper script to fix Poetry console script quoting bug.
This should be run after pip install to ensure the correct wrapper is in place.
"""
import os
import stat
import sys
from pathlib import Path


def install_plato_wrapper():
    """Install the correct plato wrapper script."""

    # Define the wrapper script content
    wrapper_content = '''#!/bin/sh
exec /opt/plato/bin/python -m platogram.cli "$@"
'''

    # Try common installation paths
    install_paths = [
        "/usr/local/bin/plato",
        "/usr/bin/plato",
        "/opt/plato/bin/plato"
    ]

    for path in install_paths:
        try:
            # Create directory if it doesn't exist
            Path(path).parent.mkdir(parents=True, exist_ok=True)

            # Write the wrapper script
            with open(path, 'w') as f:
                f.write(wrapper_content)

            # Make it executable
            os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

            print(f"✅ Installed plato wrapper at {path}")
            return True

        except (PermissionError, OSError) as e:
            print(f"⚠️  Could not install to {path}: {e}")
            continue

    print("❌ Could not install plato wrapper to any location")
    print("You may need to manually create the wrapper script")
    return False


if __name__ == "__main__":
    success = install_plato_wrapper()
    sys.exit(0 if success else 1)