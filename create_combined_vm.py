import sys
import base64

usage = 'python3 create_combined_vm.py instructions out_vm template_vm'

ins_file = 'ins.json'
out_vm = 'out.js'
vm_file = 'debug_vm.js'

if len(sys.argv) > 1:
    ins_file = sys.argv[1]

if len(sys.argv) > 2:
    out_vm = sys.argv[2]

if len(sys.argv) > 3:
    vm_file = sys.argv[3]

with open(ins_file, 'r') as f:
    b = base64.b64encode(f.read().encode('utf-8')).decode('utf-8')

vm = "let instructions = JSON.parse(decodeURIComponent(escape(atob('{}'))));\n".format(b)

reading = False
with open(vm_file, 'r') as f:
    for line in f:
        if line == '// end vm\n':
            reading = False

        if reading:
            vm += line

        if line == '// begin vm\n':
            reading = True

with open(out_vm, 'w') as f:
    f.write(vm)
