from runners.runner_python import PythonRunner
from runners.runner_cpp import CppRunner
from runners.runner_go import GoRunner
from runners.runner_pascal import PascalRunner
from runners.runner_php import PHPRunner
from runners.runner_rust import RustRunner

from runners.runner import Runner
from runners.init_runner import InitRunner

import logging
import re

logging.basicConfig(level=logging.INFO)

runners = [PythonRunner, CppRunner, GoRunner, PascalRunner, PHPRunner, RustRunner]

REGISTER = {r.NAME: r for r in runners}


class MasterRunner:
    def __init__(self, code, prefix='', variables=None):
        self.code = code
        self.runners = []
        self.location = 'tmp/'+prefix+'runer{}'
        self.variables = variables

    def prepare(self):
        """
        Args:
          code (list[pairs[code, language]]): code.
        """
        for i, (line, language) in enumerate(self.code):
            special_match = re.match("IF (.*) IS NOT ZERO GOTO (\d*)", line)
            if special_match is None:
                runner = REGISTER[language](line, self.location.format(i), self.variables)
                # TODO catch errors
                prepare_status, prepare_message = runner.prepare()
                if prepare_status != 0:
                    return "CERR", i+1, prepare_message
                self.runners.append(runner)
            else:
                groups = special_match.groups()
                self.runners.append((groups[0], int(groups[1])))
        return None

    def run(self, input_file):
        counter = 0
        line = 0
        last_memory = input_file
        init_runner = InitRunner(self.variables)
        while line < len(self.runners):
            counter += 1
            runner = self.runners[line]
            if not isinstance(runner, tuple):
                logging.info('Line %d, counter %d, runner %s', line, counter, runner.NAME)
                out_memory = self.location.format("_mem_"+str(counter))
                logging.info('From: %s, To: %s', last_memory, out_memory)
                execute_result = self.runners[line].execute(last_memory, out_memory)
                execute_status, execute_message = execute_result
                if execute_status != 0:
                    return "EXEC", line+1, execute_message
                last_memory = out_memory
                line += 1
            else:
                logging.info('Jupming on line: %d', line)
                variable = runner[0]
                to_line = runner[1]-1
                memory = init_runner.load_memory(last_memory)
                logging.info('Memory: %s = %d', variable, memory[variable])

                if memory[variable] != 0:
                    line = to_line
                else:
                    line += 1

        logging.info('Reading final memory: %s', last_memory)
        memory = init_runner.load_memory(last_memory)
        return memory


if __name__ == "__main__":
    # Custom Variables
    variables = {
        'INTS': ['int1'],
        'STRS': ['str1']
    }
    custom_init = InitRunner(variables)
    code2 = [
      [custom_init.SOME_INT + '=5', 'Python'],
      [custom_init.SOME_STR + '="loool";', 'C++'],
    ]

    custom_init.create_init_memory('tmp/memory.txt')
    master = MasterRunner(code2, '2', variables)
    master.prepare()
    memory = master.run('tmp/memory.txt')
    print(memory)
    assert len(memory) == 2
    assert memory['int1'] == 5
    assert memory['str1'] == "loool"

    # Basic multilanguage
    init = InitRunner()
    code = [
      [init.SOME_STR_VECTOR + '.append("P 1")', 'Python'],
      [init.SOME_STR_VECTOR + '.push_back("C 1");', 'C++'],
      [init.SOME_STR_VECTOR + '.append("P 2")', 'Python'],
      [init.SOME_STR_VECTOR + '.push_back("C 2");', 'C++'],
    ]
    init.create_init_memory('tmp/memory.txt')
    master = MasterRunner(code, '1')
    master.prepare()
    memory = master.run('tmp/memory.txt')
    print(memory[init.SOME_STR_VECTOR])
    assert memory[init.SOME_STR_VECTOR] == ["P 1", "C 1", "P 2", "C 2"]

    # CODE 2 with flow control
    code2 = [
      [init.SOME_INT + '=5', 'Python'],
      [init.SOME_STR + '=""', 'Python'],
      [init.SOME_STR + '+="a";', 'C++'],
      [init.SOME_INT + '-=1', 'Python'],
      ['IF ' + init.SOME_INT + ' IS NOT ZERO GOTO 3', 'C++'],
    ]

    init.create_init_memory('tmp/memory.txt')
    master = MasterRunner(code2, '2')
    master.prepare()
    memory = master.run('tmp/memory.txt')
    print(memory[init.SOME_STR])
    print(memory[init.SOME_INT])
    assert memory[init.SOME_STR] == "aaaaa"

    # CODE 3 with flow control
    code3 = [
      [init.SOME_INT + '=5', 'Python'],
      [init.SOME_STR + '=""', 'Python'],
      [init.SOME_STR_VECTOR + '[10]="fff";', 'C++'],
      [init.SOME_INT + '-=1', 'Python'],
      ['IF ' + init.SOME_INT + ' IS NOT ZERO GOTO 3', 'C++'],
    ]

    init.create_init_memory('tmp/memory.txt')
    master = MasterRunner(code3, '3')
    prepare_log = master.prepare()
    print(prepare_log)
    memory = master.run('tmp/memory.txt')
    print(memory)

    # CODE 4 prepare memory
    memory = {init.SOME_STR_VECTOR: ["str1", "str2", "fffg f3"]}
    init.prepare_memory(memory, "tmp/prefilled_memory.txt")
    out_memory = init.load_memory("tmp/prefilled_memory.txt")
    print(memory)
    print(out_memory)