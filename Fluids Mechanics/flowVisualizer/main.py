import streamlit as st
from stream_functions import calculate_stream_function, calculate_velocity_field
from visualization import create_flow_visualization, display_equations
from ui_components import create_sidebar_controls
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.set_page_config(page_title="Flow Visualizer", layout="wide")
    
    st.title("Flow Visualizer")
    st.write("""
    This app helps you understand and visualize stream functions in fluid dynamics.
    Stream functions (ψ) describe fluid flow patterns where streamlines are lines of constant ψ.
    The velocity components can be derived from the stream function as:
    u = ∂ψ/∂y and v = -∂ψ/∂x
             
    Developed by Vijay N
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Flow Parameters")
        
        # Get all user inputs and parameters from the controls in the left column
        pattern_type, params, domain_settings, viz_settings = create_sidebar_controls(col1)
        
    with col2:
        # Extract domain settings
        domain_size = domain_settings["domain_size"]
        grid_points = domain_settings["grid_points"]
        
        # Create visualization based on user parameters
        create_flow_visualization(
            pattern_type, 
            params, 
            domain_size, 
            grid_points, 
            viz_settings
        )
        
        # Display relevant equations for the selected flow pattern
        # Pass params to display_equations for custom functions
        display_equations(pattern_type, params)

if __name__ == "__main__":
    main()