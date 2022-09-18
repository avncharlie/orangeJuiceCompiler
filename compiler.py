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
Unsupported:
    - '||='. '&&=' and '??=' assignments
    - void, delete and throw statements
    - try / catch / throw
    - closures (functions as arguments, return values, callbacks and anonymous
      functions supported)
    - arrow functions
    - classes / super ('this' and 'new' statement supported)
    - spread operator
    - sequence expressions
    - do expression

todo: 
    - error messages?
    - var hoisting?
    - try / catch
    - definetely could refactor code to avoid duplicating MemberExpression code
      everywhere (have a version that you can select what you want held or
      freed)
      
possible bugs:
    - expressions of form a[b++]++ don't evaluate correctly
    - remove_all_var_registers called for while loops but not with for loops 
      it probably should?
    - definetely a bunch of register leaking happening
    - undefined / null not defined well for all instructions in VM
      should have a standard function to retrieve value for argument
    - protection for re-evaluating member expression properties probably doesn't
      work in all cases (band aid solution)
    - var scoping incorrect maybe?
      vars should access the closest var but looks like they are accessing the
      most global var at the moment?
      need to investigate more
'''

DEBUG = False; DEBUGDEBUG = False
DEBUG = True; DEBUGDEBUG = False
#DEBUG = True; DEBUGDEBUG = True

# if registers[x] == false or doesn't exist, register unclaimed
reg_stack = []
registers = [False, False, False]

vars_changed = []
scopes_backup = []
scopes = {}

scope_stack_stack = []
scope_stack = [None]
curr_scope = lambda : scope_stack[len(scope_stack)-1]
prev_scope = lambda : scope_stack[len(scope_stack)-2]

break_stack = []

branch_counter = 0
asm = []

loc_info = None

varset_table = []

used_names = ['function_map'] # used in vm
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

def _calculate_top_store(store_below=False, scopes_below=0):
    store_stoppers = [
        'Program',
        'ForStatement',
        'WhileStatement',
        'DoWhileStatement',
        'SwitchStatement',
        'FunctionExpression',
        'FunctionDeclaration'
    ]

    # start with function_map var accounted for
    looking_through = scope_stack[1:len(scope_stack)-scopes_below][::-1]
    if store_below:
        new = []
        capturing = False
        for scope in looking_through:
            if capturing:
                new.append(scope)
            created_from = scopes[scope]['created_from']
            if created_from in store_stoppers:
                capturing = True
        looking_through = new

    t = 1 
    for scope in looking_through:
        created_from = scopes[scope]['created_from']
        t += len(scopes[scope]['declared']) 
    
        if created_from in store_stoppers:
            break
    return t

def _current_top_store_declared(instr):
    op = instr[0]

    #if op in ['delvar']: print(json.dumps(scopes, indent=2))

    t = _calculate_top_store()

    if op == 'setvar':
        var_name = instr[1][3:-3]
        if var_name in varset_table:
            # variable already declared
            return t
        varset_table.append(var_name)

        # This setvar is creating this variable and increasing the vars in the 
        # top store, but only after this instruction runs
        # So at the time the VM sees this instruction, the variable hasn't been
        # created yet (but it is bookkept in the compiler data store)
        # So subtract 1 from t to fix
        t -= 1
    return t

@_debug_print_ins
def gen_ins(ins, forced_top_declared=None):
    '''
    function to generate instructions from a string representation

    op r5 #5 """5""" None !True = op <register 5> <number 5> <string 5> str null true

    adds string representation as 'string_repr' attribute
    '''
    if ins[0] == ':':
        print(ins)
        return {
                "type": "label",
                "id": ins[1:],
                "string_repr": ins
        }

    arguments = []

    # shlex with the posix flag splits 'foo """bar"""'  as ['foo', '""', '"bar"', '""']
    # a bit of ugly code to make it split instead like ['foo', '"""bar"""']
    temp_split = shlex.split(ins, posix=False)
    ins_split = []
    seen_q = 0
    for i, part in enumerate(temp_split):
        if part[0] == '"':
            seen_q += 1
            if seen_q == 2 and i != len(temp_split) and temp_split[i+1][0] == '"':
                ins_split.pop()
                part = '""' + part + '""'
            elif seen_q == 3:
                seen_q = 0
                continue
        ins_split.append(part)

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
        elif part == "Undefined":
            f_part["type"] = "Undefined"
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


    # used for variable dependent op code obfuscation
    curr_top_declared = forced_top_declared
    if curr_top_declared is None:
        curr_top_declared = _current_top_store_declared(ins_split)

    print(curr_top_declared, ins) #DEBUG

    approx_loc = loc_info['start']['line'] if loc_info is not None else 0

    return {
            "type": "operation",
            "op": ins_split[0],
            "args": arguments,
            "string_repr": ins,
            "approx_loc": approx_loc,
            "top_scope_declared": curr_top_declared
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

def nullify_var(var_id):
    '''
    set variable register to null
    TODO: use this in FunctionDeclaration node 
    '''
    for scope in scopes:
        for var_name in scopes[scope]['declared']:
            if scopes[scope]['declared'][var_name]['id'] == var_id:
                scopes[scope]['declared'][var_name]['register'] = None

def search_scope_table(scope, name, scope_boundary=None):
    '''
    find variable referenced by identifier name

    if scope_boundary is True: only look at current scope
    otherwise search up until scope_boundary scope created found
    will return (object in 'declared' list for variable or None, scope found in)
    '''

    # try to find variable name in scope
    # stop at global scope or when scope boundary reached
    while scope is not None and scopes[scope]['created_from'] != scope_boundary:

        if name in scopes[scope]['declared']:
            # name found!
            return (scopes[scope]['declared'][name], scope)
        elif scope_boundary is True:
            # not in current scope, exit
            return (None, None)
        else:
            # not in current scope, lets look up
           scope = scopes[scope]['parent']

    # name not found
    return (None, None)

def handle_node(node, named_block=None, declare_func_mode=False, assigning_ids=False):
    '''
    if given expression, assign reg to current_scope, t
    will be attached in 'register' attribute
    will also return register
    document! especially keyword arguments
    '''

    global asm
    global registers, reg_stack
    global scope_stack, scope_stack_stack
    global scopes, scopes_backup
    global loc_info

    #print(node['type'])
    if 'loc' in node:
        loc_info = node['loc']
        #print(node['loc'])


    t = node["type"]

    if t in ['FunctionDeclaration', 'FunctionExpression']:
        '''
        TODO: document declare_func_mode
        '''

        # prepare function in compiler and VM:

        # 'declare' function first if a function expression
        # if expression, declare and handle at same time
        if declare_func_mode or t == 'FunctionExpression':
            # step 1: get function label 
            func_name = None
            func_label = get_name('anon')
            func_end_label = get_name('anon_end')
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
                asm.append(gen_ins('arrpush r{} """{}"""'.format(arg_list_reg, arg_id)))
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
                asm.append(gen_ins('setvar """{}""" r{}'.format(func_id, func_reg)))

            # store names for handling run
            node['func_name'] = func_name
            node['func_label'] = func_label
            node['func_end_label'] = func_end_label
            node['func_preset_vars'] = func_preset_vars

            # TODO: this messy
            if t == 'FunctionDeclaration': return

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
        vars_changed.append([])

        # step 6: handle body of function with arguments as preset vars
        asm.append(gen_ins(':' + func_label)) # start label
        handle_block(node['body']['body'], t, preset_vars=func_preset_vars)
        asm.append(gen_ins('return Undefined')) # catch all return if there is no return in func body
        asm.append(gen_ins(':' + func_end_label))

        # cleanup:

        # step 7: restore all backed up registers and scope information
        registers = reg_stack.pop()
        scope_stack = scope_stack_stack.pop()
        scopes = scopes_backup.pop()

        for var in vars_changed.pop():
            nullify_var(var)

    elif t == 'ReturnStatement':
        if node['argument'] is not None:
            handle_node(node['argument'])
            return_reg = node['argument']['register']
            asm.append(gen_ins('return r{}'.format(return_reg)))
        else:
            asm.append(gen_ins('return Undefined'))

    elif t in ['CallExpression', 'NewExpression']:
        # BUG: whatever your constructor function returns will be returned as
        # the result of the new statement (even if it is not an object)
        # if it doesn't return anything thats ok

        result_reg = request_register()

        # generate arguments
        arg_reg = request_register()
        asm.append(gen_ins('arr r{}'.format(arg_reg)))
        for arg in node['arguments']:
            handle_node(arg)
            asm.append(gen_ins('arrpush r{} r{}'.format(arg_reg, arg['register'])))
            free_register(arg['register'])

        ctx_reg = None
        r_new_obj = None
        if node['callee']['type'] != 'MemberExpression':
            # get function
            handle_node(node['callee'])
            func_reg = node['callee']['register']

            if t != 'NewExpression':
                # use global context by default
                ctx_reg = request_register()
                asm.append(gen_ins('global r{}'.format(ctx_reg)))

        else:
            # we handle member expressions differently as we will use the object
            # as the context (e.g. for [].push, we need [] as the context)
            callee = node['callee']

            # use calling object context (unless is NewExpression)
            handle_node(callee['object'])
            ctx_reg = callee['object']['register']

            if callee['computed']:
                handle_node(callee['property'])
                prop = 'r{}'.format(callee['property']['register'])
            else:
                prop = '"""{}"""'.format(callee['property']['name'])

            # get function
            func_reg = request_register()
            asm.append(gen_ins('getprop r{} {} r{}'.format(ctx_reg, prop, func_reg)))

            if callee['computed']:
                free_register(callee['property']['register'])

            if t == 'NewExpression':
                free_register(ctx_reg)

        if t == 'NewExpression':
            # use empty object as context for constructors
            r_new_obj = request_register()
            asm.append(gen_ins('obj r{}'.format(r_new_obj)))
            ctx_reg = r_new_obj

            # set __proto__ property to function.prototype
            proto_prop = request_register()
            asm.append(gen_ins('getprop r{} "prototype" r{}'.format(func_reg, proto_prop)))
            asm.append(gen_ins('setprop r{} "__proto__" r{}'.format(ctx_reg, proto_prop)))
            free_register(proto_prop)


        # call function
        asm.append(gen_ins('call r{} r{} r{} r{}'.format(func_reg, arg_reg, ctx_reg, result_reg)))

        if t == 'NewExpression':
            '''
            <result_is_object>
            jt <result_is_object> :after
            mov result_reg obj_reg
            :after
            '''

            after_test = get_name('after_test')
            r_test = request_register()

            asm.append(gen_ins('global r{}'.format(r_test)))
            asm.append(gen_ins('getprop r{} "Object" r{}'.format(r_test, r_test)))
            asm.append(gen_ins('check_instance r{} r{} r{}'.format(result_reg, r_test, r_test)))
            asm.append(gen_ins('jt r{} :{}'.format(r_test, after_test)))
            asm.append(gen_ins('mov r{} r{}'.format(result_reg, r_new_obj)))
            asm.append(gen_ins(':' + after_test))
            free_register(r_new_obj)

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
            var_info, _ = search_scope_table(curr_scope(), var_name, scope_boundary)

            if var_info is not None:
                if var_info['type'] != 'var':
                    # let and const variables cannot be redeclared
                    print("Cannot redeclare variable declared with '{}'!".format(var_info['type']))
                    exit(1)

                # if variable already declared and init is None, don't do anything
                if decl['init'] is None:
                    continue

                # otherwise treat as assignment expression
                handle_node({
                    'type': 'AssignmentExpression',
                    'operator': '=',
                    'left': decl['id'],
                    'right': decl['init'],
                    'loc': decl['loc']
                })
                continue

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
            r = 'Undefined' if r == None else 'r{}'.format(r)
            asm.append(gen_ins('setvar """{}""" {}'.format(var_id, r)))

    elif t == 'Identifier':
        # tries to get load identifier from scope table or from global and puts
        # in register. essentially acts as expression node
        # also stores scope identifier was loaded from 

        name = node['name']

        # try to find identifier in scope table
        id_info, scope = search_scope_table(curr_scope(), name)

        if id_info is not None:
            # identifier found, retrieve from var table if not already in register
            node['scope'] = scope

            # record assignments to variables
            if vars_changed != []:
                top_changed = vars_changed[len(vars_changed) - 1]
                if id_info['id'] not in top_changed:
                    top_changed.append(id_info['id'])

            node['id'] = id_info['id'] # store runtime variable id in node
            if id_info['register'] is not None:
                # variable currently stored in a register
                node['register'] = id_info['register']
            else:
                # variable not in register, only in runtime var table
                # so retrieve with getvar and put in register
                r = request_register()
                asm.append(gen_ins('getvar """{}""" r{}'.format(id_info['id'], r)))
                node['register'] = r

        else:
            # name not in any scope, attempt loading from global
            node['global_prop'] = True 
            r = request_register()
            asm.append(gen_ins('global r{}'.format(r)))
            asm.append(gen_ins('getprop r{} """{}""" r{}'.format(r, name, r)))
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
            },
            'loc': node['loc']
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
            asm.append(gen_ins('unary_neg r{} r{}'.format(r, r_result)))
        elif op == '+':
            asm.append(gen_ins('unary_plus r{} r{}'.format(r, r_result)))
        elif op == '!':
            asm.append(gen_ins('unary_not r{} r{}'.format(r, r_result)))
        elif op == '~':
            asm.append(gen_ins('unary_bit_not r{} r{}'.format(r, r_result)))
        elif op == 'typeof':
            asm.append(gen_ins('unary_typeof r{} r{}'.format(r, r_result)))
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
        elif op == '%':
            asm.append(gen_ins('mod r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '**':
            asm.append(gen_ins('pow r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '|':
            asm.append(gen_ins('bit_or r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '&':
            asm.append(gen_ins('bit_and r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '^':
            asm.append(gen_ins('xor r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '==':
            asm.append(gen_ins('eq r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '!=':
            asm.append(gen_ins('neq r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '===':
            asm.append(gen_ins('eqt r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '!==':
            asm.append(gen_ins('neqt r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '<<':
            asm.append(gen_ins('shl r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '>>':
            asm.append(gen_ins('shr r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '>>>':
            asm.append(gen_ins('ushr r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '>':
            asm.append(gen_ins('ge r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '>=':
            asm.append(gen_ins('geeq r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '<':
            asm.append(gen_ins('le r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == '<=':
            asm.append(gen_ins('leeq r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == 'in':
            asm.append(gen_ins('inside r{} r{} r{}'.format(r_left, r_right, r_ans)))
        elif op == 'instanceof':
            asm.append(gen_ins('check_instance r{} r{} r{}'.format(r_left, r_right, r_ans)))
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
        asm.append(gen_ins('regex """{}""" """{}""" r{}'.format(pattern, flags, r)))
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
        asm.append(gen_ins('mov r{} """{}"""'.format(r, s)))
        node['register'] = r

    elif t == 'BooleanLiteral':
        r = request_register()
        boolean = node['value']
        asm.append(gen_ins('mov r{} !{}'.format(r, boolean)))
        node['register'] = r

    elif t == 'AssignmentExpression':
        # asign variables (through setvar) or object/arrays (through setprop)
        # or global properties (through setprop)

        left = node['left']
        right = node['right']

        r_left = None

        obj_reg = None
        prop_reg = None
        prop = None
        if left['type'] == 'MemberExpression':
            # to avoid evaluating obj[foo] twice in getting and setting member
            # expression, we must deal load them without handling them with
            # MemberExpression handler. this is as that handler frees the
            # register that the stores the property whereas we will keep it
            # to set the member expression
            handle_node(left['object'], assigning_ids=True)
            obj_reg = left['object']['register']
            if left['computed']:
                handle_node(left['property'])
                prop_reg = left['property']['register']
                prop = 'r{}'.format(prop_reg)
            else:
                prop = '"""{}"""'.format(left['property']['name'])
            # store prop in r_left
            r_left = request_register()
            asm.append(gen_ins('getprop r{} {} r{}'.format(obj_reg, prop, r_left)))
        else:
            # needed for operations like +=, -=, etc
            handle_node(left, assigning_ids=True)
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
        elif op == '*=':
            asm.append(gen_ins('mul r{} r{} r{}'.format(r_left, r_right, r_left)))
        elif op == '/=':
            asm.append(gen_ins('div r{} r{} r{}'.format(r_left, r_right, r_left)))
        elif op == '%=':
            asm.append(gen_ins('mod r{} r{} r{}'.format(r_left, r_right, r_left)))
        elif op == '**=':
            asm.append(gen_ins('pow r{} r{} r{}'.format(r_left, r_right, r_left)))
        elif op == '<<=':
            asm.append(gen_ins('shl r{} r{} r{}'.format(r_left, r_right, r_left)))
        elif op == '>>=':
            asm.append(gen_ins('shr r{} r{} r{}'.format(r_left, r_right, r_left)))
        elif op == '>>>=':
            asm.append(gen_ins('ushr r{} r{} r{}'.format(r_left, r_right, r_left)))
        elif op == '|=':
            asm.append(gen_ins('bit_or r{} r{} r{}'.format(r_left, r_right, r_left)))
        elif op == '^=':
            asm.append(gen_ins('xor r{} r{} r{}'.format(r_left, r_right, r_left)))
        elif op == '&=':
            asm.append(gen_ins('bit_and r{} r{} r{}'.format(r_left, r_right, r_left)))
        else:
            print('AssignmentExpression operation {} not supported!'.format(op))

        if left['type'] == 'MemberExpression':
            # call setprop with saved registers
            asm.append(gen_ins('setprop r{} {} r{}'.format(obj_reg, prop, r_left)))
            if prop_reg is not None:
                # free register storing property if computed
                free_register(prop_reg)
            free_register(obj_reg)

        elif 'id' in left:
            # update var table to new assignment
            asm.append(gen_ins('setvar """{}""" r{}'.format(left['id'], r_left)))
        elif 'global_prop' in left:
            # update global property
            r = request_register()
            asm.append(gen_ins('global r{}'.format(r)))
            asm.append(gen_ins('setprop r{} """{}""" r{}'.format(r, left['name'], r_left)))
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
        should_pop = None if 'pop_after_compile' not in node else node['pop_after_compile']
        handle_block(node['body'], name, pop_after_compile=should_pop)

    elif t == 'ArrayExpression':
        r = request_register()
        asm.append(gen_ins('arr r{}'.format(r)))
        for elem in node['elements']:
            handle_node(elem)
            asm.append(gen_ins('arrpush r{} r{}'.format(r, elem['register'])))
            free_register(elem['register'])

        node['register'] = r

    elif t == 'ThisExpression':
        this_reg = request_register()
        node['register'] = this_reg
        asm.append(gen_ins('whatsthis r{}'.format(this_reg)))

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

                k = 'r{}'.format(key) if key_isreg else '"""{}"""'.format(key)
                asm.append(gen_ins('setprop r{} {} r{}'.format(obj_reg, k, val_reg)))
                free_register(val_reg)

                # property evaulated and moved into object, no need to hang on
                # to register holding
                if key_isreg:
                    free_register(key)

            elif prop['type'] == 'ObjectMethod':
                # handle as property mapping to anonymous function 
                fake_function = {
                    'type': 'FunctionExpression',
                    'id': None,
                    'params': prop['params'],
                    'body': prop['body'],
                    'loc': prop['loc']
                }
                handle_node(fake_function)
                method_reg = fake_function['register']
                k = prop['key']['name']
                asm.append(gen_ins('setprop r{} """{}""" r{}'.format(obj_reg, k, method_reg)))

            else:
                print('{} not implemented!'.format(prop['type']))

    elif t == 'MemberExpression':
        handle_node(node['object'], assigning_ids=assigning_ids)
        obj_reg = node['object']['register']

        if node['computed']:
            handle_node(node['property'])
            prop = 'r{}'.format(node['property']['register'])
        else:
            prop = '"""{}"""'.format(node['property']['name'])

        # store prop in obj_reg
        asm.append(gen_ins('getprop r{} {} r{}'.format(obj_reg, prop, obj_reg)))

        # we will claim the obj reg as register for this expression
        claim_register(obj_reg)
        node['register'] = obj_reg

        if node['computed']:
            free_register(node['property']['register'])

    elif t == 'BreakStatement':
        asm.append(gen_ins('pop_store'))

        # as store is popped we need to force the top declared the top declared
        # of the store below
        below_scope_declared = _calculate_top_store(store_below=True)
        asm.append(gen_ins('jmp :{}'.format(break_stack[len(break_stack)-1]['loop_end']),
            forced_top_declared=below_scope_declared))

    elif t == 'ContinueStatement':
        asm.append(gen_ins('pop_store'))

        # same as break statement
        below_scope_declared = _calculate_top_store(store_below=True)
        asm.append(gen_ins('jmp :{}'.format(break_stack[len(break_stack)-1]['continue_loc']),
            forced_top_declared=below_scope_declared))

    elif t == 'ForStatement':
        '''
        <init>

        :start_for
        <test>
        jnt :end_for

        <create store>
        <body>
        <pop store>

        :end_body

        <update>
        jmp :start_for

        :end_for
        '''

        start_for = get_name('start_for')
        end_for = get_name('end_for')
        end_body = get_name('end_body')

        # add pop store to end of body (create block if body not block)
        if 'body' not in node['body']:
            node['body'] = {
                'type': 'BlockStatement',
                'body': [ copy.deepcopy(node['body']) ],
            }

        node['body']['pop_after_compile'] = True

        # bookkeep loop bounds for break and continue statements
        break_stack.append({
            'continue_loc': end_body,
            'loop_end': end_for,
        })

        # run initialise block if one exists
        if node['init'] is not None:
            handle_node(node['init'])
        asm.append(gen_ins(':' +start_for))

        # backup scope
        scope_stack_stack.append(scope_stack[:])
        scopes_backup.append(copy.deepcopy(scopes))
        remove_all_var_registers()
        vars_changed.append([])

        # run test if one exists
        if node['test'] is not None:
            handle_node(node['test'])
            t_result = node['test']['register']
            # end loop if needed
            asm.append(gen_ins('jnt r{} :{}'.format(t_result, end_for)))

        # loop body (pop done through pop_after_compile flag)
        asm.append(gen_ins('push_store'))
        handle_node(node['body'], named_block=t)

        asm.append(gen_ins(':' + end_body))

        # update if update exists
        if node['update'] is not None:
            handle_node(node['update'])
        # restart loop
        asm.append(gen_ins('jmp :{}'.format(start_for)))
        asm.append(gen_ins(':{}'.format(end_for)))

        # no longer in loop, remove bookkeeping info
        break_stack.pop()

        # restore backed up scope
        scope_stack = scope_stack_stack.pop()
        scopes = scopes_backup.pop()

        # remove reference to registers holding variables if changed inside loop
        for var in vars_changed.pop():
            nullify_var(var)


    elif t in ['WhileStatement', 'DoWhileStatement']:
        '''
        while loop:

        :start_while
        <test>
        jnt :end_while

        <create store>
        <body>
        <pop store>

        jmp :start_while
        :end_while

        move body before <test> for do while
        '''

        # TODO: any problems, 
        #   backup up registers too

        start_while = get_name('start_while')
        end_while = get_name('end_while')

        # first backup scope (will restore after loop is handled)
        scope_stack_stack.append(scope_stack[:])
        scopes_backup.append(copy.deepcopy(scopes))
        remove_all_var_registers()
        vars_changed.append([])

        # add pop store to end of body (create block if body not block)
        if 'body' not in node['body']:
            node['body'] = {
                'type': 'BlockStatement',
                'body': [ copy.deepcopy(node['body']) ]
            }

        node['body']['pop_after_compile'] = True

        # bookkeep loop bounds for break and continue statements
        break_stack.append({
            'continue_loc': start_while,
            'loop_end': end_while,
        })

        # start loop
        asm.append(gen_ins(':'+start_while))

        if t == 'DoWhileStatement':
            # loop body (pop was inserted earlier)
            asm.append(gen_ins('push_store'))
            handle_node(node['body'], named_block=t)

        # handle test
        handle_node(node['test'])
        t_result = node['test']['register']
        # end loop if needed
        asm.append(gen_ins('jnt r{} :{}'.format(t_result, end_while)))

        if t == 'WhileStatement':
            # loop body (pop was inserted earlier)
            asm.append(gen_ins('push_store'))
            handle_node(node['body'], named_block=t)

        # restart loop
        asm.append(gen_ins('jmp :{}'.format(start_while)))
        asm.append(gen_ins(':'+end_while))

        # no longer in loop, remove bookkeeping info
        break_stack.pop()

        # restore backed up scope
        scope_stack = scope_stack_stack.pop()
        scopes = scopes_backup.pop()

        # remove reference to registers holding variables if changed inside loop
        for var in vars_changed.pop():
            nullify_var(var)

    elif t == 'LogicalExpression':
        '''
        &&
        jnt r_left :short_circuit
        mov r_ans r_right
        jmp :end
        :short_circuit
        mov r_ans r_left
        :end

        ||
        jt r_left :short_circuit
        mov r_ans r_right
        jmp :end
        :short_circuit
        mov r_ans r_left
        :end
        '''

        end = get_name('logic_end')
        short_circuit = get_name('short_circuit')

        r_ans = request_register()
        handle_node(node['left'])
        r_left = node['left']['register']
        handle_node(node['right'])
        r_right = node['right']['register']

        op = node['operator']
        asm.append(gen_ins('{} r{} :{}'.format('jt' if op == '||' else 'jnt', r_left, short_circuit)))
        asm.append(gen_ins('mov r{} r{}'.format(r_ans, r_right)))
        asm.append(gen_ins('jmp :{}'.format(end)))
        asm.append(gen_ins(':{}'.format(short_circuit)))
        asm.append(gen_ins('mov r{} r{}'.format(r_ans, r_left)))
        asm.append(gen_ins(':{}'.format(end)))
 
        free_register(r_left)
        free_register(r_right)

        node['register'] = r_ans

    elif t == 'ConditionalExpression':
        '''
        <test>
        jnt :alternate
        <handle_consequent>
        mov rAns rConsequent
        jmp :end
        :alternate
        <handle_alternate>
        mov rAns rAlternate
        :end
        '''

        alternate = get_name('alternate')
        end_conditional = get_name('end_conditional')

        r_result = request_register()
        node['register'] = r_result

        handle_node(node['test'])
        r_test = node['test']['register']
        asm.append(gen_ins('jnt r{} :{}'.format(r_test, alternate)))

        handle_node(node['consequent'])
        r_cons = node['consequent']['register']
        asm.append(gen_ins('mov r{} r{}'.format(r_result, r_cons)))
        asm.append(gen_ins('jmp :{}'.format(end_conditional)))

        asm.append(gen_ins(':{}'.format(alternate)))
        handle_node(node['alternate'])
        r_alt = node['alternate']['register']
        asm.append(gen_ins('mov r{} r{}'.format(r_result, r_alt)))

        asm.append(gen_ins(':{}'.format(end_conditional)))

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

    elif t == 'SwitchStatement':
        '''
        <evaluate discriminant>
        <decide what case to take and jump there>
        :case1
        <case1 code>
        ...
        '''

        end_switch = get_name('end_switch')

        # backup scope (we do this as a break can come from anywhere destroying
        # whatever scope is built up)
        scope_stack_stack.append(scope_stack[:])
        scopes_backup.append(copy.deepcopy(scopes))

        # when break occurs, jump to end of switch
        break_stack.append({
            'loop_end': end_switch,
        })

        asm.append(gen_ins('push_store'))

        # generate combined block of all code in switch statement with labels at
        # where different cases start
        default_name = None
        combined_block = []
        for i, c in enumerate(node['cases']):
            name = None
            if c['test'] is None:
                name = get_name('case_default')
                default_name = name
            else:
                name = get_name('case_{}'.format(i))

            c['label'] = name

            # add labels between code blocks to jump to
            combined_block.append({
                'type': 'InstructionInsert',
                'instructions': [
                    gen_ins(':' + name)
                ]
            })
            combined_block += c['consequent']

        combined_block.append({
            'type': 'InstructionInsert',
            'instructions': [
                gen_ins(':' + end_switch)
            ]
        })

        handle_node(node['discriminant'])
        d_reg = node['discriminant']['register']

        # generate code deciding what case to take
        r_result = request_register()
        for c in node['cases']:
            # test will only be None if default case 
            if c['test'] is not None:
                # test case, if equal jump to label
                handle_node(c['test'])
                r_test = c['test']['register']
                asm.append(gen_ins('eqt r{} r{} r{}'.format(d_reg, r_test, r_result)))
                asm.append(gen_ins('jt r{} :{}'.format(r_result, c['label'])))

                free_register(r_test)

        free_register(d_reg)
        free_register(r_result)

        # if no case matches either go to end of switch or to default case if
        # it exists
        if default_name is not None:
            asm.append(gen_ins('jmp :{}'.format(default_name)))
        else:
            asm.append(gen_ins('jmp :{}'.format(end_switch)))


        handle_block(combined_block, base_node=t)

        asm.append(gen_ins('pop_store'))

        # no longer in switch, remove bookkeeping info
        break_stack.pop()

        # restore backed up scope
        scope_stack = scope_stack_stack.pop()
        scopes = scopes_backup.pop()

    elif t == 'InstructionInsert':
        # not generated from babel, used to insert assembly
        asm += node['instructions']

    elif t == 'UngeneratedInstructionInsert':
        # not generated from babel, used to insert assembly
        # generate now 
        asm += [gen_ins(ins) for ins in node['instructions']]

    else:
        print(node['loc'])
        print('{} node not implemented!'.format(t))

            
def handle_block(block, base_node, root=False, preset_vars=None, pop_after_compile=None):
    '''
    will create new scope and execute code in scope (if not root, root scope manually created)
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

    # this round will hoist function declarations (will not create func bodies)
    for node in block:
        if node['type'] == 'FunctionDeclaration':
            handle_node(node, declare_func_mode=True)

    # this round will hoist 'var' variable declarations
    # (just declaration, no initialisation)
    for node in block:
        if node['type'] == 'VariableDeclaration' and node['kind'] == 'var':
            just_declaration = copy.deepcopy(node)
            for decl in just_declaration['declarations']:
                decl['init'] = None
            handle_node(just_declaration)

    # this round will handle everything else
    for node in block:
        handle_node(node)

    # deconstruct scope:

    # no need to deconstruct if root; program ended
    if root: return
    # delete from parent scope's children list
    parent_children = scopes[prev_scope()]['children']
    del parent_children[parent_children.index(scope_id)]

    # delete all declared variables and free registers holding them
    declared = scopes[scope_id]['declared']
    for key in list(declared):
        symbol = declared[key]

        asm.append(gen_ins('delvar """{}"""'.format(symbol['id'])))

        # ignore current scope from scope calculations (as it will be deleted)
        #below_scope_declared = _calculate_top_store(scopes_below=1)
        #asm.append(gen_ins('delvar """{}"""'.format(symbol['id']),
        #    forced_top_declared=below_scope_declared))

        free_register(symbol['register'], force=True)
        del declared[key]

    if pop_after_compile is True:
        asm.append(gen_ins('pop_store'))

    # remove as current scope
    scope_stack.pop()

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
instructions_string = ''

for ins in asm: 
    instructions_string += ins['string_repr'] + '\n'

if '-l' in sys.argv:
    print(instructions_string)

f = open('.ins_read', 'w')
f.write(instructions_string)
f.close()

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

#print(used_names, len(used_names))
