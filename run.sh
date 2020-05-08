#!/bin/bash
clear
cc lexer.c -o lexer
./lexer p.lang

python3 astgen.py
