from runners.runner import Runner, InitRunner
import os, logging

the_genesis = '''
package main

import (
	"fmt"
	"io"
	"os"
)

func loadIt(r io.Reader, value interface{}) {
	var dummy string
	fmt.Fscan(r, &dummy) // <TYPE>
	fmt.Fscan(r, &dummy) // <name>
	fmt.Fscan(r, value)
}

func loadInts(r io.Reader) []int {
	var dummy string
	fmt.Fscan(r, &dummy) // VECTOR_INT
	fmt.Fscan(r, &dummy) // <name>

	var size int
	fmt.Fscan(r, &size)

	ints := make([]int, size)
	for i := range ints {
		fmt.Fscan(r, &ints[i])
	}
	return ints
}

func loadFloats(r io.Reader) []float64 {
	var dummy string
	fmt.Fscan(r, &dummy) // VECTOR_FLOAT
	fmt.Fscan(r, &dummy) // <name>

	var size int
	fmt.Fscan(r, &size)

	floats := make([]float64, size)
	for i := range floats {
		fmt.Fscan(r, &floats[i])
	}
	return floats
}

func loadStrings(r io.Reader) []string {
	var dummy string
	fmt.Fscan(r, &dummy) // VECTOR_STRING
	fmt.Fscan(r, &dummy) // <name>

	var size int
	fmt.Fscan(r, &size)

	strings := make([]string, size)
	for i := range strings {
		fmt.Fscan(r, &strings[i])
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
	in, err := os.Open(os.Args[1])
	if err != nil {
		panic(err)
	}
	out, err := os.Create(os.Args[2])
	if err != nil {
		panic(err)
	}
	defer in.Close()
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
        var {0} string
        loadIt(in, &{0})
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
        cmd = 'go build -o {} {}'.format(self.codename, filename)
        logging.info("Running: %s", cmd)
        return os.system(cmd)

    def execute(self, in_memory, out_memory):
        cmd = './{} {} {}'.format(self.codename, in_memory, out_memory)
        logging.info('Executing: %s', cmd)
        return os.system(cmd)
