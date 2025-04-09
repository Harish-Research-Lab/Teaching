import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

from stream_functions import calculate_stream_function, calculate_velocity_field

def create_flow_visualization(pattern_type, params, domain_size, grid_points, viz_settings):
    """Create and display the flow visualization based on user parameters"""
    
    # Create grid
    x = np.linspace(-domain_size/2, domain_size/2, grid_points)
    y = np.linspace(-domain_size/2, domain_size/2, grid_points)
    X, Y = np.meshgrid(x, y)
    
    # Calculate stream function
    psi = calculate_stream_function(X, Y, pattern_type, params)
    
    # Calculate velocity field
    h = domain_size / (grid_points - 1)
    u, v = calculate_velocity_field(X, Y, psi, h)
    speed = np.sqrt(u**2 + v**2)
    
    # Extract visualization settings
    show_streamlines = viz_settings["show_streamlines"]
    streamline_density = viz_settings["streamline_density"]
    show_velocity = viz_settings["show_velocity"]
    vector_density = viz_settings["vector_density"]
    show_contour = viz_settings["show_contour"]
    contour_levels = viz_settings["contour_levels"]
    colormap = viz_settings["colormap"]
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot stream function contour
    if show_contour:
        contour = ax.contourf(X, Y, psi, levels=contour_levels, cmap=colormap, alpha=0.7)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        fig.colorbar(contour, cax=cax, label="Stream Function (ψ)")
    
    # Plot streamlines
    if show_streamlines:
        ax.streamplot(X, Y, u, v, density=streamline_density/10, 
                      color='white' if show_contour else 'black',
                      linewidth=1, arrowsize=1)
    
    # Plot velocity vectors
    if show_velocity:
        # Subsample for clearer visualization
        skip = grid_points // vector_density
        ax.quiver(X[::skip, ::skip], Y[::skip, ::skip], 
                  u[::skip, ::skip], v[::skip, ::skip],
                  scale=25, color='black', alpha=0.7)
    
    # Plot special features for certain flow patterns
    if pattern_type == "Cylinder in Flow":
        circle = plt.Circle((0, 0), params["radius"], color='black', fill=False, linewidth=2)
        ax.add_patch(circle)
    
    ax.set_aspect('equal')
    ax.set_title(f"Stream Function Visualization: {pattern_type}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Display the plot in Streamlit
    st.pyplot(fig)

def display_equations(pattern_type, params=None):
    """Display relevant equations for the selected flow pattern"""
    
    st.subheader("Governing Equations")
    
    if pattern_type == "Uniform Flow":
        st.latex(r"\psi(x, y) = U \cdot y")
        st.latex(r"u = U, \quad v = 0")
        
    elif pattern_type == "Source/Sink":
        st.latex(r"\psi(x, y) = \frac{Q}{2\pi} \cdot \theta")
        st.latex(r"u = \frac{Q}{2\pi} \cdot \frac{x}{x^2 + y^2}, \quad v = \frac{Q}{2\pi} \cdot \frac{y}{x^2 + y^2}")
        
    elif pattern_type == "Vortex":
        st.latex(r"\psi(x, y) = \frac{\Gamma}{2\pi} \cdot \ln(r)")
        st.latex(r"u = -\frac{\Gamma}{2\pi} \cdot \frac{y}{x^2 + y^2}, \quad v = \frac{\Gamma}{2\pi} \cdot \frac{x}{x^2 + y^2}")
        
    elif pattern_type == "Doublet":
        st.latex(r"\psi(x, y) = -\frac{\kappa \sin\theta}{r} = -\frac{\kappa y}{x^2 + y^2}")
        
    elif pattern_type == "Cylinder in Flow":
        st.latex(r"\psi(x, y) = U \cdot \left(r - \frac{a^2}{r}\right) \cdot \sin\theta")
        st.write("Where r is the distance from origin and a is the cylinder radius")
        
    elif pattern_type == "Custom Function" and params and "func_string" in params:
        # Display the user's custom function
        st.latex(r"\psi(x, y) = " + params["func_string"])
        st.write("Velocity components are calculated using numerical differentiation")
        st.latex(r"u = \frac{\partial \psi}{\partial y}, \quad v = -\frac{\partial \psi}{\partial x}")


def create_flow_visualization(pattern_type, params, domain_size, grid_points, viz_settings):
    """Create and display the flow visualization based on user parameters"""
    
    # Create grid
    x = np.linspace(-domain_size/2, domain_size/2, grid_points)
    y = np.linspace(-domain_size/2, domain_size/2, grid_points)
    X, Y = np.meshgrid(x, y)
    
    # Calculate stream function
    try:
        psi = calculate_stream_function(X, Y, pattern_type, params)
        
        # Check if the result contains any invalid values
        if np.isnan(psi).any() or np.isinf(psi).any():
            if pattern_type == "Custom Function":
                st.error("Your function produced invalid values (NaN or Inf). Please check your expression.")
                return
            
        # Calculate velocity field
        h = domain_size / (grid_points - 1)
        u, v = calculate_velocity_field(X, Y, psi, h)
        speed = np.sqrt(u**2 + v**2)

        # print(f"Average u: {np.mean(u):.4f}, Average v: {np.mean(v):.4f}")
        # print(f"Max u: {np.max(u):.4f}, Min u: {np.min(u):.4f}")
        # print(f"Max v: {np.max(v):.4f}, Min v: {np.min(v):.4f}")
        
        # Extract visualization settings
        show_streamlines = viz_settings["show_streamlines"]
        streamline_density = viz_settings["streamline_density"]
        show_velocity = viz_settings["show_velocity"]
        vector_density = viz_settings["vector_density"]
        show_contour = viz_settings["show_contour"]
        contour_levels = viz_settings["contour_levels"]
        colormap = viz_settings["colormap"]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot stream function contour
        if show_contour:
            contour = ax.contourf(X, Y, psi, levels=contour_levels, cmap=colormap, alpha=0.7)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            fig.colorbar(contour, cax=cax, label="Stream Function (ψ)")
        
        # Plot streamlines
        if show_streamlines:
            ax.streamplot(X, Y, u, v, density=streamline_density/10, 
                        color='white' if show_contour else 'black',
                        linewidth=1, arrowsize=1)
        
        # Plot velocity vectors
        if show_velocity:
            # Subsample for clearer visualization
            skip = grid_points // vector_density
            ax.quiver(X[::skip, ::skip], Y[::skip, ::skip], 
                    u[::skip, ::skip], v[::skip, ::skip],  # Original, correct order
                    scale=25, color='black', alpha=0.7)
        
        # Plot special features for certain flow patterns
        if pattern_type == "Cylinder in Flow":
            circle = plt.Circle((0, 0), params["radius"], color='black', fill=False, linewidth=2)
            ax.add_patch(circle)
        
        ax.set_aspect('equal')
        ax.set_title(f"Flow Visualization: {pattern_type}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Display the plot in Streamlit
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error generating visualization: {str(e)}")
        if pattern_type == "Custom Function":
            st.error("There was a problem with your custom function. Please check the syntax and try again.")