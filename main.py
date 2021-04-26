import asyncio
import sys

import qasync

from gui.main_window import main

if __name__ == "__main__":
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)
