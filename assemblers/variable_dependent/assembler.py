import sys
import json
import struct
import base64
import random

if len(sys.argv) < 4:
    print('usage: python3 assembler.py instructions template_vm out')
    exit()

ins_file = sys.argv[1]
vm_file = sys.argv[2]
outfile = sys.argv[3]

with open(ins_file) as ins:
    instructions = json.load(ins)['instructions']

ARG_TYPE_CODES = {
    'string': 1, 
    'boolean': 2, 
    'null': 3, 
    'Undefined': 4, 
    'register': 5, 
    'number': 6, 
    'label': 6, 
    'float': 7, 
}

OP_CODE_SIZE = 1
OPS = [
    "push_store",
    "pop_store",
    "whatsthis",
    "create_func",
    "call",
    "global",
    "mov",
    "add",
    "sub",
    "mul",
    "div",
    "jmp",
    "jt",
    "jnt",
    "setvar",
    "getvar",
    "delvar",
    "arr",
    "arrpush",
    "obj",
    "setprop",
    "getprop",
    "eq",
    "neq",
    "eqt",
    "neqt",
    "ge",
    "geeq",
    "le",
    "leeq",
    "mod",
    "shl",
    "shr",
    "ushr",
    "pow",
    "bit_or",
    "bit_and",
    "xor",
    "inside",
    "check_instance",
    "unary_plus",
    "unary_neg",
    "unary_not",
    "unary_bit_not",
    "unary_typeof",
    "nop",
    "regex",
    "ret",
]

# randomise op codes
random.shuffle(OPS)

OP_CODES = {op: i for i, op in enumerate(OPS)}

# bookkeep op codes an op got jjjd
encode_dict = {op:[] for op in OP_CODES}

def byte_length(i):
    return (i.bit_length() + 7) // 8

class Instruction:
    def encoded_op_code(self):
        op = OP_CODES[self.info['op']]
        encoded = op ^ self.info['top_scope_declared']
        return encoded

    def __init__(self, instruction_info):
        self.info = instruction_info

        self.is_label = False
        self.label_referenced = None
        self.patch_start = None
        if self.info['type'] == 'label':
            self.is_label = True
        else:
            if self.info['op'] == 'return':
                self.info['op'] = 'ret'

            for arg in self.info['args']:
                if arg['type'] == 'label':
                    self.label_referenced = arg['value']
                    break

        self.assembled = None
        self.size = -1
        self.start_index = -1

    def assemble(self):
        if self.is_label:
            self.assembled = b'';
            self.size = 0;
            return b'';

        assembled = []

        # add encoded op code
        encoded_op = self.encoded_op_code()
        if encoded_op not in encode_dict[self.info['op']]:
            encode_dict[self.info['op']].append(encoded_op)
        assembled.append(encoded_op)

        # encode arguments
        for arg in self.info['args']:
            t = arg['type']
            v = arg['value']

            # labels will be patched later
            if t == 'label':
                self.patch_start = len(assembled) + 2
                v = 0

            assembled.append(ARG_TYPE_CODES[t])
            if t == 'string':
                # encode string length as number
                s_len = len(v)
                l = byte_length(s_len)
                assembled.append(l)
                assembled += list(s_len.to_bytes(l, 'little'))
                # encode string
                assembled += list(v.encode())
            elif t == 'boolean':
                assembled.append(int(v))
            elif t in ['register', 'number', 'label']:
                # yuck
                if type(v) is float:
                    assembled.pop()
                    assembled.append(ARG_TYPE_CODES['float'])
                    assembled += list(struct.pack('f', v))
                else:
                    l = byte_length(v)
                    if t == 'label':
                        l = 4
                    assembled.append(l)
                    assembled += list(v.to_bytes(l, 'little'))
            elif t not in ['null', 'Undefined']:
                raise Exception('argument type {} unknown'.format(t))

        try:
            self.assembled = bytes(assembled)
        except ValueError as e:
            print(e)
            print(self.info['string_repr'])
            print(assembled)
            exit()
        self.size = len(self.assembled)
        return self.assembled

    def patch(self, patch_loc):
        self.assembled = self.assembled[:self.patch_start] \
                + patch_loc.to_bytes(4, 'little') \
                + self.assembled[self.patch_start+4:]

    def end_index(self):
        return self.start_index + self.size

class Assembler:
    def __init__(self, instructions):
        self.instructions = instructions
        self.assembled_instructions = []
        self.label_indexes = {}

    def recalculate_label_indexes(self):
        pass

    def insert_assembled_instruction(self, instruction, insert_at_end=None,
            bytecode_index=None, instruction_index=None, insert_after=True):

        if insert_at_end is None:
            raise Exception('not implemented @ insert_assembled_instruction')

        ins_index = 0
        if self.assembled_instructions != []:
            ins_index = self.assembled_instructions[-1].end_index()

        instruction.start_index = ins_index
        if instruction.is_label:
            self.label_indexes[instruction.info['id']] = ins_index

        self.assembled_instructions.append(instruction)

    def gather(self):
        gathered = b''
        for instruction in self.assembled_instructions:
            gathered += instruction.assembled
        return gathered

    def assemble(self):
        # assemble instructions
        for instruction in self.instructions:

            assembled_ins = Instruction(instruction)
            assembled_ins.assemble()

            self.insert_assembled_instruction(assembled_ins, insert_at_end=True)

        # patch instructions
        for instruction in self.assembled_instructions:
            if instruction.label_referenced is not None:
                instruction.patch(self.label_indexes[instruction.label_referenced])

        # return patched assembled instructions
        return self.gather()

    def display(self):
        for i in range(len(self.instructions)):
            assembled = self.assembled_instructions[i]
            print('{}: {}, {}'.format(str(assembled.start_index+1).zfill(3), list(assembled.assembled), self.instructions[i]['string_repr']))


assembler = Assembler(instructions)
bytecode = assembler.assemble()
encoded_bytecode = base64.b64encode(bytecode).decode('utf-8')

if '-l' in sys.argv:
    assembler.display()
    for op in encode_dict:
        if encode_dict[op] != []:
            print('{}: {}'.format(op, ', '.join([str(x) for x in sorted(encode_dict[op])])))

vm = "let bytecode = '{}';\n".format(encoded_bytecode)

operations = {}

reading = False
reading_ops = False
curr_op = None
curr_op_name = None
with open(vm_file, 'r') as f:
    for line in f:
        if line == '// end operations\n':
            reading_ops = False
            # add randomised ops
            for op in OPS:
                vm += operations[op]

        if line == '// end vm\n':
            reading = False

        if reading and not reading_ops:
            vm += line

        if reading_ops == True:
            if curr_op is None:
                if line.startswith('    function'):
                    curr_op_name = line.split()[1][:-2]
                    curr_op = line
            else:
                curr_op += line
                if line.startswith('    },'):
                    operations[curr_op_name] = curr_op
                    curr_op = None
                    curr_op_name = None

        if line == '// begin vm\n':
            reading = True

        if line == '// begin operations\n':
            reading_ops = True

with open(outfile, 'w') as f:
    f.write(vm)

