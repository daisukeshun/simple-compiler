#!/bin/bash
clear
cc -o lexer lexer.c
./lexer p.lang

python3 astgen.py

