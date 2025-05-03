# rubik's-cube-solver
Collaborators
Taehun Lee
Peter Huang

Overview
- employ group theory to solve rubik's cube
- convert between 3D model of cube and 3D matrix representation of it
- use three.js, html, css to display the cube

Overview
This project implements a Rubik's Cube solving algorithm based on concepts from group theory. The cube is represented as a 3D matrix in Python, allowing for efficient manipulation and computation of moves. The solving process is visualized using a 3D interactive model built with Three.js, styled with HTML and CSS. The goal is to provide both a mathematically grounded solution method and an intuitive, dynamic visualization of the solving steps.

Group theory
In mathemetics, groups are defined to be some set G that conforms to certain axioms after applying binary operations. These axioms include closure, associativity, identity element and inverse. In context of rubik's cube, the groups can be defined as different sides of the Rubik's cube, where each element in a group is different sides of the Rubik's cube. For instance, F would refer to the front side of the cube and rotating it in a clockwise direction. We can use prime(') notation to indicate counterclockwise movement such as F'.

![notation](https://github.com/user-attachments/assets/9bf9081b-1705-4526-84d4-5728c745065b)

Sources

https://www.youtube.com/watch?v=zkADn-9wEgc
https://www.ucl.ac.uk/~ucahmto/0007/_book/4-1-basic-definitions.html
https://web.mit.edu/sp.268/www/rubik.pdf
ChatGPT
