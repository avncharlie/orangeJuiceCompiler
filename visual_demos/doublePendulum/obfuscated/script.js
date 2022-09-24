let bytecode = '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BQErCgUBKQEBBXdpZHRoBQEqGwUBKQsFASkBAQdjYW52YXMyBQEpCwUBKQEBBXdpZHRoBQEqEQEBEHZhcl9icm93c2VyV2lkdGgFASsYBQEqBQErCgUBKQEBBXdpZHRoBQEqFQYExAgAABcFAQQJAQEDY3R4BQEFEwUBBQEBCWJlZ2luUGF0aAUBBgIFAQYFAQQFAQUFAQMXBQEECQEBAXgFAQUUBQEEBQEFCQEBAXkFAQUUBQEEBQEFCQEBA2N0eAUBBRMFAQUBAQZtb3ZlVG8FAQYCBQEGBQEEBQEFBQEDCQEBA2N0eAUBAxMFAQMBAQlsaW5lV2lkdGgFAQQABQEFBgEFAAUBBAUBBRIFAQMBAQlsaW5lV2lkdGgFAQQXBQEECQEBBG5ld3gFAQUUBQEEBQEFCQEBBG5ld3kFAQUUBQEEBQEFCQEBA2N0eAUBBRMFAQUBAQZsaW5lVG8FAQYCBQEGBQEEBQEFBQEDFwUBBAkBAQNjdHgFAQUTBQEFAQEGc3Ryb2tlBQEGAgUBBgUBBAUBBQUBAykEFgEBAXgVAQEBeRQBAQRuZXd4EwEBBG5ld3kSAQEDY3R4FQYEqQoAABcFAQQJAQEFY3R4XzUFAQUTBQEFAQEJYmVnaW5QYXRoBQEGAgUBBgUBBAUBBQUBAxcFAQQJAQEDeF8zBQEFFAUBBAUBBQkBAQN5XzQFAQUUBQEEBQEFCQEBAW0FAQUUBQEEBQEFAAUBBQYAFAUBBAUBBQAFAQUGAQIDBQEGEwUBBgEBBE1hdGgFAQYTBQEGAQECUEkFAQYPBQEFBQEGBQEHFAUBBAUBBwkBAQVjdHhfNQUBBRMFAQUBAQNhcmMFAQYCBQEGBQEEBQEFBQEDCQEBBWN0eF81BQEDEwUBAwEBCWZpbGxTdHlsZQUBBAkBAQZjb2xvdXIFAQUABQEEBQEFEgUBAwEBCWZpbGxTdHlsZQUBBBcFAQQJAQEFY3R4XzUFAQUTBQEFAQEEZmlsbAUBBgIFAQYFAQQFAQUFAQMJAQEFY3R4XzUFAQMTBQEDAQELc3Ryb2tlU3R5bGUFAQQJAQEGY29sb3VyBQEFAAUBBAUBBRIFAQMBAQtzdHJva2VTdHlsZQUBBBcFAQQJAQEFY3R4XzUFAQUTBQEFAQEGc3Ryb2tlBQEGAgUBBgUBBAUBBQUBAykEFgEBA3hfMxUBAQN5XzQUAQEBbRMBAQVjdHhfNRIBAQZjb2xvdXIVBgRbHQAADwEBCXZhcl9udW1lMQQMAQEJdmFyX251bWUyBA0BAQl2YXJfbnVtZTMECgEBCXZhcl9udW1lNAQLAQEJdmFyX2Rlbm9tBAgBAQh2YXJfYTFfYQQJAQEIdmFyX2EyX2EEBgEBBnZhcl94MQQHAQEGdmFyX3kxBAQBAQZ2YXJfeDIEBQEBBnZhcl95MgQdBQEECgUBBQYAHgUBBAUBBQoFAQUGAB4FAQQFAQUJBQEFGQUBBQEBB2NhbnZhczEFAQUZBQEFAQEFd2lkdGgFAQUeBQEEBQEFCQUBBRkFAQUBAQdjYW52YXMxBQEFGQUBBQEBBmhlaWdodAUBBR4FAQQFAQUDAQEIdmFyX2N0eDEFAQUZBQEFAQEJY2xlYXJSZWN0BQEGCAUBBgUBBAUBBQUBAwMBAQl2YXJfbnVtZTEFAQMDAQEFdmFyX2cFAQQlBQEEBQEFCgUBBAYBAgMBAQZ2YXJfbTEFAQYFBQEEBQEGBQEHAwEBBnZhcl9tMgUBBAsFAQcFAQQFAQYFBQEFBQEGBQEEHQUBBgMBAQZ2YXJfYTEFAQceBQEGBQEHCQUBBxkFAQcBAQRNYXRoBQEHGQUBBwEBA3NpbgUBCAgFAQgFAQYFAQcFAQUFBQEEBQEFBQEGCgUBAwUBBgIBAQl2YXJfbnVtZTEFAQMDAQEJdmFyX251bWUyBQEEAwEBBnZhcl9tMgUBBSUFAQUFAQYDAQEFdmFyX2cFAQUFBQEGBQEFBQEHHQUBBgMBAQZ2YXJfYTEFAQgKBQEJBgECAwEBBnZhcl9hMgUBCgUFAQkFAQoFAQsEBQEIBQELBQEJHgUBBgUBCQkFAQgZBQEIAQEETWF0aAUBCBkFAQgBAQNzaW4FAQkIBQEJBQEGBQEIBQEFBQUBBwUBBQUBBgoFAQQFAQYCAQEJdmFyX251bWUyBQEEAwEBCXZhcl9udW1lMwUBBQoFAQYGAQIlBQEGBQEHHQUBCAMBAQZ2YXJfYTEFAQkDAQEGdmFyX2EyBQEKBAUBCQUBCgUBCx4FAQgFAQsJBQEJGQUBCQEBBE1hdGgFAQkZBQEJAQEDc2luBQEKCAUBCgUBCAUBCQUBBgUFAQcFAQYFAQgDAQEGdmFyX20yBQEGBQUBCAUBBgUBBwoFAQUFAQcCAQEJdmFyX251bWUzBQEFAwEBCXZhcl9udW1lNAUBBgMBAQh2YXJfYTJfdgUBBwMBAQh2YXJfYTJfdgUBCAUFAQcFAQgFAQkDAQEGdmFyX3IyBQEHBQUBCQUBBwUBCAMBAQh2YXJfYTFfdgUBBwMBAQh2YXJfYTFfdgUBCQUFAQcFAQkFAQoDAQEGdmFyX3IxBQEHBQUBCgUBBwUBCR0FAQoDAQEGdmFyX2ExBQELAwEBBnZhcl9hMgUBDAQFAQsFAQwFAQ0eBQEKBQENCQUBCxkFAQsBAQRNYXRoBQELGQUBCwEBA2NvcwUBDAgFAQwFAQoFAQsFAQcFBQEJBQEHBQEKCwUBCAUBCgUBBwoFAQYFAQcCAQEJdmFyX251bWU0BQEGAwEBCXZhcl9kZW5vbQUBBwMBAQZ2YXJfcjEFAQgKBQEJBgECAwEBBnZhcl9tMQUBCgUFAQkFAQoFAQsDAQEGdmFyX20yBQEJCwUBCwUBCQUBCgMBAQZ2YXJfbTIFAQkdBQEMCgUBDQYBAgMBAQZ2YXJfYTEFAQ4FBQENBQEOBQEPCgUBDQYBAgMBAQZ2YXJfYTIFAQ4FBQENBQEOBQEQBAUBDwUBEAUBDR4FAQwFAQ0JBQENGQUBDQEBBE1hdGgFAQ0ZBQENAQEDY29zBQEOCAUBDgUBDAUBDQUBCwUFAQkFAQsFAQwEBQEKBQEMBQEJBQUBCAUBCQUBCgoFAQcFAQoCAQEJdmFyX2Rlbm9tBQEHAwEBCHZhcl9hMV9hBQEIAwEBCXZhcl9udW1lMQUBCQMBAQl2YXJfbnVtZTIFAQoLBQEJBQEKBQELAwEBCXZhcl9udW1lMwUBCQMBAQl2YXJfbnVtZTQFAQoFBQEJBQEKBQEMCwUBCwUBDAUBCQMBAQl2YXJfZGVub20FAQoGBQEJBQEKBQELCgUBCAUBCwIBAQh2YXJfYTFfYQUBCAMBAQl2YXJfbnVtZTEFAQkKBQEKBgECHQUBDAMBAQZ2YXJfYTEFAQ0DAQEGdmFyX2EyBQEOBAUBDQUBDgUBDx4FAQwFAQ8JBQENGQUBDQEBBE1hdGgFAQ0ZBQENAQEDc2luBQEOCAUBDgUBDAUBDQUBCwUFAQoFAQsFAQwKBQEJBQEMAgEBCXZhcl9udW1lMQUBCQMBAQl2YXJfbnVtZTIFAQkDAQEIdmFyX2ExX3YFAQoDAQEIdmFyX2ExX3YFAQsFBQEKBQELBQEMAwEBBnZhcl9yMQUBCgUFAQwFAQoFAQsDAQEGdmFyX20xBQEKAwEBBnZhcl9tMgUBDAsFAQoFAQwFAQ0FBQELBQENBQEKCgUBCQUBCgIBAQl2YXJfbnVtZTIFAQkDAQEJdmFyX251bWUzBQEJAwEBBXZhcl9nBQEKAwEBBnZhcl9tMQUBCwMBAQZ2YXJfbTIFAQwLBQELBQEMBQENBQUBCgUBDQUBCx0FAQwDAQEGdmFyX2ExBQENHgUBDAUBDQkFAQ0ZBQENAQEETWF0aAUBDRkFAQ0BAQNjb3MFAQ4IBQEOBQEMBQENBQEKBQUBCwUBCgUBDAoFAQkFAQwCAQEJdmFyX251bWUzBQEJAwEBCXZhcl9udW1lNAUBCQMBAQh2YXJfYTJfdgUBCgMBAQh2YXJfYTJfdgUBCwUFAQoFAQsFAQwDAQEGdmFyX3IyBQEKBQUBDAUBCgUBCwMBAQZ2YXJfbTIFAQoFBQELBQEKBQEMHQUBCwMBAQZ2YXJfYTEFAQ0DAQEGdmFyX2EyBQEOBAUBDQUBDgUBDx4FAQsFAQ8JBQENGQUBDQEBBE1hdGgFAQ0ZBQENAQEDY29zBQEOCAUBDgUBCwUBDQUBCgUFAQwFAQoFAQsKBQEJBQELAgEBCXZhcl9udW1lNAUBCQMBAQl2YXJfZGVub20FAQkDAQEGdmFyX3IyBQEKCgUBCwYBAgMBAQZ2YXJfbTEFAQwFBQELBQEMBQENAwEBBnZhcl9tMgUBCwsFAQ0FAQsFAQwDAQEGdmFyX20yBQELHQUBDgoFAQ8GAQIDAQEGdmFyX2ExBQEQBQUBDwUBEAUBEQoFAQ8GAQIDAQEGdmFyX2EyBQEQBQUBDwUBEAUBEgQFAREFARIFAQ8eBQEOBQEPCQUBDxkFAQ8BAQRNYXRoBQEPGQUBDwEBA2NvcwUBEAgFARAFAQ4FAQ8FAQ0FBQELBQENBQEOBAUBDAUBDgUBCwUFAQoFAQsFAQwKBQEJBQEMAgEBCXZhcl9kZW5vbQUBCQMBAQh2YXJfYTJfYQUBCQMBAQl2YXJfbnVtZTEFAQoDAQEJdmFyX251bWUyBQELAwEBCXZhcl9udW1lMwUBDAsFAQsFAQwFAQ0DAQEJdmFyX251bWU0BQELCwUBDQUBCwUBDAUFAQoFAQwFAQsD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BQUBAxAFAQQHBQEFAQEJR3Jhdml0eTogDgEBBXZhcl9nBQEGBgUBBQUBBgUBBxMFAQQFAQcEBQEFFAUBBQEBB2NvbnNvbGUFAQUUBQEFAQEDbG9nBQEGBQUBBgUBBAUBBQUBAxAFAQQOAQEMZnVuY19hbmltYXRlBQEFEwUBBAUBBQQFAQUUBQEFAQEGd2luZG93BQEFFAUBBQEBFXJlcXVlc3RBbmltYXRpb25GcmFtZQUBBgUFAQYFAQQFAQUFAQMuBBUGBAghAAAXBQEECQEBBHhfMTIFAQUUBQEEBQEFCQEBBHlfMTMFAQUUBQEEBQEFCQEBAXcFAQUUBQEEBQEFCQEBAWgFAQUUBQEEBQEFCQEBBmN0eF8xNAUBBRMFAQUBAQljbGVhclJlY3QFAQYCBQEGBQEEBQEFBQEDKQQWAQEEeF8xMhUBAQR5XzEzFAEBAXcTAQEBaBIBAQZjdHhfMTQVBgQKJAAADAEBCHZhcl9vbGR4BQEDDAEBC3Zhcl90cmFpbHN4BQEEBQUBBQYAFgUBBAUBBQUBBAUFAQMFAQQNAQEIdmFyX29sZHgFAQMMAQEIdmFyX29sZHkFAQMMAQELdmFyX3RyYWlsc3kFAQQFBQEFBgAWBQEEBQEFBQEEBQUBAwUBBA0BAQh2YXJfb2xkeQUBAwYFAQMWBQEDAQEBaQUBAwUFAQQGAAUFAQMFAQQGBQEFFwUBBQEBAWkFAQMGBQEEFgUBBAEBAWkFAQQMAQELdmFyX3RyYWlsc3gFAQUWBQEFAQEGbGVuZ3RoBQEFBQUBBgYBAQsFAQUFAQYFAQceBQEEBQEHBQEFDgUBBQYEXCMAAAMOAQELdmFyX3RyYWlsc3gFAQQEBQEGFAUBBgEBAWkFAQYUBQEEBQEGBQEHDgEBC3Zhcl90cmFpbHN4BQEIBAUBCRQFAQkBAQFpBQEJBwUBCgYBAQYFAQkFAQoFAQsUBQEIBQELBQEIBwUBBwUBCBUFAQQFAQYFAQcOAQELdmFyX3RyYWlsc3kFAQQEBQEGFAUBBgEBAWkFAQYUBQEEBQEGBQEHDgEBC3Zhcl90cmFpbHN5BQEIBAUBCRQFAQkBAQFpBQEJBwUBCgYBAQYFAQkFAQoFAQsUBQEIBQELBQEIBwUBBwUBCBUFAQQFAQYFAQcABgUBBBYFAQQBAQFpBQEEBQUBBgUBBAYFAQcWBQEHAQEBaQUBBwUFAQgGAQEEBQEHBQEIBQEHBgUBCRcFAQkBAQFpBQEHCAYEyCEAAAwBAQt2YXJfdHJhaWxzeAUBBwwBAQ92YXJfdHJhaWxMZW5ndGgFAQgWBQEHBQEIBQEJDAEBBHhfMTcFAQoFBQEJBQEKFwUBBwUBCAUBCQwBAQt2YXJfdHJhaWxzeQUBBwwBAQ92YXJfdHJhaWxMZW5ndGgFAQgWBQEHBQEIBQEJDAEBBHlfMTgFAQoFBQEJBQEKFwUBBwUBCAUBCSwEEwEBBHhfMTcSAQEEeV8xOBUGBMkkAAAHBQEDFwUBAwEBA251bQUBAxMFAQUTBQEHBwUBCBcFAQgBAQRNYXRoBQEIFwUBCAEBBnJhbmRvbQUBCQYFAQkFAQcFAQgFAQYNAQEEeF8yMQUBBwsFAQYFAQcFAQgQBQEFBQEIBwUBBhcFAQYBAQRNYXRoBQEGFwUBBgEBBWZsb29yBQEHBgUBBwUBBQUBBgUBBAQFAQMFAQQHBQEFFgUBBQEBA251bQUBAy0FAQMtBBIBAQR4XzIxMxUGBIElAAAOAQEFdmFyX2oFAQMHBQEEBgEBBgUBAwUBBAUBAw8BAQV2YXJfagUBAwQFAQMUBQEDAQEGY29sb3VyBQEDBwUBBAEBBGhzbCgOAQEFdmFyX2oFAQUGBQEEBQEFBQEGBwUBBAEBDCwgMTAwJSwgNTAlKQYFAQYFAQQFAQUHBQEDBQEFBAUBBBUFAQQBAQZjb2xvdXIFAQMEBQEDFAUBAwEBBmNvbG91cgUBAy4FAQMuBBUGBIolAAAuBA8FASobBQErGgUBCgUBKgUBKwUBKQ==';
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

            // pad func arguments smaller than expected arguments
            let args = Array.from(arguments);
            if (args.length < arglist.length) {
                for (let x = 0; x <= (arglist.length - args.length); x++) {
                    args.push(undefined);
                }
            }

            // setup arguments (manually set them in varmap)
            for (let [i, arg] of args.entries()) {
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
            //console.log('^ return')
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
