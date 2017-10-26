from runner import Runner, InitRunner
import os


class CppRunner(Runner):
    NAME = 'C++'

    def begin_ceremony(self):
        code = (
          '#include <cstdio> \n' +
          '#include <iostream> \n' +
          '#include <algorithm> \n' +
          '#include <fstream> \n' +
          '#include <vector> \n' +
          '#include <string> \n' +
          'using namespace std; \n' +
          '\n' +
          'char BUFFER[600000];\n' +
          'int BUFFER_SIZE;\n' +
          'int main(int argc, char *argv[]){ \n' +
          '\n' +
          'string TMP_STR;\n' +
          'int TMP_INT;\n' +
          'FILE* IN_MEMORY = fopen(argv[1], "r"); \n' +
          'FILE* OUT_MEMORY = fopen(argv[2], "w"); \n'
        )
        return code

    def end_ceremony(self):
        code = (
          'fclose(IN_MEMORY);\n'
          'fclose(OUT_MEMORY);\n'
          '\nreturn 0;\n' +
          '}\n'
        )
        return code

    def load_int_vector(self, vector):
        code = (
          '\n' +
          'vector<int> {};\n'.format(vector) +
          'fscanf(IN_MEMORY, "%s %d ", BUFFER, &TMP_INT);\n' +
          '{}.resize(TMP_INT);\n'.format(vector) +
          'for(int I=0; I<TMP_INT; I++){\n' +
          '  fscanf(IN_MEMORY, "%d ", &{}[I]);\n'.format(vector) +
          '}\n'
        )
        return code

    def load_str_vector(self, vector):
        code = (
          '\n' +
          'vector<string> {};\n'.format(vector) +
          'fscanf(IN_MEMORY, "%s %d ", BUFFER, &TMP_INT);\n' +
          '{}.resize(TMP_INT);\n'.format(vector) +
          'for(int I=0; I<TMP_INT; I++){\n' +
          '  fscanf(IN_MEMORY, "%[^\\n]\\n", &BUFFER);\n' +
          '  {}[I] = string(BUFFER);\n'.format(vector) +
          '  cout << {}.size()<<endl;\n'.format(vector) +
          '}\n'
        )
        return code

    def load_int(self, intt):
        code = (
          '\n' +
          'int {};\n'.format(intt) +
          'fscanf(IN_MEMORY, "%s %d ", BUFFER, &{});\n'.format(intt)
        )
        return code

    def load_str(self, strr):
        code = (
          '\n' +
          'BUFFER_SIZE = fscanf(IN_MEMORY, "%s \\n", BUFFER);\n' +
          'BUFFER_SIZE = fscanf(IN_MEMORY, "%s", BUFFER);\n' +
          'string {} (BUFFER);\n'.format(strr)
        )
        return code

    def save_int_vector(self, vector):
        code = (
          '\nfprintf(OUT_MEMORY, "{} %d", int({}.size()));\n'.format(vector, vector) +
          '\n' +
          'for(int I=0; I<{}.size(); I++)\n'.format(vector) +
          '{\n' +
          '  fprintf(OUT_MEMORY, " %d", {}[I]);\n'.format(vector) +
          '}\n' +
          'fprintf(OUT_MEMORY, "\\n");\n'
        )
        return code

    def save_str_vector(self, vector):
        code = (
          '\nfprintf(OUT_MEMORY, "{} %d\\n", int({}.size()));\n'.format(vector, vector) +
          '\n' +
          'for(int I=0; I<{}.size(); I++)\n'.format(vector) +
          '{\n' +
          '  fprintf(OUT_MEMORY, "%s\\n", {}[I].c_str());\n'.format(vector) +
          '}\n'
        )
        return code

    def save_int(self, intt):
        return 'fprintf(OUT_MEMORY, "{} %d\\n", {});\n'.format(intt, intt)

    def save_str(self, strr):
        return 'fprintf(OUT_MEMORY, "{}\\n%s\\n", {}.c_str());\n'.format(strr, strr)

    def prepare(self, codename):
        command = 'g++ {} --std=c++11 -o {}.bin'.format(codename, codename)
        os.system(command)

    def execute(self, codename, in_memory, out_memory):
        os.system('./{}.bin {} {}'.format(codename, in_memory, out_memory))


if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    runner = CppRunner()
    runner.simle_full_run('vs1.push_back("ss");\n', 'tmp/tmp.cpp', 'tmp/memory.txt', 'tmp/memory2_cpp.txt')
    runner.simle_full_run('vs1.push_back("ss");\n', 'tmp/tmp.cpp', 'tmp/memory2_cpp.txt', 'tmp/memory3_cpp.txt')
