from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
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

if __name__ == "__main__":
    main()