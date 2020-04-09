#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
from argparse import ArgumentParser, Action

class Parameters(Action):

    @staticmethod
    def parse_parameters():
        # required = True, then if no arguments then throws error and shows help
        parser = ArgumentParser(description='program_args for learning ally')
        parser.add_argument("--sarc_folder", default='/Users/georgiachanning/LA/SARC/',
                            help="directory that contains SARC pdf data")
        parser.add_argument("--lcap_folder", default='/Users/georgiachanning/LA/LCAP/',
                            help="directory that contains LCAP pdf data")
        parser.add_argument("--outfile", default='/Users/georgiachanning/LA/integrated_output.csv',
                            help="where to write output")
        parser.add_argument("--lookup_list", default='/Users/georgiachanning/LA/districts_to_focus_on.txt',
                            help="list of schools or districts to find SARCS/LCAPS for")
        parser.add_argument("--terms_list", default="/Users/georgiachanning/file.txt",
                            help="which terms would you like to search for?")
        parser.add_argument("--target", default="LCAP",
                            help="extract LCAP or SARC from Google")
        parser.add_argument("--Learning_Ally_Cali_info", default='/Users/georgiachanning/LA/CAdistricts_and_schools.csv',
                            help="Akshat's Big Google Doc or other info to combine")
        return vars(parser.parse_args())
