from os import system
from sys import platform
list=['termcolor','requests','pyfiglet', 'argparse']
for pip in list:
    if "linux" in platform:
        system(f'pip3 install {pip}')
    else:
        system(f'pip install {pip}')
