from shutil import copyfile
from devito import configuration
from devito import TimeFunction, Grid, Operator, Eq
from devito import compiler_registry
from devito.arch.compiler import GNUCompiler

files = {
    'counter': 'src/counter.c',
    'power': 'src/power.c'
    }

def operatorInjector(op, payload):

    configuration['jit-backdoor'] = True
    configuration.add('payload', payload)

    # Force compilation *and* loading upon the next `op.apply`

    op._lib = None
    op._cfunction = None

    if op._soname:
        del op._soname

    cfile = "%s.c" % str(op._compiler.get_jit_dir().joinpath(op._soname))

    copyfile(payload, cfile)

if __name__ == "__main__":

    # Running standard Devito code, no jit-backdoor.

    grid = Grid(shape=(4, 4))

    u = TimeFunction(name='u', grid=grid)
    op = Operator(Eq(u.forward, u + 1))

    op.apply(time_M=10)

    print(u.data)

    # Running Modified Devito code, using jit-backdoor.
    # Print Current Time step

    u2 = TimeFunction(name='u', grid=grid)

    #Inject the counter.c source code
    operatorInjector(op, files['counter'])
    op.apply(time_M=10, u=u2)

    print(u2.data)

    # Running Modified devito code with external parameters

    variables = {'BASE':'2'}

    # This class is used to manipulate variables inside of the generated code
    class Variable2Compiler(GNUCompiler):
        def __init__(self, *args, **kwargs):
            kwargs['suffix'] = 11 # Ensure GCC 11
            super(Variable2Compiler, self).__init__(*args, **kwargs)
            for key in variables:
                define = "%s=%s" % (key, variables[key])
                self.defines.append(define)

    # Registry a new Compiler
    compiler_registry['Variable2Compiler'] = Variable2Compiler
    configuration.add("compiler", "custom", list(compiler_registry), callback=lambda i: compiler_registry[i]())
    configuration['compiler'] = 'Variable2Compiler'

    u3 = TimeFunction(name='u', grid=grid)
    u3.data[:] = 1

    # Create a new operator
    op = Operator(Eq(u.forward, u + 1))

    #Inject the power.c source code
    operatorInjector(op, files['power'])

    # Run 2^10
    op.apply(time_M=10, u=u3)

    print(u3.data)