from candemaker.linemaker import LineMakerBase

class C1(LineMakerBase):
    __prefix__ = '                   C-1.L3!!'
    Prep = 0, dict(type='s')
    Title = 5, dict(fill=' ', align='>', type='s')
    
class C2(LineMakerBase):
    __prefix__ = '                   C-2.L3!!'
    Steps = 0, dict(fill=' ', align='>', type='d'), 1
    # 1: control data, 2: input data, 3: created data, 4: maximum
    MeshOutput = 5, dict(fill=' ', align='>', type='d'), 3 # default
    Check = 10, dict(fill=' ', align='>', type='d') # 0: run, 1: check
    PlotControl = 15, dict(fill=' ', align='>', type='d'), 3 # always 3
    ResponseOutput = 20, dict(fill=' ', align='>', type='d')
    Nodes = 25, dict(fill=' ', align='>', type='d')
    Elements = 30, dict(fill=' ', align='>', type='d')
    Boundaries = 35, dict(fill=' ', align='>', type='d')
    SoilMaterials = 40, dict(fill=' ', align='>', type='d')
    InterfMaterials = 45, dict(fill=' ', align='>', type='d')
    # 0: none, 1: minimize, 2: minimize and print
    Bandwidth = 50, dict(fill=' ', align='>', type='d'), 1
    _dummy = 55
    
class C3(LineMakerBase):
    __prefix__ = '                   C-3.L3!!'
    Limit = 0, dict(fill=' ')
    Node = 1, dict(fill=' ', align='>', type='d')
    SpecialReferenceCode = 5, dict(fill=' ', align='>', type='d')
    SpecialGenerationCode = 8, dict(type='d')
    BasicGenerationCode = 9, dict(type='d')
    x = 10, dict(fill=' ', align='>', type='f')
    y = 20, dict(fill=' ', align='>', type='f')
    Increment = 30, dict(fill=' ', align='>', type='d')
    Spacing = 40, dict(fill=' ', align='>', type='f')
    Radius = 50, dict(fill=' ', align='>', type='f')
    _dummy = 60

class C4(LineMakerBase):
    __prefix__ = '                   C-4.L3!!'
    Limit = 0, dict(fill=' ')
    Element = 1, dict(fill=' ', align='>', type='d')
    I = 5, dict(fill=' ', align='>', type='d')
    J = 10, dict(fill=' ', align='>', type='d')
    K = 15, dict(fill=' ', align='>', type='d')
    L = 20, dict(fill=' ', align='>', type='d')
    Mat = 25, dict(fill=' ', align='>', type='d')
    Step = 30, dict(fill=' ', align='>', type='d')
    # 1 for interface, 8 for link element fixed, 9 for link element pinned
    InterfLink = 35, dict(fill=' ', align='>', type='d')
    IncrementAdded = 40, dict(fill=' ', align='>', type='d')
    RowsAdded = 45, dict(fill=' ', align='>', type='d')
    IncrementBetween = 50, dict(fill=' ', align='>', type='d')
    Death = 55, dict(fill=' ', align='>', type='d')
    _dummy = 60
    
class C5(LineMakerBase):
    __prefix__ = '                   C-5.L3!!'
    Limit = 0, dict(fill=' ')
    Node = 1, dict(fill=' ', align='>', type='d')
    Xcode = 5, dict(fill=' ', align='>', type='d')
    Xvalue = 10, dict(fill=' ', align='>', type='f')
    Ycode = 20, dict(fill=' ', align='>', type='d')
    Yvalue = 25, dict(fill=' ', align='>', type='f')
    Angle = 35, dict(fill=' ', align='>', type='f')
    Step = 45, dict(fill=' ', align='>', type='d')
    End = 50, dict(fill=' ', align='>', type='d')
    Increment = 55, dict(fill=' ', align='>', type='d')
    Pressure1 = 60, dict(fill=' ', align='>', type='d')
    Pressure2 = 70, dict(fill=' ', align='>', type='d')
    _dummy = 80