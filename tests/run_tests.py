import os
import subprocess
import shlex

def run_command(cmd):
    r = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    if r.returncode != 0:
        print('command failed: ' + cmd)
        print(r.stderr)
        return False
    return r.stdout

def run_vm(f):
    # generate ast
    cmd = 'node ../generate_ast/index.js {} ast'.format(f)
    out = run_command(cmd)
    if out is False: return (False, 'ast generation failed')

    # compile
    cmd = 'python3 ../compiler.py ast ins.json'.format(f)
    out = run_command(cmd)
    if out is False: return (False, 'compilation failed')

    # run 
    cmd = 'node ../debug_vm.js ins.json'.format(f)
    out = run_command(cmd)
    if out is False: return (False, 'failed at runtime')

    return (True, out)

def run_node(f):
    # run 
    cmd = 'node {}'.format(f)
    out = run_command(cmd)
    if out is False: return False
    return out

def run_test(f):
    node_out = run_node(f)
    if node_out is False:
        print('test fault, failed running with node')
        return False

    status, vm_out = run_vm(f)
    if not status:
        print('vm failed, reason: {}'.format(vm_out))
        return False

    result = node_out == vm_out
    if not result:
        print('expected:\n{}'.format(node_out))
        print('but got:\n{}'.format(vm_out))

    return result

test_files = [f for f in os.listdir() if f.startswith('test_')]
benchnmarks = ['../benchmarks/'+f for f in os.listdir('../benchmarks')]

succ = 0
fail = 0

print('* unit tests *')
for test_file in test_files:
    print('testing: {} ... '.format(test_file))
    result = run_test(test_file)
    if result: succ += 1
    else: fail += 1
    print('...'+('PASSED' if result else 'FAILED'))
    print()

print('{} tests passed, {} tests failed'.format(succ, fail))
print()


succ = 0
fail = 0
print('* benchmarks *')
for test_file in benchnmarks:
    print('testing: {} ... '.format(test_file))
    result = run_test(test_file)
    if result: succ += 1
    else: fail += 1
    print('...'+('PASSED' if result else 'FAILED'))
    print()

run_command('rm ast .ins_read ins.json')

print('{} benchmarks passed, {} benchmarks failed'.format(succ, fail))
