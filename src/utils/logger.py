import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logger
logger = logging.getLogger('bloodprint')
logger.setLevel(logging.INFO)

# Create file handler
log_file = os.path.join('logs', f'bloodprint_{datetime.now().strftime("%Y%m")}.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(file_handler) 