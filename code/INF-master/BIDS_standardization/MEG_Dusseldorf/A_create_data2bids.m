%% BIDS Standard IKN MEG Lab Duesseldorf
% Mona Plettenberg, Bahne Bahners,... (2021)
clear variables;

%% Fields to fill %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
met= 'copy';    % 'copy' or 'decorate'
% 'copy'            creates a new bids structure and copies the raw fif
%                   files to bids structure, thereby creating meg.json file
% 'decorate'        add information to json files in existing bids
%                   structure or add/complete participants.tsv
%directories%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
direc='E:/SFB_DATA/DUS013/meg/'; % raw data directory
bidsfolder='E:/SFB_DATA/BIDSraw/raw_data';  %top level directory for the BIDS output
load('E:/SFB_DATA/bids/filenamingscheme.mat');
addpath C:/fieldtrip ;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%obligatory information%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
subind              = 1:6 ; % indices of Subject ID in filename (e.g. DUS013_OFF_stim-01.fif)
taskname            = 'RestDBS'; %task name string
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

taskdescription ='In this experiment, patients with Parkinson s Disease (PD) and an implanted Deep Brain Stimulation (DBS) electrode inside the subthalamic nucleus (STN) were asked to sit relaxed in the MEG scanner with their eyes open and to fixate a cross. During each run of 40 seconds a low-frequency stimulation of 6 Hz was applied at a certain contact of the DBS electrode (specified under DBS.CurrentExperimentalSetting.Left.CathodalContact) and in a certain direction with a certain amplitude and pulse width (specified under DBS.CurrentExperimentalSetting.Left.StimulationAmplitude / .StimulationPulseWidth).';
acqlabel        ='StimONL'; %optional label (string)
eeg             ='yes'; % if eeg was coregistiered
description     = 'no'; % set to 'yes' if you want a dataset description written.
dbs             = 'yes'; % set to 'yes' if you want to add DBS information.
cat     = '3'; % cathodal contact

participants    = 'no';
% age         =  75;
% sex         = 'm';
% device      = 'Abbott Infinity'; %dbs device
% pdduration  = 8 ; % Parkinsons duration in years
% dbsduration = 2 ; % time since DBS surgery in years

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   sub-        label is taken from the filename taking the indices (subind)
%               specified above.
%   ses-        label is taken from filename if it contains OFF or ON
%               as Medication state. If these labels do not occur in the
%               filename, the session label is the date, the file is
%               saved (CAVE: as soon as  the file is transferred, recording
%               date and time do not match saving date anymore). This date
%               is however also used for the scans.tsv.
%   task-       label is specified above and obligatory to construct the
%               BIDS file name
%   run-        extracts run number from filename using different indices
%               for ON and OFF (DUS013_OFF_stim02.fif / DUS013_ON_stim02.fif)
%
%
%% TODO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1) extract actual measurement date/recording date
% 2) add medication state variable instead of reading it from file name as
% an additional option
% 3) Add prompts for session specific information ( subject/DBS
% information)
% 4) Add automated Experimental DBS settings information via table
% /filename (TRR295) (Check!)
% 5) Extract Hardware Filters from .fif file (hdr.orig)
% 6) Extract Information for
%  cfg.DigitizedLandmarks          = 'true';
%  cfg.DigitizedHeadPoints         = 'true';
%  cfg.RecordingType               = 'continuous';
%  cfg.ContinuousHeadLocalization  = 'false';
% 7) Implement 'decorate' option for the script (See if loops below).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% START
% add your fieldtrip
ft_defaults;
if contains(met,'decorate')
find(contains(bidsfolder,subind))
end
bidslist= dir(bidsfolder)
datlist= dir(direc);
for i=3:5;%length(datlist)
    %General Information
    
    cfg.method                  = met; %'decorate'; %string, can be 'decorate', 'convert' or 'copy', see below (default is automatic), convert does not
    %for Neuromag, use system
    %specific tool
    cfg.dataset                 = fullfile(direc,datlist(i).name) ;      %string, filename and directory of the input data
    %cfg.dataset                 = '/data/project/pathos/dbs_freq/rest/dacq/sub-03/ses-01/meg/run-01/sub-03_ses-01_task-rest_run-freq1_meg.fif' ; %for decorating
    if contains(cfg.method, 'decorate')
        cfg.dataset                 =  bidsfolder;
        cfg.outputfile              =  bidsfolder; %string, optional filename and directory for the output data
        cfg.writejson               = 'yes';
    else
        %cfg.mri.deface              = string, 'yes' or 'no' (default = 'no')
        %cfg.mri.writesidecar        = string, 'yes', 'replace', 'merge' or 'no' (default = 'yes')
        cfg.meg.writesidecar        = 'yes';
        cfg.events.writesidecar     = 'yes';  %'yes', 'replace', 'merge' or 'no' (default = 'yes')
        cfg.coordystem.writesidecar = 'yes'; %, 'yes', 'replace', 'merge' or 'no' (default = 'yes')
        cfg.channels.writesidecar   = 'yes';
    end
    
    
    %Output Information
    %subdirectories are created
    cfg.bidsroot                = bidsfolder;
    cfg.sub                     = datlist(i).name(subind); %string, subject name
    
    
    %% session label from filename
    if contains(datlist(i).name, 'ON')
        cfg.ses= 'MedOn'; %string, optional session name
    elseif contains(datlist(i).name,'OFF')
        cfg.ses= 'MedOff';
    else
        ft_warning('data naming seems to be wrong, check whether filenames contain "ON" or "OFF", using date as session label');
        cfg.ses= datestr(datetime(datlist(i).date,'InputFormat','dd-MMMM-yyyy HH:mm:ss','Locale','de_DE','Format','yyyyMMdd'),'yyyyMMdd');
    end
    if contains(datlist(i).name,'ON')
        cfg.run= datlist(i).name(15:16) ;      %number, optional
    elseif contains(datlist(i).name,'OFF')
        cfg.run= datlist(i).name(16:17);
    end
    
    cfg.task                    = taskname;
    cfg.datatype                = 'meg';
    cfg.acq                     = acqlabel;
    %    cfg.ce                      = string
    %    cfg.rec                     = string
    %    cfg.dir                     = string
    %    cfg.mod                     = string
    %    cfg.echo                    = string
    %    cfg.proc                    = string
    %% case empty room
    
    if contains(datlist(i).name,'empty')
        cfg.sub='emptyroom';
        cfg.ses=datestr(datetime(datlist(i).date,'InputFormat','dd-MMMM-yyyy HH:mm:ss','Locale','de_DE','Format','yyyyMMdd'),'yyyyMMdd');
    end
    
    %% Information for participants.tsv
    if contains(participants,'yes')
        cfg.participants.age         =  age;
        cfg.participants.sex         = sex;
        cfg.participants.device      = dbsdevice; %dbs device
        cfg.participants.pdduration  = pdduration; % Parkinsons duration in years
        cfg.participants.dbsduration = dbsduration ; % time since DBS surgery in years
        cfg.participants.predominantside = [];
        cfg.participants.stimulatedcontactleft = [];
        cfg.participants.stimulatedcontactright = [];
        cfg.participants.stimulationleft = [];
        cfg.participants.stimulationright = [];
    end
    
    
    %% Information for scans.tsv
    
    cfg.scans.acq_time           = datlist(i).date;%'2019-09-20T15:13:38'; %string, should be formatted according to  RFC3339 as '2019-05-22T15:13:38'
    %    cfg.scans.eo                 = '5 min';
    %    cfg.scans.ec                 = '5 min';
    
    % Information for events.tsv
    % trl = [0 300 0; 305 420 305];
    % cfg.events.trl = trl; % Problem trl nicht definiert in line 1106
    
    
    
    %% General Information
    % General BIDS options that apply to all data types are
    cfg.InstitutionName             = 'Heinrich-Heine-University, Institute of Clinical Neuroscience and Medical Psychology';
    cfg.InstitutionAddress          = 'Moorenstrasse 5, 40225 Düsseldorf';
    cfg.Manufacturer                = 'Neuromag/Elekta/MEGIN';
    cfg.ManufacturersModelName      = 'ElektaVectorview';
    cfg.DeviceSerialNumber          = '3042';
    %    cfg.SoftwareVersions            = string
    cfg.PowerLineFrequency          = 50;
    cfg.DewarPosition               = 'upright';
    cfg.SoftwareFilters             = 'n/a';
    cfg.HardwareFilters             = 'n/a';
    cfg.DigitizedLandmarks          = 'true';
    cfg.DigitizedHeadPoints         = 'true';
    cfg.RecordingType               = 'continuous';
    cfg.ContinuousHeadLocalization  = 'false';
    cfg.HeadCoilFrequency           = [];
    cfg.AssociatedEmptyRoom         = [];
    
    
    %% MEEG Information (combined MEG+EEG Recordings)
    
    if contains(eeg, 'yes')
        cfg.EEGSamplingFrequency       = []; % equal to MEG sampling frequency
        cfg.EEGPlacementScheme         = ['Fz','C3', 'Cz', 'C4', 'P3', 'Pz', 'P4', 'Oz'];
        cfg.CapManufacturer            = 'n/a';
        cfg.CapManufacturersModelName  ='n/a';
        cfg.EEGReference               = 'frontal';
    end
    
    %% DBS Settings
    if contains(dbs, 'yes')
        cfg.DBS.Manufacturer='Abbott';
        cfg.DBS.ModelName='Infinity';
        cfg.DBS.StimulationTarget='STN';
        cfg.DBS.StimulationMode='constant current';
        cfg.DBS.CurrentExperimentalSetting.Left.AnodalContact='G';
        cfg.DBS.CurrentExperimentalSetting.Left.CathodalContact=cat;
        cfg.DBS.CurrentExperimentalSetting.Left.CathodalContactDirection=t.Contact(find(contains(t.FileIndex,cfg.run)));
        cfg.DBS.CurrentExperimentalSetting.Left.StimulationAmplitude=t.Amplitude(find(contains(t.FileIndex,cfg.run)));
        cfg.DBS.CurrentExperimentalSetting.Left.StimulationPulseWidth=t.PulseWidth(find(contains(t.FileIndex,cfg.run)));
        cfg.DBS.CurrentExperimentalSetting.Left.StimulationFrequency='6';
    end
    
    %% Dataset Description
    cfg.dataset_description.writesidecar           = description;
    cfg.dataset_description.Name	                = 'sfb_dbs_markers (WP1)';
    cfg.dataset_description.BIDSVersion	        = '1.2.0';
    %      cfg.dataset_description.License	              = string
    cfg.dataset_description.Authors	            = {'Bahne H. Bahners', 'Alfons Schnitzler', 'Esther Florin'};
    %    cfg.dataset_description.Acknowledgements	      = string
    %    cfg.dataset_description.HowToAcknowledge	      = string
    cfg.dataset_description.Funding	              = 'DFG TRR 295'
    %    cfg.dataset_description.ReferencesAndLinks	      = string
    %    cfg.dataset_description.DatasetDOI	              = string
    %
    cfg.TaskName                    = 'RestDBS';
    cfg.TaskDescription             = taskdescription;
    %
    %    cfg.Instructions                = string
    %    cfg.CogAtlasID                  = string
    %    cfg.CogPOID                     = string
    
    data2bids(cfg)
end
