#!/usr/bin/python3

import copy
import datetime
import re
import os
import sys
import xml.etree.ElementTree as ET


TIMESTAMP_EX = "TODO"
LATLONGS_CHILDREN_TAG = "{http://www.topografix.com/GPX/1/1}trkpt"

def help():
    print("Usage: ./gpx_splitter.py my_file.gpx timestamp1 timestamp2 ..."
          "\n       ./gpx_splitter.py help")
    print(f"\nTimestamps should be in NOCOMMIT format, e.g. {TIMESTAMP_EX}")



def gpx_time_string_to_timestamp(s):
    if s is None:
        return None
    assert s.endswith("Z")
    return datetime.datetime.fromisoformat(f"{s[:-1]}+00:00")


def rename_tree(tree, i):
    old_name = tree.getroot()[0][0].text
    tree.getroot()[0][0].text = f"{old_name} (Split #{i + 1})"


def write_trees(trees):
    filename_base_fn = lambda i: re.match(
        r"(.*)\.gpx", sys.argv[1]).groups()[0]
    new_filename_fn = lambda i: f"{filename_base_fn(i)}-split-{i + 1}.gpx"
    for i in range(len(trees)):
        name = new_filename_fn(i)
        if os.path.isfile(name):
            print(f"{name} already exists; removing")
            os.remove(name)

    for i, tree in enumerate(trees):
        rename_tree(tree, i)
        name = new_filename_fn(i)
        tree.write(name)
        print(f"Wrote {name}")


def split_gpx(start_s, end_s):
    # latlongs live at tree.getroot()[0][3]
    # >>> p = tree.getroot()[0][3][0]
    # >>> x = p[0]
    # >>> y = p[1]
    # >>> x.text
    # '1213.3'
    # >>> y.text
    # '2023-10-29T12:27:17Z'
    # >>>
    # >>> p.items()
    # [('lat', '37.734814'), ('lon', '-119.566125')]

    tree = ET.parse(sys.argv[1])
    latlongs_node = tree.getroot()[0][3]
    start = gpx_time_string_to_timestamp(start_s)
    end = gpx_time_string_to_timestamp(end_s)
    for e in latlongs_node.findall(LATLONGS_CHILDREN_TAG):
        # using root.findall() to avoid removal during traversal
        assert len(e) == 2, f"GPX file is not in a valid format: {e}"
        e_t = gpx_time_string_to_timestamp(e[1].text)
        if ((start is not None and e_t < start) or
            (end   is not None and e_t > end)):
            latlongs_node.remove(e)
    return tree

def main():
    if (len(sys.argv) == 2 and sys.argv[1] == "help"
        or len(sys.argv) < 3
        or not sys.argv[1].endswith(".gpx")):
        help()
        sys.exit(1)

    ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
    #ET.register_namespace('', "http://www.topografix.com/GPX/1/0")
    # TODO:
    #   * inspect XML to find this^
    #   * interactively prompt user with time boundaries in their TZ
    #   * display???


    filename = sys.argv[1]
    timestamps = [None] + sorted(sys.argv[2:]) + [None]
    trees = [split_gpx(ts[0], ts[1]) for ts in zip(timestamps, timestamps[1:])]
    write_trees(trees)


if __name__ == "__main__":
    main()
