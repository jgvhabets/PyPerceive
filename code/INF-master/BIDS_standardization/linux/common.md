
**freesurfer recon-all**
*recon-all -i image.nii -s 001 -all*

**BIH cluster wiki**
https://github.com/bihealth/bih-cluster/wiki

**Convert Putty key to linux**

To generate the private key:

cd ~
puttygen id_dsa.ppk -O private-openssh -o id_dsa

and to generate the public key:

puttygen id_dsa.ppk -O public-openssh -o id_dsa.pub

Move these keys to ~/.ssh and make sure the permissions are set to private for your private key:

mkdir -p ~/.ssh
mv -i ~/id_dsa* ~/.ssh
chmod 600 ~/.ssh/id_dsa
chmod 666 ~/.ssh/id_dsa.pub

If you have already tried to perform a 'git clone' operation you might need to do this also
chmod 666 ~/.ssh/known_hosts

**Connect to cluster**

ctivating your Key in the SSH Key Agent

Activate the key (if this is your first SSH key then it will be enabled by default) by making sure ssh-agent runs in the background

# eval "$(ssh-agent -s)"

and adding the key

# ssh-add

or if you created another key, specify the file name, e.g. ~/.ssh/mdc_id_rsa

# ssh-add ~/.ssh/mdc_id_rsa

 ssh -A -t -l <USERNAME> med-login<X>.bihealth.org

 

