#!/usr/bin/env python

out_set_file = "out_set.list"

in_set_file = "in_set.list"

outs = {}

with open( out_set_file, "r") as o:
    for line in o:
        outs[ line.strip() ] = True

print "here we go"

with open( in_set_file, "r") as i:
    for line in i:
        func = line.strip()
        if not ( func in outs ):
            print func

