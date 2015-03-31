## Setup the Nova.el.physiology Box

1. Download Virtual Box 

Virtual box is a machine virtualizer that we will use to set up a box that will be used to compile and use the physionet toolbox. 

Download from: [Link](https://www.virtualbox.org/wiki/Downloads)

2. Download the iso from Ubuntu (or Lubuntu)

3. Open a console and execute
 * sudo apt-get install gcc libcurl4-openssl-dev perl make 

4. Install wfdb (following link: 
http://physionet.org/physiotools/wfdb-linux-quick-start.shtml) some commands need sudo powers.

5. Test the download of a signals with:
 * rdsamp -r mitdb/100 >100.txt 

We are asking for the full datset caled 100 on the mitdb to be saved on a local file "100.txt". 

