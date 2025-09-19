import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def bloch_vector(qubit_state):
    """
    Converts a qubit state vector to its corresponding Bloch sphere coordinates.
    
    Args:
        qubit_state (np.ndarray): A 2x1 complex numpy array representing the qubit state.
        
    Returns:
        np.ndarray: A 3x1 numpy array of the (x, y, z) Bloch sphere coordinates.
    """
    if qubit_state.shape != (2, 1):
        raise ValueError("The qubit state vector must be a 2x1 array.")
        
    alpha = qubit_state[0, 0]
    beta = qubit_state[1, 0]
    
    # Calculate Bloch sphere coordinates
    x = 2 * np.real(np.conj(alpha) * beta)
    y = 2 * np.imag(np.conj(alpha) * beta)
    z = np.real(np.abs(alpha)**2 - np.abs(beta)**2)
    
    return np.array([x, y, z])

def plot_bloch_sphere(bloch_coords, title="Bloch Sphere"):
    """
    Plots the Bloch sphere with a given state vector.
    
    Args:
        bloch_coords (np.ndarray): A 3x1 numpy array of the (x, y, z) Bloch sphere coordinates.
        title (str): The title of the plot.
    """
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title, fontsize=16)
    
    # Draw the Bloch sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x, y, z, color='b', alpha=0.1)
    
    # Add axes and labels
    ax.plot([-1, 1], [0, 0], [0, 0], 'k--')
    ax.plot([0, 0], [-1, 1], [0, 0], 'k--')
    ax.plot([0, 0], [0, 0], [-1, 1], 'k--')
    
    ax.text(0, 0, 1.1, "|0⟩", fontsize=12)
    ax.text(0, 0, -1.2, "|1⟩", fontsize=12)
    ax.text(1.1, 0, 0, "|+⟩", fontsize=12)
    ax.text(-1.1, 0, 0, "|-⟩", fontsize=12)
    ax.text(0, 1.1, 0, "|i+⟩", fontsize=12)
    ax.text(0, -1.1, 0, "|i-⟩", fontsize=12)
    
    # Plot the state vector
    ax.quiver(0, 0, 0, bloch_coords[0], bloch_coords[1], bloch_coords[2], 
              length=1.0, color='r', arrow_length_ratio=0.1)
    
    # Set axis limits and aspect ratio
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.set_box_aspect([1,1,1])
    
    plt.show()

# Define the standard quantum gates as 2x2 matrices
X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
H = 1/np.sqrt(2) * np.array([[1, 1], [1, -1]])
S = np.array([[1, 0], [0, 1j]])
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])

# %% Define the initial state of the qubit. Here, we start with the |0⟩ state.
initial_state = np.array([[1], [0]])

# Convert the state vector to Bloch sphere coordinates
initial_coords = bloch_vector(initial_state)

# Plot the initial state
plot_bloch_sphere(initial_coords, title="Initial State: |0⟩")

# %% Apply the Pauli-X gate (bit-flip) to the initial |0⟩ state
x_gate_state = np.dot(X, initial_state)
x_gate_coords = bloch_vector(x_gate_state)

# Plot the result. Notice the vector flips to the south pole.
plot_bloch_sphere(x_gate_coords, title="State after Pauli-X Gate")

# %% Apply the Pauli-Y gate to the initial |0⟩ state
y_gate_state = np.dot(Y, initial_state)
y_gate_coords = bloch_vector(y_gate_state)

# Plot the result. The vector flips to the south pole and rotates around the Z-axis.
plot_bloch_sphere(y_gate_coords, title="State after Pauli-Y Gate")

# %% Apply the Pauli-Z gate (phase-flip) to the initial |0⟩ state
z_gate_state = np.dot(Z, initial_state)
z_gate_coords = bloch_vector(z_gate_state)

# Plot the result. For the |0⟩ state, the Z gate has no effect as the state is an eigenvector.
plot_bloch_sphere(z_gate_coords, title="State after Pauli-Z Gate")

# %% Apply the Hadamard gate to the initial |0⟩ state.
# This creates a superposition state, (|0⟩ + |1⟩)/sqrt(2), which corresponds to the |+⟩ state.
h_gate_state = np.dot(H, initial_state)
h_gate_coords = bloch_vector(h_gate_state)

# Plot the result. The vector now points to the X-axis.
plot_bloch_sphere(h_gate_coords, title="State after Hadamard Gate")

# %% The S gate only adds a phase, so let's apply it to a superposition state
# to see its effect. We'll start with the |+⟩ state from the H gate.
h_gate_state = np.dot(H, initial_state)

# Now apply the S gate to the |+⟩ state
s_gate_state = np.dot(S, h_gate_state)
s_gate_coords = bloch_vector(s_gate_state)

# Plot the result. The state has rotated from the X-axis to the Y-axis.
plot_bloch_sphere(s_gate_coords, title="State after S Gate")

# %% Similarly, the T gate is a phase gate. Let's apply it to the |+⟩ state.
h_gate_state = np.dot(H, initial_state)

# Now apply the T gate to the |+⟩ state
t_gate_state = np.dot(T, h_gate_state)
t_gate_coords = bloch_vector(t_gate_state)

# Plot the result. The state has rotated 45 degrees from the X-axis towards the Y-axis.
plot_bloch_sphere(t_gate_coords, title="State after T Gate")
