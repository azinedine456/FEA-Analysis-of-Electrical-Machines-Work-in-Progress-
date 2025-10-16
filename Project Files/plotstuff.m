% Assuming femmFilePath is already defined somewhere above
timestamp = datestr(now,'yyyymmdd_HHMMSS');
folderName = sprintf('Figure_%s_%s', femmFileName, timestamp);

% Create folder if it doesn't exist
if ~exist(folderName, 'dir')
    mkdir(folderName);
end

% ---- Figure 11: Flux ----
clf(figure(11));
figure(11);
theta = pas:pas:nb_pas*pas;
hold on;
plot(theta, flux(1:nb_pas,1));
plot(theta, flux(1:nb_pas,2));
plot(theta, flux(1:nb_pas,3));
hold off;
xlabel('Angle°');
ylabel('Flux (Wb)');
legend('Flux A','Flux B','Flux C');

% Save figure 11
fluxFigName = sprintf('Flux_%s_%s.fig', femmFileName, timestamp);
saveas(figure(11), fullfile(folderName, fluxFigName));

% ---- Figure 22: EMF ----
clf(figure(22));
figure(22);
e1 = diff([flux(1,1); flux(1:nb_pas,1)]) ./ (pas*pi/180);
e2 = diff([flux(1,2); flux(1:nb_pas,2)]) ./ (pas*pi/180);
e3 = diff([flux(1,3); flux(1:nb_pas,3)]) ./ (pas*pi/180);
hold on;
plot(theta, e1);
plot(theta, e2);
plot(theta, e3);
hold off;
xlabel('Angle°');
ylabel('EMF (V)');
legend('EMF A','EMF B','EMF C');

% Save figure 22
emfFigName = sprintf('EMF_%s_%s.fig', femmFileName, timestamp);
saveas(figure(22), fullfile(folderName, emfFigName));
