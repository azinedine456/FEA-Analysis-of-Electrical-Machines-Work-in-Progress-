# ============================================================
#  2-Pole SPMSM — Full GMSH Python API
#  Builds geometry, meshes, discovers all post-boolean tags,
#  assigns Physical Groups, and saves the .msh file.
#
#  Install:  pip install gmsh
#  No path to gmsh.exe needed — the Python package is
#  self-contained and bundles its own kernel.
# ============================================================
# %%  imports
import gmsh
import numpy as np
import math
import sys
from collections import namedtuple
from itertools import chain



SlotGeometry = namedtuple('SlotGeometry', ['surface', 'curve_loop', 'curves'])
# ============================================================
# CONFIG — edit these two paths
# ============================================================
# %%  OUTPUT & params
OUTPUT_MSH = r"C:\Users\ZinouAb\Desktop\Github Projects\Ngsolve\NGSOLVE-GMSH\2POLE_SPMSM.msh"

# ============================================================
# PARAMETERS
# ============================================================
R_SHAFT    =  5   # Shaft outer radius
R_ROTOR    = 19   # Rotor iron outer radius
R_MAG      = 29   # Magnet outer / airgap inner radius
R_AG       = 30   # Airgap outer / stator inner radius
R_STATOR   = 50   # Stator outer radius
R_SLOT_IN  = 30   # Slot inner wall radius (same as airgap outer)
R_SLOT_OUT = 40   # Slot outer wall radius
SLOT_HALF  = np.pi / 12   # Half-angle of slot opening (15 deg)
lc         = 1.0    # Base mesh size

# ============================================================
# INITIALISE
# ============================================================
gmsh.initialize()
gmsh.model.add("2POLE_SPMSM")
gmsh.option.setNumber("General.Terminal", 1)   # Print progress to console
occ = gmsh.model.occ

# ============================================================
#%% SECTION 1 — ANNULAR BASE SURFACES
# We build 4 rings that will later be split by booleans.
# ============================================================

def make_annulus(r_outer, r_inner):
    """Return surface tag of an annular ring."""
    co=occ.addCircle(0, 0, 0, r_outer)
    ci=occ.addCircle(0, 0, 0, r_inner)
    clo = occ.addCurveLoop([co])
    cli = occ.addCurveLoop([ci])
    return [occ.addPlaneSurface([co, ci]),clo,cli,ci]



def gmsh_gui():
    """ Visualize Design"""
    occ.synchronize()
    if '-nopopup' not in sys.argv:
        gmsh.fltk.run()
    return True

P0=occ.addPoint(0,0,0,lc)

def make_circlearc(r):
    pc1=occ.addPoint(r,0,0)
    pc2=occ.addPoint(-r,0,0)
    CA=occ.addCircleArc(pc1,P0,pc2)
    return [(pc1,pc2),CA]
def flatten_chain(matrix):
    return list(chain.from_iterable(matrix))

Curve_shaft=occ.addCircle(0,0,0,R_SHAFT)
Curveloop_shaft=occ.addCurveLoop([Curve_shaft])
s_stator_base,Curveloop_stator_outer,Curveloop_stator_inner,Curve_stator_inner=make_annulus(R_STATOR,R_AG)


pointsarcr1=make_circlearc(R_ROTOR)
pointsarcr2=make_circlearc(-R_ROTOR)
pointsarcm1=make_circlearc(R_MAG)
pointsarcm2=make_circlearc(-R_MAG)
occ.removeAllDuplicates()


# ============================================================
# %% SECTION 2 — SLOT GEOMETRY
# One slot centred on the +x axis, then duplicated 6 times.
# ============================================================

def make_slot(angle_center=0.0):
    """
    Build one slot surface centred at angle_center.
    Returns surface tag.
    The slot spans ±SLOT_HALF around angle_center,
    between R_SLOT_IN and R_SLOT_OUT.
    """
    a1 =  angle_center + SLOT_HALF   # left edge angle
    a2 =  angle_center - SLOT_HALF   # right edge angle

    p_li = occ.addPoint(R_SLOT_IN  * np.cos(a1), R_SLOT_IN  * np.sin(a1), 0, lc)
    p_lo = occ.addPoint(R_SLOT_OUT * np.cos(a1), R_SLOT_OUT * np.sin(a1), 0, lc)
    p_ri = occ.addPoint(R_SLOT_IN  * np.cos(a2), R_SLOT_IN  * np.sin(a2), 0, lc)
    p_ro = occ.addPoint(R_SLOT_OUT * np.cos(a2), R_SLOT_OUT * np.sin(a2), 0, lc)
    p_c  = occ.addPoint(0, 0, 0, lc)   # arc centre

    l_left  = occ.addLine(p_li, p_lo)
    arc_out = occ.addCircleArc(p_lo, p_c, p_ro)
    l_right = occ.addLine(p_ro, p_ri)
    arc_in  = occ.addCircleArc(p_ri, p_c, p_li)

    cl = occ.addCurveLoop([l_left, arc_out, l_right, arc_in])
    sf = occ.addPlaneSurface([cl])

    return SlotGeometry(surface=sf, curve_loop=cl, curves=[l_left, arc_out, l_right, arc_in])

# 6 slot centres: 0°, 60°, 120°, 180°, 240°, 300°
# Phase assignment: A→0°/180°, B→120°/300°, C→60°/240°  (adjust to your winding)
slot_angles = [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]
slot_tags = [make_slot(a) for a in slot_angles]  




# ============================================================
# %% SECTION 3 — MAKING RELEVANT SURFACE PLANES
# =========


linemag1=occ.addLine(pointsarcr1[0][0],pointsarcm1[0][0])
linemag2=occ.addLine(pointsarcm1[0][1],pointsarcr1[0][1])




mag_n_tag=occ.addPlaneSurface([occ.addCurveLoop([pointsarcm1[1],linemag1,-pointsarcr1[1],linemag2])])
mag_s_tag=occ.addPlaneSurface([occ.addCurveLoop([-pointsarcm2[1],linemag1,pointsarcr2[1],linemag2])])


Curve_list_rotor=[pointsarcr1[1],-pointsarcr2[1]]
Curve_list_magnet=[-pointsarcm1[1],pointsarcm2[1]]

Curveloop_rotor=occ.addCurveLoop(Curve_list_rotor)
Curveloop_magnet=occ.addCurveLoop(Curve_list_magnet)


s_rotor_iron=occ.addPlaneSurface([Curveloop_rotor,Curveloop_shaft])
s_airgap=occ.addPlaneSurface([Curveloop_magnet,Curveloop_stator_inner])


s_shaft=occ.addPlaneSurface([Curveloop_shaft])


# ============================================================
# %% SECTION  — BOOLEAN OPERATIONS
# ============================================================

# --- 3b. Cut slots into stator ---
stator_obj  = [(2, s_stator_base)]



slot_tools      = [(2, s.surface)    for s in slot_tags]
slot_wall_tags  = [c for s in slot_tags for c in s.curves]


stator_out, _ = occ.cut(stator_obj, slot_tools, removeTool=False)



occ.synchronize()
assert len(stator_out) >= 1, "Stator boolean cut produced no output"
stator_tag = stator_out[0][1]

stator_bounds = gmsh.model.getBoundary([(2,stator_tag)], oriented=False)
slot_dimtags = {(1, c) for c in slot_wall_tags}
outer_bounds = [dt for dt in stator_bounds if dt not in slot_dimtags]
Curve_stator_outer = outer_bounds[0][1]




# --- 3c. Coherence: merge shared vertices / edges ---

occ.synchronize()

# ============================================================
# %% SECTION 4 — DISCOVER POST-BOOLEAN CURVE TAGS
#
# After booleans, we cannot assume which tag belongs to which
# physical boundary. We classify every surviving 1D entity by
# its bounding-box geometry.
# ============================================================

gmsh.model.occ.synchronize()
all_curves = gmsh.model.getEntities(dim=1)




# ============================================================
# %% SECTION 5 — PHYSICAL GROUPS
# ============================================================

# --- 5a. 2D Domains (Materials) ---
gmsh.model.addPhysicalGroup(2, [s_rotor_iron],            tag=-1, name="Rotor")
gmsh.model.addPhysicalGroup(2, [mag_n_tag],               tag=-1, name="MagnetN")
gmsh.model.addPhysicalGroup(2, [mag_s_tag],               tag=-1, name="MagnetS")
gmsh.model.addPhysicalGroup(2, [s_airgap],                tag=-1, name="AirGap")
gmsh.model.addPhysicalGroup(2, [stator_tag],              tag=-1, name="Stator")
gmsh.model.addPhysicalGroup(2, [slot_tags[0].surface, slot_tags[3].surface], tag=-1, name="PhaseA")
gmsh.model.addPhysicalGroup(2, [slot_tags[2].surface, slot_tags[5].surface], tag=-1, name="PhaseB")
gmsh.model.addPhysicalGroup(2, [slot_tags[1].surface, slot_tags[4].surface], tag=-1, name="PhaseC")
gmsh.model.addPhysicalGroup(2, [s_shaft],              tag=-1, name="Shaft")
# --- 5b. 1D Boundaries (Critical for NGSolve) ---
gmsh.model.addPhysicalGroup(1,[Curve_stator_outer],tag=-1,name="OuterBoundary")
gmsh.model.addPhysicalGroup(1,[Curve_shaft],tag=-1,name="Shaft")
gmsh.model.addPhysicalGroup(1,Curve_list_rotor,tag=-1,name="Rotor")
gmsh.model.addPhysicalGroup(1,[Curve_stator_inner],tag=-1,name="InnerStator")
gmsh.model.addPhysicalGroup(1,Curve_list_magnet,tag=-1,name="MagnetOuter")



# Lines
split_tags=[linemag1,linemag2]

if split_tags:
    gmsh.model.addPhysicalGroup(1, split_tags, tag=-1, name="MagnetSplitLine")
    print(f"  ✓ Physical Curve 'MagnetSplitLine' = curves {split_tags}")
else:
    print("  ✗ WARNING: MagnetSplitLine not found — check classifier thresholds")

if slot_wall_tags:
    gmsh.model.addPhysicalGroup(1, slot_wall_tags, tag=-1, name="SlotWalls")
    print(f"  ✓ Physical Curve 'SlotWalls' = {len(slot_wall_tags)} curves {slot_wall_tags}")
else:
    print("  ✗ WARNING: SlotWall curves not found — check classifier thresholds")

# ============================================================
# %% SECTION 6 — MESH SIZE FIELDS
# ============================================================
f_dist = gmsh.model.mesh.field.add("Distance")
gmsh.model.mesh.field.setNumbers(f_dist, "CurvesList",
    abs(np.array(flatten_chain([Curve_list_rotor,Curve_list_magnet,[Curve_stator_inner]]))))
gmsh.model.mesh.field.setNumber(f_dist, "NumPointsPerCurve", 150)

f_thresh = gmsh.model.mesh.field.add("Threshold")
gmsh.model.mesh.field.setNumber(f_thresh, "InField",  f_dist)
gmsh.model.mesh.field.setNumber(f_thresh, "SizeMin",  0.2)
gmsh.model.mesh.field.setNumber(f_thresh, "SizeMax",  2.5)
gmsh.model.mesh.field.setNumber(f_thresh, "DistMin",  0.5)
gmsh.model.mesh.field.setNumber(f_thresh, "DistMax",  2.0)

gmsh.model.mesh.field.setAsBackgroundMesh(f_thresh)

gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
gmsh.option.setNumber("Mesh.MeshSizeFromPoints",         0)
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature",      0)

# ============================================================
# %% SECTION 7 — MESH AND SAVE
# ============================================================
gmsh.option.setNumber("Mesh.MshFileVersion",     2.2)
gmsh.option.setNumber("Mesh.SaveAll",             0)
gmsh.option.setNumber("Mesh.SaveElementTagType",  2)

gmsh.model.mesh.generate(2)
gmsh.write(OUTPUT_MSH)

print(f"\n✓ Mesh saved to: {OUTPUT_MSH}")

# ============================================================
# %% SECTION 8 — VERIFICATION SUMMARY
# ============================================================
print("\n── Physical Group Summary ─────────────────────────────────────────────")
for dim in [2, 1]:
    for tag in gmsh.model.getPhysicalGroups(dim):
        name = gmsh.model.getPhysicalName(dim, tag[1])
        ents = gmsh.model.getEntitiesForPhysicalGroup(dim, tag[1])
        print(f"  dim={dim}  tag={tag[1]:>3}  name='{name}'  entities={list(ents)}")
gmsh_gui()
gmsh.finalize()
print("\n✓ Done. Load 2POLE_SPMSM.msh in NGSolve with ReadGmsh().")
# %%
