from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def ex1():
    """ Example from ENME302 Lab 2 """
    n_1 = Node("node1", 0, 0)
    n_2 = Node("node2", 1.1, 0, T_x=1, T_y=1)
    n_3 = Node("node3", 1.1 + np.cos(0.8), np.sin(0.8))

    bar1 = Local_Bar("bar1", E=200e9, A=400e-6, L=1.1, node_a=n_1, node_b=n_2, alpha=0)
    bar2 = Local_Bar("bar2", E=200e9, A=600e-6, L=0.8, node_a=n_2, node_b=n_3, alpha=55)

    structure1 = Assembly("structure1", Q=np.array([0, -20000]))
    structure1.add_element(bar1)
    structure1.add_element(bar2)
    structure1.A_matrices()

    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=100)
    structure1.show_structure()

def ex2():
    """ Example from p49 of ENME302 course reader """
    Ae = np.pi * (100e-3) ** 2 / 4

    n_1 = Node("node1", 0, 0)
    n_2 = Node("node2", 10, 0, T_x=1, T_y=1)
    n_3 = Node("node3", 0, -10)

    bar1 = Local_Bar("bar1", E=200e9, A=Ae, L=10, node_a=n_1, node_b=n_2, alpha=0)
    bar2 = Local_Bar("bar2", E=200e9, A=Ae, L=14.1, node_a=n_2, node_b=n_3, alpha=45)

    structure1 = Assembly("structure1", Q=np.array([0, 100000]))
    structure1.add_element(bar1)
    structure1.add_element(bar2)
    structure1.A_matrices()

    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=100)
    structure1.show_structure()

def ex3():
    """ Example from p58 of ENME302 course reader """
    n_1 = Node("node1", 0, 0)
    n_2 = Node("node2", 2.5, 5 * np.sin(np.radians(60)), T_x=1, T_y=1)
    n_3 = Node("node3", 5, 0, T_x=1)

    Ae = np.pi / 4 * (0.1 ** 2 - 0.08 ** 2)

    bar1 = Local_Bar("bar1", E=70e9, A=Ae, L=5, node_a=n_1, node_b=n_2, alpha=60)
    bar2 = Local_Bar("bar2", E=70e9, A=Ae, L=5, node_a=n_1, node_b=n_3, alpha=0)
    bar3 = Local_Bar("bar3", E=70e9, A=Ae, L=5, node_a=n_2, node_b=n_3, alpha=-60)

    structure1 = Assembly("structure1", Q=np.array([500e3, 0, 0]))
    structure1.add_element(bar1)
    structure1.add_element(bar2)
    structure1.add_element(bar3)
    structure1.A_matrices()

    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=30)
    structure1.show_structure()

def ex4():
    """ Example from p84 of ENME302 course reader """
    n_1 = Node("node1", 0, 0)
    n_2 = Node("node2", 0, -10, T_x=1, R_z=1)
    n_3 = Node("node3", 10, -10, R_z=1)

    frame1 = Local_Frame("frame1", E=200e9, I=5e-4, A=1e-5, L=10, node_a=n_1, node_b=n_2, alpha=-90)
    frame2 = Local_Frame("frame2", E=200e9, I=5e-4, A=1e-5, L=10, node_a=n_2, node_b=n_3, alpha=0)

    structure1 = Assembly("structure1", Q=np.array([0, 140000, 0]))
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.A_matrices()

    # structure1.draw_structure_initial()
    # structure1.draw_structure_deflected(deflection_scale=100)
    structure1.draw_full_deflected_frame(100, 20)
    structure1.show_structure()

def ex5():
    """ Example from ENME302 Lab 3 """
    n_1 = Node("node1", 0, 0)
    n_2 = Node("node2", 5, 0, T_x=1, R_z=1)
    n_3 = Node("node3", 7.5, 0, T_x=1, T_y=1, R_z=1)

    frame1 = Local_Frame("frame1", E=200e9, I=640e-6, A=2e-4, L=5, node_a=n_1, node_b=n_2, alpha=0)
    frame2 = Local_Frame("frame2", E=200e9, I=640e-6, A=2e-4, L=2.5, node_a=n_2, node_b=n_3, alpha=0)

    structure1 = Assembly("structure1", Q=np.array([0, 0, 0, -150000, 0]))
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.A_matrices()

    # structure1.draw_structure_initial()
    # structure1.draw_structure_deflected(deflection_scale=50)
    structure1.draw_full_deflected_frame(100, 20)
    structure1.show_structure()

def ex6():
    """ Example from p97 of ENME302 course reader """
    n_1 = Node("node1", 0, 0, R_z=1)
    n_2 = Node("node2", 4, 0, T_x=1, T_y=1, R_z=1)
    n_3 = Node("node3", 8, -0)
    n_4 = Node("node4", 4, -4)

    frame1 = Local_Frame("frame1", E=200e9, I=5e-4, A=1e-5, L=4, node_a=n_1, node_b=n_2, alpha=0)
    frame2 = Local_Frame("frame2", E=200e9, I=5e-4, A=1e-5, L=4, node_a=n_2, node_b=n_3, alpha=0)
    frame3 = Local_Frame("frame3", E=200e9, I=5e-4, A=1e-5, L=4, node_a=n_2, node_b=n_4, alpha=-90)

    structure1 = Assembly("structure1", Q=np.array([0, 0, 100000, 0]))
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.add_element(frame3)
    structure1.A_matrices()

    # structure1.draw_structure_initial()
    # structure1.draw_structure_deflected(deflection_scale=100)
    structure1.draw_full_deflected_frame(100, 20)
    structure1.show_structure()

def ex7():
    """ Example from p105 of ENME302 course reader """
    n_1 = Node("node1", 0, 0, constraint='fixed')
    n_2 = Node("node2", 0, 3, constraint='free')
    # n_2 = Node("node2", 0, 3, T_x=1, R_z=1) # Not considering axial deflections
    n_3 = Node("node3", 4.5, 3, constraint='free') 
    # n_3 = Node("node3", 4.5, 3, T_x=1, R_z=1) # Not considering axial deflections
    n_4 = Node("node4", 4.5, 0, constraint='fixed')

    frame1 = Local_Frame("frame1", E=200e9, I=5e-4, A=1e-5, L=3, node_a=n_1, node_b=n_2, alpha=90)
    frame2 = Local_Frame("frame2", E=200e9, I=5e-4, A=1e-5, L=4.5, node_a=n_2, node_b=n_3, alpha=0)
    frame3 = Local_Frame("frame3", E=200e9, I=5e-4, A=1e-5, L=3, node_a=n_3, node_b=n_4, alpha=-90)


    # structure1 = Assembly("structure1", Q=np.array([10000, 0, 10000, 0])) # Not considering axial deflections
    structure1 = Assembly("structure1", Q=np.array([10000, 0, 0, 10000, 0, 0]))
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.add_element(frame3)
    structure1.A_matrices()

    # structure1.draw_structure_initial()
    # structure1.draw_structure_deflected(deflection_scale=100)
    structure1.draw_full_deflected_frame(200, 20)
    structure1.show_structure()

def ex8():
    """ From the 2020 test - Q1 """
    a1 = np.radians(45)
    a2 = np.radians(75)
    a3 = np.radians(10)

    n_1 = Node('node1', 0, 0, constraint='fixed')
    n_2 = Node('node2', 0, 0.5, constraint='free')
    n_3 = Node('node3', 2*np.cos(a1), 0.5+2*np.sin(a1), constraint='free')
    n_4 = Node('node4', 2*(np.cos(a1)+np.cos(a2)), 0, constraint='fixed')

    frame1 = Local_Frame('frame1', E=10e9, I=1e-6, A=4e-4, L=0.5, node_a=n_1, node_b=n_2, alpha=90)
    frame2 = Local_Frame('frame2', E=10e9, I=1e-6, A=4e-4, L=2, node_a=n_2, node_b=n_3, alpha=45)
    frame3 = Local_Frame('frame3', E=10e9, I=1e-6, A=4e-4, L=2, node_a=n_3, node_b=n_4, alpha=-75)

    Q_applied = 4e3 # [N]
    Q_axial = Q_applied * np.sin(a3)
    Q_transverse = -Q_applied * np.cos(a3) # negative because acting down

    Q_comp_1 = concentrated_axial_load(Q_axial, frame2.L, 1.5)
    Q_comp_2 = transverse_point_load(Q_transverse, frame2.L, 1.5)

    structure1 = Assembly('structure1', Q=0)
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.add_element(frame3)
    structure1.A_matrices()
    structure1.Q = frame2.A_matrix @ frame2.Lambda().T @ (Q_comp_1+Q_comp_2)
    structure1.set_reaction_loads()

    for node in structure1.nodes:
        print(f"{node.name} Reactions: {node.ReactionLoads}")

    # for element in structure1.elements:
    #     print(element.A_matrix)

    # print(Q_axial)
    # print(Q_transverse)
    # print(Q_comp_1)
    # print(Q_comp_2)
    # print(frame2.A_matrix @ frame2.Lambda().T @ (Q_comp_1+Q_comp_2)) # force vector in global coordinates
    # print(structure1.q())

    structure1.draw_full_deflected_frame(20, 20)
    structure1.show_structure()

def ex9():
    """ From the 2020 test - Q2 """
    a1 = np.radians(80)

    n_1 = Node('node1', 0, 0, constraint='fixed')
    n_2 = Node('node2', 3*np.cos(a1), 3*np.sin(a1), constraint='free')
    n_3 = Node('node3', 2+3*np.cos(a1), 3*np.sin(a1), T_y=1)

    frame1 = Local_Frame('frame1', E=30e9, I=6e-6, A=2e-4, L=3, node_a=n_1, node_b=n_2, alpha=80)
    frame2 = Local_Frame('frame2', E=30e9, I=6e-6, A=2e-4, L=2, node_a=n_2, node_b=n_3, alpha=0)

    Q_bit = uniformly_distributed_load(-10e3, 2)

    structure1 = Assembly('structure1', Q=0)
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.A_matrices()
    structure1.Q = frame2.A_matrix @ frame2.Lambda().T @ Q_bit
    structure1.set_reaction_loads()

    for node in structure1.nodes:
        print(f"{node.name} Reactions: {node.ReactionLoads}")

    for element in structure1.elements:
        print(element.A_matrix)

    print(structure1.q())

    structure1.draw_full_deflected_frame(5, 20)
    structure1.show_structure()

def test2021_1():
    """ From the 2021 test """
    n_1 = Node('node1', 0, 0, constraint='fixed')
    n_2 = Node('node2', 3, 0, constraint='roller-horizontal-pin')
    n_3 = Node('node3', 5, 0, constraint='free')

    frame1 = Local_Frame('frame1', E=200e9, I=1e-6, A=1e-4, L=3, node_a=n_1, node_b=n_2, alpha=0)
    frame2 = Local_Frame('frame2', E=200e9, I=1e-6, A=1e-4, L=2, node_a=n_2, node_b=n_3, alpha=0)

    structure1 = Assembly('structure1', Q=0)
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.A_matrices()

    f_1_eq = uniformly_distributed_load(40e3, frame1.L)
    Q_1_eq = frame1.A_matrix @ (frame1.Lambda().T @ f_1_eq)
    Q_2 = np.array([0, 0, 25e3, -10e3, 0])

    structure1.Q = Q_1_eq + Q_2
    structure1.set_reaction_loads()

    for node in structure1.nodes:
        print(f"{node.name} Reactions: {node.ReactionLoads}")

    # for element in structure1.elements:
    #     print(element.K_G_e()/1e6)

    structure1.draw_full_deflected_frame(10, 20)
    structure1.show_structure()

def test2021_2():
    """ From the 2021 test """
    n_1 = Node('node1', 0, 2.5, constraint='free')
    n_2 = Node('node2', 0, 0, constraint='fixed')
    n_3 = Node('node3', 2, 1, constraint='free')
    n_4 = Node('node4', 2, 0, constraint='fixed')

    L2 = np.sqrt(2 * 2 + 1.5 * 1.5)

    frame1 = Local_Frame('frame1', E=200e9, I=7.5e-6, A=9e-4, L=2.5, node_a=n_1, node_b=n_2, alpha=-90)
    frame2 = Local_Frame('frame2', E=200e9, I=7.5e-6, A=9e-4, L=L2, node_a=n_1, node_b=n_3, alpha=-36.87)
    frame3 = Local_Frame('frame3', E=200e9, I=7.5e-6, A=9e-4, L=1, node_a=n_3, node_b=n_4, alpha=-90)

    structure1 = Assembly('structure1', Q=0)
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.add_element(frame3)
    structure1.A_matrices()

    f_eq_1 = linearly_varying_load(1000 * 9.81 * 2.5 * 3, frame1.L)
    frame1.force_equivalent = f_eq_1.reshape(6,1)
    print(f_eq_1)
    structure1.Q = frame1.A_matrix @ frame1.Lambda().T @ f_eq_1
    structure1.set_reaction_loads()

    for node in structure1.nodes:
        print(f"{node.name} Reactions:\n{node.ReactionLoads}")

    # for element in structure1.elements:
    #     print(element.K_G_e()/1e6)

    # print(frame1.force_equivalent)

    print(structure1.Q)
    print(structure1.q())
    u = structure1.get_deflection_axial(frame2, 0.5 * frame2.L)
    v = structure1.get_deflection_transverse(frame2, 0.5 * frame2.L)
    deflections_XG = u * np.cos(frame2.alpha) - v * np.sin(frame2.alpha)
    deflections_YG = u * np.sin(frame2.alpha) + v * np.cos(frame2.alpha)

    # print(deflections_XG)
    # print(deflections_YG)

    # print(structure1.F_e(frame2))

    print(structure1.stress_in_element(frame2))

    # structure1.draw_full_deflected_frame(10, 20)
    # structure1.show_structure()

def test2022_1():
    """ 2022 test - Q1 """
    n_1 = Node('node1', 0, 0, constraint='fixed')
    n_2 = Node('node2', 4, 0, constraint='roller-horizontal-pin')
    n_3 = Node('node3', 4, 3, constraint='free')

    frame1 = Local_Frame('frame1', E=200e9, I=5e-6, A=2e-4, L=4, node_a=n_1, node_b=n_2, alpha=0)
    frame2 = Local_Frame('frame2', E=200e9, I=5e-6, A=2e-4, L=5, node_a=n_1, node_b=n_3, alpha=38.65)
    frame3 = Local_Frame('frame3', E=200e9, I=5e-6, A=2e-4, L=3, node_a=n_2, node_b=n_3, alpha=90)

    structure1 = Assembly('structure1', Q=0)
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.add_element(frame3)
    structure1.A_matrices()
    structure1.print_assembly_matrices()
    structure1.print_K_G_e()

    Q_1 = np.array([0, 0, 20e3, 40e3, 0])
    f_eq_1 = uniformly_distributed_load(-25e3, frame1.L)
    Q_2 = frame1.A_matrix @ frame1.Lambda().T @ uniformly_distributed_load(-25e3, frame1.L)
    frame1.force_equivalent = f_eq_1.reshape(6,1)
    structure1.Q = Q_1 + Q_2
    print(f"f1_eq: {uniformly_distributed_load(-25e3, frame1.L)}\n")
    print(f"q vector: {structure1.q()*1e3}\n")
    structure1.print_global_element_forces()
    print(structure1.Q)
    structure1.set_reaction_loads()
    structure1.print_reaction_loads()
    # print(f"Maximum magnitude of bending moment within element 2: {structure1.get_max_deflection_transverse(frame2, np.linspace(0, frame2.L, 100)[0])}")
    # print(f"Location: {structure1.get_max_deflection_transverse(frame2, np.linspace(0, frame2.L, 100)[1])}")

    # print(f"Horizontal deflection at mid-span of element 1: {1e3 * structure1.get_deflection_axial(frame1, 0.5 * frame1.L)}\n")


    structure1.draw_full_deflected_frame(20, 20)
    structure1.show_structure()
    
def test2023_1():
    
    """ 2023 test - Q1 """
    n_1 = Node('node1', 0, 0, constraint='free')
    n_2 = Node('node2', 3, 0, constraint='roller-vertical')
    n_3 = Node('node3', -3, -4, constraint='pin')
    n_4 = Node('node4', 3, -4, constraint='roller-vertical')

    frame1 = Local_Frame('frame1', E=200e9, I=6e-6, A=2e-4, L=3, node_a=n_1, node_b=n_2, alpha=0)
    frame2 = Local_Frame('frame2', E=200e9, I=6e-6, A=2e-4, L=5, node_a=n_3, node_b=n_1, alpha=53.13)
    frame3 = Local_Frame('frame3', E=200e9, I=6e-6, A=2e-4, L=5, node_a=n_1, node_b=n_4, alpha=-53.13)
    frame4 = Local_Frame('frame4', E=200e9, I=6e-6, A=2e-4, L=6, node_a=n_3, node_b=n_4, alpha=0)

    structure1 = Assembly('structure1', Q=0)
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.add_element(frame3)
    structure1.add_element(frame4)
    structure1.A_matrices()
    structure1.print_assembly_matrices()
    structure1.print_K_G_e()

    Q_1 = uniformly_distributed_load(-40e3, frame4.L)
    print(Q_1)
    structure1.Q = frame4.A_matrix @ frame4.Lambda().T @ Q_1
    print(structure1.Q)
    print(f"f1_eq: {uniformly_distributed_load(-25e3, frame1.L)}\n")
    print(f"q vector: {structure1.q()*1e3}\n")
    structure1.print_global_element_forces()
    structure1.set_reaction_loads()
    structure1.print_reaction_loads()
    
    print(f"Maximum magnitude of bending moment within element 2: {1e3 * structure1.get_max_deflection_transverse(frame2, np.linspace(0, frame2.L, 100))[0]}")
    print(f"Horizontal deflection at mid-span of element 1: {1e3 * structure1.get_deflection_axial(frame1, 0.5 * frame1.L)}\n")
    
    structure1.draw_full_deflected_frame(10, 20)
    structure1.show_structure()

def test2023_2():
    """ 2023 test - Q2 """
    n_1 = Node('node1', 0, 0, constraint='fixed')
    n_2 = Node('node2', 3.46, -2, constraint='free')
    n_3 = Node('node3', 3.46, -5, constraint='pin')
    n_4 = Node('node4', -0.54, -5, constraint='fixed')

    frame1 = Local_Frame('frame1', E=200e9, I=1e-4, A=2e-4, L=4, node_a=n_1, node_b=n_2, alpha=-30)
    frame2 = Local_Frame('frame2', E=200e9, I=1e-4, A=2e-4, L=3, node_a=n_2, node_b=n_3, alpha=-90)
    frame3 = Local_Frame('frame3', E=200e9, I=1e-4, A=2e-4, L=4, node_a=n_4, node_b=n_3, alpha=0)

    structure1 = Assembly('structure1', Q=np.array([0,0,0,0]))
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.add_element(frame3)
    structure1.A_matrices()
    
    f_eq_3 = uniformly_distributed_load(117720, frame3.L)
    frame3.force_equivalent = f_eq_3.reshape(6,1)
    f_eq_2 = linearly_varying_load(-117720, frame2.L)
    frame2.force_equivalent = f_eq_2.reshape(6,1)

    print(f"F_eq_1:\n{frame1.force_equivalent}")    
    print(f"F_eq_2:\n{frame2.force_equivalent}")
    print(f"F_eq_3:\n{frame3.force_equivalent}")

    print(frame3.Lambda())
    
    Q_1 = frame3.A_matrix @ frame3.Lambda().T @ f_eq_3
    Q_2 = frame2.A_matrix @ frame2.Lambda().T @ f_eq_2
    
    # print(f"f_eq_2: {f_eq_2}\n")
    # print(f"f_eq_3: {f_eq_3}\n")
    # print(f"Q: {Q_1+Q_2}\n")
    
    structure1.Q = Q_1 + Q_2
    
    print(f"F_2:\n{structure1.F_e(frame2).reshape(6,1)}")
    print(f"F_3:\n{structure1.F_e(frame3).reshape(6,1)}")

    # print(f"q: {structure1.q()*1e3}n")
    
    # structure1.print_assembly_matrices()
    # structure1.print_K_G_e()

    structure1.set_reaction_loads()
    structure1.print_reaction_loads()

    # print(structure1.F_e(frame1))

    structure1.draw_full_deflected_frame(200, 20)
    structure1.show_structure()

if __name__ == "__main__":
    test2023_1()