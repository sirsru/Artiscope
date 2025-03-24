![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Status](https://img.shields.io/badge/Stable-green.svg)

**ARTISCOPE**
======================
**About Artiscope**
======================
Artiscope is a python based ascii internet browser capable of rendering art from websites and allowing you to browse further through the website. This project is meant to be lightweight, with the ultimate goal being able to use a browser on a pi zero w at a fast speed!

![image](https://github.com/user-attachments/assets/bb35d689-9d4a-49d1-a516-6e8a018628ab)


**examples**
======================
Here are some example websites being rendered.
websites in this order:

*github.com*

*python.org*

*newgrounds.com*

***github***
-------------------
![image](https://github.com/user-attachments/assets/2b1ccce0-c19d-492e-9aa5-fa0183bdd2c7)
![image](https://github.com/user-attachments/assets/eaa1fd75-92dd-4f68-928d-3ee7ae229ae7)



***python.org***
---------------------
![image](https://github.com/user-attachments/assets/4879321e-7eab-43c8-ac4b-12998aadbd1b)
![image](https://github.com/user-attachments/assets/4363a0d5-f0a2-44d2-b398-aa235caff0e2)



***newgrounds.com***
---------------------
![image](https://github.com/user-attachments/assets/13237c89-90a2-4e64-ab5f-372c1c82200f)


**install**
===============

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


**Further use**
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


**settings**
----------------------
The settings menu for Artiscope can be accessed from the main menu, in which you can change the ascii image resolution and size, allowed image formats, and similar image toggle.

![image](https://github.com/user-attachments/assets/f04666f0-103f-4af8-baba-f788c8c8a40a)

**How to use**
======================
**Go to link #** - input a links number that was output earlier

**Enter another URL** - enter a different URL

**Go back to the Main Menu** - goes back to the homescreen with settings and other options

**Browse the web** - prompts you for a URL along with other options


