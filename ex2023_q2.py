from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
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
    main()