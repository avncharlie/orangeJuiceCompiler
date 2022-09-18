let fs = require('fs');

if (process.argv.length != 3) {
    console.log('Usage: node template_vm.js bytecode');
    return;
}

let bytecode_file = process.argv[2];
let bytecode = fs.readFileSync(bytecode_file, 'utf8');

// begin vm
function base64_to_bytearray(base64) {
    let binary_string = atob(base64);
    let len = binary_string.length;
    let bytes = [];
    for (let i = 0; i < len; i++) {
        bytes.push(binary_string.charCodeAt(i));
    }
    return bytes;
}

bytecode = base64_to_bytearray(bytecode);

let instruction_index = 0
let reg_stack = []
let registers = []
let variables = [{'function_map': false}]
let this_stack = [globalThis]

function bytes_to_float(bytes) {
    var sign = (bytes & 0x80000000) ? -1 : 1;
    var exponent = ((bytes >> 23) & 0xFF) - 127;
    var significand = (bytes & ~(-1 << 23));

    if (exponent == 128) 
        return sign * ((significand) ? Number.NaN : Number.POSITIVE_INFINITY);

    if (exponent == -127) {
        if (significand == 0) return sign * 0.0;
        exponent = -126;
        significand /= (1 << 22);
    } else significand = (significand | (1 << 23)) / (1 << 23);

    return sign * significand * Math.pow(2, exponent);
}


function b_next() {
    return bytecode[instruction_index++];
}

function argload_register_value_or_literal() {
    switch (b_next()) {
        case 1:
            return argload_string(false);
        case 2:
            return argload_bool(false);
        case 3:
            return null;
        case 4:
            return undefined;
        case 5:
            return registers[argload_number(false)]
        case 6:
            return argload_number(false);
        case 7:
            return argload_float(false);
        default:
            throw 'unknown arg type';
    }
}

function argload_bool(skip) {
    return Boolean(b_next())
}

function argload_string(skip) {
    if (skip) {
        instruction_index++;
    }
    let size = argload_number();
    let s =  String.fromCharCode(...bytecode.slice(instruction_index, instruction_index+size));
    instruction_index += size;

    return s;
}

function argload_float(skip) {
    if (skip) {
        instruction_index++;
    }
    let num = 0;
    for (let x = 0; x<4; x++) {
        num += b_next() * (256**x);
    }
    return bytes_to_float(num); 
}

function argload_number(skip) {
    if (skip) {
        instruction_index++;
    }
    let size = b_next();

    let num = 0;
    for (let x = 0; x<size; x++) {
        num += b_next() * (256**x);
    }
    return num;
}

function argload_register(skip) {
    return argload_number(skip);
}

let operations = [
    function push_store() {
        variables.push({'function_map': false});
    },

    function pop_store() {
        variables.pop();
    },

    function whatsthis() {
        let r = argload_register(true)
        registers[r] = this_stack[this_stack.length - 1]
    },

    function create_func() {
        let func_start_index = argload_number(true);
        let arglist = registers[argload_register(true)];
        let r = argload_register(true);

        registers[r] = function() {

            // push 'this' to the 'this stack'
            this_stack.push(this);

            // backup then reset registers 
            reg_stack.push(registers);
            registers = [];

            // backup instruction index
            let instruction_index_backup = instruction_index;

            // create new varmap for function declared vars
            let func_varmap = {'function_map': true};
            variables.push(func_varmap);

            // setup arguments (manually set them in varmap)
            for (let [i, arg] of Array.from(arguments).entries()) {
                func_varmap[arglist[i]] = arg
            }

            // run function at function label and get return value
            let rval = run({ func_start_index: func_start_index });

            // pop scopes until function scope reavhed
            let seen_own_frame = false;
            for (let index = variables.length - 1; index >= 0; index--) {
                if (variables[index]['function_map']) {
                    // this is our own frame
                    variables.pop() 
                    break;
                }
                variables.pop()
            }

            // restore instruction index
            instruction_index = instruction_index_backup;

            // restore registers
            registers = reg_stack.pop();

            // pop this from this_stack
            this_stack.pop();

            // return!
            return rval;
        }
    },

    function call() {
        let func = registers[argload_register(true)];
        let func_args = registers[argload_register(true)];
        let ctx = registers[argload_register(true)];
        let result_reg = argload_register(true);

        let result = func.apply(ctx, func_args);
        registers[result_reg] = result;
    },

    function global() {
        let dst = argload_register(true);
        registers[dst] = globalThis;
    },

    function mov() {
        let dst = argload_register(true);
        let src = argload_register_value_or_literal();
        registers[dst] = src;
    },

    function add() {
        let a = argload_register_value_or_literal();
        let b = argload_register_value_or_literal();
        let dst = argload_register(true);
        registers[dst] = a + b;
    },

    function sub() {
        let a = argload_register_value_or_literal();
        let b = argload_register_value_or_literal();
        let dst = argload_register(true);
        registers[dst] = a - b;
    },

    function mul() {
        let a = argload_register_value_or_literal();
        let b = argload_register_value_or_literal();
        let dst = argload_register(true);
        registers[dst] = a * b;
    },

    function div() {
        let a = argload_register_value_or_literal();
        let b = argload_register_value_or_literal();
        let dst = argload_register(true);
        registers[dst] = a / b;
    },

    function jmp() {
        instruction_index = argload_number(true)
    },

    function jt() {
        let cond = registers[argload_register(true)];
        let new_index = argload_number(true);
        if (cond) {
            instruction_index = new_index
        }
    },

    function jnt() {
        let cond = registers[argload_register(true)];
        let new_index = argload_number(true);
        if (!cond) {
            instruction_index = new_index
        }
    },

    function setvar() {
        let var_name = argload_string(true);
        let val = argload_register_value_or_literal();

        // pick variable from scope from favouring more global scopes
        let varmap = variables[variables.length - 1];
        let seen_own_frame = false;
        for (let index = variables.length - 1; index >= 0; index--) {
            if (variables[index]['function_map']) {
                if (seen_own_frame) {
                    continue; // don't set variables in other functions
                }
                seen_own_frame = true
            }
            if (var_name in variables[index]) {
                varmap = variables[index];
                break;
            }
        }
        varmap[var_name] = val
    },

    function getvar() {
        let var_name = argload_string(true);
        let reg = argload_register(true);

        // pick variable from scope from favouring more local scopes
        let varmap = variables[0];
        let seen_own_frame = false;
        for (let index = variables.length - 1; index >= 0; index--) {
            if (variables[index]['function_map']) {
                if (seen_own_frame) {
                    continue; // don't retrieve variables in other functions
                }
                seen_own_frame = true
            }
            if (var_name in variables[index]) {
                varmap = variables[index];
                break;
            }
        }
        registers[reg] = varmap[var_name];
    },

    function delvar() {
        let var_name = argload_string(true);
        let varmap = variables[variables.length - 1]
        delete varmap[var_name];
    },

    function arr() {
        registers[argload_register(true)] = [];
    },

    function arrpush() {
        let arr = registers[argload_register(true)];
        let elem = argload_register_value_or_literal(true);
        arr.push(elem);
    },

    function obj() {
        registers[argload_register(true)] = {};
    },

    function setprop() {
        let obj_reg = argload_register(true);
        let prop = argload_register_value_or_literal();
        let value = argload_register_value_or_literal();
        registers[obj_reg][prop] = value;
    },

    function getprop() {
        let obj_reg = argload_register(true);
        let prop = argload_register_value_or_literal();
        let dest = argload_register(true);
        registers[dest] = registers[obj_reg][prop]
    },

    function eq() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 == r2;
    },

    function neq() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 != r2;
    },

    function eqt() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 === r2;
    },

    function neqt() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 !== r2;
    },

    function ge() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 > r2;
    },

    function geeq() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 >= r2;
    },

    function le() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 < r2;
    },

    function leeq() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 <= r2;
    },

    function mod() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 % r2;
    },

    function shl() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 << r2;
    },

    function shr() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 >> r2;
    },

    function ushr() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 >>> r2;
    },

    function pow() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 ** r2;
    },

    function bit_or() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 | r2;
    },

    function bit_and() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 & r2;
    },

    function xor() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 ^ r2;
    },

    function inside() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 in r2;
    },

    function check_instance() {
        let r1 = registers[argload_register(true)];
        let r2 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = r1 instanceof r2;
    },

    function unary_plus() {
        let r1 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = +r1;
    },

    function unary_neg() {
        let r1 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = -r1;
    },

    function unary_not() {
        let r1 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = !r1;
    },

    function unary_bit_not() {
        let r1 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = ~r1;
    },

    function unary_typeof() {
        let r1 = registers[argload_register(true)];
        let ans = argload_register(true);
        registers[ans] = typeof r1;
    },

    function nop() {

    },

    function regex() {
        let pattern = argload_register_value_or_literal();
        let flags = argload_register_value_or_literal();
        let reg = argload_register()
        registers[reg] = new RegExp(pattern, flags)
    }

]

function num_top_scope_vars() {
    return Object.keys(variables[variables.length - 1]).length;
}

function decode(op) {
    return op ^ num_top_scope_vars();
}

function run(args) {

    if (args != undefined) {
        // used when running as function
        instruction_index = args.func_start_index;
    }

    while (instruction_index < bytecode.length) {
        let op = decode(b_next());

        //console.log(instruction_index, op, operations[op], num_top_scope_vars());
        //console.log(instruction_index, op, operations[op], num_top_scope_vars(), variables);

        // special handling for return
        if (op == 47) {
            return argload_register_value_or_literal();
        }

        operations[op]();
        /*
        try {
            operations[op]();
        } catch(err) {
            console.log('ERROR: ' + err.message);
            console.log('...... instruction index: ' + instruction_index);
            process.exit();
        }
        */
    }
}

run();
// end vm
