let fs = require('fs');

if (process.argv.length != 3) {
    console.log('Usage: node debug_vm.js instructions.js');
    return;
}

let instruction_file = process.argv[2];
let instructions = JSON.parse(fs.readFileSync(instruction_file, 'utf8'))

// begin vm
instructions = instructions['instructions'];
let instruction_index = 0
let label_indexes = {}
let reg_stack = []
let registers = []
let variables = [{}]
let this_stack = [globalThis]

let operations = {

    push_store(args) {
        variables.push({});
        instruction_index += 1;
    },

    pop_store(args) {
        variables.pop();
        instruction_index += 1;
    },

    whatsthis(args) {
        let r = args[0].value
        registers[r] = this_stack[this_stack.length - 1]
        instruction_index += 1;
    },

    create_func(args) {
        let func_start_label = args[0].value
        let arglist = registers[args[1].value]
        let r = args[2].value

        registers[r] = function() {

            // push 'this' to the 'this stack'
            this_stack.push(this);

            // backup then reset registers 
            reg_stack.push(registers);
            registers = [];

            // backup instruction index
            let instruction_index_backup = instruction_index;

            // create new varmap for function declared vars
            let func_varmap = {};
            variables.push(func_varmap);

            // setup arguments (manually set them in varmap)
            for (let [i, arg] of Array.from(arguments).entries()) {
                func_varmap[arglist[i]] = arg
            }

            // run function at function label and get return value
            let rval = run({ start_at_label: func_start_label });

            // pop varmap
            variables.pop();

            // restore instruction index
            instruction_index = instruction_index_backup;

            // restore registers
            registers = reg_stack.pop();

            // pop this from this_stack
            this_stack.pop();

            // return!
            return rval;
        }

        instruction_index += 1;
    },

    call(args) {
        let func = registers[args[0].value];
        let func_args = registers[args[1].value];
        let ctx = registers[args[2].value];
        let result_reg = args[3].value;

        let result = func.apply(ctx, func_args);
        registers[result_reg] = result;
        instruction_index += 1;
    },

    global(args) {
        let dst = args[0].value;
        registers[dst] = globalThis;
        instruction_index += 1;
    },

    mov(args) {
        let dst = args[0].value;
        let src = args[1];
        // load src from registers or load as literal
        src = (src.type != "register") ? src.value : registers[src.value]
        registers[dst] = src;
        instruction_index += 1;
    },

    add(args) {
        let a = args[0];
        let b = args[1];
        a = (a.type != "register") ? a.value : registers[a.value];
        b = (b.type != "register") ? b.value : registers[b.value];
        let dst = args[2].value;
        registers[dst] = a + b;
        instruction_index += 1;
    },

    sub(args) {
        let a = args[0];
        let b = args[1];
        a = (a.type != "register") ? a.value : registers[a.value];
        b = (b.type != "register") ? b.value : registers[b.value];
        let dst = args[2].value;
        registers[dst] = a - b;
        instruction_index += 1;
    },

    mul(args) {
        let a = args[0];
        let b = args[1];
        a = (a.type != "register") ? a.value : registers[a.value];
        b = (b.type != "register") ? b.value : registers[b.value];
        let dst = args[2].value;
        registers[dst] = a * b;
        instruction_index += 1;
    },

    div(args) {
        let a = args[0];
        let b = args[1];
        a = (a.type != "register") ? a.value : registers[a.value];
        b = (b.type != "register") ? b.value : registers[b.value];
        let dst = args[2].value;
        registers[dst] = a / b;
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
        let value = args[1];

        let val;
        if (value.type == 'Undefined') {
            val = undefined;
        } else {
            val = (value.type != "register") ? value.value : registers[value.value]
        }

        // pick variable from scope from favouring more global scopes
        let varmap = variables[variables.length - 1]
        for (let scope of variables) {
            if (var_name in scope) {
                varmap = scope
            } 
        }

        varmap[var_name] = val
        instruction_index += 1;
    },

    getvar(args) {

        let var_name = args[0].value;
        let reg = args[1].value;

        // pick variable from scope from favouring more local scopes
        let varmap = variables[0]
        for (let index = variables.length - 1; index >= 0; index--) {
            if (var_name in variables[index]) {
                varmap = variables[index]
            }
        }

        registers[reg] = varmap[var_name];
        instruction_index += 1;
    },

    delvar(args) {
        let var_name = args[0].value;
        let varmap = variables[variables.length - 1]
        delete varmap[var_name];
        instruction_index += 1;
    },

    arr(args) {
        registers[args[0].value] = [];
        instruction_index += 1;
    },

    arrpush(args) {
        let arr = registers[args[0].value];
        let elem = args[1];
        elem = (elem.type != "register") ? elem.value : registers[elem.value]
        arr.push(elem);
        instruction_index += 1;
    },

    obj(args) {
        registers[args[0].value] = {};
        instruction_index += 1;
    },

    setprop(args) {
        let obj_reg = args[0].value;
        let prop = args[1];
        prop = (prop.type != "register") ? prop.value : registers[prop.value]
        let value = args[2];
        value = (value.type != "register") ? value.value : registers[value.value]
        registers[obj_reg][prop] = value;
        instruction_index += 1;
    },

    getprop(args) {
        let obj_reg = args[0].value;
        let prop = args[1];
        prop = (prop.type != "register") ? prop.value : registers[prop.value]
        let dest = args[2].value;
        registers[dest] = registers[obj_reg][prop]
        instruction_index += 1;
    },

    eq(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 == r2;
        instruction_index += 1;
    },

    neq(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 != r2;
        instruction_index += 1;
    },

    eqt(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 === r2;
        instruction_index += 1;
    },

    neqt(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 !== r2;
        instruction_index += 1;
    },

    ge(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 > r2;
        instruction_index += 1;
    },

    geeq(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 >= r2;
        instruction_index += 1;
    },

    le(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 < r2;
        instruction_index += 1;
    },

    leeq(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 <= r2;
        instruction_index += 1;
    },

    neq(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 != r2;
        instruction_index += 1;
    },

    mod(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 % r2;
        instruction_index += 1;
    },

    shl(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 << r2;
        instruction_index += 1;
    },

    shr(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 >> r2;
        instruction_index += 1;
    },

    ushr(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 >>> r2;
        instruction_index += 1;
    },

    pow(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 ** r2;
        instruction_index += 1;
    },

    bit_or(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 | r2;
        instruction_index += 1;
    },

    bit_and(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 & r2;
        instruction_index += 1;
    },

    xor(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 ^ r2;
        instruction_index += 1;
    },

    inside(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 in r2;
        instruction_index += 1;
    },

    check_instance(args) {
        let r1 = registers[args[0].value];
        let r2 = registers[args[1].value];
        let ans = args[2].value;
        registers[ans] = r1 instanceof r2;
        instruction_index += 1;
    },

    unary_plus(args) {
        let r1 = registers[args[0].value];
        let ans = args[1].value;
        registers[ans] = +r1;
        instruction_index += 1;
    },

    unary_neg(args) {
        let r1 = registers[args[0].value];
        let ans = args[1].value;
        registers[ans] = -r1;
        instruction_index += 1;
    },

    unary_not(args) {
        let r1 = registers[args[0].value];
        let ans = args[1].value;
        registers[ans] = !r1;
        instruction_index += 1;
    },

    unary_bit_not(args) {
        let r1 = registers[args[0].value];
        let ans = args[1].value;
        registers[ans] = ~r1;
        instruction_index += 1;
    },

    unary_typeof(args) {
        let r1 = registers[args[0].value];
        let ans = args[1].value;
        registers[ans] = typeof r1;
        instruction_index += 1;
    },

    nop(args) {
        instruction_index += 1;
    },

    regex(args) {
        let pattern = args[0];
        let flags = args[1];
        pattern = (pattern.type != "register") ? pattern.value : registers[pattern.value];
        flags = (flags.type != "register") ? flags.value : registers[flags.value];
        let reg = args[2].value;
        registers[reg] = new RegExp(pattern, flags)
        instruction_index += 1;
    }

}

function populate_label_indexes() {
    for (let [index, ins] of instructions.entries()) {
        if (ins.type == 'label') {
            label_indexes[ins.id] = index;
        }
    }
}

function run(args) {

    if (args != undefined) {
        // used when running as function
        instruction_index = label_indexes[args.start_at_label];
    }

    while (instruction_index < instructions.length) {
        let ins = instructions[instruction_index]

        if (instruction_index == 1388) {
            debugger;
        }

        if (ins.type == 'label') {
            instruction_index += 1;
            continue;
        }

        // special handling for return
        if (ins.op == 'return') {
            let rval = ins.args[0]
            rval = (rval.type != "register") ? rval.value : registers[rval.value]
            return rval
        }

        try {
            //console.log(ins.string_repr);
            operations[ins.op](ins.args);
        } catch(err) {
            console.log('ERROR: ' + err.message);
            console.log('...... instruction index: ' + instruction_index);
            console.log('...... instruction: ' + ins.string_repr);
            console.log('...... approximate location in source: line ' + ins.approx_loc);
            throw err;
            process.exit();
        }
        //console.log(registers, variables);
    }
}

populate_label_indexes();
run()
// end vm

console.log('--------');
console.log(variables);
//console.log(registers);
