from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
    """ Example from p58 of ENME302 course reader """
    n_1 = Node("node1", 0, 0)
    n_2 = Node("node2", 2.5, 5 * np.sin(np.radians(60)), T_x=1, T_y=1)
    n_3 = Node("node3", 5, 0, T_x=1)

    Ae = np.pi / 4 * (0.1 ** 2 - 0.08 ** 2)

    bar1 = Local_Bar("bar1", E=70e9, A=Ae, L=5, node_a=n_1, node_b=n_2, alpha=60)
    bar2 = Local_Bar("bar2", E=70e9, A=Ae, L=5, node_a=n_1, node_b=n_3, alpha=0)
    bar3 = Local_Bar("bar3", E=70e9, A=Ae, L=5, node_a=n_2, node_b=n_3, alpha=-60)

    structure1 = Assembly("structure1", Q=np.array([500e3, 0, 0]))
    structure1.add_element(bar1)
    structure1.add_element(bar2)
    structure1.add_element(bar3)
    structure1.A_matrices()

    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=30)
    structure1.show_structure()

if __name__ == "__main__":
    main()