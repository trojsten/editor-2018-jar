from runners.runner import Runner

import os
import logging

logging.basicConfig(level=logging.INFO)


class RRunner(Runner):

    NAME = 'R'

    def begin_ceremony(self):
        code = (
          '#!/usr/bin/env Rscript\n' + 
          'args <- commandArgs(trailingOnly=TRUE);\n' +
          'IN_MEMORY <- file(args[1], "r");\n'
          'OUT_MEMORY <- file(args[2], "w");\n'
        )
        return code

    def end_ceremony(self):
        code = (
          'close(IN_MEMORY);\n' +
          'close(OUT_MEMORY);\n'
        )
        return code

    def load_int_vector(self, vector):
        code = (
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          'SIZE <- readLines(IN_MEMORY, n = 1);\n' +
          '{} <- c();\n'.format(vector) +
          'if (SIZE > 0) {\n' +
          '    {} <- c(1:SIZE);\n'.format(vector) +
          '    for (I in 1:SIZE) {\n' +
          '        {}[I] <- as.integer(readLines(IN_MEMORY, n = 1));\n'.format(vector) + 
          '    }\n' +
          '}\n'
        )
        return code

    def load_float_vector(self, vector):
        code = (
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          'SIZE <- readLines(IN_MEMORY, n = 1);\n' +
          'if (SIZE > 0) {\n' +
          '    {} <- c(1:SIZE);\n'.format(vector) +
          '    for (I in 1:SIZE) {\n' +
          '        {}[I] <- as.double(readLines(IN_MEMORY, n = 1));\n'.format(vector) + 
          '    }\n' +
          '} else {\n' +
          '    {} <- c();\n'.format(vector) +
          '}\n'
        )
        return code

    def load_str_vector(self, vector):
        code = (
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          'SIZE <- readLines(IN_MEMORY, n = 1);\n' +
          '{} <- c(1:SIZE);\n'.format(vector) +
          'if (SIZE > 0) {\n' +
          '    for (I in 1:SIZE) {\n' +
          '        {}[I] <- readLines(IN_MEMORY, n = 1);\n'.format(vector) + 
          '    }\n' +
          '}\n'
        )
        return code

    def load_int(self, intt):
        code = (
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          '{} <- as.integer(readLines(IN_MEMORY, n = 1));\n'.format(intt)
        )
        return code

    def load_float(self, floatt):
        code = (
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          '{} <- as.double(readLines(IN_MEMORY, n = 1));\n'.format(floatt)
        )
        return code

    def load_str(self, strr):
        code = (
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          'FAKE_SHIT <- readLines(IN_MEMORY, n = 1);\n' +
          '{} <- readLines(IN_MEMORY, n = 1);\n'.format(strr)
        )
        return code

    def save_int_vector(self, vector):
        code = (
          'writeLines("VECTOR_INT:", con = OUT_MEMORY);\n' +
          'writeLines("{}", con = OUT_MEMORY);\n'.format(vector) +
          'SIZE <- length({});\n'.format(vector) +
          'writeLines(as.character(SIZE), con = OUT_MEMORY);\n' +
          'if (SIZE > 0) {\n' +
          '    for (I in %s) {\n' % (vector, ) +
          '        writeLines(as.character(I), con = OUT_MEMORY);\n'
          '    }\n'
          '}\n'
        )
        return code

    def save_float_vector(self, vector):
        code = (
          'writeLines("VECTOR_FLOAT:", con = OUT_MEMORY);\n' +
          'writeLines("{}", con = OUT_MEMORY);\n'.format(vector) +
          'SIZE <- length({});\n'.format(vector) +
          'writeLines(as.character(SIZE), con = OUT_MEMORY);\n' +
          'if (SIZE > 0) {\n' +
          '    for (I in %s) {\n' % (vector, ) +
          '        writeLines(as.character(I), con = OUT_MEMORY);\n'
          '    }\n'
          '}\n'
        )
        return code

    def save_str_vector(self, vector):
        code = (
          'writeLines("VECTOR_STR:", con = OUT_MEMORY);\n' +
          'writeLines("{}", con = OUT_MEMORY);\n'.format(vector) +
          'SIZE <- length({});\n'.format(vector) +
          'writeLines(as.character(SIZE), con = OUT_MEMORY);\n'.format(vector) +
          'if (SIZE > 0) {\n' +
          '    for (I in %s) {\n' % (vector, ) +
          '        writeLines(as.character(I), con = OUT_MEMORY);\n'
          '    }\n'
          '}\n'
        )
        return code

    def save_int(self, intt):
        code = (
          'writeLines("INT:", con = OUT_MEMORY);\n' +
          'writeLines("{}", con = OUT_MEMORY);\n'.format(intt) +
          'writeLines(as.character({}), con = OUT_MEMORY);\n'.format(intt)
        )
        return code

    def save_float(self, floatt):
        code = (
          'writeLines("FLOAT:", con = OUT_MEMORY);\n' +
          'writeLines("{}", con = OUT_MEMORY);\n'.format(floatt) +
          'writeLines(as.character({}), con = OUT_MEMORY);\n'.format(floatt)
        )
        return code

    def save_str(self, strr):
        code = (
          'writeLines("STR:", con = OUT_MEMORY);\n' +
          'writeLines("{}", con = OUT_MEMORY);\n'.format(strr) +
          'writeLines(as.character({}), con = OUT_MEMORY);\n'.format(strr)
        )
        return code

    def prepare(self):
        code_file = open(self.codename+".r", "w")
        code_file.write(self.generate())
        code_file.close()
        return 0, ''

    def execute(self, in_memory, out_memory):
        log_fname = "{}.log_file".format(self.codename)
        command = 'Rscript {}.r {} {} 2> {}'.format(self.codename, in_memory, out_memory, log_fname)
        return os.system(command), open(log_fname).read()


if __name__ == '__main__':
    from runners.init_runner import InitRunner
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    init.create_init_memory('tmp/memory2.txt') # just to be sure
    init.create_init_memory('tmp/memory3.txt') # just to be sure
    runner = RRunner(
      '{} <- c({}, "f");\n'.format(init.SOME_STR_VECTOR, init.SOME_STR_VECTOR) +
      '{} <- c({}, 0.112, 0.4652);\n'.format(init.SOME_FLOAT_VECTOR, init.SOME_FLOAT_VECTOR) +
      '{} <- ({}+5)*5;\n'.format(init.SOME_INT, init.SOME_INT) 
      , 'tmp/tmp')
    runner.simple_full_run('tmp/memory.txt', 'tmp/memory2.txt')
    mem = init.load_memory('tmp/memory2.txt')
    print(mem)
    assert mem[init.SOME_FLOAT_VECTOR] == [0.112, 0.4652]
    assert mem[init.SOME_STR_VECTOR] == ['1', '0', 'f']
    assert mem[init.SOME_INT] == 25
    runner.simple_full_run('tmp/memory2.txt', 'tmp/memory3.txt')
    mem = init.load_memory('tmp/memory3.txt')
    print(mem)
    assert mem[init.SOME_FLOAT_VECTOR] == [0.112, 0.4652, 0.112, 0.4652]
    assert mem[init.SOME_STR_VECTOR] == ['1', '0', 'f','f']
    assert mem[init.SOME_INT] == 150


