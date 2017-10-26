from runner import Runner, InitRunner
import os
import logging


class PythonRunner(Runner):

    NAME = 'Python'

    def begin_ceremony(self):
        code = (
          'import sys\n' +
          'IN_MEMORY_NAME = sys.argv[1]\n' +
          'OUT_MEMORY_NAME = sys.argv[2]\n' +
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
        return vector + ' = list(map(int, IN_MEMORY.readline().split()[2:]))\n'

    def load_str_vector(self, vector):
        code = (
          vector + ' = []\n' +
          '_, SIZE = IN_MEMORY.readline().split()[:2]\n' +
          'for I in range(int(SIZE)):\n' +
          '    {}.append(IN_MEMORY.readline())\n'.format(vector)
        )
        return code

    def load_int(self, intt):
        return intt + ' = int(IN_MEMORY.readline().split()[1])\n'

    def load_str(self, strr):
        code = (
          '_ = IN_MEMORY.readline()\n' +
          strr + ' = IN_MEMORY.readline().strip()\n'
        )
        return code

    def save_int_vector(self, vector):
        code = (
          'print("{} ", file=OUT_MEMORY, end="")\n'.format(vector) +
          'print(str(len({}))+" ", file=OUT_MEMORY, end="")\n'.format(vector) +
          'print("".join(map(str, {})), file=OUT_MEMORY)\n'.format(vector)
        )
        return code

    def save_str_vector(self, vector):
        code = (
          'print("{} ", file=OUT_MEMORY, end="")\n'.format(vector) +
          'print(str(len({})), file=OUT_MEMORY)\n'.format(vector) +
          'for I in {}:\n'.format(vector) +
          '    print(I, file=OUT_MEMORY)\n'
        )
        return code

    def save_int(self, intt):
        code = (
          'print("{} ", file=OUT_MEMORY, end="")\n'.format(intt) +
          'print({}, file=OUT_MEMORY)\n'.format(intt)
        )
        return code

    def save_str(self, strr):
        code = (
          'print("{}", file=OUT_MEMORY)\n'.format(strr) +
          'print({}, file=OUT_MEMORY)\n'.format(strr)
        )
        return code

    def prepare(self, codename):
        # Nothing to do for python.
        pass

    def execute(self, codename, in_memory, out_memory):
        command = 'python3 {} {} {}'.format(codename, in_memory, out_memory)
        os.system(command)

    def name(self):
        return 'Python'

if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    runner = PythonRunner()
    runner.simle_full_run('vs1.append("f")\n', 'tmp/tmp.py', 'tmp/memory.txt', 'tmp/memory2_py.txt')