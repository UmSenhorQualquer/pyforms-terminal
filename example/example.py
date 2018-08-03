from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlFile
from pyforms.controls   import ControlText
from pyforms.controls   import ControlSlider
from pyforms.controls   import ControlPlayer
from pyforms.controls   import ControlButton

class ComputerVisionAlgorithm(BaseWidget):
    
    def __init__(self):
        super().__init__('Computer vision algorithm example')

        #Definition of the forms fields
        self._videofile     = ControlFile('Video')
        self._outputfile    = ControlText('Results output file')
        self._threshold     = ControlSlider('Threshold', 114, 0,255)
        self._blobsize      = ControlSlider('Minimum blob size', 100, 100,2000)
        self._player        = ControlPlayer('Player')
        self._runbutton     = ControlButton('Run')

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