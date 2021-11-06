#!/usr/bin/env python

import re
import contextlib
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_file",
        type=argparse.FileType("r"),
        default="-",
        help="input Markdown file",
    )
    args = parser.parse_args()

    with contextlib.closing(args.input_file) as f:
        l = f.readlines()

    IN_FRONTMATTER = False
    IN_CODEBLOCK = False

    for i in l:
        if re.match(r"^---", i) != None and not IN_FRONTMATTER:  # frontmatterを表示しない
            IN_FRONTMATTER = True
        if IN_FRONTMATTER and i == "\n":
            IN_FRONTMATTER = False
            continue
        if IN_FRONTMATTER:
            continue
        if re.match(r"^```", i) != None:  # コードブロック内では置換しない
            if IN_CODEBLOCK:
                IN_CODEBLOCK = False
            else:
                IN_CODEBLOCK = True
        if not IN_CODEBLOCK:
            i = re.sub(r"^###\s", r"##### ", i)  # 小見出し
            i = re.sub(r"^##\s", r"#### ", i)  # 中見出し
            i = re.sub(r"^#\s", r"### ", i)  # 大見出し
        print(i, end="")


if __name__ == "__main__":
    main()
