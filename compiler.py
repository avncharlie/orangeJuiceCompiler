import sys
import ast as py_ast 
import copy
import json
import pprint
import secrets
import shlex
import random

out_file = open(sys.argv[2], 'w')
ast_file = open(sys.argv[1])
ast = json.load(ast_file)

'''
todo: 
    - try stack
    - loop stack
    - documentation on:
        - data stores:
            - symbols
            - registers
            - asm
        - compiler
            - how expressions are handled
    - op support
        - array arguments
        - floats
    - debug mode for get_name

compiler todo:
    - hoisting vars
'''

DEBUG = False; DEBUGDEBUG = False
#DEBUG = True; DEBUGDEBUG = False
#DEBUG = True; DEBUGDEBUG = True

# if registers[x] == false or doesn't exist, register unclaimed
reg_stack = []
registers = [False, False, False]

scopes_backup = []
scopes = {}

scope_stack_stack = []
scope_stack = [None]
curr_scope = lambda : scope_stack[len(scope_stack)-1]

loopstack = []

branch_counter = 0
asm = []

used_names = []
debug_name_counter = 0
def get_name(name='ojc'):
    '''
    return unique string for whatever purpose
    won't give 2 of the same string twice
    will ignore given name if DEBUG is false
    '''

    global debug_name_counter, used_names

    rand_length = random.randrange(4,12)

    if not DEBUG:
        name = secrets.token_hex(rand_length)
        while name in used_names:
            name = secrets.token_hex(rand_length)
        used_names.append(name)
        return name
    else:
        if name in used_names:
            debug_name_counter += 1
            name = name + '_' + str(debug_name_counter) 
        used_names.append(name)
        return name

def _debug_print_ins(func):
    def wrapper(*args, **kwargs):
        a = func(*args, **kwargs)
        if DEBUGDEBUG:
            print(a['string_repr'])
        return a

    return wrapper

@_debug_print_ins
def gen_ins(ins):
    '''
    helper function to generate instructions from a string representation

    op r5 #5 "5" None !True = op <register 5> <number 5> <string 5> str null true

    adds string representation as 'string_repr' attribute
    '''
    if ins[0] == ':':
        return {
                "type": "label",
                "id": ins[1:],
                "string_repr": ins
        }

    arguments = []
    ins_split = shlex.split(ins, posix=False)
    for part in ins_split[1:]:
        f_part = {}
        if part[0] in ['"', "'"]:
            f_part["type"] = "string"
            f_part["value"] = py_ast.literal_eval(part)
        elif part[0] in '!':
            f_part["type"] = "boolean"
            f_part["value"] = py_ast.literal_eval(part[1:])
        elif part == "None":
            f_part["type"] = "null"
            f_part["value"] = None
        elif part[0] == ":":
            f_part["type"] = "label"
            f_part["value"] = part[1:]
        else:
            if part[0] == 'r':
                f_part["type"] = "register"
            elif part[0] == '#':
                f_part["type"] = "number"
            try:
                f_part["value"] = int(part[1:])
            except ValueError:
                f_part["value"] = float(part[1:])

        arguments.append(f_part)

    return {
            "type": "operation",
            "op": ins_split[0],
            "args": arguments,
            "string_repr": ins,
    }

def request_register():
    global registers

    for i, x in enumerate(registers):
        if i in [0,1,2]: continue # can't request scratch registers
        if x == False:
            registers[i] = True
            if DEBUGDEBUG: print('...alloc r{}'.format(i))
            return i

    registers += [True]
    if DEBUGDEBUG: print('...alloc r{}'.format(len(registers)-1))
    return len(registers) - 1

def remove_all_var_registers():
    '''
    unset all registers holding variables
    '''
    for scope in scopes:
        for var_name in scopes[scope]['declared']:
            scopes[scope]['declared'][var_name]['register'] = None

def remove_var_reg(r):
    '''
    sets variables who have this register to have no register
    '''
    for scope in scopes:
        for var_name in scopes[scope]['declared']:
            if scopes[scope]['declared'][var_name]['register'] == r:
                scopes[scope]['declared'][var_name]['register'] = None

def reg_holding_var(r):
    '''
    returns true if register holding variable
    '''
    for scope in scopes:
        for var_name in scopes[scope]['declared']:
            if scopes[scope]['declared'][var_name]['register'] == r:
                return True
    return False

def free_register(r, force=False):
    '''
    unallocate specific register
    if force flag false, won't free register holding variable
    '''
    if DEBUGDEBUG: print('...free r{}'.format(r))

    if r is None:
        return

    if not force:
        if reg_holding_var(r):
            return

    global registers
    registers[r] = False
    remove_var_reg(r)

def claim_register(r):
    '''
    claim specific register (like request register but you choose the register)
    '''
    if DEBUGDEBUG: print('...claim r{}'.format(r))
    remove_var_reg(r)

def get_var_from_id(var_id):
    '''
    return 'declared' list info for a given var id
    '''
    for scope in scopes:
        for var_name in scopes[scope]['declared']:
            if scopes[scope]['declared'][var_name]['id'] == var_id:
                return scopes[scope]['declared'][var_name]
    return None

def search_scope_table(scope, name, scope_boundary='FunctionExpression'):
    '''
    find variable referenced by identifier name

    if scope_boundary is True: only look at current scope
    otherwise search up until scope_boundary scope created found
    will return object in 'declared' list for variable or None
    '''

    # try to find variable name in scope
    # stop at global scope or when scope boundary reached
    while scope is not None and scopes[scope]['created_from'] != scope_boundary:

        if name in scopes[scope]['declared']:
            # name found!
            return scopes[scope]['declared'][name]
        elif scope_boundary is True:
            # not in current scope, exit
            return None
        else:
            # not in current scope, lets look up
           scope = scopes[scope]['parent']

    # name not found
    return None

def handle_node(node, named_block=None, declare_func_mode=False):
    '''
    if given expression, assign reg to current_scope, t
    will be attached in 'register' attribute
    will also return register
    '''

    global registers, reg_stack
    global scope_stack, scope_stack_stack
    global scopes, scopes_backup

    t = node["type"]

    if t in ['FunctionDeclaration', 'FunctionExpression']:
        '''
        TODO: document declare_func_mode
        '''

        # prepare function in compiler and VM:

        if declare_func_mode:
            # step 1: get function label 
            func_name = None
            func_label = 'anon'
            func_end_label = 'anon_end'
            if node['id'] is not None:
                func_name = node['id']['name']
                func_label = get_name('func_start_'+func_name)
                func_end_label = get_name('func_end_'+func_name)


            # step 2: get arg names and store in array for VM to create func and to
            # sneak into function scope when handling function body
            arg_list_reg = request_register()
            asm.append(gen_ins('arr r{}'.format(arg_list_reg)))
            func_preset_vars = {}
            for arg in node['params']:
                arg_id = get_name(arg['name'])
                asm.append(gen_ins('arrpush r{} "{}"'.format(arg_list_reg, arg_id)))
                func_preset_vars[arg['name']] = {
                    'id': arg_id,
                    'register': None,
                    'type': 'var',
                }

            # step 3: create function in vm and store as variable if need be
            func_reg = request_register()
            node['register'] = func_reg # function declarations are an expression (e.g. anonymous functions)
            asm.append(gen_ins('create_func :{} r{} r{}'.format(func_label,
                arg_list_reg, func_reg)))

            # TODO: free arg_list_reg??

            # if function not anonymous, assign as variable
            if func_name is not None:
                func_id = get_name('func_' + node['id']['name']);

                # book keep created var (define in top scope)
                top_scope = scope_stack[1]
                scopes[top_scope]['declared'][func_name] = {
                    'id': func_id,
                    'register': func_reg,
                    'type': 'function'
                }

                # create var at runtime
                asm.append(gen_ins('setvar "{}" r{}'.format(func_id, func_reg)))

            # store names for handling run
            node['func_name'] = func_name
            node['func_label'] = func_label
            node['func_end_label'] = func_end_label
            node['func_preset_vars'] = func_preset_vars

            return

        func_name = node['func_name'] 
        func_label = node['func_label'] 
        func_end_label = node['func_end_label'] 
        func_preset_vars = node['func_preset_vars'] 

        # jump to end of function if function accidently 'run into' (calls to
        # function will jump directly to label defining it)
        asm.append(gen_ins('jmp :{}'.format(func_end_label)))

        # handle body of function:

        # step 4: push and reset register allocations
        reg_stack.append(registers[:]) # push copy of registers
        registers = [False, False, False]

        # step 5: backup scoped symbol table and remove register allocations for
        # variables
        scope_stack_stack.append(scope_stack[:])
        scopes_backup.append(copy.deepcopy(scopes))
        remove_all_var_registers()

        # step 6: handle body of function with arguments as preset vars
        asm.append(gen_ins(':' + func_label)) # start label
        handle_block(node['body']['body'], t, preset_vars=func_preset_vars)
        asm.append(gen_ins('return None')) # catch all return if there is no return in func body
        asm.append(gen_ins(':' + func_end_label))

        # cleanup:

        # step 7: restore all backed up registers and scope information
        registers = reg_stack.pop()
        scope_stack = scope_stack_stack.pop()
        scopes = scopes_backup.pop()

    elif t == 'ReturnStatement':
        if 'argument' in node:
            handle_node(node['argument'])
            return_reg = node['argument']['register']
            asm.append(gen_ins('return r{}'.format(return_reg)))
        else:
            asm.append(gen_ins('return None'))

    elif t == 'CallExpression':
        result_reg = request_register()

        # generate arguments
        arg_reg = request_register()
        asm.append(gen_ins('arr r{}'.format(arg_reg)))
        for arg in node['arguments']:
            handle_node(arg)
            asm.append(gen_ins('arrpush r{} r{}'.format(arg_reg, arg['register'])))
            free_register(arg['register'])

        ctx_reg = None
        if node['callee']['type'] != 'MemberExpression':
            # get function
            handle_node(node['callee'])
            func_reg = node['callee']['register']

            # use global context
            ctx_reg = request_register()
            asm.append(gen_ins('global r{}'.format(ctx_reg)))
        else:
            # we handle member expressions differently as we will use the object
            # as the context (e.g. for [].push, we need [] as the context)
            callee = node['callee']

            # use calling object context
            handle_node(callee['object'])
            ctx_reg = callee['object']['register']

            if callee['computed']:
                handle_node(callee['property'])
                prop = 'r{}'.format(callee['property']['register'])
            else:
                prop = '"{}"'.format(callee['property']['name'])

            # get function
            func_reg = request_register()
            asm.append(gen_ins('getprop r{} {} r{}'.format(ctx_reg, prop, func_reg)))

            if callee['computed']:
                free_register(callee['property']['register'])

        # call function
        asm.append(gen_ins('call r{} r{} r{} r{}'.format(func_reg, arg_reg, ctx_reg, result_reg)))

        # return result register
        node['register'] = result_reg

        # free all other registers
        free_register(func_reg)
        free_register(arg_reg)
        free_register(ctx_reg)


    elif t == 'VariableDeclaration':
        for decl in node['declarations']:

            var_name = decl['id']['name']
            var_type = node['kind']

            # first check if variable already declared in scope (appropriate to its declaration)
            scope_boundary = 'FunctionExpression' if var_type == 'var' else True
            var_info = search_scope_table(curr_scope(), var_name, scope_boundary)

            if var_info is not None:
                if var_info['type'] != 'var':
                    # let and const variables cannot be redeclared
                    print("Cannot redeclare variable declared with '{}'!".format(var_info['type']))
                    exit(1)

                # if variable already declared and init is None, don't do anything
                if decl['init'] is None:
                    return

                # otherwise treat as assignment expression
                handle_node({
                    'type': 'AssignmentExpression',
                    'operator': '=',
                    'left': decl['id'],
                    'right': decl['init']
                })
                return

            # create new variable
            var_id = get_name('var_' + var_name)
            # handle variable initialisation
            r = None
            if decl['init'] is not None:
               decl['init']['var_name'] = var_name
               decl['init']['var_id'] = var_id
               handle_node(decl['init']) # handle expr and store in register
               r = decl['init']['register']

            # book keep created var
            scopes[curr_scope()]['declared'][var_name] = {
                'id': var_id,
                'register': r,
                'type': var_type
            }
            # create var at runtime
            r = 'None' if r == None else 'r{}'.format(r)
            asm.append(gen_ins('setvar "{}" {}'.format(var_id, r)))

    elif t == 'Identifier':
        # tries to get load identifier from scope table or from global and puts
        # in register. essentially acts as expression node

        name = node['name']

        # try to find identifier in scope table
        id_info = search_scope_table(curr_scope(), name)

        if id_info is not None:
            # identifier found, retrieve from var table if not already in register

            node['id'] = id_info['id'] # store runtime variable id in node
            if id_info['register'] is not None:
                # variable currently stored in a register
                node['register'] = id_info['register']
            else:
                # variable not in register, only in runtime var table
                # so retrieve with getvar and put in register
                r = request_register()
                asm.append(gen_ins('getvar "{}" r{}'.format(id_info['id'], r)))
                node['register'] = r

        else:
            # name not in any scope, attempt loading from global
            node['global_prop'] = True 
            r = request_register()
            asm.append(gen_ins('global r{}'.format(r)))
            asm.append(gen_ins('getprop r{} "{}" r{}'.format(r, name, r)))
            node['register'] = r

    elif t == 'UpdateExpression':
        arg_reg = None
        if not node['prefix']:
            handle_node(node['argument'])
            handled_reg = node['argument']['register']
            arg_reg = request_register()
            asm.append(gen_ins('mov r{} r{}'.format(arg_reg, handled_reg)))

        op = node['operator']

        fake_assignment = {
            'type': 'AssignmentExpression',
            'operator': '+=' if op == '++' else '-=',
            'left': node['argument'],
            'right': {
                'type': 'NumericLiteral',
                'value': 1
            }
        }
        handle_node(fake_assignment)
        assigned_reg = fake_assignment['register']

        if node['prefix']:
            node['register'] = assigned_reg 
        else:
            node['register'] = arg_reg
            free_register(assigned_reg)

    elif t == 'UnaryExpression':
        handle_node(node['argument'])
        r = node['argument']['register']
        r_result = request_register()

        op = node['operator']

        if op == '-':
            asm.append(gen_ins('sub #0 r{} r{}'.format(r, r_result)))
        else:
            print('UnaryExpression operator {} not supported!'.format(op))

        node['register'] = r_result
        free_register(r)

    elif t == 'BinaryExpression':
        handle_node(node['left'])
        handle_node(node['right'])
        r_left = node['left']['register']
        r_right = node['right']['register']

        r_ans = request_register()
        node['register'] = r_ans

        op = node['operator']
        if op == '+':
            asm.append(gen_ins('add r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '-':
            asm.append(gen_ins('sub r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '*':
            asm.append(gen_ins('mul r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '/':
            asm.append(gen_ins('div r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '==':
            asm.append(gen_ins('eq r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '!=':
            asm.append(gen_ins('neq r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '>':
            asm.append(gen_ins('ge r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '>=':
            asm.append(gen_ins('geeq r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '<':
            asm.append(gen_ins('le r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '<=':
            asm.append(gen_ins('leeq r{} r{} r{}'.format(r_left, r_right, r_ans)))
        else:
            print('BinaryExpression operator {} not supported!'.format(op))

        free_register(r_left)
        free_register(r_right)

    elif t == 'EmptyStatement':
        asm.append(gen_ins('nop'))

    elif t == 'RegExpLiteral':
        r = request_register()
        pattern = node['pattern']
        flags = node['flags']
        asm.append(gen_ins('regex "{}" "{}" r{}'.format(pattern, flags, r)))
        node['register'] = r

    elif t == 'NullLiteral':
        r = request_register()
        asm.append(gen_ins('mov r{} None'.format(r)))
        node['register'] = r

    elif t == 'NumericLiteral':
        r = request_register()
        num = node['value']
        asm.append(gen_ins('mov r{} #{}'.format(r, num)))
        node['register'] = r

    elif t == 'StringLiteral':
        r = request_register()
        s = node['value']
        asm.append(gen_ins('mov r{} "{}"'.format(r, s)))
        node['register'] = r

    elif t == 'BooleanLiteral':
        r = request_register()
        boolean = node['value']
        asm.append(gen_ins('mov r{} !{}'.format(r, boolean)))
        node['register'] = r

    elif t == 'AssignmentExpression':
        # asign variables (through setvar) or object/arrays (through setprop)

        left = node['left']
        right = node['right']

        is_member = False
        if left['type'] == 'MemberExpression':
            is_member = True

        # needed for operations like +=, -=, etc
        handle_node(left)
        r_left = left['register']

        # handle value
        handle_node(right)
        r_right = right['register']

        # TODO: should this be claimed before use?
        node['register'] = r_left # assignments are expressions

        # check that variable is not const
        if 'id' in left:
            var_info = get_var_from_id(left['id'])
            if var_info is not None and var_info['type'] == 'const':
                print('Cannot reassign a const!')
                exit(1)

        op = node['operator']
        # operations will leave assignment result in r_left
        if op == '=':
            asm.append(gen_ins('mov r{} r{}'.format(r_left, r_right)))
        elif op == '+=':
            asm.append(gen_ins('add r{} r{} r{}'.format(r_left, r_right, r_left)))
        elif op == '-=':
            asm.append(gen_ins('sub r{} r{} r{}'.format(r_left, r_right, r_left)))
        else:
            print('AssignmentExpression operation {} not supported!'.format(op))

        if is_member:
            handle_node(left['object'])
            obj_reg = left['object']['register']

            if left['computed']:
                handle_node(left['property'])
                prop = 'r{}'.format(left['property']['register'])
            else:
                prop = '"{}"'.format(left['property']['name'])

            asm.append(gen_ins('setprop r{} {} r{}'.format(obj_reg, prop, r_left)))

            free_register(obj_reg)
            if left['computed']:
                free_register(left['property']['register'])
                

        elif 'id' in left:
            # update var table to new assignment
            asm.append(gen_ins('setvar "{}" r{}'.format(left['id'], r_left)))
        elif 'global_prop' in left:
            # update global property
            r = request_register()
            asm.append(gen_ins('global r{}'.format(r)))
            asm.append(gen_ins('setprop r{} "{}" r{}'.format(r, left['name'], r_left)))
            free_register(r)

        # free right side as was only evaluated to assign to left
        # we don't free left as it is the return register for this expression
        free_register(r_right)

    elif t == 'ExpressionStatement':
        # statement of just one expression, so evaluate expression and free
        # register containing it
        handle_node(node['expression'])
        free_register(node['expression']['register'])

    elif t == 'BlockStatement':
        name = t if named_block is None else named_block
        handle_block(node['body'], name)

    elif t == 'ArrayExpression':
        r = request_register()
        asm.append(gen_ins('arr r{}'.format(r)))
        for elem in node['elements']:
            handle_node(elem)
            asm.append(gen_ins('arrpush r{} r{}'.format(r, elem['register'])))
            free_register(elem['register'])

        node['register'] = r

    elif t == 'ObjectExpression':
        # we start with an empty object and load properties into one by one
        obj_reg = request_register()
        node['register'] = obj_reg
        asm.append(gen_ins('obj r{}'.format(obj_reg)))

        for prop in node['properties']:
            if prop['type'] == 'ObjectProperty':
                key = None
                key_isreg = False
                if prop['computed']:
                    handle_node(prop['key'])
                    key = prop['key']['register']
                    key_isreg = True
                else:
                    # I've only seen keys to be strings or identifiers if not
                    # computed
                    if prop['key']['type'] == 'Identifier':
                        key = prop['key']['name']
                    elif prop['key']['type'] == 'StringLiteral':
                        key = prop['key']['value']
                    else:
                        print('Object key type {} not implemented!'.format(prop['key']['type']))
                handle_node(prop['value'])
                val_reg = prop['value']['register']

                k = 'r{}'.format(key) if key_isreg else '"{}"'.format(key)
                asm.append(gen_ins('setprop r{} {} r{}'.format(obj_reg, k, val_reg)))
                free_register(val_reg)

                # property evaulated and moved into object, no need to hang on
                # to register holding
                if key_isreg:
                    free_register(key)
            else:
                print('{} not implemented!'.format(prop['type']))

    elif t == 'MemberExpression':
        handle_node(node['object'])
        obj_reg = node['object']['register']

        if node['computed']:
            handle_node(node['property'])
            prop = 'r{}'.format(node['property']['register'])
        else:
            prop = '"{}"'.format(node['property']['name'])

        # store prop in obj_reg
        asm.append(gen_ins('getprop r{} {} r{}'.format(obj_reg, prop, obj_reg)))

        # we will claim the obj reg as register for this expression
        claim_register(obj_reg)
        node['register'] = obj_reg

        if node['computed']:
            free_register(node['property']['register'])

    elif t == 'ForStatement':
        '''
        <init>
        :start_for
        <test>
        jnt :end_for
        <body>
        <update>
        jmp :start_for
        :end_for
        '''

        start_for = get_name('start_for')
        end_for = get_name('end_for')

        # run initialise block
        handle_node(node['init'])
        asm.append(gen_ins(':' +start_for))
        # run test
        handle_node(node['test'])
        t_result = node['test']['register']
        # end loop if needed
        asm.append(gen_ins('jnt r{} :{}'.format(t_result, end_for)))
        # loop body
        handle_node(node['body'], named_block=t)
        # update
        handle_node(node['update'])
        # restart loop
        asm.append(gen_ins('jmp :{}'.format(start_for)))
        asm.append(gen_ins(':{}'.format(end_for)))


    elif t == 'WhileStatement':
        '''
        :start_while
        <test>
        jnt :end_while
        <body>
        jmp :start_while
        :end_while
        '''

        start_while = get_name('start_while')
        end_while = get_name('end_while')
        asm.append(gen_ins(':'+start_while))
        # handle test
        handle_node(node['test'])
        t_result = node['test']['register']
        # end loop if needed
        asm.append(gen_ins('jnt r{} :{}'.format(t_result, end_while)))
        # loop body
        handle_node(node['body'], named_block=t)
        # restart loop
        asm.append(gen_ins('jmp :{}'.format(start_while)))
        asm.append(gen_ins(':'+end_while))


    elif t == 'IfStatement':
        '''
        <test>
        jnt :after_consequent
        <consequent>
        jmp :end_if
        :after_consequent
        <alternate>
        :end_if
        '''

        after_consequent = get_name('after_consequent')
        end_if = get_name('end_if')

        # handle test (result will be in register)
        handle_node(node['test'])
        t_result = node['test']['register']

        # jump if needed to after consequent
        asm.append(gen_ins('jnt r{} :{}'.format(t_result, after_consequent)))

        handle_node(node['consequent'], named_block=t) # is always a block statement
        # jump to end of if statement after finishing consequent
        asm.append(gen_ins('jmp :{}'.format(end_if)))
    
        asm.append(gen_ins(':'+after_consequent))
        if node['alternate'] is not None:
            handle_node(node['alternate'], named_block=t)

        asm.append(gen_ins(':'+end_if))
        
    else:
        print('{} node not implemented!'.format(t))
        print(json.dumps(node, indent=2))
        exit()

            
def handle_block(block, base_node, root=False, preset_vars=None):
    '''
    will create new scope and execute code in scope (if not root, root scope manually created)

    TODO: should hoist vars and funcs
    '''

    # create scope:

    scope_id = get_name('scope')
    # define scope as child of current scope (root doesn't have a parent)
    if not root:
        scopes[curr_scope()]['children'].append(scope_id)
    # add scope to scopes datastore (with preset vars if needed)
    scopes[scope_id] = {
        'parent': curr_scope(),
        'children': [],
        'declared': {} if preset_vars is None else preset_vars,
        'created_from': base_node
    }
    # update current scope to newly created one
    scope_stack.append(scope_id)

    # generate asm inside scope

    # this round will declare functions
    for node in block:
        if node['type'] == 'FunctionDeclaration':
            handle_node(node, declare_func_mode=True)

    # this round will generate everything (and function bodies)
    for node in block:
        handle_node(node)

    # deconstruct scope:
    #return

    # no need to deconstruct if root; program ended
    if root: return
    # remove as current scope
    scope_stack.pop()
    # delete from parent scope's children list
    parent_children = scopes[curr_scope()]['children']
    del parent_children[parent_children.index(scope_id)]
    # delete all declared variables and free registers holding them
    declared = scopes[scope_id]['declared']
    for symbol in declared:
        symbol = declared[symbol]
        asm.append(gen_ins('delvar "{}"'.format(symbol['id'])))
        free_register(symbol['register'], force=True)
    # delete from scope db
    del scopes[scope_id]

def scope_for_loops(node):
    '''
    wrap for loops around a block
    '''

    # apply to every item of list and return list
    if type(node) is list:
        new = []
        for x in node:
            new.append(scope_for_loops(x))
        return new
    
    # if not object, return as is
    if type(node) is not dict:
        return node

    # base case: found for statement
    if 'type' in node and node['type'] == 'ForStatement':
        return {
            'type': 'BlockStatement',
            'body': [
                node
            ]
        }

    # apply to every key and return node
    for key in node:
        node[key] = scope_for_loops(node[key])

    return node

def preprocess(a):
    global ast
    ast = scope_for_loops(ast)

def compile(ast):
    handle_block(ast['body'], ast['type'], root=True)


preprocess(ast)

#print(json.dumps(ast, indent=2))

compile(ast)

# detailed instructions
#print(json.dumps(asm, indent=2))

# short form instructions
if True or 'silent' not in sys.argv:
    for ins in asm: print(ins['string_repr'])

# scope info
#print(json.dumps(scopes, indent=2), scope_stack)

instructions = {
    'instructions': asm
}

if DEBUG:
    json.dump(instructions, out_file, indent=2)
else:
    json.dump(instructions, out_file)

out_file.close()
