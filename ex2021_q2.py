from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
    """ 2021 test - Q2 """
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

    for element in structure1.elements:
        print(element.K_G_e()/1e6)

    print(frame1.force_equivalent)

    print(structure1.Q)
    print(structure1.q())
    u = structure1.get_deflection_axial(frame2, 0.5 * frame2.L)
    v = structure1.get_deflection_transverse(frame2, 0.5 * frame2.L)
    deflections_XG = u * np.cos(frame2.alpha) - v * np.sin(frame2.alpha)
    deflections_YG = u * np.sin(frame2.alpha) + v * np.cos(frame2.alpha)

    print(deflections_XG)
    print(deflections_YG)

    print(structure1.F_e(frame2))

    print(structure1.axial_stress_in_element(frame2))

    structure1.draw_full_deflected_frame(10, 20)
    structure1.show_structure()

if __name__ == "__main__":
    main()