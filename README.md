# Pygame Projects
> In this repository, there are a few sample games coded in Pygame as well as some templates to help you get started.

# Installing Python
If you have Python installed on your device, you can skip this step. Otherwise, go to [this website](https://www.python.org/downloads/) to get it installed.

In addition to Python, also install an IDE if you don't have one already. [PyCharm (make sure to scroll down to download community edition)](https://jetbrains.com/pycharm/download/) and [VSCode](https://code.visualstudio.com/download) are some great free IDEs for coding Python *(if you want to push your files to GitHub, it is best to use PyCharm).*

### If you are using VSCode

Make sure to install the Python extension provided by Microsoft. To do this, first go to the extensions tab on the left sidebar (the icon with the four boxes)
![](tutorial%20pictures/Extensions%20Tab.png)
Then, search "python" in the search bar. The one you need should be the first one that shows up and should be from Microsoft.
![](tutorial%20pictures/Extensions%20Tab%20Search%20Python.png)
Click on it and click ```Install```

# Installing PyGame
Next, you will have to install PyGame. To do this, open Command Prompt if you are on Windows and Terminal if you are on Mac, and then run the following command: ```pip install pygame```.

You can download [this template](https://github.com/gamingkitty/Pygame-Projects/blob/master/exampleFiles/game_scaffold.py) to get started with Pygame.

The sample games are [here](https://github.com/gamingkitty/Pygame-Projects/tree/master/games).

# Pushing your games to GitHub
> If you are using VSCode, switch to PyCharm. VSCode does not have a built in git feature and the extension is very buggy.

If you want to push your games to GitHub, you will need to [create a github account](https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home) if you don't have one already.

Once you create your account (or if you have one already), [fork this repository](https://github.com/gamingkitty/Pygame-Projects/fork).
## If you are using PyCharm
Click on ```File```>```Project from Version Control...```.

Login to your GitHub account in the popup.

Once you are logged in, the window should look like this (with a different account name and directory, of course):\
![](/tutorial%20pictures/PyCharm%20VCS.png)

For the URL, go to your forked GitHub repository, and click the green ```<> Code``` dropdown on the page.
![](tutorial%20pictures/GitHub%20Clone%20URL.png)
Then, copy the HTTPS link and paste it into the URL section of the PyCharm VCS popup and click ```Clone```.

Now, all the files should be cloned and ready to go!

The template is in ```exampleFiles/game_scaffold.py```.

Sample games are in the ```games``` folder.

### Pushing, Committing, and Pulling
To pull your files from GitHub, click on ```Git```>```Pull...```

To push your files to GitHub, you need to commit them first. To do this, click on ```Git```>```Commit...``` and select the files you want to commit. Then, write your commit message in the provided box, and click ```Commit and Push``` if you want to push them to GitHub.
