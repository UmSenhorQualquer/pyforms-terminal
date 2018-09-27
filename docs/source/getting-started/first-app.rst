******************
First application
******************

.. note::

    More documentation to read about this example at:

        * :class:`pyforms_terminal.basewidget.BaseWidget`

        * :class:`pyforms_terminal.controls.control_base.ControlBase`


Here it is shown how to create the first pyforms app.


Create the first app
____________________

Create the file **example.py** and add the next code to it.

.. code:: python

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



Now execute in the terminal the next command:

.. code-block:: bash

    $ python example.py terminal_mode --help

You will visualize the next result:

.. code-block:: bash

    usage: example.py [-h] [--_videofile _VIDEOFILE] [--_outputfile _OUTPUTFILE]
                  [--_threshold _THRESHOLD] [--_blobsize _BLOBSIZE]
                  [--exec EXEC] [--load LOAD]
                  terminal_mode

    positional arguments:
      terminal_mode         Flag to run pyforms in terminal mode

    optional arguments:
      -h, --help            show this help message and exit
      --_videofile _VIDEOFILE
                            Video
      --_outputfile _OUTPUTFILE
                            Results output file
      --_threshold _THRESHOLD
                            Threshold
      --_blobsize _BLOBSIZE
                            Minimum blob size
      --exec EXEC           Function from the application that should be executed.
                            Use | to separate a list of functions.
      --load LOAD           Load a json file containing the pyforms form
                            configuration.


.. note::

    In alternative if you would not like to use the **terminal_mode** parameter you can create the file **local_settings.py** in the same directory
    where you are going to run the application and add the next code:

    .. code:: python

        SETTINGS_PRIORITY = 0
        PYFORMS_MODE = 'TERMINAL'

    This code will set pyforms to run in terminal mode.

    Now you can run the application in terminal mode using the command:

    .. code-block:: bash

        $ python example.py --help
