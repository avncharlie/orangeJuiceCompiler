# orangeJuiceCompiler
OJC is an obfuscating JavaScript compiler.

Design goals, design analysis and an instruction set reference can be found [here](report.pdf).

## Install
Clone this repository. `cd` into `generate_ast` and run `npm install` to install Babel.

To generate disassembly graph output, install [PyGraphviz](https://pygraphviz.github.io/). This will involve installing [Graphviz](https://www.graphviz.org/) itself. After installation, ensure the Graphviz provided programs `neato` and `gvpack` are in your path.

## Build
The build script is `build.sh`. To use it, run this command:
``` $ build.sh <assembler> <file> ```
`assembler` must be an installed assembler. The currently available assemblers are `debug` `basic_bytecode` and `variable_dependent`.

The build script will generate the AST of `file`, compile it with `compile.py` then assemble it with the chosen assembler. The loaded VM (the obfuscated program) will be in `build/out.js`.

To build and run in one command, use `go.sh` script with the same argument format as above.

## Tests
To run tests, `cd` into the `tests` directory. Every JavaScript file in the directory that starts with "test" is a unit test. The python script `run_tests.py` will compare the output of these tests when running under `node` to the output of the compiled test. The test will fail if there are any differences in output.

To run all tests and benchmarks under a specific assembler run `./run_tests.py <assembler>`. To test specific tests or files, run `./run_tests.py <assembler> test1.js test2.js test3.js ...`

## Graph
To generate a disassembly, run `./graph.sh <assembler> <file>`. This will create the file `disass.png` containing the disassembly.
To generate different images for different functions (this is useful for inspecting larger programs), run `./graph.sh <assembler> <file> -s`

This will generate output dissasembly graphs in the `build/graph` directory.
