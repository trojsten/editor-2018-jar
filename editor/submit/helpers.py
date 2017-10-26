import os

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
