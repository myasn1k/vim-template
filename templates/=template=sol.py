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
GDB_FLAV="gef"    # pwndbg - gef - vanilla
BINARY=""         # path to the binary file
ENV={}            # list of enviroment variables, useful if you need to use a given library
GDB=""            # commands to execute if you debug using gdb
HOST=""           # host for remote connection
PORT=1337         # port for remote connection
DBG_PORT='12345'  # debug port, for different architectures
#########################################################

if len(sys.argv) < 2:
    print("args: bin|net|gdb\n")
    sys.exit(1)

if sys.argv[1] == "bin":
    if context.arch == 'aarch64':
        p = process(['qemu-aarch64', '-L', '/usr/aarch64-linux-gnu', BINARY])
    elif context.arch == 'riscv':
        p = process(['qemu-riscv64', '-L', '/usr/riscv64-linux-gnu', BINARY])
    else:
        p = process(BINARY, env=ENV)
elif sys.argv[1] == "net":
    p = remote(HOST, PORT)
elif sys.argv[1] == "gdb":
    if GDB_FLAV == "vanilla":
        if context.arch == 'aarch64':
            p = process(['qemu-aarch64', '-L', '/usr/aarch64-linux-gnu', '-g', DBG_PORT, BINARY])
            q = process("tmux split -v aarch64-linux-gnu-gdb -ex 'file " + BINARY + " ' -ex 'target remote localhost:" + DBG_PORT + "' -ex '" + GDB + "'", shell=True)
        elif context.arch == 'riscv':
            p = process(['qemu-riscv64', '-L', '/usr/riscv64-linux-gnu', '-g', DBG_PORT, BINARY])
            q = process("tmux split -v riscv64-linux-gnu-gdb -ex 'file " + BINARY + " ' -ex 'target remote localhost:" + DBG_PORT + "' -ex '" + GDB + "'", shell=True)
        else:
            p = process(BINARY, env=ENV)
            gdb.attach(p, gdbscript=GDB)
    else:
        if context.arch == 'aarch64':
            p = process(['qemu-aarch64', '-L', '/usr/aarch64-linux-gnu', '-g', DBG_PORT, BINARY])
            q = process("tmux split -v aarch64-linux-gnu-gdb -ex 'file " + BINARY + " ' -ex 'target remote localhost:" + DBG_PORT + "' -ex init-" + GDB_FLAV + " -ex '" + GDB + "'", shell=True)
        elif context.arch == 'riscv':
            p = process(['qemu-riscv64', '-L', '/usr/riscv64-linux-gnu', '-g', DBG_PORT, BINARY])
            q = process("tmux split -v riscv64-linux-gnu-gdb -ex 'file " + BINARY + " ' -ex 'target remote localhost:" + DBG_PORT + "' -ex init-" + GDB_FLAV + " -ex '" + GDB + "'", shell=True)
        else:
            p = process(BINARY, env=ENV)
            gdb.attach(p, gdb_args=["-ex", "init-" + GDB_FLAV], gdbscript=GDB)
else:
    print("args: bin|net|ida|gdb")
    sys.exit(1)

binary = ELF(BINARY)    # creates an ELF object useful to access easily symbols in the binary

p.interactive()
