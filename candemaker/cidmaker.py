from candemaker.linemaker import LineMakerBase

class A1(LineMakerBase):
    __prefix__ = '                      A-1!!'
    Mode = 0, dict(fill=' ', align='>', type='s')
    Level = 8, dict(fill=' ', align='>', type='d')
    Method = 10, dict(fill=' ', align='>', type='d')
    Groups = 12, dict(fill=' ', align='>', type='d')
    Heading = 15, dict(fill=' ', align='<', type='s')
    Iterations = 75, dict(fill=' ', align='>', type='d')
    CulvertID = 80, dict(fill=' ', align='>', type='d')
    ProcessID = 85, dict(fill=' ', align='>', type='d')
    SubdomainID = 90, dict(fill=' ', align='>', type='d')
    _dummy = 95
        
class D1(LineMakerBase):
    __prefix__ = '                      D-1!!'
    Limit = 0, dict(fill=' ')
    ID = 1, dict(fill=' ', align='>', type='d')
    # 1: isotropic, 2: orthotropic, 3: Duncan/Seling, 4: Overburden Dependent,
    # 5: Extended Hardin, 6: Interface, 7: Composite Link, 8: Mohr/Coulomb
    Model = 5, dict(fill=' ', align='>', type='d'), 1
    Density = 10, dict(fill=' ', align='>', type='d') # pcf
    Name = 20, dict(fill=' ', align='>', type='s')
    Layers = 40, dict(fill=' ', align='>', type='d')
    _dummy = 42
    
class E1(LineMakerBase):
    __prefix__ = '                      E-1!!'
    Start = 0, dict(fill=' ', align='>', type='d')
    Last = 5, dict(fill=' ', align='>', type='d')
    Factor = 10, dict(fill=' ', align='>', type='f')
    Comment = 20, dict(fill=' ', align='>', type='s')
    _dummy = 60
