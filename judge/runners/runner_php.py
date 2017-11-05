from runners.runner import Runner, InitRunner
import os
import logging

logging.basicConfig(level=logging.INFO)


class PHPRunner(Runner):

    NAME = 'PHP'

    def begin_ceremony(self):
        code = (
          '<?php\n' +
          '$IN_MEMORY_NAME = $argv[1];\n' +
          '$OUT_MEMORY_NAME = $argv[2];\n' +
          '$IN_MEMORY = fopen($IN_MEMORY_NAME, "r");\n' +
          '$OUT_MEMORY = fopen($OUT_MEMORY_NAME, "w");\n'
        )
        return code

    def end_ceremony(self):
        code = (
          'fclose($IN_MEMORY);\n' +
          'fclose($OUT_MEMORY);\n' +
          '?>\n'
        )
        return code

    def load_int_vector(self, vector):
        code = (
          '${} = array();\n'.format(vector) +
          '$_ = fgets($IN_MEMORY);\n' +
          '$_ = fgets($IN_MEMORY);\n' +
          '$SIZE = fgets($IN_MEMORY);\n' +
          'for ($i = 0; $i < $SIZE; $i++) {\n' +
          '  array_push(${}, trim(fgets($IN_MEMORY)));'.format(vector) +
          '}\n'
        )
        return code

    def load_float_vector(self, vector):
        code = (
          '${} = array();\n'.format(vector) +
          '$_ = fgets($IN_MEMORY);\n' +
          '$_ = fgets($IN_MEMORY);\n' +
          '$SIZE = fgets($IN_MEMORY);\n' +
          'for ($i = 0; $i < $SIZE; $i++) {\n' +
          '  array_push(${}, trim(fgets($IN_MEMORY)));'.format(vector) +
          '}\n'
        )
        return code

    def load_str_vector(self, vector):
        code = (
          '${} = array();\n'.format(vector) +
          '$_ = fgets($IN_MEMORY);\n' +
          '$_ = fgets($IN_MEMORY);\n' +
          '$SIZE = fgets($IN_MEMORY);\n' +
          'for ($i = 0; $i < $SIZE; $i++) {\n' +
          '  array_push(${}, trim(fgets($IN_MEMORY)));'.format(vector) +
          '}\n'
        )
        return code

    def load_int(self, intt):
        code = (
          '$_ = fgets($IN_MEMORY);\n' +
          '$_ = fgets($IN_MEMORY);\n' +
          '${} = trim(fgets($IN_MEMORY));\n'.format(intt)
        )
        return code

    def load_float(self, floatt):
        code = (
          '$_ = fgets($IN_MEMORY);\n' +
          '$_ = fgets($IN_MEMORY);\n' +
          '${} = trim(fgets($IN_MEMORY));\n'.format(floatt)
        )
        return code

    def load_str(self, strr):
        code = (
          '$_ = fgets($IN_MEMORY);\n' +
          '$_ = fgets($IN_MEMORY);\n' +
          '${} = trim(fgets($IN_MEMORY));\n'.format(strr)
        )
        return code

    def save_int_vector(self, vector):
        code = (
          'fwrite($OUT_MEMORY, "VECTOR_INT:\\n");\n' +
          'fwrite($OUT_MEMORY, "{}\\n");\n'.format(vector) +
          'fwrite($OUT_MEMORY, count(${})."\\n");\n'.format(vector) +
          'for ($_i = 0; $_i < count(${}); $_i++) {{\n'.format(vector) +
          '    fwrite($OUT_MEMORY, ${}[$_i]."\\n");\n'.format(vector) +
          '}\n'
        )
        return code

    def save_float_vector(self, vector):
        code = (
          'fwrite($OUT_MEMORY, "VECTOR_FLOAT:\\n");\n' +
          'fwrite($OUT_MEMORY, "{}\\n");\n'.format(vector) +
          'fwrite($OUT_MEMORY, count(${})."\\n");\n'.format(vector) +
          'for ($_i = 0; $_i < count(${}); $_i++) {{\n'.format(vector) +
          '    fwrite($OUT_MEMORY, number_format((float)${}[$_i], 6, ".", "")."\\n");\n'.format(vector) +
          '}\n'
        )
        return code

    def save_str_vector(self, vector):
        code = (
          'fwrite($OUT_MEMORY, "VECTOR_STR:\\n");\n' +
          'fwrite($OUT_MEMORY, "{}\\n");\n'.format(vector) +
          'fwrite($OUT_MEMORY, count(${})."\\n");\n'.format(vector) +
          'for ($_i = 0; $_i < count(${}); $_i++) {{\n'.format(vector) +
          '    fwrite($OUT_MEMORY, ${}[$_i]."\\n");\n'.format(vector) +
          '}\n'
        )
        return code

    def save_int(self, intt):
        code = (
          'fwrite($OUT_MEMORY, "INT:\\n");\n' +
          'fwrite($OUT_MEMORY, "{}\\n");\n'.format(intt) +
          'fwrite($OUT_MEMORY, ${}."\\n");\n'.format(intt)
        )
        return code

    def save_float(self, floatt):
        code = (
          'fwrite($OUT_MEMORY, "FLOAT:\\n");\n' +
          'fwrite($OUT_MEMORY, "{}\\n");\n'.format(floatt) +
          'fwrite($OUT_MEMORY, ${}."\\n");\n'.format(floatt)
        )
        return code

    def save_str(self, strr):
        code = (
          'fwrite($OUT_MEMORY, "STR:\\n");\n' +
          'fwrite($OUT_MEMORY, "{}\\n");\n'.format(strr) +
          'fwrite($OUT_MEMORY, ${}."\\n");\n'.format(strr)
        )
        return code

    def prepare(self):
        code_file = open(self.codename+".php", "w")
        code_file.write(self.generate())
        code_file.close()
        return 0, ''

    def execute(self, in_memory, out_memory):
        log_fname = "{}.log_file".format(self.codename)
        command = 'php {}.php {} {} 2> {}'.format(self.codename, in_memory, out_memory, log_fname)
        return os.system(command), open(log_fname).read()

    def name(self):
        return 'PHP'


if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    runner = PHPRunner('array_push(${}, "blue", "green");'.format(
      Runner.SOME_STR_VECTOR), 'tmp/tmp')
    runner.simple_full_run('tmp/memory.txt', 'tmp/memory2_php.txt')
    print(init.load_memory('tmp/memory2_php.txt'))

    runner2 = PHPRunner('$' + Runner.SOME_FLOAT + ' = 4.5;\n', 'tmp/tmp2')
    runner2.simple_full_run('tmp/memory2_php.txt', 'tmp/memory3_php.txt')
    print(init.load_memory('tmp/memory3_php.txt'))
