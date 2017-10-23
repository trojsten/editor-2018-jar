import argparse
import os

parser = argparse.ArgumentParser(description='Run a line of code.')
parser.add_argument('line', type=str, help='line of code to execute')
parser.add_argument('infile', type=str, help='file with input variable state')
parser.add_argument('outfile', type=str, help='file to write output variable state')

args = parser.parse_args()
line, infile, outfile = args.line, args.infile, args.outfile

template = open('template.py', 'r')
template_lines = ''.join(template.readlines())
template.close()

template_lines = template_lines.replace('%INFILE%', infile)\
    .replace('%OUTFILE%', outfile).replace('%LINE%', line)

tmp_out = open('tmp.py', 'w')
tmp_out.write(template_lines)
tmp_out.close()

os.system('python tmp.py')

os.remove('tmp.py')
