import subprocess

from django.core.management.base import BaseCommand

from demons.models import CheckMemoryModel


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        free_cmd = "free -h | grep Mem | awk '{print $4}'"
        ps = subprocess.Popen(
            free_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        output, _ = ps.communicate()
        value =f'free {output.decode("utf-8").strip()}'
        data = CheckMemoryModel(memory_left=value)
        data.save()
