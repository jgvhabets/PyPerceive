#!/usr/bin/env bash
ID=${1?Error: no ID given}
rm -r /mnt/e/ReTune/tmp_dcm2bids/*
rmdir /mnt/e/ReTune/tmp_dcm2bids/
dcm2bids -d /mnt/e/ReTune/sourcedata/DICOM/ -o /mnt/e/ReTune/ -p $ID -s preDBS001 -c /mnt/e/ReTune/code/ReTune_dcm2bids_preop_mri.json --clobber;
dcm2bids -d /mnt/e/ReTune/sourcedata/DICOM/ -o /mnt/e/ReTune/ -p $ID -s preDBS001 -c /mnt/e/ReTune/code/ReTune_dcm2bids_preop_mri.json --clobber;
dcm2bids -d /mnt/e/ReTune/sourcedata/DICOM/ -o /mnt/e/ReTune/ -p $ID -s postDBS001 -c /mnt/e/ReTune/code/ReTune_dcm2bids_postop_ct.json --clobber;
dcm2bids -d /mnt/e/ReTune/sourcedata/DICOM/ -o /mnt/e/ReTune/ -p $ID -s postDBS001 -c /mnt/e/ReTune/code/ReTune_dcm2bids_postop_ct.json --clobber;
mkdir /mnt/e/ReTune/sub-$ID/sourcedata/DICOM/
cp /mnt/e/ReTune/sourcedata/DICOM/* /mnt/e/ReTune/sub-$ID/sourcedata/DICOM/
rm /mnt/e/ReTune/sourcedata/DICOM/*
rm -r /mnt/e/ReTune/tmp_dcm2bids/*
rmdir /mnt/e/ReTune/tmp_dcm2bids/
