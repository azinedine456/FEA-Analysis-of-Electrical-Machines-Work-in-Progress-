
# %% Imports
from netgen.occ import *
from ngsolve import *
from ngsolve.webgui import Draw
from netgen.read_gmsh import ReadGmsh

# %% # 1. Load the .msh file into a Netgen mesh object
ngmesh = ReadGmsh(r"C:\Users\ZinouAb\Desktop\Github Projects\Ngsolve\NGSOLVE-GMSH\2POLE_SPMSM.msh")

# %% 2. Wrap the Netgen mesh into an NGSolve mesh object
mesh = Mesh(ngmesh)

# %% 3. Verify boundaries and materials if physical groups were used
print(mesh.GetBoundaries())
print(mesh.GetMaterials())

# %% Defining CoefFunction
fes=H1(mesh,order=1,dirichlet="OuterBoundary")

A, v = fes.TnT()
gfu = GridFunction(fes)  # solution 

a = BilinearForm(grad(u)*grad(v)*dx).Assemble()
f = LinearForm(x*v*dx).Assemble()



   # You have just created a CoefficientFunction
# %% Drawing
Draw(ngmesh)

# %%
