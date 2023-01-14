import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        free_cmd = "free | grep Mem | awk '{print $4/$2 * 100.0}'"
        ps = subprocess.Popen(
            free_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        output, _ = ps.communicate()
        print(int(float(output.decode("utf-8").strip())))
