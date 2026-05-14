 Electromagnetic Simulation Software Comparison

This repository contains a curated overview of various Finite Element Method (FEM) and Boundary Element Method (BEM) software tools used for electromagnetic modeling and electrical machine design.

## Quick Comparison Table

| Software | License Type | Primary Strengths | Key Features |
| :--- | :--- | :--- | :--- |
| **FEMM** | Open Source | User experience, Parallel computing | LUA scripting, Active X support, Sliding band functionality |
| **COMSOL** | Commercial (Trial available) | Hybrid FEM-BEM, Multiphysics | Moving mesh, Infinite elements, Electric Discharge module |
| **Ansys Maxwell** | Commercial (Free version avail.) | Adaptive meshing, GPU acceleration | Multidomain modeling, Litz Wire Loss estimation |
| **EMworks** | Commercial | 2D and 3D FEM capabilities | Integrated engineering workflow |
| **FluxMotor** | Commercial | Quick global analysis | Equivalent model determination, Winding scheme customization |
| **Flux** | Commercial | Advanced customization | Accurate rotor-stator field interactions, Winding tool |
| **NGSolve** | Open Source | Speed, GPU Acceleration | Modern C++ core, Python steering, Active community |
| **EMDTool** | Source-available (Free for students) | Simulation speed, Customizability | Rotor skew handling, Scriptable extensions |
| **EMDLab** | Open Source | Research-oriented, Modular | Multiple mesh generators, Scriptable framework |
| **Elmer** | Open Source | HPC / Supercomputer support | Large-scale electromagnetic problem solving |

---

## Detailed Software Insights

### FEMM (Finite Element Method Magnetics)
* **Performance:** Simulations can be slow via the GUI/Matlab-LUA interface. Significant speedups are achieved by using LUA directly without the MATLAB interface.
* **Parallelization:** Supports parallel computing through Active X.
* **Pro-tip:** Use the sliding band functionality to reduce simulation time significantly.

### COMSOL Multiphysics
* **Methodology:** Supports both FEM and BEM. Excellent for hybrid FEM-BEM simulations, especially for models with small surface-to-volume ratios.
* **Capabilities:** Features general-purpose moving mesh for linear motion and infinite elements for modeling large/unbounded domains.
* **Modules:** Includes specialized [Electric Discharge](https://www.comsol.com/electric-discharge-module) and [AC/DC](https://www.comsol.com/acdc-module) modules.

### Ansys Maxwell
* **Automation:** Automatic adaptive meshing—users only need to specify geometry and material properties.
* **Hardware:** Supports [Nvidia GPU Acceleration](https://www.ansys.com/products/electronics/ansys-maxwell#tab1-2) to speed up complex simulations.
* **Specialty:** Detailed Litz Wire Loss estimation and multidomain system modeling.

### Altair Flux & FluxMotor
* **FluxMotor:** Best for rapid "global" analysis to determine operating points and initial motor topologies.
* **Flux:** A more advanced, flexible tool for custom designs. Offers a highly accurate representation of rotor-stator field interactions (armature reaction) and a robust winding tool.

### NGSolve
* **Architecture:** High-performance core written in C++ with a flexible Python interface.
* **High Performance:** Features native [GPU Acceleration](https://ngsolve.org/) (CUDA) for solving Poisson equations.
* **Learning:** Excellent [interactive tutorials](https://ngsolve.org/) and a strong active community.

### EMDTool & EMDLab
* **EMDTool:** Regarded as faster than FEMM or Maxwell. It is source-available, allowing for deep debugging and modification. Notable for handling rotor skew.
* **EMDLab:** A modular, scriptable framework designed specifically for researchers needing flexible optimization and automation.

### Elmer
* **Scale:** Robust open-source option capable of utilizing external resources like CSC supercomputers for high-end electromagnetic problems.

## References & Resources
* [Boundary Element Method - Wikipedia](https://en.wikipedia.org/wiki/Boundary_element_method)
* [Comparison of FEM Software in Electrical Machine Design](https://www.researchgate.net/publication/311940466_A_Comparison_of_The_Programmes_Using_Finite_Element_Software_in_Electrical_Machine_Design)
* [NGSolve Documentation](https://ngsolve.org/)
* [EMDTool Official Site](https://www.emdtool.com/)
