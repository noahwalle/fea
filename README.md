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
Can input degrees of freedom manually (T_x, T_y, R_z),
or use the keywords which handle all the cases.
Keywords to set degrees of freedom at a node:
- fixed
- free
- pin/pinned
- roller-vertical
- roller-horizontal
- roller-vertical-pin
- roller-horizontal-pin

## Examples

Examples are in fea_main.py