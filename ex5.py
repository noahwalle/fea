from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
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
    # structure1.draw_structure_deflected(deflection_scale=100)
    structure1.draw_full_deflected_frame(100, 20)
    structure1.show_structure()

if __name__ == "__main__":
    main()