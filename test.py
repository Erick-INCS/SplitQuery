#!/usr/bin/env python3
"""Test the main functionality"""

from utils import split_quey

content = open('test.sql', 'r').read()
print('+' * 50)
print(split_quey(content, 'tb', 'tmp')[-1].deps)

print("\n")

