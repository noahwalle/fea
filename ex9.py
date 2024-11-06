from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
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

if __name__ == "__main__":
    main()