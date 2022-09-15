#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © %YEAR% %USER% <%MAIL%>
#
# Distributed under terms of the %LICENSE% license.

from pwn import *
import sys

# context.log_level = 'debug'
# context.arch = 'X86'

#########################################################
GDB_FLAV="gef" # pwndbg - gef - vanilla
BINARY=""   # path to the binary file
ENV={}      # list of enviroment variables, useful if you need to use a given library
GDB=""      # commands to execute if you debug using gdb
HOST=""     # host for remote connection
PORT=1337   # port for remote connection
#########################################################

if len(sys.argv) < 2:
    print("args: bin|net|ida|gdb\n")
    sys.exit(1)

if sys.argv[1] == "bin":
    p = process(BINARY, env=ENV)
elif sys.argv[1] == "net":
    p = remote(HOST, PORT)
elif sys.argv[1] == "ida":
    # remote ida debugger can bu found at ~/.wine/drive_c/Program\ Files/IDA\ 7.5/dbgsrv/linux_server
    p = process("./linux_server", env=ENV)
    p.recvuntil(b"0.1...")
elif sys.argv[1] == "gdb":
    p = process(BINARY, env=ENV)
    if GDB_FLAV == "vanilla":
        gdb.attach(p, gdbscript=GDB)
    else:
        gdb.attach(p, gdb_args=["-ex", "init-" + GDB_FLAV], gdbscript=GDB)
else:
    print("args: bin|net|ida|gdb")
    sys.exit(1)

binary = ELF(BINARY)    # creates an ELF object useful to access easily symbols in the binary

p.interactive()
