This project demonstrates automation techniques using Google services. It includes scripts and configurations to automate various tasks.
Project Structure

    base/: Core scripts and base configurations as well as driver utility file used to build automation.
    config/: Configuration file for different environments.
    pages/: Scripts related to web page interactions.
    testFiles/: Test files for automation testing.
    utilities/: Utility scripts and helper functions.

Requirements
    Python 3.x

Setup

    Clone the repository:
bash
git clone https://github.com/LoganUlabarro/university_of_colorado_boulder_practical.git

Install dependencies:
bash
pip install -r requirements.txt

Usage
    You can run locally by opening with cmd and running 'Pytest -s -v testFiles/university_of_colorado_demo.py'
    alternatively you can set up docker and run in a container (but it's not currently set up to run in headless so I wouldn't recommend it)

License
This project is licensed under the MIT License.
