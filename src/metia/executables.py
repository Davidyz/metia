#!/usr/bin/env python3
import collections
import os
import sys
from typing import Dict, Iterable, List, Union
from metia.probe import Probe

try:
    from collections import Iterable
except (AttributeError, ImportError):
    from collections.abc import Iterable


__INDENT_STRING = "  "


def pprint_list(info: List, indentation: int = 0) -> None:
    indent_str = indentation * __INDENT_STRING
    if all(isinstance(i, str) for i in info):
        info.sort()

    for i in info:
        if isinstance(i, list):
            pprint_list(i, indentation + 1)
        elif isinstance(i, dict):
            pprint_dict(i, indentation)
        else:
            print(f"{indent_str}{i}")


def pprint_dict(
    info: Dict[str, Union[Dict, str]], indentation: int = 0
) -> None:
    """
    Print the metadata of the media in a nice format.
    """
    indent_str = __INDENT_STRING * indentation
    for key in sorted(info.keys()):
        value = info[key]
        if isinstance(value, dict):
            print(f"{indent_str}{key}:")
            pprint_dict(value, indentation + 1)
        elif isinstance(value, list):
            print(f"{indent_str}{key}:")
            pprint_list(value, indentation + 1)
        else:
            print(f"{indent_str}{key}: {value}")


def print_media(media: Probe, key) -> int:
    """
    Driver function for pprint()
    """
    print(media.path)
    print(len(media.path) * "=")
    if key is None:
        pprint_dict(media.dict())
    else:
        data = find_val(media.dict(), key)
        if data != None:
            print(f"{key}: ", end="")
            if isinstance(data, dict):
                print()
                pprint_dict(data, 1)
            elif isinstance(data, list):
                print()
                pprint_list(data, 1)
            else:
                print(data)
        else:
            print(f"The key {key} is not found in the media.")
            return 1
    return 0


def find_val(original: Dict, key: str):
    q = collections.deque((original,))
    while q:
        candidate = q.popleft()
        for i in candidate.keys():
            if i == key:
                return candidate[i]
            if isinstance(candidate[i], dict):
                q.append(candidate[i])
            elif isinstance(candidate[i], Iterable) and not isinstance(
                candidate[i], str
            ):
                result = find_val_from_iter(candidate[i], key)
                if result is None:
                    continue
                return result
    return None


def find_val_from_iter(iterable: Iterable, key: str):
    q = collections.deque()
    q.append(iterable)
    while q:
        candidate = q.popleft()
        for i in candidate:
            if isinstance(i, dict):
                return find_val(i, key)
            elif isinstance(i, Iterable) and not isinstance(i, str):
                q.append(i)
    return None


def metia_probe():
    print("A tool to visualize the metadata of a media file.")
    path, key = None, None
    if len(sys.argv) == 1:
        print("Usage: media-probe [PATH_TO_MEDIA]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        path = sys.argv[1]

    elif len(sys.argv) == 3:
        path, key = sys.argv[1:]
    else:
        print("Usage: media-probe [PATH_TO_MEDIA] [key]")
        sys.exit(1)
    if not os.path.isfile(path):
        print(f"Not a valid path: {path}")
        sys.exit(1)

    meta = Probe(path)
    sys.exit(print_media(meta, key))
