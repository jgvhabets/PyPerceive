%% Initialize settings
clear all, close all, clc

% Add Fieldtrip to path
% https://www.fieldtriptoolbox.org/
addpath(fullfile('C:\Users\richa\GitHub\fieldtrip\'));
ft_defaults

% Add WJN toolbox (optional, for viewing data)
% https://github.com/neuromodulation/wjn_toolbox 
addpath(fullfile('C:\Users\richa\GitHub\wjn_toolbox\'));

%% Select file, read data with Fieldtrip and inspect data with WJN Toolbox
file = 'sub-000_EphysMedOff01_task-Rest_acq-StimOn_run-01.DATA.Poly5';
cfg            = [];
cfg.dataset    = [file];
cfg.continuous = 'yes';
data = ft_preprocessing(cfg);

wjn_plot_raw_signals(data.time{1},data.trial{1},data.label);

%% Pick only channels to keep and re-read data
% Channel 27 is empty so let's exclude it. 
chans          = [[1:26] [28:33]];
cfg            = [];
cfg.dataset    = [file];
cfg.continuous = 'yes';
cfg.channel    = chans;
data = ft_preprocessing(cfg);

%% Rename channels according to ReTune standard and set chantypes/-units
ch_names = {
        'LFP_R_1_STN_MT'
        'LFP_R_2_STN_MT'
        'LFP_R_3_STN_MT'
        'LFP_R_4_STN_MT'
        'LFP_R_5_STN_MT'
        'LFP_R_6_STN_MT'
        'LFP_R_7_STN_MT'
        'LFP_R_8_STN_MT'
        'LFP_L_1_STN_MT'
        'LFP_L_2_STN_MT'
        'LFP_L_3_STN_MT'
        'LFP_L_4_STN_MT'
        'LFP_L_5_STN_MT'
        'LFP_L_6_STN_MT'
        'LFP_L_7_STN_MT'
        'LFP_L_8_STN_MT'
        'ECOG_R_1_SMC_AT'
        'ECOG_R_2_SMC_AT'
        'ECOG_R_3_SMC_AT'
        'ECOG_R_4_SMC_AT'
        'ECOG_R_5_SMC_AT'
        'ECOG_R_6_SMC_AT'
        'EEG_Cz_TM'
        'EEG_Fz_TM'
        'EMG_R_BR_TM'
        'EMG_L_BR_TM'
        'ACC_R_X_D2_TM'
        'ACC_R_Y_D2_TM'
        'ACC_R_Z_D2_TM'
        'ACC_L_X_D2_TM'
        'ACC_L_Y_D2_TM'
        'ACC_L_Z_D2_TM'
        }
data.label          = ch_names;
data.hdr.nChans     = length(ch_names);
data.hdr.label      = data.label;
% Set channel types and channel units
chantype            = cell(length(ch_names),1);
chantype(1:16)      = {'DBS'};
chantype(17:22)     = {'ECOG'};
chantype(23:24)     = {'EEG'};
chantype(25:26)     = {'EMG'};
chantype(27:end)    = {'MISC'};
data.hdr.chantype   = chantype;
chanunit            = cell(length(ch_names),1);
chanunit(:)         = {'uV'};
data.hdr.chanunit   = chanunit

%% Plot data once more with WJN viewer to double-check for bad channels
wjn_plot_raw_signals(data.time{1},data.trial{1},data.label);

%% Note which channels were bad (e.g. empty) and why
bad = {'LFP_L_1_STN_MT' 'LFP_R_2_STN_MT' 'LFP_R_3_STN_MT' 'LFP_R_4_STN_MT'};
why = {'Reference electrode' 'Stimulation contact' 'Stimulation contact' 'Stimulation contact'};

bads = cell(length(ch_names),1);
bads(:) = {'good'};
bads_descr = cell(length(ch_names),1);
bads_descr(:) = {'n/a'};
for k=1:length(ch_names)
    if ismember(ch_names{k}, bad)
        bads{k} = 'bad';
        bads_descr{k} = why{find(strcmp(bad,ch_names{k}))};
    end
end

%% Initalize containers with task keys, descriptions and instructions
keySet = {'Rest', 'SelfpacedRotationL','SelfpacedRotationR',...
    'BlockRotationL','BlockRotationR', 'Evoked', 'SelfpacedSpeech',...
    'ReadRelaxMoveL'};
descrSet = {'Rest recording', ...
    'Selfpaced left wrist rotations performed on custom-built analog rotameter which translates degree of rotation to volt.',...
    'Selfpaced right wrist rotations performed on custom-built analog rotameter which translates degree of rotation to volt.',...
    'Blocks of 30 seconds of rest followed by blocks of 30 seconds of continuous wrist rotation performed on a custom-built rotameter which translates degree of rotation to volt. Performed with the left hand.',...
    'Blocks of 30 seconds of rest followed by blocks of 30 seconds of continuous wrist rotation performed on a custom-built rotameter which translates degree of rotation to volt. Performed with the right hand.',...
    'Evoked potentials recording. Single stimulation pulses of fixed amplitude following periods of high frequency stimulation with varying amplitude (0, 1.5 and 3 mA) per block.',...
    'Selfpaced reading aloud of the fable ''The Parrot and the Cat'' by Aesop. Extended pauses in between sentences.',...
    'Block of 30 seconds of continuous left wrist rotation performed on a custom-built rotameter which translates degree of rotation to volt followed by a block of 30 seconds of rest followed by a block of 30 seconds of reading aloud (''The Parrot and the Cat'' by Aesop). Multiple sets.'};
instructionSet = {'Do not move or speak and keep your eyes open.',...
    'Perform 50 wrist rotations with your left hand with an interval of about 10 seconds. Do not count in between rotations.',...
    'Perform 50 wrist rotations with your right hand with an interval of about 10 seconds. Do not count in between rotations.',...
    'Upon the auditory command "start", perform continuous wrist rotations with your left hand, until you perceive the auditory command "stop". Perform these wrist rotations as fast as possible and with the largest possible amplitude.',...
    'Upon the auditory command "start", perform continuous wrist rotations with your right hand, until you perceive the auditory command "stop". Perform these wrist rotations as fast as possible and with the largest possible amplitude.',...
    'Do not move or speak and keep your eyes open.',...
    'Read aloud sentence by sentence the text in front of you. Leave a pause of several seconds in between sentences.',...
    'At the beginning of each block, a text will appear on the screen, specifying the task to be performed. An auditory cue will then be issued, marking the begin of your task. Perform the task until the next cue marks the end of the task. Tasks are either continuous left wrist rotation, resting with open eyes or reading aloud the text displayed on the screen.'}
task_descr = containers.Map(keySet,descrSet)
task_instr = containers.Map(keySet,instructionSet)

%% Now write data to BIDS
% Initialize a 'n/a' variable just for practicality
n_a = repmat({'n/a'},length(ch_names),1);

% This is the output root folder for our BIDS-dataset
%rawdata_root = 'C:\Users\richa\OneDrive - Charité - Universitätsmedizin Berlin\LFP-Labor\Data\BIDS_rawdata'

cfg = [];
cfg.method                  = 'convert';
% Enter the output folder for your BIDS dataset here
mkdir 'BIDS_Berlin_ECOG_LFP'
cfg.bidsroot                = 'BIDS_Berlin_ECOG_LFP';
cfg.datatype                = 'ieeg';
cfg.sub                     = '001';
cfg.ses                     = 'EphysMedOff01';
cfg.task                    = 'Rest';
cfg.acq                     = 'StimOn';
cfg.run                     = '01';

% Provide info for the scans.tsv file
cfg.scans.acq_time              = '2021-01-01T12:00:21';
if contains(cfg.ses, 'Off')
    cfg.scans.medication_state  = 'OFF';
else
    cfg.scans.medication_state  = 'ON';
end

% Specify some general information
cfg.InstitutionName                         = 'Charite - Universitaetsmedizin Berlin, corporate member of Freie Universitaet Berlin and Humboldt-Universitaet zu Berlin, Department of Neurology with Experimental Neurology/BNIC, Movement Disorders and Neuromodulation Unit';
cfg.InstitutionAddress                      = 'Chariteplatz 1, 10117 Berlin, Germany';
cfg.dataset_description.Name                = 'BIDS_Berlin_LFP_ECOG_PD';
cfg.dataset_description.BIDSVersion         = '1.5.0';
cfg.dataset_description.License             = 'n/a';
cfg.dataset_description.Funding             = [['Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - Project-ID 424778381 - TRR 295']];
cfg.dataset_description.Authors             = {'Johannes Busch', 'Meera Chikermane', 'Katharina Faust', 'Lucia Feldmann', 'Richard Koehler', 'Andrea Kuehn', 'Roxanne Lofredi', 'Timon Merk', 'Wolf-Julian Neumann', 'Gerd-Helge Schneider', 'Ulrike Uhlig','Jonathan Vanhoecke'};
cfg.dataset_description.Acknowledgements    = 'Special thanks to Ulrike Uhlig for their help in recording the data.';

% Provide the long description of the task and participant instructions
cfg.TaskName                = cfg.task;
cfg.TaskDescription         = task_descr(cfg.task);
cfg.Instructions            = task_instr(cfg.task);

% Provide info about recording hardware
manufacturer                        = 'TMSi';
if manufacturer == 'TMSi'
    cfg.Manufacturer                = 'Twente Medical Systems International B.V. (TMSi)';
    cfg.ManufacturersModelName      = 'Saga 64+';
    cfg.SoftwareVersions            = 'TMSi Polybench - QRA for SAGA - REV1.0.0';
    cfg.DeviceSerialNumber          = '1005190056';
else
    disp('No valid manufacturer found.')
    cfg.Manufacturer                = 'n/a';
    cfg.ManufacturersModelName      = 'n/a';
    cfg.SoftwareVersions            = 'n/a';
    cfg.DeviceSerialNumber          = 'n/a';
end

% Provide info about the participant	
cfg.participants.sex                    = 'male';
cfg.participants.handedness             = 'left';
cfg.participants.age                    = 60;
cfg.participants.date_of_implantation   = '2020-12-31T00:00:00';
cfg.participants.UPDRS_III_preop_OFF    = 'n/a';
cfg.participants.UPDRS_III_preop_ON     = 'n/a';
cfg.participants.disease_duration       = 'n/a';
cfg.participants.PD_subtype             = 'akinetic-rigid';
cfg.participants.symptom_dominant_side  = 'right';
cfg.participants.LEDD                   = 'n/a';

% Provide info about the DBS lead
cfg.participants.DBS_target                 = 'STN';
cfg.participants.DBS_manufacturer           = 'Medtronic';
cfg.participants.DBS_model                  = 'SenSight';
cfg.participants.DBS_directional            = 'yes';
cfg.participants.DBS_contacts               = 8;
cfg.participants.DBS_description            = '8-contact, directional DBS lead.';

% Provide info about the ECOG electrode
cfg.participants.ECOG_target                = 'sensorimotor cortex';
cfg.participants.ECOG_hemisphere            = 'right';
cfg.participants.ECOG_manufacturer          = 'Ad-Tech';
cfg.participants.ECOG_model                 = 'TS06R-AP10X-0W6';
cfg.participants.ECOG_location              = 'subdural';
cfg.participants.ECOG_material              = 'platinum';
cfg.participants.ECOG_contacts              = 6;
cfg.participants.ECOG_description           = '6-contact, 1x6 narrow-body LTM strip. Platinum contacts, 10mm spacing';

% Provide info for the coordsystem.json file
cfg.coordsystem.IntendedFor                         = "n/a"; % OPTIONAL. Path or list of path relative to the subject subfolder pointing to the structural MRI, possibly of different types if a list is specified, to be used with the MEG recording. The path(s) need(s) to use forward slashes instead of backward slashes (e.g. "ses-<label>/anat/sub-01_T1w.nii.gz").
cfg.coordsystem.iEEGCoordinateSystem                = "Other"; % REQUIRED. Defines the coordinate system for the iEEG electrodes. See Appendix VIII for a list of restricted keywords. If positions correspond to pixel indices in a 2D image (of either a volume-rendering, surface-rendering, operative photo, or operative drawing), this must be "Pixels". For more information, see the section on 2D coordinate systems
cfg.coordsystem.iEEGCoordinateUnits	                = "mm"; % REQUIRED. Units of the _electrodes.tsv, MUST be "m", "mm", "cm" or "pixels".
cfg.coordsystem.iEEGCoordinateSystemDescription	    = "MNI152 2009b NLIN asymmetric T2 template"; % RECOMMENDED. Freeform text description or link to document describing the iEEG coordinate system system in detail (e.g., "Coordinate system with the origin at anterior commissure (AC), negative y-axis going through the posterior commissure (PC), z-axis going to a mid-hemisperic point which lies superior to the AC-PC line, x-axis going to the right").
cfg.coordsystem.iEEGCoordinateProcessingDescription = "Co-registration, normalization and electrode localization done with Lead-DBS"; % RECOMMENDED. Has any post-processing (such as projection) been done on the electrode positions (e.g., "surface_projection", "none").
cfg.coordsystem.iEEGCoordinateProcessingReference	= "Horn, A., Li, N., Dembek, T. A., Kappel, A., Boulay, C., Ewert, S., et al. (2018). Lead-DBS v2: Towards a comprehensive pipeline for deep brain stimulation imaging. NeuroImage."; % RECOMMENDED. A reference to a paper that defines in more detail the method used to localize the electrodes and to post-process the electrode positions. .

% Provide columns in the electrodes.tsv
% REQUIRED. Name of the electrode
sens.label      = {    
        'LFP_R_1_STN_MT',
        'LFP_R_2_STN_MT',
        'LFP_R_3_STN_MT',
        'LFP_R_4_STN_MT',
        'LFP_R_5_STN_MT',
        'LFP_R_6_STN_MT',
        'LFP_R_7_STN_MT',
        'LFP_R_8_STN_MT',
        'LFP_L_1_STN_MT',
        'LFP_L_2_STN_MT',
        'LFP_L_3_STN_MT',
        'LFP_L_4_STN_MT',
        'LFP_L_5_STN_MT',
        'LFP_L_6_STN_MT',
        'LFP_L_7_STN_MT',
        'LFP_L_8_STN_MT',
        'ECOG_R_1_SMC_AT',
        'ECOG_R_2_SMC_AT',
        'ECOG_R_3_SMC_AT',
        'ECOG_R_4_SMC_AT',
        'ECOG_R_5_SMC_AT',
        'ECOG_R_6_SMC_AT'};
% Electrode positions are imported to MatLab from external files (e.g. 
% Lead-DBS ea_reconstruction.mat and MNI_coords.txt) and a 'sens' FieldTrip 
% struct is created(see: 
% https://www.fieldtriptoolbox.org/reference/ft_datatype_sens/)
reco = load('ea_reconstruction.mat');
sub000MNIcoords = load('MNI_coords.txt');
sens.chanpos = [
    reco.reco.mni.coords_mm{1}; ...
    reco.reco.mni.coords_mm{2}; ...
    sub000MNIcoords];
sens.elecpos = [
    reco.reco.mni.coords_mm{1}; ...
    reco.reco.mni.coords_mm{2}; ...
    sub000MNIcoords];
cfg.elec     = sens;

cfg.electrodes.name = sens.label;
% These are the surfaces of our electrode contacts (MedTronic Sensight and
% Ad-Tech 1x6 subdural strip)
cfg.electrodes.size         = {
    6 1.5 1.5 1.5 1.5 1.5 1.5 6 ...
    6 1.5 1.5 1.5 1.5 1.5 1.5 6 ...
    12.57 12.57 12.57 12.57 12.57 12.57};
% RECOMMENDED. Material of the electrode, e.g., Tin, Ag/AgCl, Gold
cfg.electrodes.material     = [
    repmat({'platinum/iridium'},16,1); 
    repmat({'platinum'},6,1)];
cfg.electrodes.manufacturer = [
    repmat({'Medtronic'},16,1);
    repmat({'Ad-Tech'},6,1)];
cfg.electrodes.group        = [
    repmat({'DBS_right'},8,1);
    repmat({'DBS_left'},8,1);
    repmat({'ECOG_strip'},6,1)];
% 'R' for right, 'L' for left
cfg.electrodes.hemisphere   = [
    repmat({'R'},8,1);
    repmat({'L'},8,1);
    repmat({'R'},6,1)];
% RECOMMENDED. Type of the electrode (e.g., cup, ring, clip-on, wire, needle)
cfg.electrodes.type         = [  
    repmat({'depth'},16,1);
    repmat({'strip'},6,1)];
% RECOMMENDED. Impedance of the electrode in kOhm
cfg.electrodes.impedance    = repmat({'n/a'},length(sens.label),1);  
cfg.electrodes.dimension    = [  
    repmat({'[1x8]'},16,1);
    repmat({'[1x6]'},6,1)];
% Provide info about our channels
cfg.channels.name               = ch_names;
cfg.channels.type               = chantype;
cfg.channels.units              = chanunit;
% Provide sampling frequency
sf = cell(length(ch_names),1);
sf(:) = {data.fsample};
cfg.channels.sampling_frequency = sf;
% Filter settings (here all 'n/a' because no filters were applied during
% recording
cfg.channels.low_cutoff         = n_a;
cfg.channels.high_cutoff        = n_a;
cfg.channels.notch              = n_a;
cfg.channels.reference          = n_a;
cfg.channels.group              = n_a;
% Here bad channels are stated
cfg.channels.status             = bads;
cfg.channels.status_description = bads_descr;

% these are iEEG specific
cfg.ieeg.PowerLineFrequency     = 50;
cfg.ieeg.iEEGReference          = 'LFP_L_1_STN_MT';
cfg.ieeg.iEEGGround             = 'Right shoulder patch';
cfg.ieeg.iEEGPlacementScheme    = 'Right subdural cortical strip and bilateral subthalamic nucleus (STN) deep brain stimulation (DBS) leads.';
cfg.ieeg.iEEGElectrodeGroups    = 'ECOG_strip: 1x6 AdTech strip on right sensorimotor cortex, DBS_left: 1x8 Medtronic directional DBS lead (SenSight) in left STN, DBS_right: 1x8 Medtronic directional DBS lead (SenSight) in right STN.';
cfg.ieeg.SoftwareFilters        = {'None'};
cfg.ieeg.HardwareFilters        = {'None'};
cfg.ieeg.RecordingType          = 'continuous';
cfg.ieeg.ElectricalStimulation  = true;
if cfg.ieeg.ElectricalStimulation
    % Enter current EXPERIMENTAL stimulation settings
    exp.DateOfSetting           = "2021-01-01";
    exp.StimulationTarget       = "STN";
    exp.StimulationMode         = "continuous";
    exp.StimulationParadigm     = "continuous stimulation";
    exp.SimulationMontage       = "monopolar";
    % We stimulated only the right hemisphere
    L                           = "OFF";
    exp.Left                    = L;
    R.AnodalContact             = "G";
    % We stimulated with the three lowermost directional contacts
    R.CathodalContact           = "2, 3 and 4";
	R.AnodalContactDirection      = "none";
	R.CathodalContactDirection    = "omni";
	R.CathodalContactImpedance    = "n/a";
	R.StimulationAmplitude        = 1.5;
	R.StimulationPulseWidth       = 60;
	R.StimulationFrequency        = 130;
	R.InitialPulseShape           = "rectangular";
	R.InitialPulseWidth           = 60;
	R.InitialPulseAmplitude       = -1.5;
	R.InterPulseDelay             = 0;
	R.SecondPulseShape            = "rectangular";
	R.SecondPulseWidth            = 60;
	R.SecondPulseAmplitude        = 1.5;
    R.PostPulseInterval           = "n/a";
    exp.Right                     = R;
    
    % Enter best CLINICAL stimulation settings
    clin.DateOfSetting            = "2021-01-01";
    clin.StimulationTarget        = "STN";
    clin.StimulationMode          = "continuous";
    clin.StimulationParadigm      = "continuous stimulation";
    clin.SimulationMontage        = "monopolar";
    L                             = "OFF";
    clin.Left                     = L;
    R.AnodalContact               = "G";
    R.CathodalContact             = "2, 3 and 4";
	R.AnodalContactDirection      = "none";
	R.CathodalContactDirection    = "omni";
	R.CathodalContactImpedance    = "n/a";
	R.StimulationAmplitude        = 1.5;
	R.StimulationPulseWidth       = 60;
	R.StimulationFrequency        = 130;
	R.InitialPulseShape           = "rectangular";
	R.InitialPulseWidth           = 60;
	R.InitialPulseAmplitude       = -1.5;
	R.InterPulseDelay             = 0;
	R.SecondPulseShape            = "rectangular";
	R.SecondPulseWidth            = 60;
	R.SecondPulseAmplitude        = 1.5;
    R.PostPulseInterval           = "n/a";
    clin.Right                    = R;
    
    % LFP recording was performed before clinical optimization of DBS 
    % settings, so we set Best Clinical 
    param.BestClinicalSetting                = "n/a";
    param.CurrentExperimentalSetting         = exp;
    cfg.ieeg.ElectricalStimulationParameters = param;
end

% Now convert data to BIDS !
% https://www.fieldtriptoolbox.org/reference/data2bids/
data2bids(cfg, data);
