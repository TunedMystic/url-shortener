#!/usr/bin/env python

# Generate an ssl certificate and key.
# 1) Create a private server key.
# 2) Create a certificate signing request.
# 3) Remove the passphrase.
# 4) Sign the SSL certificate.
# 5) Remove copied files.

import os
import optparse

parser = optparse.OptionParser()
parser.add_option(
    "-o", "--output",
    dest="output",
    action="store",
    default="server"
)


# Accept a path, and return directory (if exists) and filename.
def parse_path(path):
    name = os.path.basename(path)
    path = os.path.dirname(path)
    # Set default file name.
    name = "server" if not name else name
    return name.split(".")[0], path


# Rejoin directory with filename (with an extension).
def custom_path(name, path, ext):
    return os.path.join(path, name + "." + ext)


if __name__ == "__main__":
    args, extra = parser.parse_args()

    # Get the filename and directory path from args.
    name, path = parse_path(args.output)

    # 1) Create a private server key.
    cmd_1 = " ".join([
        "sudo openssl genrsa -des3 -out",
        custom_path(name, path, "key"),
        "2048"
    ])

    # 2) Create a certificate signing request.
    cmd_2 = " ".join([
        "sudo openssl req -new -key",
        custom_path(name, path, "key"),
        "-out",
        custom_path(name, path, "csr")
    ])

    # 3) Remove the passphrase.
    cmd_3_a = " ".join([
        "sudo cp",
        custom_path(name, path, "key"),
        custom_path(name, path, "key.org"),
    ])

    cmd_3_b = " ".join([
        "sudo openssl rsa -in",
        custom_path(name, path, "key.org"),
        "-out",
        custom_path(name, path, "key"),
    ])

    # 4) Sign the SSL certificate.
    cmd_4 = " ".join([
        "sudo openssl x509 -req -days 365 -in",
        custom_path(name, path, "csr"),
        "-signkey",
        custom_path(name, path, "key"),
        "-out",
        custom_path(name, path, "crt"),
    ])

    # 5) Remove copied files.
    cmd_5 = " ".join([
        "sudo rm",
        custom_path(name, path, "key.org"),
    ])

    os.system(cmd_1)
    os.system(cmd_2)
    os.system(cmd_3_a)
    os.system(cmd_3_b)
    os.system(cmd_4)
    os.system(cmd_5)
