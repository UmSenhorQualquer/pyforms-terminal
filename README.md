![Important](https://img.shields.io/badge/Important-Note-red.svg "Screen")  
If you find this project useful, please, do not forget to ![star it](https://raw.githubusercontent.com/UmSenhorQualquer/pyforms/v1.0.beta/docs/imgs/start.png?raw=true "Screen") it.


# Pyforms Terminal

Pyforms **Terminal** is a software layer, part of the Pyforms main library. This layer implements the execution of a Pyforms application in the terminal.

![Diagram](docs/source/_static/imgs/pyforms-layers-terminal.png "Screen")



# Pyforms

<!-- Posicione esta tag onde você deseja que o widget apareça. -->
<div class="g-follow" data-annotation="bubble" data-height="24" data-rel="publisher"></div>

Pyforms is a Python 3 cross-enviroment framework that aims the boost the developement productivity. The library provides an API in Python to develop applications that can be executed in Windows GUI mode, Web mode, or in Terminal mode.

[More @ ![Diagram](docs/source/_static/imgs/rtd.png)](https://pyforms.readthedocs.io)



## Advantages
* With a minimal API, interfaces are easily defined using a short Python code.
* Avoid the constant switching between the GUI designers and the Python IDE.
* It is designed to allow the coding of advanced functionalities with a minimal effort.
* The code is organized in modules and prepared to be reused by other applications.
* It makes the applications maintenance easier.
* Turn the prototyping much easier and fast.
* Due to its simplicity it has a low learning curve.

## Examples of applications developed in Pyforms
* [Python Video Annotator](https://github.com/UmSenhorQualquer/pythonVideoAnnotator)
* [3D tracking analyser](https://github.com/UmSenhorQualquer/3D-tracking-analyser)
* [PyBpod](http://pybpod.readthedocs.io)

## Installation

Check the documentation at [pyforms.readthedocs.org](http://pyforms.readthedocs.org) and [pyforms-terminal.readthedocs.org](http://pyforms-terminal.readthedocs.org)

## Rationale behind the framework

The development of this library started with the necessity of allowing users with low programming skills to edit parameters of my python scripts.
The idea was to transform scripts which had already been developed into GUI applications with a low effort and in a short time.

For example in my computer vision applications in the majority of the times there were variables that had to be set manually in the scripts for each video, to adjust the thresholds, blobs sizes, and other parameters to the environment light conditions... To test each set of parameters the script had to be executed.
With GUI applications, users would be able to set the parameters using a GUI interface and visualize the results instantly without the need of restarting the script. That was the idea.

After looking into the several python options for GUI interfaces, PyQt was the one that seemed the best tool for a fast development with the QtDesigner, but after a while developing in Qt, switching between the designer and the python IDE was becoming too costly in terms of time, because the interfaces were constantly evolving, and it was tedious, because GUI controls were repeated several times.

Being a Django developer, I did get inspiration on it for this framework. In the [Django](https://www.djangoproject.com/) Models we just need to define the type of variables and their disposition in the form (in ModelAdmin) to generate a HTML form for data edition.
For the GUIs that I wanted to build for my python scripts, I would like to have the same simplicity, because I did wanted to focus on the algorithms and not on GUIs developing.

The result was the simplicity that we can see in the example below:

```python
from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlFile
from pyforms.controls   import ControlText
from pyforms.controls   import ControlSlider
from pyforms.controls   import ControlPlayer
from pyforms.controls   import ControlButton

class ComputerVisionAlgorithm(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Computer vision algorithm example')

        #Definition of the forms fields
        self._videofile  = ControlFile('Video')
        self._outputfile = ControlText('Results output file')
        self._threshold  = ControlSlider('Threshold', 114, 0,255)
        self._blobsize   = ControlSlider('Minimum blob size', 100, 100,2000)
        self._player     = ControlPlayer('Player')
        self._runbutton  = ControlButton('Run')

        #Define the function that will be called when a file is selected
        self._videofile.changed     = self.__videoFileSelectionEvent
        #Define the event that will be called when the run button is processed
        self._runbutton.value       = self.__runEvent
        #Define the event called before showing the image in the player
        self._player.process_frame_event    = self.__process_frame

        #Define the organization of the Form Controls
        self._formset = [
            ('_videofile', '_outputfile'),
            '_threshold',
            ('_blobsize', '_runbutton'),
            '_player'
        ]


    def __videoFileSelectionEvent(self):
        """
        When the videofile is selected instanciate the video in the player
        """
        self._player.value = self._videofile.value

    def __process_frame(self, frame):
        """
        Do some processing to the frame and return the result frame
        """
        return frame

    def __runEvent(self):
        """
        After setting the best parameters run the full algorithm
        """
        pass


if __name__ == '__main__':

    from pyforms import start_app
    start_app(ComputerVisionAlgorithm)
```

Result of runnning the application in the terminal:

```bash

$> python test.py terminal_mode --help
```


![ScreenShot](docs/source/_static/imgs/terminal-example-computervisionalgorithm.png "Screen")
