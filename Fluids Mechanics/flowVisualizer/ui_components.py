# Update the ui_components.py file

import streamlit as st
from stream_functions import parse_custom_function

def create_sidebar_controls(container):
    """Create and handle all user interface controls"""
    
    pattern_type = container.selectbox(
        "Select Flow Pattern",
        ["Uniform Flow", "Source/Sink", "Vortex", "Doublet", "Cylinder in Flow", 
         "Custom Combination", "Custom Function"]  # Added Custom Function option
    )
    
    # Parameters for different flow patterns
    params = {}
    
    if pattern_type == "Uniform Flow":
        params["U"] = container.slider("Flow Speed (U)", -10.0, 10.0, 1.0, 0.1)
        
    elif pattern_type == "Source/Sink":
        params["Q"] = container.slider("Strength (Q)", -10.0, 10.0, 5.0, 0.1,
                               help="Positive for source, negative for sink")
        
    elif pattern_type == "Vortex":
        params["Gamma"] = container.slider("Circulation (Γ)", -10.0, 10.0, 5.0, 0.1,
                                  help="Positive for counterclockwise, negative for clockwise")
        
    elif pattern_type == "Doublet":
        params["kappa"] = container.slider("Doublet Strength (κ)", 0.0, 10.0, 5.0, 0.1)
        
    elif pattern_type == "Cylinder in Flow":
        params["U"] = container.slider("Free Stream Velocity (U)", 0.1, 10.0, 1.0, 0.1)
        params["radius"] = container.slider("Cylinder Radius (a)", 0.5, 5.0, 1.0, 0.1)
        
    elif pattern_type == "Custom Combination":
        container.subheader("Select Flow Components")
        params["include_uniform"] = container.checkbox("Uniform Flow", True)
        if params["include_uniform"]:
            params["U"] = container.slider("Flow Speed (U)", -5.0, 5.0, 1.0, 0.1)
            
        params["include_source"] = container.checkbox("Source/Sink", False)
        if params["include_source"]:
            params["Q"] = container.slider("Source Strength (Q)", -5.0, 5.0, 1.0, 0.1)
            
        params["include_vortex"] = container.checkbox("Vortex", False)
        if params["include_vortex"]:
            params["Gamma"] = container.slider("Circulation (Γ)", -5.0, 5.0, 1.0, 0.1)
    
    elif pattern_type == "Custom Function":
        container.subheader("Enter Custom Stream Function")
        
        container.markdown("""
        Enter a mathematical expression for the stream function ψ(x,y).
        
        **Available variables:**
        - `x`, `y`: Coordinates
        - `r` and `theta` will be calculated automatically
        
        **Examples:**
        - `x*y`: Simple shear flow
        - `sin(x)*cos(y)`: Cellular flow pattern
        - `x**2 - y**2`: Hyperbolic flow
        """)
        
        # Text area for custom function
        default_func = "x*y"
        func_string = container.text_area("Stream Function ψ(x,y)", default_func, 
                                height=100, help="Enter a mathematical expression in terms of x and y")
        
        # Add common mathematical functions buttons
        container.markdown("**Common Functions**")
        col1, col2, col3, col4 = container.columns(4)
        
        if col1.button("sin(x)"):
            func_string = "sin(x)"
        if col2.button("cos(y)"):
            func_string = "cos(y)"
        if col3.button("x²-y²"):
            func_string = "x**2 - y**2"
        if col4.button("x*y"):
            func_string = "x*y"
        
        # Second row of buttons
        col1, col2, col3, col4 = container.columns(4)
        
        if col1.button("log(r)"):
            func_string = "log(sqrt(x**2 + y**2))"
        if col2.button("sin(x)*cos(y)"):
            func_string = "sin(x)*cos(y)"
        if col3.button("r*sin(theta)"):
            func_string = "sqrt(x**2 + y**2)*y/sqrt(x**2 + y**2)"
        if col4.button("r²*sin(2*theta)"):
            func_string = "(x**2 + y**2)*2*x*y/(x**2 + y**2)"
        
        # Parse the function
        func = parse_custom_function(func_string)
        
        if func is None:
            container.error("Invalid function expression. Please check syntax.")
        else:
            container.success("Function parsed successfully!")
            
        params["func"] = func
        params["func_string"] = func_string
    
    # Domain settings
    container.subheader("Domain Settings")
    domain_size = container.slider("Domain Size", 2.0, 20.0, 10.0, 0.5)
    grid_points = container.slider("Grid Resolution", 20, 100, 50, 5)
    
    domain_settings = {
        "domain_size": domain_size,
        "grid_points": grid_points
    }
    
    # Visualization settings
    container.subheader("Visualization Settings")
    show_streamlines = container.checkbox("Show Streamlines", True)
    streamline_density = container.slider("Streamline Density", 5, 40, 20, 1) if show_streamlines else 20
    
    show_velocity = container.checkbox("Show Velocity Field", True)
    vector_density = container.slider("Vector Density", 5, 40, 15, 1) if show_velocity else 15
    
    show_contour = container.checkbox("Show Stream Function Contour", True)
    contour_levels = container.slider("Number of Contour Levels", 5, 50, 20, 1) if show_contour else 20
    
    colormap = container.selectbox(
        "Colormap",
        ["viridis", "plasma", "inferno", "magma", "cividis", "turbo", "jet", "coolwarm", "RdBu", "RdYlBu"]
    )
    
    viz_settings = {
        "show_streamlines": show_streamlines,
        "streamline_density": streamline_density,
        "show_velocity": show_velocity,
        "vector_density": vector_density,
        "show_contour": show_contour,
        "contour_levels": contour_levels,
        "colormap": colormap
    }
    
    return pattern_type, params, domain_settings, viz_settings