from fea import *
np.set_printoptions(linewidth=200, suppress=True)

def main():
    """ Example from ENME302 Lab 2 """
    n_1 = Node("node1", 0, 0)
    n_2 = Node("node2", 1.1, 0, T_x=1, T_y=1)
    n_3 = Node("node3", 1.1 + np.cos(0.8), np.sin(0.8))

    bar1 = Local_Bar("bar1", E=200e9, A=400e-6, L=1.1, node_a=n_1, node_b=n_2, alpha=0)
    bar2 = Local_Bar("bar2", E=200e9, A=600e-6, L=0.8, node_a=n_2, node_b=n_3, alpha=55)

    structure1 = Assembly("structure1", Q=np.array([0, -20000]))
    structure1.add_element(bar1)
    structure1.add_element(bar2)
    structure1.A_matrices()

    structure1.draw_structure_initial()
    structure1.draw_structure_deflected(deflection_scale=100)
    structure1.show_structure()

if __name__ == "__main__":
    main()