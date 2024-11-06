from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
    """ 2024 test - Q1 """
    n_1 = Node('node1', 0, 0, constraint='fixed')
    n_2 = Node('node2', 5, 0, constraint='free')
    n_3 = Node('node3', 3.2, -2.4, constraint='roller-horizontal-pin')

    frame1 = Local_Frame('frame1', E=200e9, I=5e-6, A=3e-4, L=5, node_a=n_1, node_b=n_2, alpha=0)
    frame2 = Local_Frame('frame2', E=200e9, I=5e-6, A=3e-4, L=4, node_a=n_1, node_b=n_3, alpha=-36.9)
    frame3 = Local_Frame('frame3', E=200e9, I=5e-6, A=3e-4, L=3, node_a=n_3, node_b=n_2, alpha=53.1)

    structure1 = Assembly('structure1', Q=np.array([0,0,0,0,0]))
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.add_element(frame3)
    structure1.A_matrices()

    structure1.print_assembly_matrices()

    f_eq_1 = uniformly_distributed_load(-30e3, frame1.L)
    frame1.force_equivalent = f_eq_1.reshape(6,1)
    
    print(frame1.force_equivalent)

    f_eq = np.array([15e3, -20e3, 0, 0, 0])
    
    structure1.Q = frame1.A_matrix @ frame1.Lambda().T @ f_eq_1 + f_eq
    
    print(structure1.Q)
    print(f"q: {structure1.q()*1e3}\n")

    structure1.set_reaction_loads()
    structure1.print_reaction_loads()

    print(structure1.F_e(frame2).reshape(6,1))

    structure1.draw_full_deflected_frame(20, 20)
    structure1.show_structure()
    
    print(structure1.strain_in_element(frame3)*1e3)
    print(structure1.d_e(frame2)*1e3)
    
    u = structure1.get_deflection_axial(frame2, 0.75 * frame2.L)
    v = structure1.get_deflection_transverse(frame2, 0.75 * frame2.L)
    deflections_XG = u * np.cos(frame2.alpha) - v * np.sin(frame2.alpha)
    deflections_YG = u * np.sin(frame2.alpha) + v * np.cos(frame2.alpha)

    print(f"Deflection in global X: {deflections_XG*1e3}\n")
    print(f"Deflection in global Y: {deflections_YG*1e3}")

if __name__ == "__main__":
    main()