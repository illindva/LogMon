import os
import time
import random
import logging
from threading import Thread

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
filename = 'your_log_file.log'
log_file_full_path = os.path.join(BASE_DIR, 'logs', filename)

# Configure logging
logging.basicConfig(filename=log_file_full_path, level=logging.INFO, format='%(asctime)s - %(message)s')

log_messages = [
    "User logged in",
    "User logged out",
    "File uploaded",
    "File downloaded",
    "Error occurred",
    "Connection established",
    "Connection lost",
    "Database query executed",
    "Configuration updated"
]

def generate_random_log_entry():
    while True:
        message = random.choice(log_messages)
        logging.info(message)
        time.sleep(30)

def start_log_generator():
    log_thread = Thread(target=generate_random_log_entry)
    log_thread.daemon = True  # This makes sure the thread will exit when the main program exits
    log_thread.start()
