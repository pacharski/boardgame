import pstats
from pstats import SortKey
p = pstats.Stats('prof.out')
p.sort_stats(SortKey.TIME).print_stats(30)
#p.strip_dirs().sort_stats(-1).print_stats()