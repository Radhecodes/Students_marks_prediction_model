import logging
import os
from datetime import datetime

# Step 1: Create a log file with current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Step 2: Define log folder path
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Step 3: Define full path to log file
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# Step 4: Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
# to check log file 
# if __name__=="__main__":
    # logging.info("Logging has started")