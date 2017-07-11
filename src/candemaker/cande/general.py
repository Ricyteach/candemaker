from collections import namedtuple as nt


def add_specs_defaults_to_nts(obj, d):
    obj._field_specs = tuple(d[field_name].spec for field_name in obj._fields)
    obj._defaults = tuple(d[field_name].default for field_name in obj._fields)


ObjDef = nt('ObjDef', 'spec default')


def register_objects():
    from ..cid import register, format_specs as fs

    # Section A1
    master_dict = dict(
                        # ANALYS or DESIGN
                        Mode = ObjDef(fs.s8, 'ANALYS'),
                        # 1, 2, or 3
                        Level = ObjDef(fs.d2, 3),
                        Method = ObjDef(fs.d2, 1),
                        NGroups = ObjDef(fs.d3, 1),
                        Heading = ObjDef(fs.s60, ''),
                        Iterations = ObjDef(fs.d5, -99),
                        CulvertID = ObjDef(fs.d5, 0),
                        ProcessID = ObjDef(fs.d5, 0),
                        SubdomainID = ObjDef(fs.d5, 0)
                        )

    Master = nt('Master', master_dict.keys())
    Master._prefix = 'A-1'
    Master._name = 'A1'

    # Section E1
    factor_dict = dict(
                        Start = ObjDef(fs.d5, 0),
                        Last = ObjDef(fs.d5, 0),
                        Factor = ObjDef(fs.f10, 1),
                        Comment = ObjDef(fs.s40, '')
                        )

    Factor = nt('Factor', factor_dict.keys())
    Factor._prefix = 'E-1'
    Factor._name = 'E1'

    for obj, d, gen in ((Master, master_dict, A1_gen),
                        (Factor, factor_dict, E1_gen)
                        ):
        add_specs_defaults_to_nts(obj, d)
        register(obj, d, gen)
        yield obj

for obj in register_objects():
    exec('{} = obj'.format(obj.__name__))

del register_objects
del obj
del nt
