def register_objects():
    from collections import namedtuple as nt
    from .. import format_specs as fs
    from ..cid import register
    from .general import ObjDef, add_specs_defaults_to_nts
    from mytools.blank import BlankInt, BlankFloat

    prefix_spec = '{}.L3!!' # overwrites prefix_spec from .format_specs

    # Section A2
    pipe_group_dict = dict(
                        # ALUMINUM, BASIC, CONCRETE, PLASTIC, STEEL, CONRIB, CONTUBE
                        Type = ObjDef(fs.s10, 'NO_DEFAULT'),
                        Num = ObjDef(fs.d5, 0)
                        )
        
    PipeGroup = nt('PipeGroup', pipe_group_dict.keys())
    PipeGroup._prefix = prefix_spec.format('A-2')
    PipeGroup._name = 'A2'

    # Section C1
    L3_info_dict = dict(
                        Prep = ObjDef(fs.s5, 'PREP'),
                        Title = ObjDef(fs.s68, '')
                        )

    L3Info = nt('L3Info', ['Title'])
    L3Info._prefix = prefix_spec.format('C-1')
    L3Info._name = 'C1'

    # Section C2
    L3_control_dict = dict(
                            Steps = ObjDef(fs.d5, 1),
                            # 1: control data, 2: input data,
                            # 3: created data, 4: maximum
                            MeshOutput = ObjDef(fs.d5, 3),
                            Check = ObjDef(fs.d5, 1),  # 0: run, 1: check
                            PlotControl = ObjDef(fs.d5, 3),  # always 3
                            # 0: minimal, 1: standard, 2: plus Duncan,
                            # 3: plus interface, 4: plus Mohr Coulomb
                            ResponseOutput = ObjDef(fs.d5, 0),
                            Nodes = ObjDef(fs.d5, 0),
                            Elements = ObjDef(fs.d5, 0),
                            Boundaries = ObjDef(fs.d5, 0),
                            SoilMaterials = ObjDef(fs.d5, 0),
                            InterfMaterials = ObjDef(fs.d5, 0),
                            # 0: none, 1: minimize, 2: minimize and print
                            Bandwidth = ObjDef(fs.d5, 1)
                            )

    L3Control = nt('L3Control', 'Steps Check Nodes Elements Boundaries SoilMaterials InterfMaterials Bandwidth')
    L3Control._prefix = prefix_spec.format('C-2')
    L3Control._name = 'C2'

    # Section C3
    node_dict = dict(
                        Limit = ObjDef(fs.s1, ' '),
                        Num = ObjDef(fs.d4, 0),
                        SpecialReferenceCode = ObjDef(fs.d3, 0),
                        SpecialGenerationCode = ObjDef(fs.d1, 0),
                        BasicGenerationCode = ObjDef(fs.d1, BlankInt()),
                        X = ObjDef(fs.f10, 0),
                        Y = ObjDef(fs.f10, 0),
                        Increment = ObjDef(fs.d5, BlankInt()),
                        Spacing = ObjDef(fs.f10, BlankFloat()),
                        Radius = ObjDef(fs.f10, BlankFloat())
                        )

    Node = nt('Node', 'Num X Y')
    NodeLast = nt('NodeLast', 'Limit Num X Y')
    for NT in (Node, NodeLast):
        NT._prefix = prefix_spec.format('C-3')
        NT._name = 'C3'

    # Section C4
    element_dict = dict(
                        Limit = ObjDef(fs.s1, ' '),
                        Num = ObjDef(fs.d4, 0),
                        I = ObjDef(fs.d5, 0),
                        J = ObjDef(fs.d5, 0),
                        K = ObjDef(fs.d5, 0),
                        L = ObjDef(fs.d5, 0),
                        Mat = ObjDef(fs.d5, 0),
                        Step = ObjDef(fs.d5, 0),
                        # 0 for normal, 1 for interface,
                        # 8 for link element fixed, 9 for link element pinned
                        InterfLink = ObjDef(fs.d5, BlankInt()),
                        IncrementAdded = ObjDef(fs.d5, BlankInt()),
                        RowsAdded = ObjDef(fs.d5, BlankInt()),
                        IncrementBetween = ObjDef(fs.d5, BlankInt()),
                        Death = ObjDef(fs.d5, BlankInt())
                        )

    Element = nt('Element', 'Num I J K Mat Step InterfLink')
    TriaElement = nt('TriaElement', 'Num I J K Mat Step')
    QuadElement = nt('QuadElement', 'Num I J K L Mat Step')
    SoilElement = nt('SoilElement', 'Num I J K L Mat Step')
    BeamElement = nt('BeamElement', 'Num I J Mat Step')
    InterfElement = nt('InterfElement', 'Num I J K Mat Step InterfLink')
    ElementLast = nt('ElementLast', 'Limit Num I J K Mat Step InterfLink')

    for NT in (Element, TriaElement, QuadElement, SoilElement, BeamElement, InterfElement, ElementLast):
        NT._prefix = prefix_spec.format('C-4')
        NT._name = 'C4'

    # Section C5
    bound_dict = dict(
                        Limit = ObjDef(fs.s1, ' '),
                        Node = ObjDef(fs.d4, 0),
                        Xcode = ObjDef(fs.d5, 0),
                        Xvalue = ObjDef(fs.f10, 0),
                        Ycode = ObjDef(fs.d5, 0),
                        Yvalue = ObjDef(fs.f10, 0),
                        Angle = ObjDef(fs.f10, 0),
                        Step = ObjDef(fs.d5, 0),
                        EndNode = ObjDef(fs.d5, BlankInt()),
                        Increment = ObjDef(fs.d5, BlankInt()),
                        Pressure1 = ObjDef(fs.f10, BlankFloat()),
                        Pressure2 = ObjDef(fs.f10, BlankFloat())
                        )
    
    Bound = nt('Bound', 'Node Xcode Xvalue Ycode Yvalue Angle Step')
    ForceBound = nt('ForceBound', 'Node Xvalue Yvalue Step')
    SideBound = nt('SideBound', 'Node Xcode Step')
    BotBound = nt('BotBound', 'Node Ycode Step')
    CornerBound = nt('CornerBound', 'Node Xcode Ycode Step')
    BoundLast = nt('BoundLast', 'Limit Node Xcode Xvalue Ycode Yvalue Angle Step')

    for NT in (Bound, ForceBound, SideBound, BotBound, CornerBound, BoundLast):
        NT._prefix = prefix_spec.format('C-5')
        NT._name = 'C5'

    for obj, d, gen in ((PipeGroup, pipe_group_dict, A2_gen),
                        (L3Info, L3_info_dict, C1_gen),
                        (L3Control, L3_control_dict, C2_gen),
                        (Node, node_dict, C3_gen),
                        (NodeLast, node_dict, C3_gen),
                        (Element, element_dict, C4_gen),
                        (TriaElement, element_dict, C4_gen),
                        (QuadElement, element_dict, C4_gen),
                        (SoilElement, element_dict, C4_gen),    
                        (BeamElement, element_dict, C4_gen),
                        (InterfElement, element_dict, C4_gen),
                        (ElementLast, element_dict, C4_gen),
                        (Bound, bound_dict, C5_gen),
                        (ForceBound, bound_dict, C5_gen),
                        (SideBound, bound_dict, C5_gen),
                        (BotBound, bound_dict, C5_gen),
                        (CornerBound, bound_dict, C5_gen),
                        (BoundLast, bound_dict, C5_gen)
                        ):
        add_specs_defaults_to_nts(obj, d)
        register(obj, d, gen)
        yield obj

for obj in register_objects():
    print(obj.__name__, obj)
    input('\n')
    exec('{} = obj'.format(obj.__name__))

del register_objects
del obj
