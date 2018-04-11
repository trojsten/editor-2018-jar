import os
import json

from submit import constants

def write_lines_to_file(file_path, lines):
    try:
        os.makedirs(os.path.dirname(file_path))
    except os.error:
        pass

    with open(file_path, 'w+') as destination:
        for line in lines:
            destination.write("%s\n" % line)

def write_chunks_to_file(file_path, chunks):
    try:
        os.makedirs(os.path.dirname(file_path))
    except os.error:
        pass

    with open(file_path, 'wb+') as destination:
        for chunk in chunks:
            destination.write(chunk)

def get_default_custom_input(problem):
    variables = {}
    try:
        variables = json.loads(problem.variables)
    except:
        pass

    vars = []
    for group_name in variables:
        if len(variables[group_name]) == 0: continue
        for var in variables[group_name]:
            vars.append('"%s": %s' % (var, constants.DEFAULT_VAR[group_name]))

    return ',\n'.join(vars)
