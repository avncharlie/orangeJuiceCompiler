import sys
import json
import struct
import base64

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
OP_CODES = {
    "push_store": 0,
    "pop_store": 1,
    "whatsthis": 2,
    "create_func": 3,
    "call": 4,
    "global": 5,
    "mov": 6,
    "add": 7,
    "sub": 8,
    "mul": 9,
    "div": 10,
    "jmp": 11,
    "jt": 12,
    "jnt": 13,
    "setvar": 14,
    "getvar": 15,
    "delvar": 16,
    "arr": 17,
    "arrpush": 18,
    "obj": 19,
    "setprop": 20,
    "getprop": 21,
    "eq": 22,
    "neq": 23,
    "eqt": 24,
    "neqt": 25,
    "ge": 26,
    "geeq": 27,
    "le": 28,
    "leeq": 29,
    "mod": 30,
    "shl": 31,
    "shr": 32,
    "ushr": 33,
    "pow": 34,
    "bit_or": 35,
    "bit_and": 36,
    "xor": 37,
    "inside": 38,
    "check_instance": 39,
    "unary_plus": 40,
    "unary_neg": 41,
    "unary_not": 42,
    "unary_bit_not": 43,
    "unary_typeof": 44,
    "nop": 45,
    "regex": 46,
    "return": 47,
}

def byte_length(i):
    return (i.bit_length() + 7) // 8

class Instruction:
    def __init__(self, instruction_info):
        self.info = instruction_info

        self.is_label = False
        self.label_referenced = None
        self.patch_start = None
        if self.info['type'] == 'label':
            self.is_label = True
        else:
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

        # add op code
        assembled.append(OP_CODES[self.info['op']])

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
            print(self.instructions[i]['string_repr'])
            assembled = self.assembled_instructions[i]
            print('{}-{}: {}'.format(assembled.start_index, assembled.end_index(), list(assembled.assembled)))
            print()


assembler = Assembler(instructions)
bytecode = assembler.assemble()
encoded_bytecode = base64.b64encode(bytecode).decode('utf-8')

if '-l' in sys.argv:
    assembler.display()

vm = "let bytecode = '{}';\n".format(encoded_bytecode)

reading = False
with open(vm_file, 'r') as f:
    for line in f:
        if line == '// end vm\n':
            reading = False

        if reading:
            vm += line

        if line == '// begin vm\n':
            reading = True

with open(outfile, 'w') as f:
    f.write(vm)

