# pycggcrg
A Python binding for the CGGC-RG algorithm family.

## Installation
To install run `python setup.py install` and ensure the C++ sources of 
[*CGGC-RG*](https://github.com/FabianBall/cggc_rg) are found in the 
path `./cggc_rg`.

## Tests
Tests can be run calling `python setup.py test`.

## Changes
0.2.5
  - Add: more tests
  - Add: more/better docstrings
  - Change: 'hardened' the wrapper
  
0.2.4
  - Fix: set C pseudo RNG seed
  - Fix: get_partition used vector.capacity() instead of vector.size()
  
0.2.3
  - Testing connectedness of the graph is now optional
  
0.2.2
  - Fixes

0.2.1
  - Added tests

0.2
  - CGGC algorithms can be called
  - Fixes
  
0.1
  - First version
