import json
import subprocess
from datetime import datetime

from django.core.management.base import BaseCommand

from clientsviewer.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        free_cmd = "free -h | grep Mem | awk '{print $7}'"
        ps = subprocess.Popen(
            free_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        output, _ = ps.communicate()
        log = {
            "content": [str(datetime.now()), f'free {output.decode("utf-8").strip()}']
        }
        with open(f"{BASE_DIR}/logs.json", "w", encoding="utf-8") as f:
            json.dump(log, f)
