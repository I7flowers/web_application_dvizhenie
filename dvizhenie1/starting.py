import psycopg2

import dvizhenie1.Raschet
from dvizhenie1.Raschet_filling import clear_not_all, raschet


def main():
    clear_not_all()
    raschet()
    dvizhenie.Raschet.handmade_raschet()


def final():
    dvizhenie.Raschet.auto_raschet()
