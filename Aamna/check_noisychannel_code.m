clc;
clear all;

d=load('S001R04.mat');
ChannelData=d.record;
data=ChannelData;
srate=160;
%ChannelData=data.data{1,2}.X';
%data=ChannelData;
originalNumberChannels = size(data, 1); 
originalChannels = 1:size(data, 1);
evaluationChannels=1:originalNumberChannels;
data = double(data(evaluationChannels, :))';      % Remove the unneeded channels
signalSize = size(data, 1);


robustChannelDeviation = zeros(originalNumberChannels, 1);

nanChannelMask = sum(isnan(data), 1) > 0;
noSignalChannelMask = mad(data, 1, 1) < 10e-10 | std(data, 1, 1) < 10e-10;
badChannelsFromNaNs = evaluationChannels(nanChannelMask);
badChannelsFromNoData = evaluationChannels(noSignalChannelMask);
evaluationChannels = setdiff(evaluationChannels, ...
    union(badChannelsFromNaNs,badChannelsFromNoData));
data = ChannelData;
data = double(data(evaluationChannels, :))';  
[signalSize, numberChannels] = size(data);

channelDeviation = 0.7413 *iqr(data); % Robust estimate of SD
channelDeviationSD =  0.7413 * iqr(channelDeviation);
channelDeviationMedian = nanmedian(channelDeviation)
robustChannelDeviation(evaluationChannels) = ...
    (channelDeviation - channelDeviationMedian) / channelDeviationSD;

% Find channels with unusually high deviation 
badChannelsFromDeviation = ...
    abs(robustChannelDeviation) > 5 | ...
             isnan(robustChannelDeviation);
badChannelsFromDeviation = originalChannels(badChannelsFromDeviation);
badChannelsFromDeviation_out = badChannelsFromDeviation(:)';

%finding high frequency noise channels
if srate > 100
    % Remove signal content above 50Hz and below 1 Hz
    B = design_fir(100,[2*[0 45 50]/srate 1],[1 1 0 0]);
    X = zeros(signalSize, numberChannels);
    for k = 1:numberChannels  % Could be changed to parfor
        X(:,k) = filtfilt(B, 1, data(:, k)); 
    end
    % Determine z-scored level of EM noise-to-signal ratio for each channel
    noisiness = mad(data- X, 1)./mad(X, 1);
    noisinessMedian = nanmedian(noisiness);
    noisinessSD = mad(noisiness, 1)*1.4826;
    zscoreHFNoiseTemp = (noisiness - noisinessMedian) ./ noisinessSD;
    noiseMask = (zscoreHFNoiseTemp > 5) | ...
                isnan(zscoreHFNoiseTemp);
    % Remap channels to original numbering
    badChannelsFromHFNoise  = evaluationChannels(noiseMask);
    badChannelsFromHFNoise = badChannelsFromHFNoise(:)';
else
    X = data;
    noisinessMedian = 0;
    noisinessSD = 1;
    zscoreHFNoiseTemp = zeros(numberChannels, 1);
    badChannelsFromHFNoise = [];
end

% Remap the channels to original numbering for the zscoreHFNoise
zscoreHFNoise(evaluationChannels) = zscoreHFNoiseTemp;
noisinessMedian = noisinessMedian;
noisinessSD = noisinessSD;

%finding channels by correlation
correlationWindowSeconds=1;
correlationFrames = correlationWindowSeconds * srate;
correlationWindow = 0:(correlationFrames - 1);
correlationOffsets = 1:correlationFrames:(signalSize-correlationFrames);
WCorrelation = length(correlationOffsets);
noiseLevels_out = zeros(originalNumberChannels, WCorrelation);
channelDeviations_out = zeros(originalNumberChannels, WCorrelation);
maximumCorrelations = ones(originalNumberChannels, WCorrelation);
dropOuts_out=zeros(originalNumberChannels,WCorrelation);
channelCorrelations = ones(WCorrelation, numberChannels);
noiseLevels = zeros(WCorrelation, numberChannels);
channelDeviations = zeros(WCorrelation, numberChannels);
n = length(correlationWindow);
xWin = reshape(X(1:n*WCorrelation, :)', numberChannels, n, WCorrelation);
size(xWin)
dataWin = reshape(data(1:n*WCorrelation, :)', numberChannels, n, WCorrelation);
for k = 1:WCorrelation 
    eegPortion = squeeze(xWin(:, :, k))';
    dataPortion = squeeze(dataWin(:, :, k))';
    windowCorrelation = corrcoef(eegPortion);
    abs_corr = abs(windowCorrelation - diag(diag(windowCorrelation)));
    channelCorrelations(k, :)  = quantile(abs_corr, 0.98);
    noiseLevels(k, :) = mad(dataPortion - eegPortion, 1)./mad(eegPortion, 1);
    channelDeviations(k, :) =  0.7413 *iqr(dataPortion);
end
dropOuts = isnan(channelCorrelations) | isnan(noiseLevels);
channelCorrelations(dropOuts) = 0.0;
noiseLevels(dropOuts) = 0.0;
clear xWin;
clear dataWin;
maximumCorrelations(evaluationChannels, :) = channelCorrelations';
noiseLevels_out(evaluationChannels, :) = noiseLevels';
channelDeviations_out(evaluationChannels, :) = channelDeviations';
dropOuts_out(evaluationChannels, :) = dropOuts';
thresholdedCorrelations = maximumCorrelations < 0.4;
fractionBadCorrelationWindows = mean(thresholdedCorrelations, 2);
fractionBadDropOutWindows = mean(dropOuts_out, 2);
badChannelsFromCorrelation = find(fractionBadCorrelationWindows > 0.01);
badChannelsFromCorrelation_out = badChannelsFromCorrelation(:)'; badChannelsFromDropOuts = find(fractionBadDropOutWindows > 0.01);
badChannelsFromDropOuts_out = badChannelsFromDropOuts(:)';
medianMaxCorrelation = median(maximumCorrelations, 2);
noisyChannels =union(union(union(badChannelsFromDeviation, union(badChannelsFromCorrelation, badChannelsFromDropOuts)),badChannelsFromHFNoise),badChannelsFromDropOuts_out);


