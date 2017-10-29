from runners.runner import Runner, InitRunner
import os
import logging

logging.basicConfig(level=logging.INFO)


class PythonRunner(Runner):

    NAME = 'Python'

    def begin_ceremony(self):
        code = (
          'import sys\n' +
          'IN_MEMORY_NAME = sys.argv[1]\n' +
          'OUT_MEMORY_NAME = sys.argv[2]\n' +
          'sys = None\n' +
          'IN_MEMORY = open(IN_MEMORY_NAME, "r")\n' +
          'OUT_MEMORY = open(OUT_MEMORY_NAME, "w")\n'
        )
        return code

    def end_ceremony(self):
        code = (
          'IN_MEMORY.close()\n' +
          'OUT_MEMORY.close()\n'
        )
        return code

    def load_int_vector(self, vector):
        code = (
          vector + ' = []\n' +
          '_ = IN_MEMORY.readline()\n' +
          '_ = IN_MEMORY.readline()\n' +
          'SIZE = IN_MEMORY.readline().strip()\n' +
          'for I in range(int(SIZE)):\n' +
          '    {}.append(int(IN_MEMORY.readline()))\n'.format(vector)
        )
        return code

    def load_float_vector(self, vector):
        code = (
          vector + ' = []\n' +
          '_ = IN_MEMORY.readline()\n' +
          '_ = IN_MEMORY.readline()\n' +
          'SIZE = IN_MEMORY.readline().strip()\n' +
          'for I in range(int(SIZE)):\n' +
          '    {}.append(float(IN_MEMORY.readline()))\n'.format(vector)
        )
        return code

    def load_str_vector(self, vector):
        code = (
          vector + ' = []\n' +
          '_ = IN_MEMORY.readline()\n' +
          '_ = IN_MEMORY.readline()\n' +
          'SIZE = IN_MEMORY.readline().strip()\n' +
          'for I in range(int(SIZE)):\n' +
          '    {}.append(IN_MEMORY.readline().strip())\n'.format(vector)
        )
        return code

    def load_int(self, intt):
        code = (
          '_ = IN_MEMORY.readline()\n' +
          '_ = IN_MEMORY.readline()\n' +
          intt + ' = int(IN_MEMORY.readline().strip())\n'
        )
        return code

    def load_float(self, floatt):
        code = (
          '_ = IN_MEMORY.readline()\n' +
          '_ = IN_MEMORY.readline()\n' +
          floatt + ' = float(IN_MEMORY.readline().strip())\n'
        )
        return code

    def load_str(self, strr):
        code = (
          '_ = IN_MEMORY.readline()\n' +
          '_ = IN_MEMORY.readline()\n' +
          strr + ' = IN_MEMORY.readline().strip()\n'
        )
        return code

    def save_int_vector(self, vector):
        code = (
          'print("VECTOR_INT:", file=OUT_MEMORY)\n'.format(vector) +
          'print("{}", file=OUT_MEMORY)\n'.format(vector) +
          'print(str(len({})), file=OUT_MEMORY)\n'.format(vector) +
          'for I in {}:\n'.format(vector) +
          '    print(str(I), file=OUT_MEMORY)\n'
        )
        return code

    def save_float_vector(self, vector):
        code = (
          'print("VECTOR_FLOAT:", file=OUT_MEMORY)\n'.format(vector) +
          'print("{}", file=OUT_MEMORY)\n'.format(vector) +
          'print(str(len({})), file=OUT_MEMORY)\n'.format(vector) +
          'for I in {}:\n'.format(vector) +
          '    print("{0:.6f}".format(I), file=OUT_MEMORY)\n'
        )
        return code

    def save_str_vector(self, vector):
        code = (
          'print("VECTOR_STR:", file=OUT_MEMORY)\n'.format(vector) +
          'print("{}", file=OUT_MEMORY)\n'.format(vector) +
          'print(str(len({})), file=OUT_MEMORY)\n'.format(vector) +
          'for I in {}:\n'.format(vector) +
          '    print(I, file=OUT_MEMORY)\n'
        )
        return code

    def save_int(self, intt):
        code = (
          'print("INT:", file=OUT_MEMORY)\n'.format(intt) +
          'print("{}", file=OUT_MEMORY)\n'.format(intt) +
          'print({}, file=OUT_MEMORY)\n'.format(intt)
        )
        return code

    def save_float(self, floatt):
        code = (
          'print("FLOAT:", file=OUT_MEMORY)\n'.format(floatt) +
          'print("{}", file=OUT_MEMORY)\n'.format(floatt) +
          'print("{0:.6f}".format(%s), file=OUT_MEMORY)\n' % floatt
        )
        return code

    def save_str(self, strr):
        code = (
          'print("STR:", file=OUT_MEMORY)\n'.format(strr) +
          'print("{}", file=OUT_MEMORY)\n'.format(strr) +
          'print({}, file=OUT_MEMORY)\n'.format(strr)
        )
        return code

    def prepare(self):
        code_file = open(self.codename+".py", "w")
        code_file.write(self.generate())
        code_file.close()
        return 0, ''

    def execute(self, in_memory, out_memory):
        log_fname = "{}.log_file".format(self.codename)
        command = 'python3 {}.py {} {} 2> {}'.format(self.codename, in_memory, out_memory, log_fname)
        return os.system(command), open(log_fname).read()

    def name(self):
        return 'Python'

if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    runner = PythonRunner(Runner.SOME_STR_VECTOR + '.append("f")\n', 'tmp/tmp')
    runner.simple_full_run('tmp/memory.txt', 'tmp/memory2_py.txt')
    runner2 = PythonRunner(Runner.SOME_FLOAT_VECTOR + '.append(0.5)\n', 'tmp/tmp2')
    runner2.simple_full_run('tmp/memory2_py.txt', 'tmp/memory3_py.txt')
