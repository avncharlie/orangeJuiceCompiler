import sys
import ast as py_ast 
import json
import pprint
import secrets
import shlex

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

DEBUG = False 
DEBUG = True; DEBUGDEBUG = False

# if registers[x] == false or doesn't exist, register unclaimed
registers = [False, False, False]

scopes = {}

scope_stack = [None]
curr_scope = lambda : scope_stack[len(scope_stack)-1]

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

    if not DEBUG:
        name = secrets.token_hex(16)
        while name in used_names:
            name = secrets.token_hex(16)
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
        else:
            if part[0] == 'r':
                f_part["type"] = "register"
            elif part[0] == '#':
                f_part["type"] = "number"
            f_part["value"] = int(part[1:])
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

def remove_var_reg(r):
    '''
    sets variables who have this register to have no register
    '''
    for scope in scopes:
        for var_name in scopes[scope]['declared']:
            if scopes[scope]['declared'][var_name]['register'] == r:
                scopes[scope]['declared'][var_name]['register'] = None

def free_register(r):
    '''
    unallocate specific register
    '''
    if DEBUGDEBUG: print('...free r{}'.format(r))
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

def handle_node(node):
    '''
    if given expression, assign reg to icurrent_scope, t
    will be attached in 'register' attribute
    will also return register
    '''

    t = node["type"]

    if t == 'VariableDeclaration':
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
                #id_info['register'] = r # update id_info with register

        else:
            # name not in any scope, attempt loading from global
            node['global_prop'] = True 
            r = request_register()
            asm.append(gen_ins('global r{}'.format(r)))
            asm.append(gen_ins('getprop r{} "{}" r{}'.format(r, name, r)))
            node['register'] = r

    elif t == 'BinaryExpression':
        handle_node(node['left'])
        handle_node(node['right'])
        r_left = node['left']['register']
        r_right = node['right']['register']

        op = node['operator']
        if op == '+':
            asm.append(gen_ins('add r{} r{}'.format(r_left, r_right)))
        else:
            print('BinaryExpression operator {} not supported!'.format(op))

        # free right reg and hijack right reg for whole expression register
        # TODO: this isn't great if either expression is housing variable
        free_register(r_right)
        claim_register(r_left)
        node['register'] = r_left

    elif t == 'NumericLiteral':
        r = request_register()
        num = node['value']
        asm.append(gen_ins('mov r{} #{}'.format(r, num)))
        node['register'] = r

    elif t == 'StringLiteral':
        r = request_register()
        num = node['value']
        asm.append(gen_ins('mov r{} "{}"'.format(r, num)))
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

        '''
        if left['type'] == 'MemberExpression':
            is_member = True
            r_left = request_register()
        else:
            # needed for operations like +=, -=, etc
            handle_node(left)
            r_left = left['register']
        '''

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
            asm.append(gen_ins('add r{} r{}'.format(r_left, r_right)))
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
        handle_block(node['body'], t)

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
    else:
        print('{} node not implemented!'.format(t))

            
def handle_block(block, base_node, root=False):
    '''
    will create new scope and execute code in scope (if not root, root scope manually created)

    TODO: should hoist vars and funcs
    '''

    # create scope:

    scope_id = get_name('scope')
    # define scope as child of current scope (root doesn't have a parent)
    if not root:
        scopes[curr_scope()]['children'].append(scope_id)
    # add scope to scopes datastore
    scopes[scope_id] = {
        'parent': curr_scope(),
        'children': [],
        'declared': {},
        'created_from': base_node
    }
    # update current scope to newly created one
    scope_stack.append(scope_id)

    # generate asm inside scope
    for node in block:
        handle_node(node)

    # deconstruct scope:

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
        free_register(symbol['register'])
    # delete from scope db
    del scopes[scope_id]

def compile(ast):
    handle_block(ast['body'], ast['type'], root=True)

compile(ast)

# detailed instructions
#print(json.dumps(asm, indent=2))

# short form instructions
for ins in asm: print(ins['string_repr'])

# scope info
#print(json.dumps(scopes, indent=2), scope_stack)

instructions = {
    'instructions': asm
}

if DEBUG:
    #json.dump(instructions, out_file, indent=2)
    json.dump(instructions, out_file)
else:
    json.dump(instructions, out_file)

out_file.close()
