Install virtual environment
pip install virtualenv
installing on manjaro 
sudo pacman -S python-virtualenv

Create a Virtual Environment:
Navigate to your project directory and run:
virtualenv venv

Activate the Virtual Environment:
On linux
source venv/bin/activate 

To run the file on linux with root privileges
sudo python DosBlockerExample.py

Ensure Your Virtual Environment is Activated:
You should see the name of your virtual environment (e.g., (venv))
at the beginning of your command line prompt. This indicates that 
any Python packages you install will only affect this virtual environment, 
rather than your global Python installation.

To generate a requirements.txt 
pip freeze > requirements.txt

To install all dependencies 
pip install -r requirements.txt

To execute with root privileges
sudo python3 filename.py

To find host private ip address through bash
hostname --i  