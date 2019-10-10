
function [EEG, varargout] = preprocess(data, varargin)

Comments in these blocks indicate the start of a section of code
I sectioned the code by categories.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   This section of the code is setting up all the possible parameters and
% information needed for preprocessing. It adds and orginizes all the parameters
% that will be used and if anything is missing deafult and recommended
% parameters are used. It also sets up all the paths to the functions that
% will be used and removes possible interfering pathways so that automagic
% functions are used instead of matlab deafult functions
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Defaults = DefaultParameters;
Recs = RecommendedParameters;
Csts = PreprocessingConstants;
p = inputParser;
addParameter(p,'EEGSystem', Defaults.EEGSystem, @isstruct);
addParameter(p,'FilterParams', Defaults.FilterParams, @isstruct);
addParameter(p,'PrepParams', Defaults.PrepParams, @isstruct);
addParameter(p,'CRDParams', Defaults.CRDParams, @isstruct);
addParameter(p,'RPCAParams', Defaults.RPCAParams, @isstruct);
addParameter(p,'HighvarParams', Defaults.HighvarParams, @isstruct);
addParameter(p,'MARAParams', Defaults.MARAParams, @isstruct);
addParameter(p,'ICLabelParams', Defaults.ICLabelParams, @isstruct);
addParameter(p,'InterpolationParams', Defaults.InterpolationParams, @isstruct);
addParameter(p,'EOGRegressionParams', Defaults.EOGRegressionParams, @isstruct);
addParameter(p,'ChannelReductionParams', Defaults.ChannelReductionParams, @isstruct);
addParameter(p,'Settings', Defaults.Settings, @isstruct);
addParameter(p,'DetrendingParams', Defaults.DetrendingParams, @isstruct);
addParameter(p,'ORIGINAL_FILE', Csts.GeneralCsts.ORIGINAL_FILE, @ischar);
parse(p, varargin{:});
params = p.Results;
EEGSystem = p.Results.EEGSystem;
FilterParams = p.Results.FilterParams;
CRDParams = p.Results.CRDParams;
PrepParams = p.Results.PrepParams;
HighvarParams = p.Results.HighvarParams;
RPCAParams = p.Results.RPCAParams;
MARAParams = p.Results.MARAParams;
ICLabelParams = p.Results.ICLabelParams;
InterpolationParams = p.Results.InterpolationParams; %#ok<NASGU>
EOGRegressionParams = p.Results.EOGRegressionParams;
ChannelReductionParams = p.Results.ChannelReductionParams;
Settings = p.Results.Settings;
DetrendingParams = p.Results.DetrendingParams;
ORIGINAL_FILE = p.Results.ORIGINAL_FILE;

if isempty(Settings)
    Settings = Recs.Settings;
end
clear p varargin;

% Add and download necessary paths
addPreprocessingPaths(struct('PrepParams', PrepParams, 'CRDParams', CRDParams, ...
    'RPCAParams', RPCAParams, 'MARAParams', MARAParams, 'ICLabelParams', ICLabelParams));

% Set system dependent parameters and separate EEG from EOG
[EEG, EOG, EEGSystem, MARAParams] = ...
    systemDependentParse(data, EEGSystem, ChannelReductionParams, ...
    MARAParams, ORIGINAL_FILE);
EEGRef = EEG;

% Remove the reference channel from the rest of preprocessing
if ~isempty(EEGSystem.refChan)
    [~, EEG] = evalc('pop_select(EEG, ''nochannel'', EEGSystem.refChan.idx)');
end
EEG.automagic.channelReduction.newRefChan = EEGSystem.refChan;
EEGOrig = EEG;

if Settings.trackAllSteps
   allSteps = matfile(Settings.pathToSteps, 'Writable', true);
   allSteps.EEGOrig = EEGOrig;
end


% Remove biosemi before preprocessing steps to avoid potential conflicts
allPaths = path;
allPaths = strsplit(allPaths, pathsep);
idx = contains(allPaths, 'biosig');
allPaths(~idx) = [];
automagicPaths = strjoin(allPaths, pathsep);
rmpath(automagicPaths);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% This section is the beginning of the actual preprocessing!
% First it sets up the data and performs "performPrep()"
% then performs "clean_rawdata()", checks for input bad channels,
% next "performFilter()" is done one the data and also done one the EOG data
% if it is provided. Next any noisy channels are removed, and then all the
% effects of the eyes (EOG) is removed. Next ICA, MARA, or RPCA is performed
% to identify noise in the data. next detrending occurs by subtracting the mean
% from all the data. Lastly channels are regected based of high varience noise.
%
% (important to note that all these proccessies are tracked and
%   outputed to a text file "Methods log file")
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%% Preprocessing
[s, ~] = size(EEG.data);
EEG.automagic.preprocessing.toRemove = [];
EEG.automagic.preprocessing.removedMask = false(1, s); clear s;

% Running prep
[EEG, EOG] = performPrep(EEG, EOG, PrepParams, EEGSystem.refChan);
if Settings.trackAllSteps && ~isempty(PrepParams)
   allSteps = matfile(Settings.pathToSteps, 'Writable', true);
   allSteps.EEGprep = EEG;
end

% Clean EEG using clean_rawdata()
[EEG, EOG] = performCleanrawdata(EEG, EOG, CRDParams);
if Settings.trackAllSteps && ~isempty(CRDParams)
   allSteps = matfile(Settings.pathToSteps, 'Writable', true);
   allSteps.EEGcrd = EEG;
end

if isfield(EEG.automagic.crd,'badChans')
if (length(EEG.automagic.crd.badChans) == length(EEG.automagic.channelReduction.usedEEGChannels))
    message = 'All non-excluded channels identified as bad channels. Interpolation will not be possible';
    warning(message)
    EEG.automagic.badChanError = message;
end
end

% Filtering on the whole dataset
display(PreprocessingConstants.FilterCsts.RUN_MESSAGE);
EEG = performFilter(EEG, FilterParams);
if ~isempty(EOG.data)
    EOG = performFilter(EOG, FilterParams);
end

if Settings.trackAllSteps && ~isempty(FilterParams)
   allSteps = matfile(Settings.pathToSteps, 'Writable', true);
   allSteps.EEGfiltered = EEG;
end

% Remove channels
toRemove = EEG.automagic.preprocessing.toRemove;
removedMask = EEG.automagic.preprocessing.removedMask;
[~, newToRemove] = intersect(find(~removedMask), toRemove); %#ok<ASGLU>
[~, EEG] = evalc('pop_select(EEG, ''nochannel'', newToRemove)');
removedMask(toRemove) = 1;
toRemove = [];
EEG.automagic.preprocessing.removedMask = removedMask;
EEG.automagic.preprocessing.toRemove = toRemove;
clear toRemove removedMask newToRemove;

% Remove effect of EOG
EEG = performEOGRegression(EEG, EOG, EOGRegressionParams);
EEG_regressed = EEG;

if Settings.trackAllSteps && ~isempty(EOGRegressionParams)
   allSteps = matfile(Settings.pathToSteps, 'Writable', true);
   allSteps.EEGRegressed = EEG;
end

% PCA or ICA
EEG.automagic.mara.performed = 'no';
EEG.automagic.rpca.performed = 'no';
EEG.automagic.iclabel.performed = 'no';
if ( ~isempty(ICLabelParams) )
    try
        EEG = performICLabel(EEG, ICLabelParams);
    catch ME
        message = ['ICLabel is not done on this subject, continue with the next steps: ' ...
            ME.message];
        warning(message)
        EEG.automagic.iclabel.performed = 'FAILED';
        EEG.automagic.error_msg = message;
    end
elseif ( ~isempty(MARAParams) )
    try
        EEG = performMARA(EEG, MARAParams);
    catch ME
        message = ['MARA ICA is not done on this subject, continue with the next steps: ' ...
            ME.message];
        warning(message)
        EEG.automagic.mara.performed = 'FAILED';
        EEG.automagic.error_msg = message;
    end
elseif ( ~isempty(RPCAParams))
    [EEG, pca_noise] = performRPCA(EEG, RPCAParams);
end
EEG_cleared = EEG;

if Settings.trackAllSteps
    if ~isempty(RPCAParams)
       allSteps = matfile(Settings.pathToSteps, 'Writable', true);
       allSteps.EEGRPCA = EEG;
    elseif ~isempty(MARAParams)
       allSteps = matfile(Settings.pathToSteps, 'Writable', true);
       allSteps.EEGMARA = EEG;
    end
end

% Detrending
if ~ isempty(DetrendingParams)
    doubled_data = double(EEG.data);
    res = bsxfun(@minus, doubled_data, mean(doubled_data, 2));
    singled_data = single(res);
    EEG.data = singled_data;
    clear doubled_data res singled_data;

    if Settings.trackAllSteps
       allSteps = matfile(Settings.pathToSteps, 'Writable', true);
       allSteps.EEGdetrended = EEG;
    end
end

% Reject channels based on high variance
EEG.automagic.highVarianceRejection.performed = 'no';
if ~isempty(HighvarParams)
    [~, EEG] = evalc('performHighvarianceChannelRejection(EEG, HighvarParams)');
end

if Settings.trackAllSteps && ~isempty(HighvarParams)
   allSteps = matfile(Settings.pathToSteps, 'Writable', true);
   allSteps.EEGHighvarred = EEG;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% This last section is responsible for creating the outputed figures for
% the data.
% Plots:
%   -filtered EOG data
%   -Filtered EEG data
%   -Detected bad channels
%   -EOG reressed out
%   -ICA(or MARA or RPCA) corrected clean data
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Put back removed channels
removedChans = find(EEG.automagic.preprocessing.removedMask);
for chan_idx = 1:length(removedChans)
    chan_nb = removedChans(chan_idx);
    EEG.data = [EEG.data(1:chan_nb-1,:); ...
                  NaN(1,size(EEG.data,2));...
                  EEG.data(chan_nb:end,:)];
    EEG.chanlocs = [EEG.chanlocs(1:chan_nb-1), ...
                      EEGOrig.chanlocs(chan_nb), EEG.chanlocs(chan_nb:end)];
    EEG.nbchan = size(EEG.data,1);
end

% Put back refrence channel
if ~isempty(EEGSystem.refChan)
    refChan = EEGSystem.refChan.idx;
    EEG.data = [EEG.data(1:refChan-1,:); ...
                            zeros(1,size(EEG.data,2));...
                            EEG.data(refChan:end,:)];
    EEG.chanlocs = [EEG.chanlocs(1:refChan-1), EEGRef.chanlocs(refChan), ...
                        EEG.chanlocs(refChan:end)];
    EEG.nbchan = size(EEG.data,1);
    clear chan_nb re_chan;
end

% Write back output
if ~isempty(EEGSystem.refChan)
    EEG.automagic.autoBadChans = setdiff(removedChans, EEGSystem.refChan.idx);
else
    EEG.automagic.autoBadChans = removedChans;
end
EEG.automagic.params = params;
EEG.automagic = rmfield(EEG.automagic, 'preprocessing');

if Settings.trackAllSteps
   allSteps = matfile(Settings.pathToSteps, 'Writable', true);
   allSteps.EEGFinal = EEG;
end

%% Creating the final figure to save
if ~isempty(FilterParams.high)
    plot_FilterParams = FilterParams;
else
    disp('No high-pass filter selected. Plotting with 1Hz by default');

    plot_FilterParams.high.freq = 1;
    plot_FilterParams.high.order = [];
end
% plot_FilterParams.high.freq = 1;
% plot_FilterParams.high.order = [];
EEG_filtered_toplot = performFilter(EEGOrig, plot_FilterParams);
fig1 = figure('visible', 'off');
set(gcf, 'Color', [1,1,1])
hold on
% eog figure
subplot(11,1,1)
if ~isempty(EOG.data)
    imagesc(EOG.data);
    colormap jet
    scale_min = round(min(min(EOG.data)));
    scale_max = round(max(max(EOG.data)));
    caxis([scale_min scale_max])
    XTicks = [] ;
    XTicketLabels = [];
    set(gca,'XTick', XTicks)
    set(gca,'XTickLabel', XTicketLabels)
    yticks = get(gca,'YTickLabel');
    set(gca,'YTickLabel', yticks, 'fontsize', 7);
    title('Filtered EOG data');
    colorbar;
else
    title('No EOG data available');
end
%eeg figure
subplot(11,1,2:3)
imagesc(EEG_filtered_toplot.data);
colormap jet
caxis([-100 100])
XTicks = [] ;
XTicketLabels = [];
set(gca,'XTick', XTicks)
set(gca,'XTickLabel', XTicketLabels)
if isempty(FilterParams.high)
    title('1Hz Filtered EEG data')
else
    title('Filtered EEG data')
end
colorbar;
%eeg figure
subplot(11,1,4:5)
imagesc(EEG_filtered_toplot.data);
axe = gca;
hold on;
bads = EEG.automagic.autoBadChans;
for i = 1:length(bads)
    y = bads(i);
    p1 = [0, size(EEG_filtered_toplot.data, 2)];
    p2 = [y, y];
    plot(axe, p1, p2, 'b' ,'LineWidth', 0.5);
end
hold off;
colormap jet;
caxis([-100 100])
set(gca,'XTick', XTicks)
set(gca,'XTickLabel', XTicketLabels)
title('Detected bad channels')
colorbar;
% figure;
eogRegress_subplot=subplot(11,1,6:7);
imagesc(EEG_regressed.data);
colormap jet
caxis([-100 100])
set(gca,'XTick',XTicks)
set(gca,'XTickLabel',XTicketLabels)
if strcmp(EEG_regressed.automagic.EOGRegression.performed,'no')
            title_text = '\color{red}No EOG-Regression requested';
            cla(eogRegress_subplot)
else
    title_text = 'EOG regressed out';
end
title(title_text);
colorbar;
%figure;
ica_subplot = subplot(11,1,8:9);
imagesc(EEG_cleared.data);
colormap jet
caxis([-100 100])
set(gca,'XTick',XTicks)
set(gca,'XTickLabel',XTicketLabels)
if (~isempty(MARAParams))
    if strcmp(EEG.automagic.mara.performed, 'FAILED')
        title_text = '\color{red}ICA FALIED';
        cla(ica_subplot)
    else
        title_text = 'ICA corrected clean data';
    end
elseif(~isempty(RPCAParams))
    title_text = 'RPCA corrected clean data';
else
    title_text = '';
end
title(title_text)
colorbar;
%figure;
if( ~isempty(fieldnames(RPCAParams)) && (isempty(RPCAParams.lambda) || RPCAParams.lambda ~= -1))
    subplot(11,1,10:11)
    imagesc(pca_noise);
    colormap jet
    caxis([-100 100])
    XTicks = 0:length(EEG.data)/5:length(EEG.data) ;
    XTicketLabels = round(0:length(EEG.data)/EEG.srate/5:length(EEG.data)/EEG.srate);
    set(gca,'XTick',XTicks)
    set(gca,'XTickLabel',XTicketLabels)
    title('RPCA noise')
    colorbar;
end

if isempty(FilterParams.high)
    annotation('textbox', [0.3, 0.2, 0, 0], 'string', 'No high-pass filter selected. Plotting with 1Hz by default','FitBoxToText','on');
end

% Pot a seperate figure for only the original filtered data
fig2 = figure('visible', 'off');
ax = gca;
outerpos = ax.OuterPosition;
ti = ax.TightInset;
left = outerpos(1) + ti(1) * 1.5;
bottom = outerpos(2);
ax_width = outerpos(3) - ti(1) - ti(3) * 1.5;
ax_height = outerpos(4) - ti(2) * 0.5 - ti(4);
ax.Position = [left bottom ax_width ax_height];
set(gcf, 'Color', [1,1,1])
imagesc(EEG_filtered_toplot.data);
colormap jet
caxis([-100 100])
set(ax,'XTick', XTicks)
set(ax,'XTickLabel', XTicketLabels)
title_str = [num2str(plot_FilterParams.high.freq) ' Hz High pass filtered EEG data'];
title(title_str, 'FontSize', 10)
colorbar;

varargout{1} = fig1;
varargout{2} = fig2;
