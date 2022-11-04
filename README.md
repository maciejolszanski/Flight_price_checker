# Flight Price Checker

The name says everything :D


In version 1.0 i plan only to check flights to Barcelona between fixed dates. I plan to visit FC Barcelona match during that weekend and I am looking for the best fligt prices ;)

## How to use
### 1. Download this repository to your local machine

### 2. Create and activate virtual environment
In the console, navigate to the location of the repository files and type:
```python -m venv env```. "env" is a name of your virtual environment, you can change it as you wish.

To activate this environment type one of the following (depending on you OS)
* On Unix or MacOS, using the bash shell: ```source /path/to/venv/bin/activate```
* On Unix or MacOS, using the csh shell: ```source /path/to/venv/bin/activate.csh```
* On Unix or MacOS, using the fish shell: ```source /path/to/venv/bin/activate.fish```
* On Windows using the Command Prompt: ```path\to\venv\Scripts\activate.bat```
* On Windows using PowerShell: ```path\to\venv\Scripts\Activate.ps1```

### 3. Install dependencies
With your venv activated, type ```pip install requirements.txt```. This command will install all required python modules.

### 4. Install web driver
To let Selenium work. There has to be a web driver installed in your machine. Each browser needs different driver. Here are the links to most popular ones:
* Chrome:	https://sites.google.com/chromium.org/driver/
* Edge:	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
* Firefox:	https://github.com/mozilla/geckodriver/releases

The web driver has to be installed in PATH or its location should be specified in the code (if you choose the second option you will have to edit ```flights.py```). If you use browser other than Edge, then you should change the line 223 ```driver = webdriver.Edge()```.

For more information about drivers please refer the official documentation https://www.selenium.dev/documentation/webdriver/getting_started/

### 5. Run code
Python file responsible for web scraping is ```flights.py```. Run it and wait until the web scraping is done - in the terminal will appear following text:
```
-----------------------------
Web Scraping: SUCCEEDED
Unable to read 0 flights data
-----------------------------
Writing Data to File: SUCCEEDED
-----------------------------
```

There will be created a new directry named ```\data``` and a file inside it named ```flights_data.json```. This file contains all data from the begginning of your web scraping. You can use it to do analysis on your own or use my Jupyter notebook named  ```visualize.ipynb```.
