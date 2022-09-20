# DEVITO-Operator-Injector

Efficient use of DEVITO_JIT_BACKDOOR in large codes with many Operators.

## How it works: OperatorInjector

Inject a new source file - `payload` - to a defined devito operator.

```python

from devito import configuration

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

```

