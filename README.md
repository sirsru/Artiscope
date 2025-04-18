![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Status](https://img.shields.io/badge/Stable-green.svg) <br>
Version 1.0.3

**ARTISCOPE**
======================

**About Artiscope**
======================
Artiscope is a python based ascii internet browser capable of rendering art from websites and allowing you to browse further through the website. This project is meant to be lightweight, with the ultimate goal being able to use a browser on a pi zero at a fast speed with a useable interface and results! This feature rich browser even comes with a built in update manager that automatically downloads the newest version of the browser!

**warning**
----------------
some images may not be the most recent ones!

![image](https://github.com/user-attachments/assets/8430fcc7-1009-4a51-a8d7-aacc595f3c37)

Table of contents
-------------------
[about](#About-Artiscope)<br>
[examples](#examples)<br>
[install](#install)<br>
[running Artiscope](#How-to-run)<br>
[settings](#settings)<br>
[how to use](#How-to-use)<br>
[updates](#updates)<br>


**examples**
======================
Here are some example websites being rendered.
websites in this order:

*github.com*

*python.org*

*newgrounds.com*

***github***
-------------------
<img src="https://github.com/user-attachments/assets/2b1ccce0-c19d-492e-9aa5-fa0183bdd2c7" width="400">
<img src="https://github.com/user-attachments/assets/eaa1fd75-92dd-4f68-928d-3ee7ae229ae7" width="400">

***python.org***
---------------------
<img src="https://github.com/user-attachments/assets/4879321e-7eab-43c8-ac4b-12998aadbd1b" width="400">
<img src="https://github.com/user-attachments/assets/4363a0d5-f0a2-44d2-b398-aa235caff0e2" width="300">


***newgrounds.com***
---------------------
<img src="https://github.com/user-attachments/assets/13237c89-90a2-4e64-ab5f-372c1c82200f" width="300">


**install**
===============

Simple way
------------

Now after I Had to install everything multiple times it got pretty annoying, so I made launch files for this browser, I dont know why anyone would use it on windows but thats here too.

>*MacOS or Linux*
>launch the browser using launch.sh <br>
>**Make sure to make the file an executable file!**

>*Windows*
>launch browser using launch.bat


Hard way
-----------

If you dont trust my **.bat** and **.sh** files you can just DIY the setup and launch process.

To install and use Artiscope you need to run these commands.
```
git clone https://github.com/sirsru/Artiscope.git

cd Artiscope

python3 -m venv venv
```
>*windows*
>`venv\Scripts\activate`

>*linux and macos*
>`source venv/bin/activate`

```
pip install -r requirements.txt
python3 browser.py
```

**If you encounter any errors with installing python dependencies use the following**

>`pip install requests`
`pip install beautifulsoup4`
`pip install Pillow`


**How to run**
==========================
After downloading Artiscope and closing it, if you wish to start it again you need to run these commands to start the python environment.

```
cd Artiscope
```
>*windows*
>`venv\Scripts\activate`

>*linux and macos*
>`source venv/bin/activate`

```
python3 browser.py
```
After the original install all updates done to this repository can be done from inside the browser by going to **info and updates** and selecting option 1.

**settings**
----------------------
The settings menu for Artiscope can be accessed from the main menu, in which you can change the ascii image resolution and size, allowed image formats, and similar image toggle.

![image](https://github.com/user-attachments/assets/803ae639-adde-4ca9-86cf-5b10dac16c48)

**How to use**
======================
**Go to link #** - input a links number that was output earlier

**Enter another URL** - enter a different URL

**Go back to the Main Menu** - goes back to the homescreen with settings and other options

**Browse the web** - prompts you for a URL along with other options

**Setting** - allows you to change options in the browser like **themes** and **emoji compatibility**

**Info and updates** - shows you the current version of your browser, allows you to check the newest version of the browser, and download the latest version!


**updates**
======================
Last but not least we have the updates! There is a built in option to update or check if you are up to date in Artiscope! All you have to do to install a new update is go to **info and updates** and choose **Update by cloning github repo** or **Check for update**. You do need to be connected to the internet to update the browser, but lets be honest, what are you using a browser for without internet?
