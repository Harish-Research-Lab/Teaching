import numpy as np
from sympy import symbols, lambdify, sympify, parsing


def parse_custom_function(expr_string):
    """
    Parse a user-provided string into a callable function
    
    Parameters:
    expr_string (str): String representation of a mathematical expression
    
    Returns:
    callable: Function that takes x, y arrays and returns evaluated expression
    """
    try:
        # Define symbols
        x, y = symbols('x y')
        
        # Parse the expression string
        expr = sympify(expr_string, evaluate=True)
        
        # Convert to a numpy-compatible function
        func = lambdify((x, y), expr, modules=['numpy'])
        
        return func
    except (parsing.sympy_parser.ParserError, SyntaxError, TypeError, ValueError) as e:
        # Return None if parsing fails
        return None

def calculate_stream_function(x, y, pattern_type, params):
    """Calculate stream function values based on selected flow pattern"""
    if pattern_type == "Uniform Flow":
        # ψ = U * y (uniform flow in x-direction)
        return params["U"] * y
    
    elif pattern_type == "Source/Sink":
        # ψ = (Q/2π) * θ (source or sink at origin)
        r = np.sqrt(x**2 + y**2) + 1e-10  # avoid division by zero
        theta = np.arctan2(y, x)
        return (params["Q"]/(2*np.pi)) * theta
    
    elif pattern_type == "Vortex":
        # ψ = (Γ/2π) * ln(r) (vortex at origin)
        r = np.sqrt(x**2 + y**2) + 1e-10  # avoid division by zero
        return (params["Gamma"]/(2*np.pi)) * np.log(r)
    
    elif pattern_type == "Doublet":
        # ψ = -κ * sin(θ)/r (doublet at origin)
        r = np.sqrt(x**2 + y**2) + 1e-10  # avoid division by zero
        theta = np.arctan2(y, x)
        return -params["kappa"] * np.sin(theta)/r
    
    elif pattern_type == "Cylinder in Flow":
        # Combination of uniform flow and doublet
        U = params["U"]
        a = params["radius"]
        r = np.sqrt(x**2 + y**2) + 1e-10
        theta = np.arctan2(y, x)
        return U * (r - a**2/r) * np.sin(theta)
    
    elif pattern_type == "Custom Combination":
        # Combined flow patterns
        psi = np.zeros_like(x)
        
        if params["include_uniform"]:
            psi += params["U"] * y
            
        if params["include_source"]:
            r = np.sqrt(x**2 + y**2) + 1e-10
            theta = np.arctan2(y, x)
            psi += (params["Q"]/(2*np.pi)) * theta
            
        if params["include_vortex"]:
            r = np.sqrt(x**2 + y**2) + 1e-10
            psi += (params["Gamma"]/(2*np.pi)) * np.log(r)
            
        return psi
    
    elif pattern_type == "Custom Function":
        # User-defined function
        if params.get("func") is not None:
            try:
                return params["func"](x, y)
            except Exception as e:
                # Return zeros if evaluation fails
                return np.zeros_like(x)
        return np.zeros_like(x)
    
    return np.zeros_like(x)

def calculate_velocity_field(x, y, psi, h=0.1):
    """Calculate velocity field from stream function using finite difference"""
    u = np.zeros_like(psi)
    v = np.zeros_like(psi)
    
    # Interior points (central difference)
    # Calculate derivatives correctly: u = ∂ψ/∂y, v = -∂ψ/∂x
    u[1:-1, 1:-1] = (psi[2:, 1:-1] - psi[:-2, 1:-1]) / (2 * h)  # ∂ψ/∂y (vertical derivative)
    v[1:-1, 1:-1] = -(psi[1:-1, 2:] - psi[1:-1, :-2]) / (2 * h)  # -∂ψ/∂x (negative horizontal derivative)
    
    return u, v