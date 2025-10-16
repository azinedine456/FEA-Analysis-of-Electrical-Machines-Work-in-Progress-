clear all;
close all;
clc;
femmDirPath = 'C:\femm42\mfiles';
femmfilePath = 'C:\femm42\MYFILES\Tp2412ROTATION.FEM';
[~, femmFileName, ~] = fileparts(femmfilePath);
addpath(femmDirPath)
openfemm;
% Nom du fichier
opendocument(femmfilePath);
mi_saveas(['RUN_',femmFileName,'SIM.fem']);
nb_pas=180; % nombre de pas de déplacement à vide
pas=2; % pas de déplacement en degres
pos_rot=0 ; % position du rotor en degres
alpha =90;
cor_xcp=34.75;

%pre-allocation
flux = zeros(nb_pas,3);
couple = zeros(1,nb_pas);
co_energie= zeros(1,nb_pas);
energie= zeros(1,nb_pas);
cont_torque = zeros(1,nb_pas);


for i= 1:nb_pas
 mi_seteditmode('group');
 mi_selectgroup(10);
 mi_moverotate(0,0,pas); % deplacement du rotor
 mi_clearselected()

 pos_rot= pos_rot+ pas ; % actualisation de la position du rotor
 %courants
%  ia=10.*cosd(pos_rot + alpha);
%  ib=10.*cosd(pos_rot -120 + alpha);
%  ic=10.*cosd(pos_rot -240+ alpha);
ia=0;
ib=0;
ic=0;

 mi_modifycircprop('A',1,ia); % on impose le courant dans chaque circuit
 mi_modifycircprop('B',1,ib);
 mi_modifycircprop('C',1,ic);

 mi_analyze(1); % calcul
 mi_loadsolution; % chargement de la solution

 %***********************************calcul des flux
 temp1=mo_getcircuitproperties('A');
 flux(i,1)=temp1(3);

 temp2=mo_getcircuitproperties('B');
 flux(i,2)=temp2(3);

 temp3=mo_getcircuitproperties('C');
 flux(i,3)=temp3(3);

%  ***********************************calcul du couple
 mo_seteditmode('area');
 mo_groupselectblock(10);
 couple(i)=mo_blockintegral(22);
 mo_clearblock();

%  ***********************************calcul de la co-energie mag
 mo_seteditmode('area');
 mo_groupselectblock(10);
 mo_groupselectblock(0);
 co_energie(i)=mo_blockintegral(17);
 energie(i)   =mo_blockintegral(2);
 mo_clearblock();


 %**********************************calcul du couple a travers de
 %l'integration contour
 mo_seteditmode('contour');
 mo_addcontour(cor_xcp,0);
 mo_addcontour(-cor_xcp,0);
 mo_bendcontour(180,1);

 mo_addcontour(-cor_xcp,0);
 mo_addcontour(cor_xcp,0);
 mo_bendcontour(180,1);

 cont_torquearr=mo_lineintegral(4);
 cont_torque(i)=cont_torquearr(1);
 mo_clearcontour();
end

plotstuff