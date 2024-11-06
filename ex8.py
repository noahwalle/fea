from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
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

if __name__ == "__main__":
    main()