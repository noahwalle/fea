from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
    """ Example from p49 of ENME302 course reader """
    Ae = np.pi * (100e-3) ** 2 / 4

    n_1 = Node("node1", 0, 0)
    n_2 = Node("node2", 10, 0, T_x=1, T_y=1)
    n_3 = Node("node3", 0, -10)

    bar1 = Local_Bar("bar1", E=200e9, A=Ae, L=10, node_a=n_1, node_b=n_2, alpha=0)
    bar2 = Local_Bar("bar2", E=200e9, A=Ae, L=14.1, node_a=n_2, node_b=n_3, alpha=45)

    structure1 = Assembly("structure1", Q=np.array([0, 100000]))
    structure1.add_element(bar1)
    structure1.add_element(bar2)
    structure1.A_matrices()

    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=100)
    structure1.show_structure()

if __name__ == "__main__":
    main()