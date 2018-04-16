#!/bin/bash

rm -r judge/tmp/
mkdir judge/tmp/
rm -r judge/submits
rm -r editor/editor/submit/
rm editor/db.sqlite3

cd editor
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_problems ../judge/test/
