from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main1():
    """ Example from p49 of ENME302 course reader """
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

def lab2():
    """ Example from ENME302 Lab 2 """
    Ae = np.pi * (100e-3)**2 / 4

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

def main3():
    """ Example from p58 of ENME302 course reader """
    n_1 = Node("node1", 0, 0)
    n_2 = Node("node2", 5, 0, T_x=1)
    n_3 = Node("node3", 2.5, 5 * np.sin(np.radians(60)), T_x=1, T_y=1)

    Ae = np.pi / 4 * (0.1 ** 2 - 0.08 ** 2)

    bar1 = Local_Bar("bar1", E=70e9, A=Ae, L=5, node_a=n_1, node_b=n_3, alpha=60)
    bar2 = Local_Bar("bar2", E=70e9, A=Ae, L=5, node_a=n_1, node_b=n_2, alpha=0)
    bar3 = Local_Bar("bar3", E=70e9, A=Ae, L=5, node_a=n_3, node_b=n_2, alpha=300)

    structure1 = Assembly("structure1", Q=np.array([500e3, 0, 0]))
    structure1.add_element(bar1)
    structure1.add_element(bar2)
    structure1.add_element(bar3)
    structure1.A_matrices()

    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=30)
    structure1.show_structure()

def main4():
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

    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=100)
    structure1.show_structure()

def lab3():
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

    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=50)
    structure1.show_structure()

def main5():
    """ Example from p97 of ENME302 course reader """
    n_1 = Node("node1", 0, 0, R_z=1)
    n_2 = Node("node2", 4, 0, T_x=1, T_y=1, R_z=1)
    n_3 = Node("node3", 8, -0)
    n_4 = Node("node4", 4, -4)

    frame1 = Local_Frame("frame1", E=200e9, I=5e-4, A=1e-5, L=4, node_a=n_1, node_b=n_2, alpha=0)
    frame2 = Local_Frame("frame2", E=200e9, I=5e-4, A=1e-5, L=4, node_a=n_2, node_b=n_3, alpha=0)
    frame3 = Local_Frame("frame3", E=200e9, I=5e-4, A=1e-5, L=4, node_a=n_2, node_b=n_4, alpha=270)

    structure1 = Assembly("structure1", Q=np.array([0, 0, 100000, 0]))
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.add_element(frame3)
    structure1.A_matrices()

    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=100)
    structure1.show_structure()

if __name__ == "__main__":
    main5()
    # exec(open('fea_main.py').read())