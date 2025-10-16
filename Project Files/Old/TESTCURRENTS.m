clear all;
close all;
clc;
addpath('C:\femm42\mfiles')
openfemm;
% Nom du fichier
opendocument('C:\femm42\MYFILES\Tp2412.FEM');
mi_saveas('msap2.fem');

 pos_rot =0;
 alpha=90;
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
 flux(1)=temp1(3);

 temp2=mo_getcircuitproperties('B');
 flux(2)=temp2(3);

 temp3=mo_getcircuitproperties('C');
 flux(3)=temp3(3);

%  ***********************************calcul du couple
 mo_seteditmode('area');
 mo_groupselectblock(10);
 couple=mo_blockintegral(22);
 disp(['COUPLE : ',num2str(couple)])
 mo_clearblock();

%  ***********************************calcul de la co-energie mag
 mo_seteditmode('area');
 mo_groupselectblock(10);
 mo_groupselectblock(0);
 co_energie=mo_blockintegral(17);
  disp(['coenergie : ',num2str(co_energie)])
 energie   =mo_blockintegral(2);
  disp(['energie : ',num2str(energie)])
 mo_clearblock();



