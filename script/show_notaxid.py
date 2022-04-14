#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
import argparse

LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep="\t"):

    for line in open(file):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)


def show_notaxid(fa2taxid, taxid):

    r = set()

    for line in read_tsv(taxid, sep="\t"):
        r.add(line[0])
    
    LOG.info("show taxid")
    for line in read_tsv(fa2taxid, sep="\t"):
        if line[1] not in r:
            LOG.info("\t".join(line))
            continue
        print("\t".join(line))


    return 0


def add_help_parser(parser):

    parser.add_argument("fa2taxid", metavar="FILE", type=str,
        help="Input sequence id and tax id mapping file.")
    parser.add_argument("-ti", "--taxid", metavar="FILE", type=str, required=True,
        help="Input the taxid file.")

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
    show_notaxid.py

attention:
    show_notaxid.py 2021-01-07.nr.fastaid2LCAtaxid --taxid Viruses.taxid >new_fastaid2LCAtaxid 2>log


version: %s
contact:  %s <%s>\
        ''' % (__version__, ' '.join(__author__), __email__))

    args = add_help_parser(parser).parse_args()

    show_notaxid(args.fa2taxid, args.taxid)


if __name__ == "__main__":

    main()
