import json
import glob
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from submit.models import Problem


class Command(BaseCommand):
    help = 'Populate Problems from tests directory.'

    def add_arguments(self, parser):
        parser.add_argument('path_to_test_dir', type=str)

    def _populate_problems(self, dir_path):

        order = 1
        used_orders = set([p.order for p in Problem.objects.all()])
        for input_path in sorted(glob.glob('%s/*/variables.json' % dir_path), key=lambda x : int(x.split('/')[-2])):
            problem_id = int(os.path.dirname(input_path).split('/')[-1])
            if problem_id < 1: continue

            with open(input_path, 'r') as json_file:
                json_txt = json_file.read()

                problem = Problem.objects.filter(id=problem_id).first()

                if problem is None:
                    while order in used_orders: order += 1
                    problem, _ = Problem.objects.update_or_create(
                        id=problem_id,
                        title='Uloha %d' % problem_id,
                        content='a',
                        variables=json_txt,
                        order=order,
                    )
                    self.stdout.write(self.style.NOTICE('Created %s problem' % problem.title))
                    order += 1
                else:
                    Problem.objects.update_or_create(
                        id=problem_id,
                        variables=json_txt,
                    )
                    self.stdout.write(self.style.NOTICE('Updated %s problem' % problem.title))

    def handle(self, *args, **options):
        self._populate_problems(options['path_to_test_dir'])
