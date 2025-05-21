import os
import logging
import subprocess
from datetime import datetime as dt

from .config import USER, PASSWORD, HOST, PORT, DB


logger = logging.getLogger(__name__)

def backup_db():
    backup_dir = "/app/dumps"
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = dt.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(backup_dir, f"backup-{timestamp}.dump")

    cmd = [
        "pg_dump",
        "-U", USER,
        "-h", HOST,
        "-p", PORT,
        "-d", DB,
        "-F", "c",
        "-f", backup_file
    ]
    env = os.environ.copy()
    env["PGPASSWORD"] = PASSWORD
    try:
        subprocess.run(cmd, env=env, check=True)
        logger.info(f"Backup saved to {backup_file}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Backup failed: {e}")