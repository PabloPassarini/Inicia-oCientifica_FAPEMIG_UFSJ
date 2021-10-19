function [TRIAdata] = triangulationData(select, dados)

%% Escolhendo indicador foco, 8 indicadores totais

switch (select)
    case 1
        ind = 'evaPiche';
        pos = 4; %posi��o do indicador   
    case 2
        ind = 'insolacao';
        pos = 8; %posi��o do indicador 
    case 3
        ind = 'precipitacao';
        pos = 12; %posi��o do indicador 
    case 4
        ind = 'tmax';
        pos = 16; %posi��o do indicador 
    case 5 
        ind = 'tmed';
        pos = 20; %posi��o do indicador 
    case 6
        ind = 'tmin';
        pos = 24; %posi��o do indicador 
    case 7
        ind = 'umidadeRelativa';
        pos = 28; %posi��o do indicador 
    case 8
        ind = 'ventoVelocidade';
        pos = 32; %posi��o do indicador 
end

date = dados(:,1:3);
TRIAdata= [date dados(:,pos:(pos+3))];
