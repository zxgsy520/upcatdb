#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import time
import random
import logging
import argparse

from Bio import SeqIO
from Bio import Entrez

LOG = logging.getLogger(__name__)

__version__ = "v1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


Entrez.email = "mingyan24@126.com"

def read_id(file):

    ids = []

    for line in open(file, 'r'):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        line=line.split("\t")
        ids.append(line[0])

    return ids


def get_taxid(file, database="protein"):

    data = read_id(file)

    for i in data:
        handle = Entrez.efetch(db=database, id=i, rettype="gb")
        fh = SeqIO.parse(handle, "genbank")

        for record in fh:
            for seqdict in record.features:
                if seqdict.type != "source":
                    continue
                if "db_xref" not in seqdict.qualifiers:
                    continue
                taxid = seqdict.qualifiers["db_xref"][0]
                taxid = taxid.split(":")[1]
                print("%s\t%s" % (i, taxid))
                break
            break

    return 0


def add_help_parser(parser):

    parser.add_argument("input", metavar="FILE",
        help="Enter a file containing sequence information on NCBI.")
    parser.add_argument("-db", "--database", metavar="STR", type=str, default="protein",
        help="Enter the name of the database(nucleotide or protein, default=nucleotide.")

    return parser


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
name:
    get_taxid.py

attention:
    get_taxid.py un.id --database protein >fastaid2taxid.tsv


version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_help_parser(parser).parse_args()

    get_taxid(args.input, args.database)


if __name__ == "__main__":

    main()
