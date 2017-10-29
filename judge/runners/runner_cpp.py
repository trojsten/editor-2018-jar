from runners.runner import Runner, InitRunner
import os
import logging

logging.basicConfig(level=logging.INFO)


class CppRunner(Runner):
    NAME = 'C++'

    def begin_ceremony(self):
        code = (
          '#include <cstdio>\n' +
          '#include <iostream>\n' +
          '#include <iomanip>\n' +
          '#include <algorithm>\n' +
          '#include <fstream>\n' +
          '#include <vector>\n' +
          '#include <cmath>\n' +
          '#include <string>\n' +
          'using namespace std;\n' +
          '\n' +
          'char BUFFER[600000];\n' +
          'string BUFFERS;\n' +
          'int BUFFER_SIZE;\n' +
          'int main(int argc, char *argv[]){ \n' +
          '\n' +
          'string TMP_STR;\n' +
          'int TMP_INT;\n' +
          'ifstream IN_MEMORY;\n' +
          'ofstream OUT_MEMORY;\n' +
          'IN_MEMORY.open(argv[1]); \n' +
          'OUT_MEMORY.open(argv[2]); \n'
        )
        return code

    def end_ceremony(self):
        code = (
          'IN_MEMORY.close();\n'
          'OUT_MEMORY.close();\n'
          '\nreturn 0;\n' +
          '}\n'
        )
        return code

    def load_vector(self, vector, vector_type, fun=''):
        code = (
          '\n' +
          'vector<{}> {};\n'.format(vector_type, vector) +
          'getline(IN_MEMORY, BUFFERS);\n' +
          'getline(IN_MEMORY, BUFFERS);\n' +
          'getline(IN_MEMORY, BUFFERS);\n' +
          'TMP_INT = stoi(BUFFERS);\n' +
          '{}.resize(TMP_INT);\n'.format(vector) +
          'for(int I=0; I<TMP_INT; I++){\n' +
          '  getline(IN_MEMORY, BUFFERS);\n' +
          '  {}[I] = {}(BUFFERS);\n'.format(vector, fun) +
          '}\n'
        )
        return code

    def load_int_vector(self, vector):
        return self.load_vector(vector, "int", 'stoi')

    def load_str_vector(self, vector):
        return self.load_vector(vector, "string", '')

    def load_float_vector(self, vector):
        return self.load_vector(vector, "float", 'stof')

    def load_var(self, var_name, var_type, fun=''):
        code = (
          '\n' +
          '{} {};\n'.format(var_type, var_name) +
          'getline(IN_MEMORY, BUFFERS);\n' +
          'getline(IN_MEMORY, BUFFERS);\n' +
          'getline(IN_MEMORY, BUFFERS);\n' +
          '{} = {}(BUFFERS);\n'.format(var_name, fun)
        )
        return code

    def load_int(self, intt):
        return self.load_var(intt, 'int', 'stoi')

    def load_float(self, floatt):
        return self.load_var(floatt, 'float', 'stof')

    def load_str(self, strr):
        return self.load_var(strr, 'string', '')

    def vector_saver(self, vector_type, vector, floats=False):
        normal = '  OUT_MEMORY << {}[I] << endl;\n'.format(vector)
        precise = (
          '  sprintf(BUFFER, "%.6f", {}[I]);\n'.format(vector) +
          '  OUT_MEMORY << BUFFER << endl;\n'
        )
        print_part = precise if floats else normal
        code = (
          '\n' +
          'OUT_MEMORY << "{}:" << endl;\n'.format(vector_type) +
          'OUT_MEMORY << "{}" << endl;\n'.format(vector) +
          'OUT_MEMORY << int({}.size()) << endl;\n'.format(vector) +
          'for(int I=0; I<{}.size(); I++)\n'.format(vector) +
          '{\n' +
          print_part +
          '}\n'
        )
        return code

    def save_int_vector(self, vector):
        return self.vector_saver("VECTOR_INT", vector)

    def save_float_vector(self, vector):
        return self.vector_saver("VECTOR_FLOAT", vector)

    def save_str_vector(self, vector):
        return self.vector_saver("VECTOR_STR", vector, floats=True)

    def save_int(self, intt):
        code = (
          '\n' +
          'OUT_MEMORY << "INT:" << endl;\n' +
          'OUT_MEMORY << "{}" << endl;\n'.format(intt) +
          'OUT_MEMORY << {} << endl;\n'.format(intt)
        )
        return code

    def save_float(self, floatt):
        code = (
          '\n' +
          'OUT_MEMORY << "FLOAT:" << endl;\n' +
          'OUT_MEMORY << "{}" << endl;\n'.format(floatt) +
          'sprintf(BUFFER, "%.6f", {});\n'.format(floatt) +
          'OUT_MEMORY << BUFFER << endl;\n'
        )
        return code

    def save_str(self, strr):
        code = (
          '\n' +
          'OUT_MEMORY << "STR:" << endl;\n' +
          'OUT_MEMORY << "{}" << endl;\n'.format(strr) +
          'OUT_MEMORY << {} << endl;\n'.format(strr)
        )
        return code

    def prepare(self):
        code_file = open(self.codename+".cpp", "w")
        code_file.write(self.generate())
        code_file.close()
        command = 'g++ {}.cpp --std=c++11 -w -o {}.bin'.format(self.codename, self.codename)
        logging.info("Running: %s", command)
        return os.system(command)

    def execute(self, in_memory, out_memory):
        command = './{}.bin {} {}'.format(self.codename, in_memory, out_memory)
        logging.info('Executing: %s', command)
        return os.system(command)


if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    runner1 = CppRunner(Runner.SOME_INT_VECTOR + '.push_back(10);\n', 'tmp/tmp.cpp')
    runner1.simple_full_run('tmp/memory.txt', 'tmp/memory2_cpp.txt')
    runner2 = CppRunner(Runner.SOME_FLOAT_VECTOR + '.push_back(0.5);\n', 'tmp/tmp2.cpp')
    runner2.simple_full_run('tmp/memory2_cpp.txt', 'tmp/memory3_cpp.txt')
