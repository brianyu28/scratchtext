from scratch import *

import sys
filename = sys.argv[1]
code = open(filename).read()

tree = parse(code)

print(tree)
