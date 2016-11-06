#!/usr/bin/env python

from argparse import ArgumentParser
import os
from os.path import abspath, dirname, join
import sys

DB_NAME = join(dirname(dirname(abspath(__file__))), 'db.sqlite3')
DUMP = 'sqlite3 {} .dump > {}'
RESTORE = 'sqlite3 {} < {}'


def write(s):
    sys.stdout.write(s)

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(
        '-r'
        '--restore',
        action='store_true',
        dest='restore',
        default=False,
        help='Restore a database.'
    )

    parser.add_argument(
        '-d'
        '--dump',
        action='store_true',
        dest='dump',
        default=False,
        help='Dump a database.'
    )

    parser.add_argument(
        '-f'
        '--file',
        action='store',
        dest='filename',
        default=None,
        help='Filename of database.'
    )

    args = parser.parse_args()

    # Check if a database action is passed.
    if not (args.dump or args.restore):
        write('Please specifiy a dump (-d) or restore (-r) option.\n')
        sys.exit(1)

    # Check if a filename is passed.
    if not args.filename:
        write('Please specify a filename (-f).\n')
        sys.exit(1)

    # Dump the database.
    if args.dump:
        cmd = DUMP.format(DB_NAME, args.filename)
        write('Dumping database with: {}\n'.format(cmd))
        os.system(cmd)

        sys.exit()

    # Restore the database.
    if args.restore:
        # Delete the existing database.
        write('Deleting existing database {}\n'.format(DB_NAME))
        try:
            os.remove(DB_NAME)
        except (FileNotFoundError):
            write('File {} not found \n'.format(DB_NAME))

        # Restore the database.
        cmd = RESTORE.format(DB_NAME, args.filename)
        write('Restoring database with: {}\n'.format(cmd))
        os.system(cmd)

        sys.exit()
