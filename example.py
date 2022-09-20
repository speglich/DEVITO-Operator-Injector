from shutil import copyfile
from devito import configuration
from devito import TimeFunction, Grid, Operator, Eq

files = {
    'counter': 'src/counter.c',
    'power': 'src/power.c'
    }

def OperatorInjector(operator, payload):

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

    u2 = TimeFunction(name='u', grid=grid)
    OperatorInjector(op, files['counter'])
    op.apply(time_M=10, u=u2)

    print(u2.data)

    u3 = TimeFunction(name='u', grid=grid)
    OperatorInjector(op, files['power'])
    op.apply(time_M=10, u=u3)

    print(u3.data)