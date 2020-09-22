#!/usr/bin/env python

# a COMPLETE passthrough to vagrant that makes use of an ansible vault

from ansible_vault import Vault
import os
import sys
import subprocess

vaultpass = os.environ.get("VAULTPASS" , None)
if vaultpass is None:
    sys.stderr.write("Set the VAULTPASS environment variable to unlock the ansible vault.\n")
    sys.exit(3)

vaultfile = os.environ.get("VAULTFILE", None)
if vaultfile is None:
    vaultfile = os.path.join(os.getcwd(), "secrets.vault")

if not os.path.isfile(vaultfile):
    sys.stderr.write("No ansible vault found in %s. Either create one or set the environment variable VAULTFILE.\n" % vaultfile)
    sys.exit(3)

vault = Vault(vaultpass)
data = vault.load(open(vaultfile).read())

# create an environment for vagrant, injecting our vault content
venv = os.environ.copy()
if data is None:
    sys.stderr.write("The ansible vault is empty. Exiting.\n")
    sys.exit(3)
for key, value in data.items():
    venv[key] = value

if len(sys.argv) >= 1:
    cmd = ["vagrant"] + sys.argv[1:]
else:
    cmd = ["vagrant"]

sys.stdout.write("Starting vagrant...\n")
subprocess.run(cmd, env=venv, shell=True, check=True)