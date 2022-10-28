#!/usr/bin/env python3
import os
import sys
import subprocess
import shlex

def run_command(cmd):
    r = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    if r.returncode != 0:
        print('command failed: ' + cmd)
        print(r.stderr)
        return False
    return r.stdout

def run_vm(assembler, f):
    # generate ast
    cmd = 'node ../generate_ast/index.js {} build/ast'.format(f)
    out = run_command(cmd)
    if out is False: return (False, 'ast generation failed')

    # compile
    cmd = 'python3 ../compiler.py build/ast build/ins.json'.format(f)
    out = run_command(cmd)
    if out is False: return (False, 'compilation failed')

    # assemble
    cmd = 'python3 {}/assembler.py build/ins.json {}/template_vm.js build/out.js'.format(assembler, assembler)
    out = run_command(cmd)
    if out is False: return (False, 'assembly failed')

    # run 
    cmd = 'node build/out.js'
    out = run_command(cmd)
    if out is False: return (False, 'failed at runtime')

    return (True, out)

def run_node(f):
    # run 
    cmd = 'node {}'.format(f)
    out = run_command(cmd)
    if out is False: return False
    return out

def run_test(assembler, f):
    node_out = run_node(f)
    if node_out is False:
        print('test fault, failed running with node')
        return False

    status, vm_out = run_vm(assembler, f)
    if not status:
        print('vm failed, reason: {}'.format(vm_out))
        return False

    result = node_out == vm_out
    if not result:
        print('expected:\n{}'.format(node_out))
        print('but got:\n{}'.format(vm_out))

    return result


summary = ""

def test_files(assembler, file_list, name='tests'):
    global summary
    succ = 0
    fail = 0

    fails = []
    for test_file in file_list:
        print('testing: {} ... '.format(test_file))
        result = run_test(assembler, test_file)
        if result:
            succ += 1
        else:
            fail += 1
            fails.append(test_file)
            
        print('...'+('PASSED' if result else 'FAILED'))
        print()

    results = ""

    results += '{} {} passed, {} {} failed.\n'.format(succ, name, fail, name)
    if len(fails) > 0:
        results += 'failed tests:\n'
        for f in fails:
            results += (' - {}\n'.format(f))

    print(results)

    summary += results + '\n'

def get_assemblers():
    assembler_files = ['../assemblers/'+f for f in os.listdir('../assemblers')]
    assemblers = []
    for pos_assembler in assembler_files:
        if os.path.isdir(pos_assembler):
            k = pos_assembler.split('/')[-1]
            if k != 'grapher':
                assemblers.append(k)
    return assemblers

if len(sys.argv) < 2:
    print('usage: python3 run_tests.py assembler [tests]')
    exit()

assembler = sys.argv[1]
valid_assemblers = get_assemblers()

if assembler not in valid_assemblers:
    print('"{}" not valid assembler, must be one of: {}'.format(assembler, valid_assemblers))
    exit()

assembler = '../assemblers/'+assembler
    
if len(sys.argv) == 2:
    tests = [f for f in os.listdir() if f.startswith('test_')]
    benchmarks = []
    for f in os.listdir('../benchmarks'):
        if f != 'silent':
            benchmarks.append('../benchmarks/'+f)

    print('* unit tests *')
    test_files(assembler, tests)

    print('* benchmarks *')
    test_files(assembler, benchmarks, name='benchmarks')
else:
    tests = sys.argv[2:]
    test_files(assembler, tests)

print('SUMMARY:')
print(summary[:-1])
