
import re

linewidth = 79

# pattern, substitution
cleanup_patterns = [
        (re.compile("<[^<>]*.pfb>"),""),
        (re.compile("{[^{}]*.enc}"),""),
        (re.compile(r"\n?\([^()]*.(tex|sty|dfu|def|cfg|fd|mdf|aux|clo|bbl|out|mkii|cls)\s*\)\n?"),""),
        (re.compile(r"\n\s*\n(\s*\n)*"), "\n\n"),
        (re.compile(r"\n(\s*\n)*\s*\)"), "\n)")
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

cleanup_patterns = [(re.compile(msg), "") for msg in messages] + cleanup_patterns

def format(msg):
    new_msg = ""
    prev = ""
    for line in msg.split("\n"):
        if len(line) >= linewidth:
            prev += line
        else:
            new_msg += prev + line + "\n"
            prev = ""
    msg = new_msg

    for regex, subs in cleanup_patterns:
        new_msg = ""
        while True:
            new_msg = regex.sub(subs, msg)
            if new_msg == msg: break
            msg = new_msg
        msg = new_msg
    return msg


