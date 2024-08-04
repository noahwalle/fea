import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name, x, y, T_x=0, T_y=0, T_z=0, R_x=0, R_y=0, R_z=0, z=0):
        """ Initialise with its coordinates in x, y, z
        Has 6 potential degrees of freedom:
        - Translation in x, y, z
        - Rotation about x, y, z 
        By default, all DOF are fixed """
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.DOF = [T_x, T_y, T_z, R_x, R_y, R_z]
    
    def __repr__(self):
        return f"{self.name}: ({self.x}, {self.y})"

class Local_Bar:
    def __init__(self, name, E, A, L, node_a: Node, node_b: Node, alpha, A_matrix=None):
        """ Class for Local Bar Element
        Assume:
        Young's Modulus taken in GPa
        Area taken in mm^2
        Length taken in m
        alpha taken in degrees"""
        self.name = name
        self.E = E
        self.A = A
        self.L = L
        self.nodes = [node_a, node_b]
        self.alpha = np.radians(alpha)
        self.A_matrix = A_matrix

    def __repr__(self):
        return f"{self.name}, E = {self.E/1e9} GPa, A = {round(self.A/1e-6, 2)} mm^2, L = {self.L} m, Node A: {self.nodes[0]}, Node B: {self.nodes[1]}, alpha = {self.alpha} degrees"
    
    def K_e(self):
        """Element stiffness matrix in local co-ordinates"""
        return self.E * self.A / self.L * np.array([[1, -1], [-1, 1]])

    def Lambda(self):
        """ Transformation matrix for a bar element, denoted by capital lambda, Λ """
        c = np.cos(self.alpha)
        s = np.sin(self.alpha)
        return np.array([[c, s, 0, 0], [0, 0, c, s]])

    def K_e_hat(self):
        """ Element stiffness matrix in global co-ordinates """
        return self.Lambda().T @ self.K_e() @ self.Lambda()

    def K_G_e(self):
        """ Element's contribution to global stiffness matrix """
        return self.A_matrix @ self.K_e_hat() @ self.A_matrix.T

class Local_Frame:
    """ Local frame class
    @params:
    name: element name
    E: Young's Modulus
    I: second moment of area
    A: cross-sectional area
    L: length
    node_a: first node
    node_b: second node
    alpha: element angle wrt xG
    A_matrix: element assembly matrix
    """
    def __init__(self, name, E, I, A, L, node_a: Node, node_b: Node, alpha, A_matrix=None):
        self.name = name
        self.E = E
        self.A = A
        self.I = I
        self.L = L
        self.nodes = [node_a, node_b]
        self.alpha = np.radians(alpha)
        self.A_matrix = A_matrix

    def __repr__(self):
        return f"{self.name}, E = {self.E/1e9} GPa, A = {round(self.A/1e-6, 2)} mm^2, I = {self.I} m^4, L = {self.L} m, Node A: {self.nodes[0]}, Node B: {self.nodes[1]}, alpha = {self.alpha} degrees"

    def K_e(self):
        """ Frame element stiffness matrix in local coordinates """
        B = self.A * self.L ** 2 / self.I
        return self.E * self.I / self.L ** 3 * np.array([[B,     0,          0,              -B,     0,          0],
                                                         [0,     12,         6*self.L,       0,      -12,        6*self.L],
                                                         [0,     6*self.L,   4*self.L**2,    0,      -6*self.L,  2*self.L**2],
                                                         [-B,    0,          0,              B,      0,          0],
                                                         [0,     -12,        -6*self.L,      0,      12,         -6*self.L],
                                                         [0,     6*self.L,   2*self.L**2,    0,      -6*self.L,  4*self.L**2]])
    
    def Lambda(self):
        """ Frame element transformation matrix, denoted Λ"""
        c = np.cos(self.alpha)
        s = np.sin(self.alpha)
        λ = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
        zeros = np.zeros((3,3))
        return np.hstack((np.vstack((λ, zeros)), np.vstack((zeros, λ))))

    def K_e_hat(self):
        """ Frame element stiffness matrix in global coordinates """
        return self.Lambda().T @ self.K_e() @ self.Lambda()
    
    def K_G_e(self):
        """ Element contribution to global stiffness matrix """
        return self.A_matrix @ self.K_e_hat() @ self.A_matrix.T

class Assembly:
    """ Assembly Class
    Initialise empty with applied force array, then add elements """
    def __init__(self, name, Q):
        self.name = name
        self.elements = []
        self.nodes = []
        self.Q = Q
        self.ax = plt.subplots()[1]
    
    def __repr__(self):
        if len(self.elements) > 0:
            element_list = [self.elements[i].name for i in range(len(self.elements))]
        else:
            element_list = ""
        return f"{self.name}\nElements: {element_list}"

    def add_element(self, element: Local_Bar | Local_Frame):
        """ Add an element to the structure """
        self.elements.append(element)
        if (not(element.nodes[0] in self.nodes)):
            self.nodes.append(element.nodes[0])
        if (not(element.nodes[1] in self.nodes)):
            self.nodes.append(element.nodes[1])
        self.nodes.sort(key = lambda s: s.name)
        self.elements.sort(key = lambda s: s.name)
    
    def dof_count(self):
        dof_count = list()

        # Work out the total number of possible non-zero deflections in the structure
        for node in self.nodes:
            for i in range(len(node.DOF)):
                if (node.DOF[i] and i < 3):
                    dof_count.append("translation")
                if (node.DOF[i] and i >= 3):
                    dof_count.append("rotation")
        return dof_count

    def K_G(self):
        """ Global stiffness matrix in global coordinates """
        K_G = 0
        for element in self.elements:
            K_G += element.K_G_e()
        return K_G

    def q(self):
        """ System deformations """
        return np.linalg.solve(self.K_G(), self.Q)
    
    def A_matrices(self):
        """ Generates the assembly matrices for all elements of a structure using DOFs """
        q_count = 0
        d_count = 0 # makes sure you go through all the entries for each bar

        for element in self.elements:
            if isinstance(element, Local_Bar):
                A_matrix = np.zeros((len(self.dof_count()), 4))
                # Work out the element's contributions to each deflection
                for node in element.nodes:
                    for i in [0, 1]:
                        A_matrix[q_count][d_count] = node.DOF[i]
                        d_count += 1
                        d_count %= 4
                        if (node.DOF[i]):
                            q_count += 1
                            q_count %= len(self.dof_count())
                element.A_matrix = A_matrix
            elif isinstance(element, Local_Frame):
                A_matrix = np.zeros((len(self.dof_count()), 6))
                # Work out the element's contributions to each deflection
                for node in element.nodes:
                    for i in [0, 1, 5]:
                        A_matrix[q_count][d_count] = node.DOF[i]
                        d_count += 1
                        d_count %= 6
                        if (node.DOF[i]):
                            q_count += 1
                            q_count %= len(self.dof_count())
                element.A_matrix = A_matrix
                
    def F_e(self, element: Local_Bar):
        """ Element nodal forces in global coordinates """
        return element.K_e_hat() @ element.A_matrix.T @ self.q()
    
    def d_e(self, element: Local_Bar):
        """ Local defromations in local coordinates """
        return element.Lambda() @ element.A_matrix.T @ self.q()
    
    def f_e(self, element: Local_Bar):
        """ Element nodal forces in local element coordinates """
        return element.K_e() @ self.d_e(element)

    def draw_element(self, element: Local_Bar | Local_Frame):
        xs = [element.nodes[0].x, element.nodes[1].x]
        ys = [element.nodes[0].y, element.nodes[1].y]
        self.ax.plot(xs, ys, 'b')

    def draw_structure_initial(self):
        for element in self.elements:
            self.draw_element(element)

    def D_e(self, element: Local_Bar | Local_Frame):
        return element.A_matrix.T @ self.q()

    def draw_deflected_element(self, element: Local_Bar | Local_Frame, deflection_scale: int):
        deflections = self.D_e(element) * deflection_scale
        if isinstance(element, Local_Bar):
            # deflections matrix is in following format for bars
            #      _    _
            #     | q_x1 | index [0]
            # q = | q_y1 | index [1]
            #     | q_x2 | index [2]
            #     | q_y2 | index [3]
            #      -    -
            xs = [element.nodes[0].x + deflections[0], element.nodes[1].x + deflections[2]]
            ys = [element.nodes[0].y + deflections[1], element.nodes[1].y + deflections[3]]
        elif isinstance(element, Local_Frame):
            # deflections matrix is in following format for Frames
            #      _    _
            #     | q_x1 | index [0]
            #     | q_y1 | index [1]
            # q = | r_z1 | index [2]
            #     | q_x2 | index [3]
            #     | q_y2 | index [4]
            #     | r_z1 | index [5]
            #      -    -
            xs = [element.nodes[0].x + deflections[0], element.nodes[1].x + deflections[3]]
            ys = [element.nodes[0].y + deflections[1], element.nodes[1].y + deflections[4]]
        self.ax.plot(xs, ys, 'r--')

    def draw_structure_deflected(self, deflection_scale):
        for element in self.elements:
            self.draw_deflected_element(element, deflection_scale)
    
    def show_structure(self):
        self.ax.grid()
        self.ax.set_aspect("equal")
        plt.show()