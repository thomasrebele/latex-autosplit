#!/usr/bin/env python3

"""latex-autosplit

Usage:
    latex-autosplit.py [options] <latex-file>

Options:
    --tmp-dir <directory>           Directory for saving temporary files
    -h, --help                      Show this screen
    -v, --version                   Show version

"""

from docopt import docopt

class Document:

    @staticmethod
    def from_file(path):
        """Reads the content of a file and stores it in the an instance of Document"""
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

    def split(self):
        """Splits a latex document in multiple files.
        Every frame environment will be written in its own file, including the preamble of this document."""
        result = []
        header = ""
        part = ""
        mode = "header"
        next_mode = mode
        for line in self.content.splitlines(True):
            # determine to which mode we should switch for the next line
            if "\\begin{frame}" in line:
                next_mode = "part"

            if mode == "header":
                header += line
            elif mode == "part":
                part += line

            if "\\end{frame}" in line:
                result += [Document(header + part + "\n\\end{document}\n")]
                part = ""
                next_mode = header

            mode = next_mode

        return result


if __name__=='__main__':
    arguments = docopt(__doc__, version="latex-autosplit 0.01")

    input_file = arguments["<latex-file>"]
    tmp_dir = arguments["--tmp-dir"]

    doc = Document.from_file(input_file)

    for i, d in enumerate(doc.split()):
        path = tmp_dir + "/test" + str(i) + ".tex"
        d.write(path)
        print("generated " + path)




