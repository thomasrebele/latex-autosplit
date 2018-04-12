
import re

linewidth = 79

# pattern, substitution
basic_patterns = [
        (re.compile("<[^<>]*\.(pfb|png)>"),""), # remove files within <>
        (re.compile("{[^{}]*\.(enc|map)}"),""), # remove files within {}
        (re.compile(r"\n?\([^()]*\.(tex|sty|dfu|def|cfg|fd|mdf|aux|clo|bbl|out|mkii|cls)\s*(\[[0-9]+\]\s*)*\)\n?"),""), # remove files within ()
        (re.compile(r"\s*\]"), "]"), # remove spaces in front of ]
        (re.compile(r"\](\s*\[[0-9]+\])*\s*"), "]\n"), # remove unnecessary pages
        (re.compile(r"\n\s*\n(\s*\n)*"), "\n\n"), # remove unnecessary newlines
        (re.compile(r"\n(\s*\n)*\s*\)"), " )"), # remove newlines in front of )
        (re.compile(r"\n(\s*\[\]\s*\n)+\s*"), "\n"), # remove [] lines
        (re.compile(r"\n(\s*\n\s*)*\[([0-9]+)\]"), r" (page \g<2>)\n"), # reformat [...] to (page ...)
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
        "Excluding comment 'comment'",
        re.escape("*geometry* driver: auto-detecting"),
        re.escape("*geometry* detected driver: pdftex"),
        "ABD: EveryShipout initializing macros",
        "\[Loading MPS to PDF converter \(version .*\).\]",
        "Document Class: report .{10,20} Standard LaTeX document class",
        "This is pdfTeX, Version [^\n]{10,250}\n",
        "entering extended mode",
        "LaTeX2e [^\n]{10,50}\n",
        "Babel .{,10} and hyphenation patterns for .{,3} language\(s\) loaded.",
        "Transcript written on[^\n]*"
    ]

message_patterns = [(re.compile(msg), "") for msg in messages]

def format(msg, args):
    new_msg = ""
    prev = ""
    for line in msg.split("\n"):
        if len(line) >= linewidth:
            prev += line
        else:
            new_msg += prev + line + "\n"
            prev = ""
    msg = new_msg

    cleanup_patterns = message_patterns + ("--no-box-warnings" and box_patterns or []) + basic_patterns
    for regex, subs in cleanup_patterns:
        new_msg = ""
        while True:
            new_msg = regex.sub(subs, msg)
            if new_msg == msg: break
            msg = new_msg
        msg = new_msg

    return msg


