#!/usr/bin/python3

import copy
import datetime
import re
import os
import sys
import time
import xml.etree.ElementTree as ET


# GPX structure from GaiaGPS files:
#
# Root node:
# [('creator', 'GaiaGPS'),
#  ('version', '1.1'),
#  ('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
#   'http://www.topografix.com/GPX/1/1
#    http://www.topografix.com/GPX/1/1/gpx.xsd')]


TIMESTAMP_EX = "TODO"
LATLONGS_CHILDREN_TAG = "{http://www.topografix.com/GPX/1/1}trkpt"
BACKUP_NAMESPACE = "http://www.topografix.com/GPX/1/1"  # Gaia GPS
UTC_SUFFIX = "+00:00"
GPX_FILE_RE = re.compile(r"(.*)\.gpx")
TEXT_BOLD = "\033[1m"
TEXT_NORMAL = "\033[0m"


def sys_tz():
    # UTC fortunately does not observe daylight savings time
    return time.tzname[0]


def bold(s):
    return f"{TEXT_BOLD}{s}{TEXT_NORMAL}"


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)


def local_to_utc(local_dt):
    return local_dt.replace(tzinfo=None).astimezone(tz=datetime.timezone.utc)


def local_utc_offset():
    naive = datetime.now()
    timezone = pytz.timezone(sys_tz())
    return timezone.localize(naive).utcoffset()



def print_file_summary(tree):
    start, end = parse_for_boundary_timestamps(tree)
    span = end - start
    creator = tree.getroot().get("creator")
    print(f"{sys.argv[1]} is a GPX file by {bold(creator)}."
          f" It spans {bold(span)} hours.\n")

    print(f"The start of the GPX file is {bold(utc_to_local(start))} ({sys_tz()}) / {start} (UTC)")
    print(f"The   end of the GPX file is {bold(utc_to_local(end))} ({sys_tz()}) / {end} (UTC)")


def gpx_time_string_to_timestamp(s):
    if s is None:
        return None
    if s.endswith("Z"):
        # fromisoformat() doesn't like the Z suffix, but it means UTC, so swap
        # it out for +00:00
        s = f"{s[:-1]}{UTC_SUFFIX}"
    elif s.endswith(UTC_SUFFIX):
        pass
    else:
        print("Unexpected non-UTC timezone. Treating as UTC; all times will be"
              "off by a constant amount")
    return datetime.datetime.fromisoformat(s)


def rename_tree(tree, i):
    old_name = tree.getroot()[0][0].text
    tree.getroot()[0][0].text = f"{old_name} (Split #{i + 1})"


def write_trees(trees):
    filename_base_fn = lambda i: re.match(
        GPX_FILE_RE, sys.argv[1]).groups()[0]
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


def get_latlongs_node(node):
    if node.tag.endswith("trkseg"):
        return node
    for child in node:
        candidate = get_latlongs_node(child)
        if candidate:
            return candidate
    return None


def split_gpx(start, end):
    tree = ET.parse(sys.argv[1])
    latlongs_node = get_latlongs_node(tree.getroot())
    for e in latlongs_node.findall(LATLONGS_CHILDREN_TAG):
        # using root.findall() to avoid removal during traversal
        assert len(e) == 2, f"GPX file is not in a valid format: {e}"
        e_t = gpx_time_string_to_timestamp(e[1].text)
        if ((start is not None and e_t < start) or
            (end   is not None and e_t > end)):
            latlongs_node.remove(e)
    return tree


def register_namespace(tree):
    # The purpose of this is so that output isn't full of "ns0"s
    namespace_match = re.match(r"{(.*)}gpx", tree.getroot().tag)
    if namespace_match is None:
        print("Couldn't determine namespace from GPX file. Using"
              " a backup namespace for our new files; this may not work.")
        namespace = BACKUP_NAMESPACE
    else:
        namespace = namespace_match.groups()[0]
    ET.register_namespace("", namespace)


def parse_for_boundary_timestamp_strings(tree):
    latlongs_node = get_latlongs_node(tree.getroot())
    nodes = latlongs_node.findall(LATLONGS_CHILDREN_TAG)
    return (nodes[0][1].text, nodes[-1][1].text)


def parse_for_boundary_timestamps(tree):
    boundaries = parse_for_boundary_timestamp_strings(tree)
    return (gpx_time_string_to_timestamp(boundaries[0]),
            gpx_time_string_to_timestamp(boundaries[1]))


def prompt_user_for_timestamps(tree):
    """Returned timestamps are in UTC"""

    start = parse_for_boundary_timestamp_strings(tree)[0]
    starting_date = start[:start.find('T')]
    print(f"Please enter timestamps in your local timezone ({sys_tz()}), one by"
          " one. Each one may be in any of the following formats:"
          "\n\t1. 2023-10-29T14:25:33"
          f"\n\t2. 14:25:33 (date inferred as {starting_date})"
          "\n\t3. 14:25 (seconds inferred as :00 and date inferred"
          f" as {starting_date}"
          "\nHit Enter when you're done.")

    timestamps = []
    while True:
        ts = input("... ")
        if ts == "":
            break

        if "T" not in ts:
            ts = f"{starting_date}T{ts}"
            n_colons = len([c for c in ts if c == ":"])
            if n_colons == 1:
                ts = f"{ts}:00"

        timestamps.append(local_to_utc(datetime.datetime.fromisoformat(ts)))

    print("UTC timestamps that will be used:")
    for t in timestamps:
        print(f"\t{t}")
    print("")
    return timestamps


def validate_args():
    if len(sys.argv) != 2:
        sys.exit(1)
    if not sys.argv[1].endswith(".gpx"):
        sys.exit(1)


def main():
    validate_args()

    tree = ET.parse(sys.argv[1])
    print_file_summary(tree)
    register_namespace(tree)
    timestamps_utc = [None] + prompt_user_for_timestamps(tree) + [None]

    filename = sys.argv[1]
    trees = [split_gpx(ts[0], ts[1])
             for ts in zip(timestamps_utc, timestamps_utc[1:])]
    write_trees(trees)


if __name__ == "__main__":
    main()
