#!/usr/bin/env python

import re
import sys

linewidth = 79

# pattern, substitution
basic_patterns = [
        (re.compile("<[^<>]*\.(pfb|png|pdf|jpe?g)( \([^)]*\))?>"),""), # remove files within <>
        (re.compile("{[^{}]*\.(enc|map)}"),""), # remove files within {}
        (re.compile(r"\n?\([^()]*\.(tex|sty|dfu|def|cfg|fd|mdf|aux|clo|bbl|out|mkii|cls|toc|ldf|dict|nav|bbx|cbx|lbx|vrb)\s*(\[[0-9]+\]\s*)*\)\n?"),""), # remove files within ()
        (re.compile(r"\s*\]"), "]"), # remove spaces in front of ]
        (re.compile(r"\](\s*\[[0-9]+\])*\s*"), "]\n"), # remove unnecessary pages
        (re.compile(r"\n\s*\n(\s*\n)*"), "\n\n"), # remove unnecessary newlines
        (re.compile(r"\n(\s*\n)*\s*\)"), " )"), # remove newlines in front of )
        (re.compile(r"(\n\s*\[\]\s*)+"), "\n"), # remove [] lines
        (re.compile(r"\n\s*(\n\s*)*(\[[0-9]+\])"), r" \g<2>"), # reformat [...] to (page ...)
        (re.compile(r"Chapter [0-9]+.\s*\[[0-9]+\]"), ""),
        (re.compile(r"Appendix [A-Z]+.\s*\[[0-9]+\]"), ""),
        (re.compile(r"\n\n+(LaTeX Warning: Citation)"), r"\n\g<1>"), # remove empty line in front of undefined reference warning
        # minted
        (re.compile(r"\n?\([^()]*\.(w18|pygstyle|pygtex)\s*(\[[0-9]+\]\s*)*\)\n?"),""), # remove files within ()
    ]

box_patterns = [
        (re.compile(r"(Under|Over)full \\.box \([^()]*\) (has occurred while \\output is active|in paragraph at lines [0-9]+--[0-9]+)"), ""),
    ]

messages = [
        "\(see the transcript file for additional information\)",
        "See the LaTeX manual or LaTeX Companion for explanation.",
        "Type  H <return>  for immediate help.",
        "Document Style algorithmicx 1.2 - a greatly improved `algorithmic' style",
        "Document Style - pseudocode environments for use with the `algorithmicx' style",
        re.escape("For additional information on amsmath, use the `?' option."),
        " ...       ",
        "Excluding '?comment'? '?comment'?\\.?",
        re.escape("*geometry* driver: auto-detecting"),
        re.escape("*geometry* detected driver: pdftex"),
        "ABD: EveryShipout initializing macros",
        "\[Loading MPS to PDF converter \(version .*\).\]",
        "Document Class: .{10,40} Standard LaTeX document class",
        "This is pdfTeX, Version [^\n]{10,250}\n",
        "entering extended mode",
        "LaTeX2e [^\n]{10,50}\n",
        "Babel .{,10} and hyphenation patterns for .{,3} language\(s\) loaded.",
        "Transcript written on[^\n]*",
        r"Output written on [^(]*\([^)]*\)\.",
        r"LaTeX Warning: Empty `thebibliography' environment on input line [0-9]+\.",
        r"LaTeX Warning: There were undefined references\.",
        r"Style option: .fancyvrb. v2.7a, with DG/SPQR fixes, and firstline=lastline fix <2008/02/07> .tvz.", # minted
        r"/usr/bin/pygmentize",
    ]

message_patterns = [(re.compile(msg), "") for msg in messages]

def apply_patterns(msg, patterns):
    for regex, subs in patterns:
        new_msg = ""
        while True:
            new_msg = regex.sub(subs, msg)
            if new_msg == msg: break
            msg = new_msg
        msg = new_msg
    return msg


def format(msg, args):
    new_msg = ""
    prev = ""
    for line in msg.split("\n"):
        if len(line) >= linewidth:
            prev += line
        else:
            new_msg += prev + line + "\n"
            prev = ""

    patterns = message_patterns + ("--no-box-warnings" and box_patterns or []) + basic_patterns
    while True:
        msg = apply_patterns(new_msg, patterns)
        if new_msg == msg:
            break
        new_msg = msg

    return msg


# to use this script as command
if __name__ == "__main__":
    msg = ""
    while 1:
        line = sys.stdin.readline()
        if not line: break
        msg += line

    print(format(msg, []))

