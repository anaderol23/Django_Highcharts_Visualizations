import os
from datetime import datetime

import django
import csv
from tqdm import tqdm

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lore_project.settings")
django.setup()
from lore_app.models import Attack

CSVPATH = "data/AWS_Honeypot_marx-geo.csv"


def get_num_rows(csvpath):
    with open(csvpath, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
        return len(data)


def has_number(s):
    return any(i.isdigit() for i in s)

total_num_rows = get_num_rows(CSVPATH) - 1
with open(CSVPATH) as f:
    reader = csv.reader(f)
    next(reader)
    rownum = 0
    for row in tqdm(reader, total=total_num_rows):
        _, created = Attack.objects.get_or_create(
            datetime=datetime.strptime(row[0], "%m/%d/%y %H:%M"),
            host=row[1],
            src=row[2],
            proto=row[3],
            type=int(row[4]) if row[4] else None,
            spt=int(row[5]) if row[5] else None,
            dpt=int(row[6]) if row[6] else None,
            srcstr=row[7],
            cc=row[8],
            country=row[9],
            locale=row[10],
            localeabbr=row[11],
            postalcode=row[12],
            latitude=row[13] if has_number(row[13]) else None,
            longitude=row[14] if has_number(row[13]) else None,
        )
