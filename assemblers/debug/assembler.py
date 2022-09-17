import sys
import base64

if len(sys.argv) != 4:
    print('usage: python3 assembler.py instructions template_vm out')
    exit()


ins_file = sys.argv[1]
vm_file= sys.argv[2]
outfile = sys.argv[3]

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

with open(outfile, 'w') as f:
    f.write(vm)
