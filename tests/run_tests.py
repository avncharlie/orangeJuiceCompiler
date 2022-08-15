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


def test_files(file_list, name='tests'):
    succ = 0
    fail = 0

    for test_file in file_list:
        print('testing: {} ... '.format(test_file))
        result = run_test(test_file)
        if result: succ += 1
        else: fail += 1
        print('...'+('PASSED' if result else 'FAILED'))
        print()

    print('{} {} passed, {} {} failed.'.format(succ, name, fail, name))
    print()


if len(sys.argv) == 1:
    tests = [f for f in os.listdir() if f.startswith('test_')]
    benchmarks = ['../benchmarks/'+f for f in os.listdir('../benchmarks')]

    print('* unit tests *')
    test_files(tests)

    print('* benchmarks *')
    test_files(benchmarks, 'benchmarks')
else:
    tests = sys.argv[1:]
    test_files(tests)
