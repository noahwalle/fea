from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
    """ 2021 test - Q1 """
    n_1 = Node('node1', 0, 0, constraint='fixed')
    n_2 = Node('node2', 3, 0, constraint='roller-horizontal-pin')
    n_3 = Node('node3', 5, 0, constraint='free')

    frame1 = Local_Frame('frame1', E=200e9, I=1e-6, A=1e-4, L=3, node_a=n_1, node_b=n_2, alpha=0)
    frame2 = Local_Frame('frame2', E=200e9, I=1e-6, A=1e-4, L=2, node_a=n_2, node_b=n_3, alpha=0)

    structure1 = Assembly('structure1', Q=0)
    structure1.add_element(frame1)
    structure1.add_element(frame2)
    structure1.A_matrices()

    f_1_eq = uniformly_distributed_load(40e3, frame1.L)
    Q_1_eq = frame1.A_matrix @ (frame1.Lambda().T @ f_1_eq)
    Q_2 = np.array([0, 0, 25e3, -10e3, 0])

    structure1.Q = Q_1_eq + Q_2
    structure1.set_reaction_loads()

    for node in structure1.nodes:
        print(f"{node.name} Reactions: {node.ReactionLoads}")

    # for element in structure1.elements:
    #     print(element.K_G_e()/1e6)

    structure1.draw_full_deflected_frame(10, 20)
    structure1.show_structure()

if __name__ == "__main__":
    main()