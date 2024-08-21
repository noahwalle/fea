import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name, x, y, T_x=0, T_y=0, R_z=0, constraint: str=None):
        """ Initialise with its coordinates in x, y, z
        Has 3 potential degrees of freedom:
        - Translation in x, y
        - Rotation about z 
        By default, all DOF are fixed """
        self.name = name
        self.x = x
        self.y = y
        if constraint == 'fixed':
            self.DOF = [0, 0, 0]
        elif constraint == 'free':
            self.DOF = [1, 1, 1]
        elif constraint == 'pin':
            self.DOF = [0, 0, 1]
        elif constraint == 'roller-vertical':
            self.DOF = [0, 1, 0]
        elif constraint == 'roller-horizontal':
            self.DOF = [1, 0, 0]
        elif constraint == 'roller-vertical-pin':
            self.DOF = [0, 1, 1]
        elif constraint == 'roller-horizontal-pin':
            self.DOF = [1, 0, 1]
        else:
            self.DOF = [T_x, T_y, R_z]
        self.constraint = constraint
        self.ReactionLoads = None
    
    def __repr__(self):
        return f"{self.name}: ({self.x}, {self.y})"

class Local_Bar:
    def __init__(self, name, E, A, L, node_a: Node, node_b: Node, alpha, A_matrix=None):
        """ Class for local bar element
        Material properties
        Young's Modulus, E: [GPa]
        Area, A: [m^2]
        Length, L: [m]
        Angle, alpha: [degrees] """
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
    """ Class for local frame element
    Material properties
    Young's Modulus, E: [GPa]
    Second moment of area, I: [m^4]
    Cross-sectional area, A: [m^2]
    Length, L: [m]
    Angle, alpha: [degrees] """
    def __init__(self, name, E, I, A, L, node_a: Node, node_b: Node, alpha, A_matrix=None):
        self.name = name
        self.E = E
        self.A = A
        self.I = I
        self.L = L
        self.nodes = [node_a, node_b]
        self.alpha = np.radians(alpha)
        self.A_matrix = A_matrix
        self.force_equivalent = None
        self.global_forces = None

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
    
    # Axial shape functions
    def phi_1(self, x):
        return 1 - x / self.L
    
    def phi_2(self, x):
        return x / self.L

    # Transverse shape functions
    def N1(self, x):
        return 1 - 3 * x ** 2 / self.L ** 2 + 2 * x ** 3 / self.L ** 3
    
    def N2(self, x):
        return x ** 3 / self.L ** 2 - 2 * x ** 2 / self.L + x

    def N3(self, x):
        return 3 * x ** 2 / self.L ** 2 - 2 * x ** 3 / self.L ** 3

    def N4(self, x):
        return x ** 3 / self.L ** 2 - x ** 2 / self.L        

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

    def reassign_dof_vals(self):
        q_counter = 0
        for node in self.nodes:
            for i in range(len(node.DOF)):
                if node.DOF[i] > 0:
                    node.DOF[i] += q_counter
                    q_counter += 1

    def dof_count(self):
        dof_count = []
        for node in self.nodes:
            for i in range(len(node.DOF)):
                if (node.DOF[i] and i < 2):
                    dof_count.append("t")
                elif (node.DOF[i] and i == 2):
                    dof_count.append("r")
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
        self.reassign_dof_vals()
        """ Generates the assembly matrices for all elements of a structure using DOFs """
        d_counter = 0 # makes sure you go through all the possible entries for each element

        for element in self.elements:
            element.force_equivalent = np.zeros((6,1), dtype=float)
            if isinstance(element, Local_Bar):
                A_matrix = np.zeros((len(self.dof_count()), 4))
                # Work out the element's contributions to each deflection
                for node in element.nodes:
                    for dof in node.DOF[0:2]:
                        if dof:
                            A_matrix[dof-1][d_counter] = 1
                        d_counter += 1
                        d_counter %= 4
                element.A_matrix = A_matrix
            elif isinstance(element, Local_Frame):
                A_matrix = np.zeros((len(self.dof_count()), 6))
                # Work out the element's contributions to each deflection
                for node in element.nodes:
                    for dof in node.DOF:
                        if dof:
                            A_matrix[dof-1][d_counter] = 1
                        d_counter += 1
                        d_counter %= 6
                element.A_matrix = A_matrix
                
    def F_e(self, element: Local_Bar | Local_Frame):
        """ Element nodal forces in global coordinates """
        return element.K_e_hat() @ element.A_matrix.T @ self.q()
    
    def d_e(self, element: Local_Bar | Local_Frame):
        """ Local defromations in local coordinates """
        return element.Lambda() @ element.A_matrix.T @ self.q()
    
    def f_e(self, element: Local_Bar | Local_Frame):
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
    
    def draw_full_deflected_frame(self, deflection_scale, n_points):
        for element in self.elements:
            x_e = np.linspace(0, element.L, n_points)
            u = element.phi_1(x_e) * self.d_e(element)[0] + element.phi_2(x_e) * self.d_e(element)[3]
            v = element.N1(x_e) * self.d_e(element)[1] + element.N2(x_e) * self.d_e(element)[2] + element.N3(x_e) * self.d_e(element)[4] + element.N4(x_e) * self.d_e(element)[5]
            deflections_XG = u * np.cos(element.alpha) - v * np.sin(element.alpha)
            deflections_YG = u * np.sin(element.alpha) + v * np.cos(element.alpha)
            undeflected_baseline_XG = np.linspace(element.nodes[0].x, element.nodes[1].x, n_points)
            undeflected_baseline_YG = np.linspace(element.nodes[0].y, element.nodes[1].y, n_points)
            deflected_XG = undeflected_baseline_XG + deflection_scale * deflections_XG
            deflected_YG = undeflected_baseline_YG + deflection_scale * deflections_YG

            self.ax.plot(undeflected_baseline_XG, undeflected_baseline_YG, 'b.-')
            self.ax.plot(deflected_XG, deflected_YG, 'r.-')
    
    def set_reaction_loads(self):
        for element in self.elements:
            if element.nodes[0].constraint != "free":
                if element.nodes[0].ReactionLoads is None:
                    element.nodes[0].ReactionLoads = np.zeros((3,1))
                element.nodes[0].ReactionLoads += self.F_e(element)[:3].reshape(3,1) - (element.Lambda().T @ element.force_equivalent)[:3]
            if element.nodes[1].constraint != "free":
                if element.nodes[1].ReactionLoads is None:
                    element.nodes[1].ReactionLoads = np.zeros((3,1))
                element.nodes[1].ReactionLoads += self.F_e(element)[3:].reshape(3,1) - (element.Lambda().T @ element.force_equivalent)[3:]
            
    def print_assembly_matrices(self):
        for element in self.elements:
            print(f"{element.name} A:\n{element.A_matrix}\n")
            
    def print_K_G_e(self):
        for element in self.elements:
            print(f"{element.name} KGe:\n{element.K_G_e()/1e6}\n")
    
    def print_global_element_forces(self):
        for element in self.elements:
            print(f"{element.name} F_e:\n{self.F_e(element)}\n")
    
    def print_reaction_loads(self):
        for node in self.nodes:
            print(f"{node.name}:\n{node.ReactionLoads}")
            
    def get_deflection_axial(self, element: Local_Frame, x_e):
        return element.phi_1(x_e) * self.d_e(element)[0] + element.phi_2(x_e) * self.d_e(element)[3]
        
    def get_deflection_transverse(self, element: Local_Frame, x_e):
        return element.N1(x_e) * self.d_e(element)[1] + element.N2(x_e) * self.d_e(element)[2] + element.N3(x_e) * self.d_e(element)[4] + element.N4(x_e) * self.d_e(element)[5]
    
    def get_max_deflection_axial(self, element: Local_Frame, x_e):
        return np.max(np.abs(element.phi_1(x_e) * self.d_e(element)[0] + element.phi_2(x_e) * self.d_e(element)[3]))
        
    def get_max_deflection_transverse(self, element: Local_Frame, x_e):
        v_max = np.max(np.abs(element.N1(x_e) * self.d_e(element)[1] + element.N2(x_e) * self.d_e(element)[2] + element.N3(x_e) * self.d_e(element)[4] + element.N4(x_e) * self.d_e(element)[5]))
        v_max_index = np.where(v_max)
        return v_max, v_max_index
    
    def strain_in_element(self, element: Local_Frame):
        epsilon = (self.d_e(element)[3] - self.d_e(element)[0]) / element.L
        return epsilon

    def stress_in_element(self, element: Local_Frame):
        sigma = element.E * self.strain_in_element(element)
        return sigma

def uniformly_distributed_load(w, L):
    """ Equivalent nodal loading definition for a UDL
        Applied along the length of a frame element
        Parameters:
        w: Load intensity [N]
        L: element length [m] 
    """
    return np.array([0, w*L/2, w*L**2/12, 0, w*L/2, -w*L**2/12])

def linearly_varying_load(w, L):
    """ Equivalent nodal loading definition for a LVL
        Applied along the length of a frame element
        Parameters:
        w: Load intensity [N]
        L: element length [m] 
    """
    return np.array([0, 3*w*L/20, w*L**2/30, 0, 7*w*L/20, -w*L**2/20])

def transverse_point_load(w, L, a):
    """ Equivalent nodal loading definition for a TPL
        Applied along the length of a frame element
        Parameters:
        w: Load intensity [N]
        L: element length [m]
        a: Load applied this distance from node 1 [m]
    """
    return w * np.array([0, 1-3*a**2/L**2+2*a**3/L**3, a**3/L**2-2*a**2/L+a, 0, 3*a**2/L**2-2*a**3/L**3, a**3/L**2-a**2/L])

def mid_span_point_load(w, L, a):
    """ Equivalent nodal loading definition for a TPL, where a = L/2
        Applied along the length of a frame element
        Parameters:
        w: Load intensity [N]
        L: element length [m]
        a: Load applied halfway along element [m]
    """
    return w * np.array([0, w/2, w*L/8, 0, w/2, -w*L/8])
    # return transverse_point_load(w, L, a/2)

def distributed_axial_load(p, L):
    """ Equivalent nodal loading definition for a DAL
        Applied along the length of a frame element
        Parameters:
        p: Load intensity [N]
        L: element length [m]
    """
    return p * np.array([L/2, 0, 0, L/2, 0, 0])

def concentrated_axial_load(p, L, a):
    """ Equivalent nodal loading definition for a CPL
        Applied at a point along a frame element
        Parameters:
        p: Load intensity [N]
        L: element length [m]
        a: Load applied this distance from node 1 [m]
    """
    return p * np.array([1-a/L, 0, 0, a/L, 0, 0])