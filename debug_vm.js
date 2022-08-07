let fs = require('fs');

if (process.argv.length != 3) {
    console.log('Usage: node debug_vm.js instructions.js');
    return;
}

let instruction_file = process.argv[2];

let instructions = JSON.parse(fs.readFileSync(instruction_file, 'utf8'))['instructions'];
let instruction_index = 0
let label_indexes = {}
let registers = []
let variables = {}

let operations = {
    mov(args) {
        let dst = args[0].value;
        let src = args[1];
        // load src from registers or load as literal
        src = (src.type != "register") ? src.value : registers[src.value]
        registers[dst] = src;
        instruction_index += 1;
    },

    add(args) {
        let dst = args[0].value;
        let src = args[1];
        src = (src.type != "register") ? src.value : registers[src.value]
        registers[dst] += src
        instruction_index += 1;
    },

    sub(args) {
        let dst = args[0].value;
        let src = args[1];
        src = (src.type != "register") ? src.value : registers[src.value]
        registers[dst] -= src
        instruction_index += 1;
    },

    mul(args) {
        let dst = args[0].value;
        let src = args[1];
        src = (src.type != "register") ? src.value : registers[src.value]
        registers[dst] *= src
        instruction_index += 1;
    },

    div(args) {
        let dst = args[0].value;
        let src = args[1];
        src = (src.type != "register") ? src.value : registers[src.value]
        registers[dst] /= src
        instruction_index += 1;
    },

    jmp(args) {
        let label = args[0].value;
        // jump instruction to label
        instruction_index = label_indexes[label]
    },

    jt(args) {
        let cond = registers[args[0].value];
        let label = args[1].value;
        instruction_index = cond ? label_indexes[label] : instruction_index + 1;
    },

    jnt(args) {
        let cond = registers[args[0].value];
        let label = args[1].value;
        instruction_index = !cond ? label_indexes[label] : instruction_index + 1;
    },

    setvar(args) {
        let var_name = args[0].value;
        let val = args[1];
        val = (val.type != "register") ? val.value : registers[val.value]
        variables[var_name] = val
        instruction_index += 1;
    },

    getvar(args) {
        let var_name = args[0].value;
        let reg = args[1].value;
        registers[reg] = variables[var_name];
        instruction_index += 1;
    },

    delvar(args) {
        let var_name = args[0].value;
        delete variables[var_name]
        instruction_index += 1;
    },

}

function populate_label_indexes() {
    for (let [index, ins] of instructions.entries()) {
        if (ins.type == 'label') {
            label_indexes[ins.id] = index;
        }
    }
}

function run() {
    while (instruction_index < instructions.length) {
        let ins = instructions[instruction_index]

        if (ins.type == 'label') {
            instruction_index += 1;
            continue;
        }

        operations[ins.op](ins.args);
        console.log(registers, variables);
    }
}

populate_label_indexes();
run()
