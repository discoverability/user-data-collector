#!/usr/bin/env python3
import argparse 


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("version", help="initial version")

parser.add_argument( "--major", action='store_true', help="bump major version")
parser.add_argument("--minor", action='store_true',help="bump minor version" )
parser.add_argument( "--release", action='store_true',help="bump minor version")

args=parser.parse_args()


versions=args.version.split(".")
if (args.major and (args.minor or args.release) ) or (args.minor and (args.major or args.release)) or (args.release and (args.major or args.minor)):
	print("please use only one of major, minor, release")
else:
	if args.major:
		major=str((int)(versions[0])+1)
		minor=0
		release=0
	elif args.minor:
		major=versions[0]
		minor=str((int)(versions[1])+1)
		release=0
	elif args.release:
		major=versions[0]
		minor=versions[1]
		release=str((int)(versions[2])+1)
	print("%s.%s.%s"% (major, minor,release))