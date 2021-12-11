from utils import split_quey

content = open('test.sql', 'r').read()
print(split_quey(content))