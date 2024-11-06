from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
    """ 2024 test - Q2 """
    n_1 = Node('node1', 0, 0, constraint='free')
    n_2 = Node('node2', 0, -2.5, constraint='fixed')
    n_3 = Node('node3', 3, -0.5, constraint='roller-vertical')

    L_2 = np.sqrt(3**2 + 0.5 ** 2)
    alpha_2 = -np.arctan(0.5/3)

    frame1 = Local_Frame('frame1', E=200e9, I=5e-6, A=3e-4, L=2.5, node_a=n_1, node_b=n_2, alpha=-90)
    frame2 = Local_Frame('frame2', E=200e9, I=5e-6, A=3e-4, L=L_2, node_a=n_1, node_b=n_3, alpha=np.degrees(alpha_2)) # have to put angle in degrees

    structure1 = Assembly('structure1', Q=np.array([0,0,0,0]))
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.A_matrices()
    structure1.print_assembly_matrices()

    load = -4e3
    f_x = load * np.cos(alpha_2)
    f_y = load * np.sin(alpha_2)
    f_eq_1 = uniformly_distributed_load(f_x, frame2.L)
    f_eq_2 = distributed_axial_load(f_y, frame2.L)
    
    print(f"f_eq_1:\n{f_eq_1.reshape(6,1)}")    
    print(f"f_eq_2:\n{f_eq_2.reshape(6,1)}")
    
    frame2.force_equivalent = (f_eq_1 + f_eq_2).reshape(6,1)
    structure1.Q = frame2.A_matrix @ frame2.Lambda().T @ f_eq_1 + frame2.A_matrix @ frame2.Lambda().T @ f_eq_2
    
    structure1.set_reaction_loads()
    structure1.print_reaction_loads()
    structure1.draw_full_deflected_frame(25, 20)
    structure1.show_structure()
    print(structure1.F_e(frame1))
    print(f"q vector:{structure1.q()*1e3}")

if __name__ == "__main__":
    main()