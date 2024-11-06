from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
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

if __name__ == "__main__":
    main()