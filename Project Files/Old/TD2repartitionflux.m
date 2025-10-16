
clear all;
% close all;
clc;
addpath('C:\femm42\mfiles')
openfemm;
% Nom du fichier
opendocument('C:\femm42\MYFILES\square.FEM');
mi_saveas('Run_square.fem');


nb_pas=180; % nombre de pas de déplacement à vide
pas=2; % pas de déplacement en degres
pos_rot=0 ; % position du rotor en degres

flux = zeros(nb_pas,3);


for i= 1:nb_pas
    mi_seteditmode('group');
    mi_selectgroup(10);
    mi_moverotate(0,0,pas); % deplacement du rotor
    mi_clearselected()

    pos_rot= pos_rot+ pas ;

    mi_analyze(1); % calcul
    mi_loadsolution; % chargement de la solution

    %***********************************calcul des flux
  temp1=mo_getcircuitproperties('A');
 flux(i,1)=temp1(3);

 temp2=mo_getcircuitproperties('B');
 flux(i,2)=temp2(3);

 temp3=mo_getcircuitproperties('C');
 flux(i,3)=temp3(3);


end