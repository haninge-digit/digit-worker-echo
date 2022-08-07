import os
import logging
import asyncio

from worker import worker_loop
from echo import echo


""" 
Environment
"""
DEBUG_MODE = os.getenv('DEBUG','false') == "true"                       # Global DEBUG logging

LOGFORMAT = "%(asctime)s %(funcName)-10s [%(levelname)s] %(message)s"   # Log format


""" 
Starting point
"""
if __name__ == "__main__":
    if DEBUG_MODE:       # Debug requested
        logging.basicConfig(level=logging.DEBUG, format=LOGFORMAT)
    logging.basicConfig(level=logging.INFO, format=LOGFORMAT)     # Default logging level

    asyncio.run(worker_loop(echo))     # Run echo worker in an async loop

