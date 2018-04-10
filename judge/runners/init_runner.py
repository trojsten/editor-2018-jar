from runners.runner import Runner
from runners.runner_python import PythonRunner

import logging

class InitRunner(Runner):
    def __init__(self, variables=None, codename=''):
        super().__init__('', codename+"init", variables)

    def create_init_memory(self, memory):
        memory = open(memory, 'w')
        for vector in self.INT_VECTORS:
            print("VECTOR_INT:\n" + vector + "\n0", file=memory)

        for intt in self.INTS:
            print("INT:\n" + intt + "\n0", file=memory)

        for vector in self.STR_VECTORS:
            print("VECTOR_STR:\n" + vector + "\n0", file=memory)

        for strr in self.STRS:
            print("STR:\n" + strr + "\n", file=memory)

        for vector in self.FLOAT_VECTORS:
            print("VECTOR_FLOAT:\n" + vector + "\n0", file=memory)

        for floatt in self.FLOATS:
            print("FLOAT:\n" + floatt + "\n0", file=memory)
        memory.close()

    def load_memory(self, memory):
        memory = open(memory, 'r')
        variables = {}
        for vector in self.INT_VECTORS:
            _ = memory.readline().strip()
            vector_name = memory.readline().strip()
            vector_size = int(memory.readline().strip())
            assert vector == vector_name
            variables[vector_name] = [int(memory.readline().strip()) for _ in range(vector_size)]

        for intt in self.INTS:
            _ = memory.readline().strip()
            intt_name = memory.readline().strip()
            intt_value = memory.readline().strip()
            assert intt == intt_name
            variables[intt_name] = int(intt_value)

        for vector in self.STR_VECTORS:
            _ = memory.readline().strip()
            vector_name = memory.readline().strip()
            vector_size = int(memory.readline().strip())
            assert vector == vector_name
            variables[vector_name] = [memory.readline().strip() for _ in range(vector_size)]

        for strr in self.STRS:
            _ = memory.readline().strip()
            strr_name = memory.readline().strip()
            strr_value = memory.readline().strip()
            assert strr == strr_name
            variables[strr_name] = strr_value

        for vector in self.FLOAT_VECTORS:
            _ = memory.readline().strip()
            vector_name = memory.readline().strip()
            vector_size = int(memory.readline().strip())
            assert vector == vector_name
            variables[vector_name] = [float(memory.readline().strip()) for _ in range(vector_size)]

        for floatt in self.FLOATS:
            _ = memory.readline().strip()
            floatt_name = memory.readline().strip()
            floatt_value = float(memory.readline().strip())
            assert floatt == floatt_name
            variables[floatt_name] = float(floatt_value)

        memory.close()
        return variables

    def prepare_memory(self, variables_with_values, filename):
        filename2 = filename + '_tmp'
        codefile = filename + '_tmp_code'
        self.create_init_memory(filename2)
        code = '\n'.join(["{} = {}".format(key, val.__repr__()) for key, val in variables_with_values.items()])
        pyrunner = PythonRunner(code, codefile, self.variables)
        pyrunner.simple_full_run(filename2, filename)

if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory_init.txt')
    print(init.load_memory('tmp/memory_init.txt'))
