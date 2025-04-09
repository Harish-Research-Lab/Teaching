# Flow Visualizer

A Streamlit application for visualizing and exploring stream functions in fluid dynamics.

## Project Structure

The application is organized into the following files:

- `main.py`: Main entry point of the application
- `stream_functions.py`: Contains the mathematical implementations of various stream functions
- `ui_components.py`: Handles all the user interface elements and controls
- `visualization.py`: Creates and displays the visualizations

## Features

- Visualize different types of flow patterns: 
  - Uniform Flow
  - Source/Sink
  - Vortex
  - Doublet
  - Cylinder in Flow
  - Custom Combinations

- Interactive controls for:
  - Adjusting flow parameters
  - Setting domain size and resolution
  - Customizing visualization options

- Multiple visualization options:
  - Stream function contours
  - Streamlines
  - Velocity vectors

## Fluid Dynamics Theory

### Stream Functions

A stream function (ψ) is a mathematical tool used in fluid dynamics to describe two-dimensional, incompressible, and irrotational fluid flow. The key properties of stream functions include:

1. **Definition**: The stream function ψ(x,y) is defined such that:
   - u = ∂ψ/∂y (x-component of velocity)
   - v = -∂ψ/∂x (y-component of velocity)

2. **Streamlines**: Lines of constant ψ are streamlines, which are tangent to the velocity at every point. Fluid particles follow these paths in steady flow.

3. **Flow Rate**: The difference in ψ between any two streamlines represents the volume flow rate between them.

4. **Incompressibility**: The stream function automatically satisfies the continuity equation for incompressible flow (∇·V = 0).

### Elementary Flows

This application allows you to visualize several elementary flows:

#### Uniform Flow
- **Stream Function**: ψ = U·y
- **Physical Interpretation**: Flow with constant velocity U in the x-direction
- **Applications**: Free-stream flow, far-field conditions

#### Source/Sink
- **Stream Function**: ψ = (Q/2π)·θ
- **Physical Interpretation**: Fluid emanating from (source, Q>0) or converging to (sink, Q<0) a point
- **Applications**: Modeling wells, jets, or suction points

#### Vortex
- **Stream Function**: ψ = (Γ/2π)·ln(r)
- **Physical Interpretation**: Circular motion around a point with circulation Γ
- **Applications**: Modeling swirling flows, wing tip vortices

#### Doublet
- **Stream Function**: ψ = -κ·sin(θ)/r
- **Physical Interpretation**: Combination of a source and sink of equal strength as they approach each other
- **Applications**: Building block for more complex flow patterns

#### Cylinder in Flow
- **Stream Function**: ψ = U·(r - a²/r)·sin(θ)
- **Physical Interpretation**: Uniform flow around a circular cylinder of radius a
- **Applications**: Flow around bluff bodies, aerodynamics

### Principle of Superposition

For irrotational, incompressible flows, the principle of superposition applies. This means that complex flow fields can be constructed by adding together simpler elementary flows. For example:
- Cylinder in flow = Uniform flow + Doublet
- Flow around airfoils = Uniform flow + Vortex + Source/Sink distributions

This principle is utilized in the "Custom Combination" option in the application.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/flow-visualizer.git
cd flow-visualizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

## Educational Use

This tool is particularly useful for:

- **Fluid Mechanics Students**: Visualize theoretical concepts learned in class
- **Engineering Courses**: Demonstrate the behavior of different flow patterns
- **Research Projects**: Quick validation of analytical flow solutions
- **Self-Study**: Interactive exploration of fluid behavior without complex CFD software

### Example Learning Exercises

1. Observe how streamlines change with different strengths of sources/sinks
2. Compare the velocity field of a vortex at different circulations
3. Explore how the stagnation points move in cylinder flow as parameters change
4. Create custom combinations to model more complex flow scenarios

## Requirements

- Python 3.6+
- Streamlit
- NumPy
- Matplotlib
- SymPy

## License

[MIT License](LICENSE)