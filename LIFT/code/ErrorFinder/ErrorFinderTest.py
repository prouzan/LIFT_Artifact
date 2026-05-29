from ErrorFinder import ErrorFinder
from Logger import Logger
# Example: ef = ErrorFinder.load('/tmpfs/tmp/gcd.bpl', ['x','y'])
ef = ErrorFinder.load(logger = Logger(), path2bpl='/tmpfs/tmp/K_3pieces_Caterina_TACAS16_modif_2.bpl', inputVars=['x','c'])
print(ef.getErrorInput())