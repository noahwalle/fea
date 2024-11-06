# FEA code repo
___
- [FEA code repo](#fea-code-repo)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Examples](#examples)

## Introduction
A simple 2D FEA visualisation package, using numpy and matplotlib
for arithmetic and visualisation.

## Features
### Degrees of Freedom
Can input degrees of freedom manually (T_x, T_y, R_z),
or use the keywords which handle all the cases.
Keywords to set degrees of freedom at a node:
- fixed                         (T_x=0, T_y=0, T_z=0)
- free                          (T_x=1, T_y=1, T_z=1)
- pin                           (T_x=0, T_y=0, T_z=1)
- roller-vertical               (T_x=0, T_y=1, T_z=0)
- roller-horizontal             (T_x=1, T_y=0, T_z=0)
- roller-vertical-pin           (T_x=0, T_y=1, T_z=1)
- roller-horizontal-pin         (T_x=1, T_y=0, T_z=1)

### Nodes
A node is a coordinate in Cartesian space that contains
position in x and y coordinates, and a degree of freedom
from the list above depending on the type of joint at the
node.

### Elements
An element is a structural member initiliased between two
nodes. Elements need to be initialised with a reasonable
Young's Modulus in Gigapascals (GPa), cross-sectional
area (mm^2), second moment of area (mm^4) (only for frame
elements), length (m), starting node, ending node, and 
rotation angle.

### Element Types
This package can be used to simulate applied loading cases
for bar and frame element types. Bars can only deflect
axially, whereas frames can take shear and moment loads.

### Structures
A structure (aka assembly) is initialised to put all of the
desired elements into the same context. The function
structure_name.A_matrices() then generates the assembly matrices
for each element, and the element stiffness matrices can be
put into the global stiffness matrix to calculate useful things
like deflections in members, forces, stresses etc.

## Examples
### Simple Examples
There are 9 simple examples (named ex#.py) that detail simple problems
from various homeworks and labs throughout the year. These are great for
learning how to set up problems.

### Test Questions
There are 7 questions from tests ranging from 2021-2024. The code produces
quite a few random-looking outputs. The fea.py module offers some insight
for details on what is going on under the hood. Refer to the code for each
question to see what is being produced.
