from candemaker.filemaker import FileOut
from pathlib import Path
import os

def test_FileOut():
    obj = ('a', 'b', 'c')
    p = Path(os.getenv('USERPROFILE'))/'Desktop'/'test.txt'
    outfile = FileOut(obj)
    with open(str(p), mode = 'w') as fout:
        fout.write('A tuple\n\n' + outfile.to_str())
        
    os.startfile(str(p))