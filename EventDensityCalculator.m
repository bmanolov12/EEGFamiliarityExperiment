%get event density per second of popular songs
folder = 'C:\School\Research\NeuroscienceExperiments\AudioFiles\popular\';
edens_list = [];
pop_files = dir(fullfile(folder, '*.wav'));
for k = 1:numel(pop_files)
    filename = strcat(folder, pop_files(k).name);
    [y,Fs] = audioread(filename);
    maud = miraudio(y(:,1),Fs);
    v = linspace(0, Fs*30, 30);
    mseg = mirsegment(maud, v);
    mev = mironsets(mseg);
    edens = mireventdensity(mev);
    edens_list = [edens_list, edens];
end
%now unpopular songs
folder = 'C:\School\Research\NeuroscienceExperiments\AudioFiles\unpopular\'
unpop_files = dir(fullfile(folder, '*.wav'))
for k = 1:numel(unpop_files)
    filename = strcat(folder, unpop_files(k).name)
    [y,Fs] = audioread(filename);
    maud = miraudio(y(:,1),Fs);
    v = linspace(0, Fs*30, 30);
    mseg = mirsegment(maud, v);
    mev = mironsets(mseg);
    edens = mireventdensity(mev);
    edens_list = [edens_list, edens];
end
dens_vals = [];
for k = 1:numel(edens_list)
    r = mirrms(edens_list(k));
    test = get(r,'Data');
    dens_vals = [dens_vals, test{1,1}{1,1}];
end

subplot(3,1,1);
bar(sort(dens_vals(1:16)), 'b');
title('Popular songs - Event density');
ylabel('Event density (s)');

subplot(3,1,2);
bar(sort(dens_vals(17:32)), 'r');
title('Unpopular songs - Event density');
ylabel('Event density (s)');

subplot(3,1,3);
boxplot(reshape(dens_vals,16,2), 'Labels',{'Popular','Unpopular'});
title('Boxplot of Event Density');
ylabel('Event density (s)');

[h,p] = ttest(dens_vals(1:16), dens_vals(17:32));
p2 = ranksum(dens_vals(1:16), dens_vals(17:32));