from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def ass_1_bar():
    """ 2024 assignment 1 - bar model """
    n_1 = Node('node1', 0, 0, constraint='pin')
    n_2 = Node('node2', 2, 0, constraint='free')
    n_3 = Node('node3', 4, 0, constraint='free')
    n_4 = Node('node4', 8/3, 0.8, constraint='free')
    n_5 = Node('node5', 4/3, 1.2, constraint='free')
    n_6 = Node('node6', 0, 1.2, constraint='pin')

    E = 200e9
    D = 50e-3
    d = 38e-3
    A = np.pi/4 * (D**2-d**2)

    a1 = 0
    a2 = 41.99
    a3 = 0
    a4 = 50.19
    a5 = 119.05
    a6 = 149.04
    a7 = 163.3
    a8 = 180

    l1 = 2
    l2 = 1.794
    l3 = 2
    l4 = 1.041
    l5 = 1.372
    l6 = 1.555
    l7 = 1.392
    l8 = 1.333

    bar1 = Local_Bar('bar1', E=E, A=A, L=l1, node_a=n_1, node_b=n_2, alpha=a1)
    bar2 = Local_Bar('bar2', E=E, A=A, L=l2, node_a=n_1, node_b=n_5, alpha=a2)
    bar3 = Local_Bar('bar3', E=E, A=A, L=l3, node_a=n_2, node_b=n_3, alpha=a3)
    bar4 = Local_Bar('bar4', E=E, A=A, L=l4, node_a=n_2, node_b=n_4, alpha=a4)
    bar5 = Local_Bar('bar5', E=E, A=A, L=l5, node_a=n_2, node_b=n_5, alpha=a5)
    bar6 = Local_Bar('bar6', E=E, A=A, L=l6, node_a=n_3, node_b=n_4, alpha=a6)
    bar7 = Local_Bar('bar7', E=E, A=A, L=l7, node_a=n_4, node_b=n_5, alpha=a7)
    bar8 = Local_Bar('bar8', E=E, A=A, L=l8, node_a=n_5, node_b=n_6, alpha=a8)

    structure1 = Assembly('bar-structure', Q=np.array([0,0,0,-25e3,0,0,0,0]))
    structure1.add_element(bar1)
    structure1.add_element(bar2)
    structure1.add_element(bar3)
    structure1.add_element(bar4)
    structure1.add_element(bar5)
    structure1.add_element(bar6)
    structure1.add_element(bar7)
    structure1.add_element(bar8)
    structure1.A_matrices()
    # structure1.print_assembly_matrices()
    structure1.set_reaction_loads()
    structure1.print_reaction_loads()
    # structure1.print_axial_stresses()
    # structure1.print_deflection()
    # structure1.print_angles()
    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=50)
    structure1.show_structure()

def ass_1_frame():
    """ 2024 assignment 1 - frame model """
    n_1 = Node('node1', 0, 0, constraint='fixed')
    n_2 = Node('node2', 2, 0, constraint='free')
    n_3 = Node('node3', 4, 0, constraint='free')
    n_4 = Node('node4', 8/3, 0.8, constraint='free')
    n_5 = Node('node5', 4/3, 1.2, constraint='free')
    n_6 = Node('node6', 0, 1.2, constraint='fixed')

    E = 200e9
    D = 50e-3
    d = 38e-3
    A = np.pi/4 * (D**2-d**2)
    I = np.pi/64 * (D**4-d**4)
    c = D / 2

    a1 = 0
    a2 = 41.99
    a3 = 0
    a4 = 50.19
    a5 = 119.05
    a6 = 149.04
    a7 = 163.3
    a8 = 180

    l1 = 2
    l2 = 1.794
    l3 = 2
    l4 = 1.041
    l5 = 1.372
    l6 = 1.555
    l7 = 1.392
    l8 = 1.333

    frame1 = Local_Frame('frame1', E=E, I=I, A=A, L=l1, node_a=n_1, node_b=n_2, alpha=a1)
    frame2 = Local_Frame('frame2', E=E, I=I, A=A, L=l2, node_a=n_1, node_b=n_5, alpha=a2)
    frame3 = Local_Frame('frame3', E=E, I=I, A=A, L=l3, node_a=n_2, node_b=n_3, alpha=a3)
    frame4 = Local_Frame('frame4', E=E, I=I, A=A, L=l4, node_a=n_2, node_b=n_4, alpha=a4)
    frame5 = Local_Frame('frame5', E=E, I=I, A=A, L=l5, node_a=n_2, node_b=n_5, alpha=a5)
    frame6 = Local_Frame('frame6', E=E, I=I, A=A, L=l6, node_a=n_3, node_b=n_4, alpha=a6)
    frame7 = Local_Frame('frame7', E=E, I=I, A=A, L=l7, node_a=n_4, node_b=n_5, alpha=a7)
    frame8 = Local_Frame('frame8', E=E, I=I, A=A, L=l8, node_a=n_5, node_b=n_6, alpha=a8)

    structure2 = Assembly('frame-structure', Q=np.array([0,0,0,0,-25e3,0,0,0,0,0,0,0]))
    structure2.add_element(frame1)
    structure2.add_element(frame2)
    structure2.add_element(frame3)
    structure2.add_element(frame4)
    structure2.add_element(frame5)
    structure2.add_element(frame6)
    structure2.add_element(frame7)
    structure2.add_element(frame8)
    structure2.A_matrices()
    # structure2.print_assembly_matrices()
    # structure2.print_deflection()
    structure2.set_reaction_loads()
    structure2.print_reaction_loads()
    # structure2.print_axial_stresses()
    # structure2.print_bending_stresses(c=c)
    # structure2.print_total_stresses(c=c)
    structure2.draw_full_deflected_frame(deflection_scale=50, n_points=10)
    structure2.show_structure()
    
if __name__ == "__main__":
    ass_1_bar()
    ass_1_frame()