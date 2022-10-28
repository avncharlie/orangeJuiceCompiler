import sys
import json
import struct
import base64
import random
import subprocess
import shlex
import pygraphviz as pgv

BUILD_DIR = 'build/graph/'

if len(sys.argv) < 2:
    print('usage: python3 assembler.py instructions [out.png]')
    exit()

OUT = 'disass.png'
if len(sys.argv) == 3:
    if sys.argv[2] != '-s':
        OUT = sys.argv[2]
def run_command(cmd):
    r = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    if r.returncode != 0:
        print('command failed: ' + cmd)
        print(r.stderr)
        return False
    return r.stdout

ins_file = sys.argv[1]
#vm_file = sys.argv[2]
#outfile = sys.argv[3]

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
    def encode(self, instr):
        key = self.info['top_scope_declared']
        return [byte ^ key for byte in instr]

    def get_op_code(self):
        return OP_CODES[self.info['op']]

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

    def get_label(self):
        for arg in self.info['args']:
            if arg['type'] == 'label':
                return arg['value']

    def assemble(self):
        if self.is_label:
            self.assembled = b'';
            self.size = 0;
            return b'';

        assembled = []

        # add op code
        assembled.append(self.get_op_code())

        # add arguments
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

        # encode instruction
        assembled = self.encode(assembled)

        encoded_op = assembled[0]
        if encoded_op not in encode_dict[self.info['op']]:
            encode_dict[self.info['op']].append(encoded_op)

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
        patch_loc = bytes(self.encode(patch_loc.to_bytes(4, 'little')))
        self.assembled = self.assembled[:self.patch_start] \
                + patch_loc \
                + self.assembled[self.patch_start+4:]

    def end_index(self):
        return self.start_index + self.size

class Assembler:
    def __init__(self, instructions):
        self.instructions = instructions
        self.assembled_instructions = []
        self.label_indexes = {}

        self.subgraph_start_keys = [0]
        self.graph_nodes = []
        self.graph_connections = {}
        self.next_key = 0

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

    def bytecode_index_to_instruction_index(self, bytecode_index):
        for i, ins in enumerate(self.assembled_instructions):
            if ins.start_index == bytecode_index:
                return i

    def label_instruction_index(self, label):
        for i, ins in enumerate(self.assembled_instructions):
            if ins.is_label and ins.info['id'] == label:
                return i

    def _create_graph(self, ins_index=0, coming_from=None):

        # don't create new node for existing node
        if coming_from is not None:
            for node in self.graph_nodes:
                if node['block_start'] == ins_index:
                    if coming_from not in self.graph_connections:
                        self.graph_connections[coming_from] = []
                    self.graph_connections[coming_from].append(node['key'])
                    return

        key = self.next_key
        self.next_key += 1
        node_info = {
            'key': key,
            'block_start': ins_index,
            'instructions': []
        }

        # TODO: should probably change to just single item or none instead of list
        if coming_from is not None:
            if coming_from not in self.graph_connections:
                self.graph_connections[coming_from] = []
            self.graph_connections[coming_from].append(key)

        first_loop = True
        while ins_index < len(self.assembled_instructions):

            # don't extend block past existing block
            for node in self.graph_nodes:
                if node['block_start'] == ins_index:
                    self.graph_nodes.append(node_info)
                    return

            curr_ins = self.assembled_instructions[ins_index]
            node_info['instructions'].append(curr_ins)
            ins_index += 1

            if not curr_ins.is_label:
                if curr_ins.info['op'] in ['jt', 'jnt']:
                    self.graph_nodes.append(node_info)
                    
                    jump_loc = self.label_instruction_index(curr_ins.get_label())
                    next_loc = ins_index + 1

                    self._create_graph(ins_index=jump_loc, coming_from=key)
                    self._create_graph(ins_index=next_loc, coming_from=key)
                    return

                elif curr_ins.info['op'] == 'jmp':
                    self.graph_nodes.append(node_info)

                    jump_loc = self.label_instruction_index(curr_ins.get_label())
                    self._create_graph(ins_index=jump_loc, coming_from=key)
                    return

                elif curr_ins.info['op'] == 'ret':
                    # return ends block and function
                    break

            elif not first_loop:
                # if label, break to new block (ignore on first loop)
                node_info['instructions'].pop()
                ins_index -= 1

                label_id = curr_ins.info['id']
                self.graph_nodes.append(node_info)

                self._create_graph(ins_index=ins_index, coming_from=key)
                return

            first_loop = False

        # if reached end, exit
        self.graph_nodes.append(node_info)

    def create_graph(self):
        # first graph top level code
        self._create_graph(ins_index=0, coming_from=None)

        subgraph_start_keys = []

        # then graph function code
        non_func_labels = []
        for node in self.graph_nodes:
            start_ins = self.assembled_instructions[node['block_start']]
            if start_ins.is_label:
                non_func_labels.append(start_ins.info['id'])
        for i, instr in enumerate(self.assembled_instructions):
            if instr.is_label:
                if instr.info['id'] not in non_func_labels:
                    subgraph_start_keys.append(self.next_key)
                    self._create_graph(ins_index=i, coming_from=None)

        # get rid of empty nodes
        new = []
        delkeys = []
        for node in self.graph_nodes:
            if len(node['instructions']) > 0:
                new.append(node)
            else:
                delkeys.append(node['key'])
        self.graph_nodes = new

        for n in subgraph_start_keys:
            if n not in delkeys:
                self.subgraph_start_keys.append(n)

    def _get_subgraphs(self, start_key, seen_keys):
        seen_keys = seen_keys[:]
        seen_keys.append(start_key)
        r = {}
        if start_key in self.graph_connections:
            r[start_key] = self.graph_connections[start_key]
            for child in self.graph_connections[start_key]:
                if child in seen_keys:
                    continue
                seen_keys.append(child)
                r.update(self._get_subgraphs(child, seen_keys))
        return r

    def get_subgraphs(self):
        subgraphs = []
        for key in self.subgraph_start_keys:
                   
            subgraphs.append((self._get_subgraphs(key, []), key),)

        return subgraphs

    def draw_graph(self, outfile, split=False):
        subgraphs = self.get_subgraphs()

        # generate dot files
        k = 0
        fnames = []
        for subgraph, start_key in subgraphs:

            allowed_nodes = []
            for s in subgraph:
                allowed_nodes.append(s)
                allowed_nodes += subgraph[s]

            g = pgv.AGraph(directed=True)
            g.node_attr['shape'] = 'box'
            g.node_attr['fontname'] = 'courier'

            # add nodes to graph
            for node in self.graph_nodes:
                if node['key'] not in allowed_nodes:
                    continue
                label = ''
                for ins in node['instructions']:
                    label += ins.info['string_repr'].replace('"""', '"') + r'\l'
                g.add_node(node['key'], label=label)

            # add edges to graph
            edges = []
            for conn in subgraph:
                for end in subgraph[conn]:
                    edges.append((conn, end),)
            g.add_edges_from(edges)

            # layout graph
            g.layout(prog='dot')

            # TODO: why are graphs being created with no nodes?
            if g.nodes() == []:
                continue

            # draw graph
            if split:
                fname = None
                for node in self.graph_nodes:
                    if node['key'] == start_key:
                        ins_index = node['block_start']
                        ins = self.assembled_instructions[ins_index]
                        bytecode_index = ins.start_index
                        fname = 'ins.{}.bcode.{}'.format(ins_index, bytecode_index)
                        if ins.is_label:
                            fname = ins.info['id'] + '.' + fname
                g.draw(BUILD_DIR+fname+'.png')
            else:
                fname = BUILD_DIR + '{}.dot'.format(k)
                fnames.append(fname)
                g.write(fname)
            k += 1

        if split:
            return

        # combine outfiles
        cmd = 'gvpack -o {} {} '.format(BUILD_DIR+'out.dot', ' '.join(fnames))
        run_command(cmd)

        # render graph
        cmd = 'neato -n2 -T png -o {} {}'.format(outfile, BUILD_DIR+'out.dot')
        run_command(cmd)

        # remove created files 
        cmd = 'rm {} {}'.format(BUILD_DIR+'out.dot', ' '.join(fnames))
        run_command(cmd)

    def display(self):
        for i in range(len(self.instructions)):
            assembled = self.assembled_instructions[i]
            print('{}: {}, {}'.format(str(assembled.start_index+1).zfill(3), list(assembled.assembled), self.instructions[i]['string_repr']))


assembler = Assembler(instructions)
bytecode = assembler.assemble()
assembler.create_graph()
split = '-s' in sys.argv
print('Rendering ...')
assembler.draw_graph(OUT, split=split)


#print(assembler.graph_connections)
#for node in assembler.graph_nodes:
#    print('---------')
#    print('key: {}'.format(node['key']))
#    print('block start: {}'.format(node['block_start']))
#    for ins in node['instructions']:
#        print('   ' + ins.info['string_repr'])


encoded_bytecode = base64.b64encode(bytecode).decode('utf-8')

if '-ll' in sys.argv:
    assembler.display()
    for op in encode_dict:
        if encode_dict[op] != []:
            print('{}: {}'.format(op, ', '.join([str(x) for x in sorted(encode_dict[op])])))

exit()

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

