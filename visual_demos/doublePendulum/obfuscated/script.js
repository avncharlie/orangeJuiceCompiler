let bytecode = '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BQErFAUBKQEBBXdpZHRoBQEqBQUBKRUFASkBAQdjYW52YXMyBQEpFQUBKQEBBXdpZHRoBQEqDwEBEHZhcl9icm93c2VyV2lkdGgFASsGBQEqBQErFAUBKQEBBXdpZHRoBQEqCwYExAgAABEFAQQPAQEDY3R4BQEFFQUBBQEBCWJlZ2luUGF0aAUBBgQFAQYFAQQFAQUFAQMRBQEEDwEBAXgFAQUSBQEEBQEFDwEBAXkFAQUSBQEEBQEFDwEBA2N0eAUBBRUFAQUBAQZtb3ZlVG8FAQYEBQEGBQEEBQEFBQEDDwEBA2N0eAUBAxUFAQMBAQlsaW5lV2lkdGgFAQQGBQEFBgEFBgUBBAUBBRQFAQMBAQlsaW5lV2lkdGgFAQQRBQEEDwEBBG5ld3gFAQUSBQEEBQEFDwEBBG5ld3kFAQUSBQEEBQEFDwEBA2N0eAUBBRUFAQUBAQZsaW5lVG8FAQYEBQEGBQEEBQEFBQEDEQUBBA8BAQNjdHgFAQUVBQEFAQEGc3Ryb2tlBQEGBAUBBgUBBAUBBQUBAxABAQF4EAEBAXkQAQEEbmV3eBABAQRuZXd5EAEBA2N0eC8ECwYEqQoAABEFAQQPAQEFY3R4XzUFAQUVBQEFAQEJYmVnaW5QYXRoBQEGBAUBBgUBBAUBBQUBAxEFAQQPAQEDeF8zBQEFEgUBBAUBBQ8BAQN5XzQFAQUSBQEEBQEFDwEBAW0FAQUSBQEEBQEFBgUBBQYAEgUBBAUBBQYFAQUGAQIFBQEGFQUBBgEBBE1hdGgFAQYVBQEGAQECUEkFAQYJBQEFBQEGBQEHEgUBBAUBBw8BAQVjdHhfNQUBBRUFAQUBAQNhcmMFAQYEBQEGBQEEBQEFBQEDDwEBBWN0eF81BQEDFQUBAwEBCWZpbGxTdHlsZQUBBA8BAQZjb2xvdXIFAQUGBQEEBQEFFAUBAwEBCWZpbGxTdHlsZQUBBBEFAQQPAQEFY3R4XzUFAQUVBQEFAQEEZmlsbAUBBgQFAQYFAQQFAQUFAQMPAQEFY3R4XzUFAQMVBQEDAQELc3Ryb2tlU3R5bGUFAQQPAQEGY29sb3VyBQEFBgUBBAUBBRQFAQMBAQtzdHJva2VTdHlsZQUBBBEFAQQPAQEFY3R4XzUFAQUVBQEFAQEGc3Ryb2tlBQEGBAUBBgUBBAUBBQUBAxABAQN4XzMQAQEDeV80EAEBAW0QAQEFY3R4XzUQAQEGY29sb3VyLwQLBgRbHQAADgEBCXZhcl9udW1lMQQOAQEJdmFyX251bWUyBA4BAQl2YXJfbnVtZTMEDgEBCXZhcl9udW1lNAQOAQEJdmFyX2Rlbm9tBA4BAQh2YXJfYTFfYQQOAQEIdmFyX2EyX2EEDgEBBnZhcl94MQQOAQEGdmFyX3kxBA4BAQZ2YXJfeDIEDgEBBnZhcl95MgQRBQEEBgUBBQYAEgUBBAUBBQYFAQUGABIFAQQFAQUFBQEFFQUBBQEBB2NhbnZhczEFAQUVBQEFAQEFd2lkdGgFAQUSBQEEBQEFBQUBBRUFAQUBAQdjYW52YXMxBQEFFQUBBQEBBmhlaWdodAUBBRIFAQQFAQUPAQEIdmFyX2N0eDEFAQUVBQEFAQEJY2xlYXJSZWN0BQEGBAUBBgUBBAUBBQUBAw8BAQl2YXJfbnVtZTEFAQMPAQEFdmFyX2cFAQQpBQEEBQEFBgUBBAYBAg8BAQZ2YXJfbTEFAQYJBQEEBQEGBQEHDwEBBnZhcl9tMgUBBAcFAQcFAQQFAQYJBQEFBQEGBQEEEQUBBg8BAQZ2YXJfYTEFAQcSBQEGBQEHBQUBBxUFAQcBAQRNYXRoBQEHFQUBBwEBA3NpbgUBCAQFAQgFAQYFAQcFAQUJBQEEBQEFBQEGBgUBAwUBBg4BAQl2YXJfbnVtZTEFAQMPAQEJdmFyX251bWUyBQEEDwEBBnZhcl9tMgUBBSkFAQUFAQYPAQEFdmFyX2cFAQUJBQEGBQEFBQEHEQUBBg8BAQZ2YXJfYTEFAQgGBQEJBgECDwEBBnZhcl9hMgUBCgkFAQkFAQoFAQsIBQEIBQELBQEJEgUBBgUBCQUFAQgVBQEIAQEETWF0aAUBCBUFAQgBAQNzaW4FAQkEBQEJBQEGBQEIBQEFCQUBBwUBBQUBBgYFAQQFAQYOAQEJdmFyX251bWUyBQEEDwEBCXZhcl9udW1lMwUBBQYFAQYGAQIpBQEGBQEHEQUBCA8BAQZ2YXJfYTEFAQkPAQEGdmFyX2EyBQEKCAUBCQUBCgUBCxIFAQgFAQsFBQEJFQUBCQEBBE1hdGgFAQkVBQEJAQEDc2luBQEKBAUBCgUBCAUBCQUBBgkFAQcFAQYFAQgPAQEGdmFyX20yBQEGCQUBCAUBBgUBBwYFAQUFAQcOAQEJdmFyX251bWUzBQEFDwEBCXZhcl9udW1lNAUBBg8BAQh2YXJfYTJfdgUBBw8BAQh2YXJfYTJfdgUBCAkFAQcFAQgFAQkPAQEGdmFyX3IyBQEHCQUBCQUBBwUBCA8BAQh2YXJfYTFfdgUBBw8BAQh2YXJfYTFfdgUBCQkFAQcFAQkFAQoPAQEGdmFyX3IxBQEHCQUBCgUBBwUBCREFAQoPAQEGdmFyX2ExBQELDwEBBnZhcl9hMgUBDAgFAQsFAQwFAQ0SBQEKBQENBQUBCxUFAQsBAQRNYXRoBQELFQUBCwEBA2NvcwUBDAQFAQwFAQoFAQsFAQcJBQEJBQEHBQEKBwUBCAUBCgUBBwYFAQYFAQcOAQEJdmFyX251bWU0BQEGDwEBCXZhcl9kZW5vbQUBBw8BAQZ2YXJfcjEFAQgGBQEJBgECDwEBBnZhcl9tMQUBCgkFAQkFAQoFAQsPAQEGdmFyX20yBQEJBwUBCwUBCQUBCg8BAQZ2YXJfbTIFAQkRBQEMBgUBDQYBAg8BAQZ2YXJfYTEFAQ4JBQENBQEOBQEPBgUBDQYBAg8BAQZ2YXJfYTIFAQ4JBQENBQEOBQEQCAUBDwUBEAUBDRIFAQwFAQ0FBQENFQUBDQEBBE1hdGgFAQ0VBQENAQEDY29zBQEOBAUBDgUBDAUBDQUBCwkFAQkFAQsFAQwIBQEKBQEMBQEJCQUBCAUBCQUBCgYFAQcFAQoOAQEJdmFyX2Rlbm9tBQEHDwEBCHZhcl9hMV9hBQEIDwEBCXZhcl9udW1lMQUBCQ8BAQl2YXJfbnVtZTIFAQoHBQEJBQEKBQELDwEBCXZhcl9udW1lMwUBCQ8BAQl2YXJfbnVtZTQFAQoJBQEJBQEKBQEMBwUBCwUBDAUBCQ8BAQl2YXJfZGVub20FAQoKBQEJBQEKBQELBgUBCAUBCw4BAQh2YXJfYTFfYQUBCA8BAQl2YXJfbnVtZTEFAQkGBQEKBgECEQUBDA8BAQZ2YXJfYTEFAQ0PAQEGdmFyX2EyBQEOCAUBDQUBDgUBDxIFAQwFAQ8FBQENFQUBDQEBBE1hdGgFAQ0VBQENAQEDc2luBQEOBAUBDgUBDAUBDQUBCwkFAQoFAQsFAQwGBQEJBQEMDgEBCXZhcl9udW1lMQUBCQ8BAQl2YXJfbnVtZTIFAQkPAQEIdmFyX2ExX3YFAQoPAQEIdmFyX2ExX3YFAQsJBQEKBQELBQEMDwEBBnZhcl9yMQUBCgkFAQwFAQoFAQsPAQEGdmFyX20xBQEKDwEBBnZhcl9tMgUBDAcFAQoFAQwFAQ0JBQELBQENBQEKBgUBCQUBCg4BAQl2YXJfbnVtZTIFAQkPAQEJdmFyX251bWUzBQEJDwEBBXZhcl9nBQEKDwEBBnZhcl9tMQUBCw8BAQZ2YXJfbTIFAQwHBQELBQEMBQENCQUBCgUBDQUBCxEFAQwPAQEGdmFyX2ExBQENEgUBDAUBDQUFAQ0VBQENAQEETWF0aAUBDRUFAQ0BAQNjb3MFAQ4EBQEOBQEMBQENBQEKCQUBCwUBCgUBDAYFAQkFAQwOAQEJdmFyX251bWUzBQEJDwEBCXZhcl9udW1lNAUBCQ8BAQh2YXJfYTJfdgUBCg8BAQh2YXJfYTJfdgUBCwkFAQoFAQsFAQwPAQEGdmFyX3IyBQEKCQUBDAUBCgUBCw8BAQZ2YXJfbTIFAQoJBQELBQEKBQEMEQUBCw8BAQZ2YXJfYTEFAQ0PAQEGdmFyX2EyBQEOCAUBDQUBDgUBDxIFAQsFAQ8FBQENFQUBDQEBBE1hdGgFAQ0VBQENAQEDY29zBQEOBAUBDgUBCwUBDQUBCgkFAQwFAQoFAQsGBQEJBQELDgEBCXZhcl9udW1lNAUBCQ8BAQl2YXJfZGVub20FAQkPAQEGdmFyX3IyBQEKBgUBCwYBAg8BAQZ2YXJfbTEFAQwJBQELBQEMBQENDwEBBnZhcl9tMgUBCwcFAQ0FAQsFAQwPAQEGdmFyX20yBQELEQUBDgYFAQ8GAQIPAQEGdmFyX2ExBQEQCQUBDwUBEAUBEQYFAQ8GAQIPAQEGdmFyX2EyBQEQCQUBDwUBEAUBEggFAREFARIFAQ8SBQEOBQEPBQUBDxUFAQ8BAQRNYXRoBQEPFQUBDwEBA2NvcwUBEAQFARAFAQ4FAQ8FAQ0JBQELBQENBQEOCAUBDAUBDgUBCwkFAQoFAQsFAQwGBQEJBQEMDgEBCXZhcl9kZW5vbQUBCQ8BAQh2YXJfYTJfYQUBCQ8BAQl2YXJfbnVtZTEFAQoPAQEJdmFyX251bWUyBQELDwEBCXZhcl9udW1lMwUBDAcFAQsFAQwFAQ0PAQEJdmFyX251bWU0BQELBwUBDQUBCwUBDAkFAQoFAQwFAQsP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BQUBAxEFAQQGBQEFAQEJR3Jhdml0eTogDwEBBXZhcl9nBQEGBwUBBQUBBgUBBxIFAQQFAQcFBQEFFQUBBQEBB2NvbnNvbGUFAQUVBQEFAQEDbG9nBQEGBAUBBgUBBAUBBQUBAxEFAQQPAQEMZnVuY19hbmltYXRlBQEFEgUBBAUBBQUFAQUVBQEFAQEGd2luZG93BQEFFQUBBQEBFXJlcXVlc3RBbmltYXRpb25GcmFtZQUBBgQFAQYFAQQFAQUFAQMvBAsGBAghAAARBQEEDwEBBHhfMTIFAQUSBQEEBQEFDwEBBHlfMTMFAQUSBQEEBQEFDwEBAXcFAQUSBQEEBQEFDwEBAWgFAQUSBQEEBQEFDwEBBmN0eF8xNAUBBRUFAQUBAQljbGVhclJlY3QFAQYEBQEGBQEEBQEFBQEDEAEBBHhfMTIQAQEEeV8xMxABAQF3EAEBAWgQAQEGY3R4XzE0LwQLBgQKJAAADwEBCHZhcl9vbGR4BQEDDwEBC3Zhcl90cmFpbHN4BQEEBgUBBQYAFQUBBAUBBQUBBAYFAQMFAQQOAQEIdmFyX29sZHgFAQMPAQEIdmFyX29sZHkFAQMPAQELdmFyX3RyYWlsc3kFAQQGBQEFBgAVBQEEBQEFBQEEBgUBAwUBBA4BAQh2YXJfb2xkeQUBAwAFBQEDFQUBAwEBAWkFAQMGBQEEBgAGBQEDBQEEBQUBBRQFAQUBAQFpBQEDBQUBBBUFAQQBAQFpBQEEDwEBC3Zhcl90cmFpbHN4BQEFFQUBBQEBBmxlbmd0aAUBBQYFAQYGAQEIBQEFBQEGBQEHHQUBBAUBBwUBBQ0FAQUGBFsjAAAPAQELdmFyX3RyYWlsc3gFAQQFBQEGFQUBBgEBAWkFAQYVBQEEBQEGBQEHDwEBC3Zhcl90cmFpbHN4BQEIBQUBCRUFAQkBAQFpBQEJBgUBCgYBAQcFAQkFAQoFAQsVBQEIBQELBQEIBgUBBwUBCBQFAQQFAQYFAQcPAQELdmFyX3RyYWlsc3kFAQQFBQEGFQUBBgEBAWkFAQYVBQEEBQEGBQEHDwEBC3Zhcl90cmFpbHN5BQEIBQUBCRUFAQkBAQFpBQEJBgUBCgYBAQcFAQkFAQoFAQsVBQEIBQELBQEIBgUBBwUBCBQFAQQFAQYFAQcFBQEEFQUBBAEBAWkFAQQGBQEGBQEEBQUBBxUFAQcBAQFpBQEHBgUBCAYBAQcFAQcFAQgFAQcFBQEJFAUBCQEBAWkFAQcLBgTJIQAAAQ8BAQt2YXJfdHJhaWxzeAUBBw8BAQ92YXJfdHJhaWxMZW5ndGgFAQgVBQEHBQEIBQEJDwEBBHhfMTcFAQoGBQEJBQEKFAUBBwUBCAUBCQ8BAQt2YXJfdHJhaWxzeQUBBw8BAQ92YXJfdHJhaWxMZW5ndGgFAQgVBQEHBQEIBQEJDwEBBHlfMTgFAQoGBQEJBQEKFAUBBwUBCAUBCRABAQR4XzE3EAEBBHlfMTgvBAsGBMkkAAAFBQEDFQUBAwEBA251bQUBAxEFAQURBQEHBQUBCBUFAQgBAQRNYXRoBQEIFQUBCAEBBnJhbmRvbQUBCQQFAQkFAQcFAQgFAQYPAQEEeF8yMQUBBwkFAQYFAQcFAQgSBQEFBQEIBQUBBhUFAQYBAQRNYXRoBQEGFQUBBgEBBWZsb29yBQEHBAUBBwUBBQUBBgUBBAYFAQMFAQQFBQEFFAUBBQEBA251bQUBAy8FAQMQAQEEeF8yMS8ELQsGBIElAAAPAQEFdmFyX2oFAQMGBQEEBgEBBwUBAwUBBAUBAw4BAQV2YXJfagUBAwUFAQMVBQEDAQEGY29sb3VyBQEDBgUBBAEBBGhzbCgPAQEFdmFyX2oFAQUHBQEEBQEFBQEGBgUBBAEBDCwgMTAwJSwgNTAlKQcFAQYFAQQFAQUGBQEDBQEFBQUBBBQFAQQBAQZjb2xvdXIFAQMFBQEDFQUBAwEBBmNvbG91cgUBAy8FAQMvBAsGBIolAAAvBBEFASoFBQErBAUBCgUBKgUBKwUBKQ==';
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

function decode(op) {
    return op;
}

function run(args) {

    if (args != undefined) {
        // used when running as function
        instruction_index = args.func_start_index;
    }

    while (instruction_index < bytecode.length) {
        let op = decode(b_next());

        //console.log(instruction_index, op, operations[op]);

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
