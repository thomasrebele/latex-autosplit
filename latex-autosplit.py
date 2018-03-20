#!/usr/bin/env python3
"""latex-autosplit

Usage:
    latex-autosplit.py [options] [--help] [--] <latex-file>

Options:
    --tmp-dir <directory>           Directory for saving temporary files
    -h, --help                      Show this screen
    -v, --version                   Show version
    --compile                       Compile with command
    --split-env=<env-names>         Put \\begin{env}...\\end{env} into a separate file [default: frame]
                                    (begin and end need to be on a separate line)
    --split-pre=<strings>           Cut the document in separate files. [default: \\chapter{]

"""

import subprocess
from docopt import docopt
import re
import os

class Document:

    @staticmethod
    def from_file(path):
        """Reads the content of a file and stores it in the an instance of Document"""
        if not os.path.exists(path) and os.path.exists(path + ".tex"):
            path += ".tex"
        if not os.path.exists(path):
            return Document("")
        with open(path, "r") as f:
            content = f.read()
            return Document(content)

    def write(self, path):
        """Writes the content of this instance into a file"""
        with open(path, "w") as f:
            f.write(self.content)

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content

    def resolve_input(self):
        p = re.compile(r"\\input\{(.*)\}")
        def h(match):
            input_file = match.group(1)
            return str(Document.from_file(input_file).resolve_input())

        return Document(p.sub(h, self.content))

    def split_env(self, env=[]):
        """Splits a latex document in multiple files.
        Every frame environment will be written in its own file, including the preamble of this document."""

        result = []
        preamble = ""
        part = ""
        # modes:
        # - header:     save to preamble, don't create parts
        # - normal:     save to preamble, allow switching to part
        # - env:NAME    within an environment with name NAME
        mode = ["header"]
        for line in self.content.splitlines(True):
            # determine to which mode we should switch for the next line
            if not mode[-1] == "header":
                # TODO: use regex
                for e in env:
                    if "\\begin{" + e + "}" in line:
                        mode += ["env:" + e]
                        break

            if "\\begin{document}" in line:
                mode += ["normal"]

            if mode[-1] == "header" or mode[-1] == "normal":
                preamble += line
            else:
                part += line

            if mode[-1].startswith("env:"):
                e = mode[-1][4:]
                if "\\end{" + e + "}" in line:
                    mode = mode[:-1]

                if mode[-1] == "normal":
                    result += [Document(preamble + part + "\n\\end{document}\n")]
                    part = ""

        return result

    def split_pre(self, pre=[]):
        """Splits a latex document in multiple files.
        Every frame environment will be written in its own file, including the preamble of this document."""

        result = []
        preamble = ""
        part = ""
        # modes:
        # - header:     save to preamble, don't create parts
        # - normal:     save to preamble, allow switching to part
        # - env:NAME    within an environment with name NAME
        mode = ["header"]
        for line in self.content.splitlines(True):
            if mode[-1] == "normal":
                for i in pre:
                    try:
                        idx = line.index(i)
                        if idx >= 0:
                            print("here")
                            print(part)
                            if len(part.strip()) > 0:
                                result += [Document(preamble + part + "\n\\end{document}\n")]
                                part = ""
                    except ValueError:
                        pass

            if "\\end{document}" in line:
                break

            if mode[-1] == "header":
                preamble += line
            else:
                part += line

            if "\\begin{document}" in line:
                mode += ["normal"]

        if len(part.strip()) > 0:
            result += [Document(preamble + part + "\n\\end{document}\n")]

        return result

def autosplit(prefix="", args=[]):
    tmp_dir = arguments["--tmp-dir"]
    path = tmp_dir + "/" + prefix + str(i) + ".tex"

    if str(Document.from_file(path)) != str(d):
        d.write(path)
        print("generated " + path)

        if "--compile" in arguments:
            cmd = "pdflatex -interaction nonstopmode"
            if tmp_dir != None:
                cmd += " -output-directory=" + tmp_dir
            cmd += " '\\input{" + path + "}'"
            try:
                subprocess.run(cmd, shell=True, check=True)
            except subprocess.CalledProcessError:
                pass




if __name__=='__main__':
    arguments = docopt(__doc__, version="latex-autosplit 0.01")
    print(arguments)

    input_file = arguments["<latex-file>"]
    tmp_dir = arguments["--tmp-dir"]

    doc = Document.from_file(input_file)
    doc = doc.resolve_input()
    doc.write(tmp_dir + "/all.tex")

    pre = arguments["--split-pre"].split(",")
    for i, d in enumerate(doc.split_pre(pre=pre)):
        autosplit(prefix="pre", args=arguments)

    env = arguments["--split-env"].split(",")
    for i, d in enumerate(doc.split_env(env=env)):
        autosplit(prefix="env", args=arguments)



