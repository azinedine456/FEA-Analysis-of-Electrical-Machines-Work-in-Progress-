SetFactory("OpenCASCADE");

lc = 1;

// --- 1. Points (Tags 1-11 are safe, no booleans yet) ---
Point(1) = {0, 0, 0, lc};
Point(2) = {0, 5, 0, lc};
Point(3) = {-19, 0, 0, lc};
Point(4) = {19, 0, 0, lc};
Point(5) = {-29, 0, 0, lc};
Point(6) = {29, 0, 0, lc};
Point(10) = {30,0,0,lc};
Point(11) = {40,0,0,lc};

// --- 2. Base Circles ---
Circle(1) = {0, 0, 0, 5, 0, 2*Pi};   // Shaft boundary
Circle(2) = {0, 0, 0, 19, 0, 2*Pi};  // Inner Iron boundary
Circle(3) = {0, 0, 0, 29, 0, 2*Pi};  // Permanent Magnet outer boundary
Circle(4) = {0, 0, 0, 30, 0, 2*Pi};  // Stator Inner boundary
Circle(5) = {0, 0, 0, 50, 0, 2*Pi};  // Stator Outer boundary

// --- 3. Base Rings (Using 200+ and 300+ to avoid auto-tag collisions) ---
Curve Loop(201) = {2}; Curve Loop(202) = {1};
Plane Surface(301) = {201, 202}; // Rotor Iron

Curve Loop(203) = {3}; 
Plane Surface(302) = {203, 201}; // Full Permanent Magnet Ring Base

Curve Loop(204) = {4}; 
Plane Surface(303) = {204, 203}; // Airgap

Curve Loop(205) = {5}; 
Plane Surface(304) = {205, 204}; // Stator Iron Solid Base


// --- 4. Base Slot (Using 80+ to avoid collisions) ---
SLOTSIDE1[] = Rotate {{0, 0, 1}, {0, 0, 0}, Pi/12} {
  Duplicata { Point{10}; Point{11}; }
};
SLOTSIDE2[] = Rotate {{0, 0, 1}, {0, 0, 0}, -Pi/12} {
  Duplicata { Point{10}; Point{11}; }
};

Line(80) = {SLOTSIDE1[0], SLOTSIDE1[1]};
Circle(90) = {SLOTSIDE1[1], 1, SLOTSIDE2[1]};   
Line(100) = {SLOTSIDE2[1], SLOTSIDE2[0]};
Circle(110) = {SLOTSIDE2[0], 1, SLOTSIDE1[0]};  

Curve Loop(120) = {80, 90, 100, 110};
Plane Surface(400) = {120}; // Base Slot


// --- 5. Auto-Generating Duplicates (Gmsh assigns low tags safely) ---
SLOT1A[] = Rotate {{0, 0, 1}, {0, 0, 0}, Pi} {
  Duplicata { Surface{400}; } 
};
SLOTB[] = Rotate {{0, 0, 1}, {0, 0, 0}, 2*Pi/3} {
  Duplicata { Surface{400, SLOT1A[0]}; } 
};
SLOTC[] = Rotate {{0, 0, 1}, {0, 0, 0}, 2*Pi/3} {
  Duplicata { Surface{SLOTB[0], SLOTB[1]}; } 
};


// --- 6. Booleans (Safe execution) ---
// Split Magnets
Rectangle(1000) = {-60, 0, 0, 120, 60}; 
NorthMagnet[] = BooleanIntersection { Surface{302}; } { Surface{1000}; };
SouthMagnet[] = BooleanDifference { Surface{302}; Delete; } { Surface{1000}; Delete; };

// Cut Stator
StatorIron[] = BooleanDifference { Surface{304}; Delete; } { Surface{400, SLOT1A[0], SLOTB[0], SLOTB[1], SLOTC[0], SLOTC[1]}; };


// --- 7. Physical Groups ---
Physical Surface("Stator") = {StatorIron[0]}; 
Physical Surface("PhaseA") = {400, SLOT1A[0]};
Physical Surface("PhaseB") = {SLOTB[0], SLOTB[1]};
Physical Surface("PhaseC") = {SLOTC[0], SLOTC[1]};
Physical Surface("AirGap") = {303};
Physical Surface("Rotor") = {301};
Physical Surface("Magnet_North") = {NorthMagnet[0]}; 
Physical Surface("Magnet_South") = {SouthMagnet[0]}; 



// --- 8. Mesh Controls ---
Field[1] = Distance;
Field[1].CurvesList = {3, 4}; 
Field[1].NumPointsPerCurve = 100; 

Field[2] = Threshold;
Field[2].InField = 1;
Field[2].SizeMin = 0.3;  
Field[2].SizeMax = 3.0;  
Field[2].DistMin = 0.1;
Field[2].DistMax = 2.0;  

Background Field = 2; 

Mesh.MeshSizeExtendFromBoundary = 0;
Mesh.MeshSizeFromPoints = 0;
Mesh.MeshSizeFromCurvature = 0;

// --- 9. Netgen Compatibility Guard Rails ---
Mesh.MshFileVersion = 2.2;
Mesh.SaveAll = 0;              // ONLY save elements that belong to a Physical Group
Mesh.SaveElementTagType = 2;   // Force elements to use dense Physical IDs


Mesh 2;
Save "2POLE_SPMSM.msh";