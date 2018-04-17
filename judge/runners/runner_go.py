from runners.runner import Runner
from runners.init_runner import InitRunner
import os
#import logging

the_genesis = '''
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

func loadLine(r *bufio.Reader) string {
	line, err := r.ReadString('\\n')
	if err != nil {
		panic(err)
	}
	return line[:len(line)-1]
}

func loadValue(r *bufio.Reader, value interface{}) {
	fmt.Sscan(loadLine(r), value)
}

func loadIt(r *bufio.Reader, value interface{}) {
	loadLine(r) // <TYPE>
	loadLine(r) // <name>
	loadValue(r, value)
}

func loadString(r *bufio.Reader) string {
	loadLine(r) // STR:
	loadLine(r) // <name>
	return loadLine(r)
}

func loadInts(r *bufio.Reader) []int {
	loadLine(r) // VECTOR_INT
	loadLine(r) // <name>

	var size int
	loadValue(r, &size)

	ints := make([]int, size)
	for i := range ints {
		loadValue(r, &ints[i])
	}
	return ints
}

func loadFloats(r *bufio.Reader) []float64 {
	loadLine(r) // VECTOR_FLOAT
	loadLine(r) // <name>

	var size int
	loadValue(r, &size)

	floats := make([]float64, size)
	for i := range floats {
		loadValue(r, &floats[i])
	}
	return floats
}

func loadStrings(r *bufio.Reader) []string {
	loadLine(r) // VECTOR_STRING
	loadLine(r) // <name>

	var size int
	loadValue(r, &size)

	strings := make([]string, size)
	for i := range strings {
		strings[i] = loadLine(r)
	}
	return strings
}

func saveIt(w io.Writer, typ, name string, value interface{}) {
	fmt.Fprintln(w, typ)
	fmt.Fprintln(w, name)
	fmt.Fprintln(w, value)
}

func saveInts(w io.Writer, name string, ints []int) {
	fmt.Fprintln(w, "VECTOR_INT:")
	fmt.Fprintln(w, name)
	fmt.Fprintln(w, len(ints))
	for _, x := range ints {
		fmt.Fprintln(w, x)
	}
}

func saveFloats(w io.Writer, name string, floats []float64) {
	fmt.Fprintln(w, "VECTOR_FLOAT:")
	fmt.Fprintln(w, name)
	fmt.Fprintln(w, len(floats))
	for _, x := range floats {
		fmt.Fprintln(w, x)
	}
}

func saveStrings(w io.Writer, name string, strings []string) {
	fmt.Fprintln(w, "VECTOR_STR:")
	fmt.Fprintln(w, name)
	fmt.Fprintln(w, len(strings))
	for _, x := range strings {
		fmt.Fprintln(w, x)
	}
}

func main() {
	inFile, err := os.Open(os.Args[1])
	if err != nil {
		panic(err)
	}
	in := bufio.NewReader(inFile)
	out, err := os.Create(os.Args[2])
	if err != nil {
		panic(err)
	}
	defer inFile.Close()
	defer out.Close()
'''

the_apocalypse = '''
}
'''


class GoRunner(Runner):
    NAME = "Go"

    def begin_ceremony(self):
        return the_genesis

    def end_ceremony(self):
        return the_apocalypse

    def load_int(self, name):
        return '''
        var {0} int
        loadIt(in, &{0})
        '''.format(name)

    def load_float(self, name):
        return '''
        var {0} float64
        loadIt(in, &{0})
        '''.format(name)

    def load_str(self, name):
        return '''
        {0} := loadString(in)
        '''.format(name)

    def load_int_vector(self, name):
        return '''
        {0} := loadInts(in)
        '''.format(name)

    def load_float_vector(self, name):
        return '''
        {0} := loadFloats(in)
        '''.format(name)

    def load_str_vector(self, name):
        return '''
        {0} := loadStrings(in)
        '''.format(name)

    def save_int(self, name):
        return '''
        saveIt(out, "INT:", "{0}", {0})
        '''.format(name)

    def save_float(self, name):
        return '''
        saveIt(out, "FLOAT:", "{0}", {0})
        '''.format(name)

    def save_str(self, name):
        return '''
        saveIt(out, "STR:", "{0}", {0})
        '''.format(name)

    def save_int_vector(self, name):
        return '''
        saveInts(out, "{0}", {0})
        '''.format(name)

    def save_float_vector(self, name):
        return '''
        saveFloats(out, "{0}", {0})
        '''.format(name)

    def save_str_vector(self, name):
        return '''
        saveStrings(out, "{0}", {0})
        '''.format(name)

    def prepare(self):
        filename = self.codename + ".go"
        f = open(filename, "w")
        f.write(self.generate())
        f.close()
        log_fname = "{}.compile_log".format(self.codename)
        cmd = 'go build -o {} {} 2>{}'.format(self.codename, filename, log_fname)
        #logging.info("Running: %s", cmd)
        return os.system(cmd), open(log_fname).read()


    def execute(self, in_memory, out_memory):
        log_fname = "{}.runtime_log".format(self.codename)
        cmd = './{} {} {} 2>{}'.format(self.codename, in_memory, out_memory, log_fname)
        #logging.info('Executing: %s', cmd)
        return os.system(self.timeout(cmd)), open(log_fname).read()


if __name__ == '__main__':
    init = InitRunner()
    init.create_init_memory('tmp/memory.txt')
    runner = GoRunner('{0} = append({0}, "one", "two");'.format(
      init.SOME_STR_VECTOR), 'tmp/tmp')
    runner.simple_full_run('tmp/memory.txt', 'tmp/memory2_go.txt')
    mem = init.load_memory('tmp/memory2_go.txt')
    assert mem[init.SOME_STR_VECTOR] == ["one", "two"]
    runner2 = GoRunner('{0} = 0.5678;'.format(
      init.SOME_FLOAT), 'tmp/tmp')
    runner2.simple_full_run('tmp/memory2_go.txt', 'tmp/memory3_go.txt')
    mem = init.load_memory('tmp/memory3_go.txt')
    assert mem[init.SOME_FLOAT] == 0.5678
