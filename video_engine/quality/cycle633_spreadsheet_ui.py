"""Cycle633: ten-genre reusable column-only spreadsheet selection and proof.
Original synthetic values, no user data or external assets.
"""
from dataclasses import dataclass
from typing import Tuple
VALUES = (120, 150, 200, 250)
CELL_LEFT, CELL_RIGHT = 235, 455
ROW_TOP, ROW_HEIGHT = 326, 64
GENRES = ('ai_productivity','trivia','cooking','beauty','money','health',
          'travel','products','story','work_tips')
SCENES = (
 (0,60,'hook'),(60,120,'problem'),(120,210,'prompt'),
 (210,300,'select'),(300,390,'formula'),(390,480,'proof'),
 (480,540,'compare'),(540,600,'cta')
)
@dataclass(frozen=True)
class Cell:
    address: str
    value: int
    rect: Tuple[int,int,int,int]
def cells():
    return tuple(Cell(f'B{j+2}',v,(CELL_LEFT,ROW_TOP+j*ROW_HEIGHT,
                 CELL_RIGHT,ROW_TOP+(j+1)*ROW_HEIGHT)) for j,v in enumerate(VALUES))
def selected_cells(progress):
    if not 0 <= progress <= 1: raise ValueError('progress outside [0,1]')
    count=min(4,max(1,int(progress*4)+1))
    return cells()[:count]
def proof():
    assert sum(VALUES)==720
    return '=SUM(B2:B5)',sum(VALUES)
def validate():
    assert len(GENRES)==10
    assert SCENES[0][0]==0 and SCENES[-1][1]==600
    assert all(SCENES[i][1]==SCENES[i+1][0] for i in range(len(SCENES)-1))
    assert [s[2] for s in SCENES].index('prompt')<[s[2] for s in SCENES].index('select')
    assert tuple(c.address for c in cells())==('B2','B3','B4','B5')
    assert all(c.rect[0]==CELL_LEFT and c.rect[2]==CELL_RIGHT for c in cells())
    assert proof()==('=SUM(B2:B5)',720)
    return True
def publication_gate(*,narration=False,sync=False,rights=False,device=False,employee=False):
    return ('ELIGIBLE_FOR_HUMAN_POSTING' if all((narration,sync,rights,device,employee))
            else 'PUBLICATION_NOT_APPROVED')
