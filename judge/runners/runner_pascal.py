from runners.runner import Runner, InitRunner
import os
import logging

logging.basicConfig(level=logging.INFO)


class PascalRunner(Runner):
    NAME = 'Pascal'

    def begin_ceremony(self):

        variables = (
          '\n'.join([x+': array of integer;' for x in self.INT_VECTORS]) + '\n' +
          '\n'.join([x+': array of ansistring;' for x in self.STR_VECTORS]) + '\n' +
          '\n'.join([x+': array of double;' for x in self.FLOAT_VECTORS]) + '\n' +
          '\n'.join([x+': integer;' for x in self.INTS]) + '\n' +
          '\n'.join([x+': ansistring;' for x in self.STRS]) + '\n' +
          '\n'.join([x+': double;' for x in self.FLOATS]) + '\n'
        )
        code = (
          'program PascalLine;\n' +
          'uses\n' +
          ' Sysutils;\n' +
          '\n' +
          'var\n' +
          'tfIn: TextFile;\n' +
          'tfOut: TextFile;\n' +
          'TMP_INT: integer;\n' +
          'TMP_INT2: integer;\n' +
          'TMP_STRING: ansistring;\n' +
          variables +
          'begin\n\n' +
          'assign(tfIn, ParamStr(1));\n' +
          'assign(tfOut, ParamStr(2));\n' +
          'reset(tfIn);\n' +
          'rewrite(tfOut);\n' +
          "TMP_STRING := '';"
        )
        return code

    def end_ceremony(self):
        code = (
          'close(tfIn);\n' +
          'close(tfOut);\n' +
          'end.\n'
        )
        return code

    def load_int_vector(self, vector):
        code = (
          '\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'TMP_INT := StrToInt(TMP_STRING);\n' +
          'SetLength({}, TMP_INT);\n'.format(vector) +
          'for TMP_INT2:=1 to TMP_INT do\n' +
          'begin\n' +
          '  readln(tfIn, TMP_STRING);\n' +
          '  {}[TMP_INT2] := StrToInt(TMP_STRING);\n'.format(vector) +
          'end;\n'
        )
        return code

    def load_str_vector(self, vector):
        code = (
          '\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'TMP_INT := StrToInt(TMP_STRING);\n' +
          'SetLength({}, TMP_INT);\n'.format(vector) +
          'for TMP_INT2:=1 to TMP_INT do\n' +
          'begin\n' +
          '  readln(tfIn, TMP_STRING);\n' +
          '  {}[TMP_INT2] := TMP_STRING;\n'.format(vector) +
          'end;\n'
        )
        return code

    def load_float_vector(self, vector):
        code = (
          '\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'TMP_INT := StrToInt(TMP_STRING);\n' +
          'SetLength({}, TMP_INT);\n'.format(vector) +
          'for TMP_INT2:=1 to TMP_INT do\n' +
          'begin\n' +
          '  readln(tfIn, TMP_STRING);\n' +
          '  {}[TMP_INT2] := StrToFloat(TMP_STRING);\n'.format(vector) +
          'end;\n'
        )
        return code

    def load_int(self, intt):
        code = (
          '\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          '{} := StrToInt(TMP_STRING);\n'.format(intt)
        )
        return code

    def load_float(self, floatt):
        code = (
          '\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          '{} := StrToFloat(TMP_STRING);\n'.format(floatt)
        )
        return code

    def load_str(self, strr):
        code = (
          '\n' +
          "{} := '';\n".format(strr) +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, TMP_STRING);\n' +
          'readln(tfIn, {});\n'.format(strr)
        )
        return code

    def vector_saver(self, vector, pom_str, isfloat=False):
        floatprint = '  writeln(tfOut, {}[TMP_INT2]:0:6);\n'.format(vector)
        normalprint = '  writeln(tfOut, {}[TMP_INT2]);\n'.format(vector)

        code = (
          '\n' +
          "writeln(tfOut, '{}:');\n".format(pom_str) +
          "writeln(tfOut, '{}');\n".format(vector) +
          'TMP_INT := Length({});\n'.format(vector) +
          'writeln(tfOut, TMP_INT);\n' +
          'for TMP_INT2:=1 to TMP_INT do\n' +
          'begin\n' +
          (floatprint if isfloat else normalprint) +
          'end;\n'
        )
        return code

    def save_int_vector(self, vector):
        return self.vector_saver(vector, 'VECTOR_INT')

    def save_float_vector(self, vector):
        return self.vector_saver(vector, 'VECTOR_FLOAT', True)

    def save_str_vector(self, vector):
        return self.vector_saver(vector, 'VECTOR_STR')

    def save_int(self, intt):
        code = (
          '\n' +
          "writeln(tfOut, '{}:');\n".format('INT') +
          "writeln(tfOut, '{}');\n".format(intt) +
          'writeln(tfOut, {});\n'.format(intt)
        )
        return code

    def save_float(self, floatt):
        code = (
          '\n' +
          "writeln(tfOut, '{}:');\n".format('FLOAT') +
          "writeln(tfOut, '{}');\n".format(floatt) +
          'writeln(tfOut, {}:0:6);\n'.format(floatt)
        )
        return code

    def save_str(self, strr):
        code = (
          '\n' +
          "writeln(tfOut, '{}:');\n".format('STR') +
          "writeln(tfOut, '{}');\n".format(strr) +
          'writeln(tfOut, {});\n'.format(strr)
        )
        return code

    def prepare(self):
        code_file = open(self.codename+".pas", "w")
        code_file.write(self.generate())
        code_file.close()
        command = 'fpc {}.pas'.format(self.codename, self.codename)
        logging.info("Running: %s", command)
        return os.system(command)

    def execute(self, in_memory, out_memory):
        command = './{} {} {}'.format(self.codename, in_memory, out_memory)
        logging.info('Executing: %s', command)
        return os.system(command)


if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    code1 = (
      "SetLength(" + Runner.SOME_INT_VECTOR + ", 10);\n" +
      "SetLength(" + Runner.SOME_FLOAT_VECTOR + ", 10);\n" +
      "SetLength(" + Runner.SOME_STR_VECTOR + ", 10);\n" +
      Runner.SOME_INT_VECTOR + "[3]:= 10;\n" +
      Runner.SOME_FLOAT_VECTOR + "[3]:= 10.123;\n" +
      Runner.SOME_STR_VECTOR + "[3]:= 'desat';\n" +
      Runner.SOME_INT + ":= 10;\n" +
      Runner.SOME_FLOAT + ":= 10.123;\n" +
      Runner.SOME_STR + ":= 'desat';\n"
    )
    runner1 = PascalRunner(code1, 'tmp/tmp')
    runner1.simple_full_run('tmp/memory.txt', 'tmp/memory2_pas.txt')
    memory = init.load_memory('tmp/memory2_pas.txt')
    print(memory)
