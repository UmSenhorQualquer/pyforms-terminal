from pyforms_terminal.controls.control_file import ControlFile
from pyforms_terminal.controls.control_slider import ControlSlider
from pyforms_terminal.controls.control_combo import ControlCombo
from pyforms_terminal.controls.control_text import ControlText
from pyforms_terminal.controls.control_checkbox import ControlCheckBox
from pyforms_terminal.controls.control_dir import ControlDir
from pyforms_terminal.controls.control_base import ControlBase
from pyforms_terminal.controls.control_number import ControlNumber
from pyforms_terminal.controls.control_list import ControlList
from pyforms_terminal.controls.control_boundingslider import ControlBoundingSlider


from datetime import datetime, timedelta
import argparse, uuid, os, shutil, time, sys, subprocess
import simplejson as json

import logging

logger=logging.getLogger(__file__)

try:
    import requests
except Exception as e:

    logger.warning("No requests lib")
    logger.error(e, exc_info=True)



class BaseWidget(object):

    def __init__(self, *args, **kwargs):
        self._parser = argparse.ArgumentParser()
        self._controlsPrefix = ''
        self._title          = kwargs.get('title', args[0] if len(args)>0 else '')
        self.stop            = False

        self._conf = kwargs.get('load', None)

    ############################################################################
    ############ Module functions  #############################################
    ############################################################################

    def set_margin(self, margin):pass

    def init_form(self, parse=True):
        for fieldname, var in self.controls.items():
            name = var._name
            if isinstance(var, (
                    ControlFile, ControlSlider,   ControlText, ControlList,
                    ControlCombo,ControlCheckBox, ControlDir, ControlNumber, ControlBoundingSlider
                ) 
            ):
                self._parser.add_argument("--%s" % name, help=var.label, default=var.value)

        if parse:
            self._parser.add_argument('terminal_mode', type=str, default='terminal_mode', help='Flag to run pyforms in terminal mode')
            self._parser.add_argument(
                "--exec{0}".format(self._controlsPrefix), 
                default='', 
                help='Function from the application that should be executed. Use | to separate a list of functions.')
            self._parser.add_argument(
                "--load{0}".format(self._controlsPrefix), 
                default=None, 
                help='Load a json file containing the pyforms form configuration.')
            self._args = self._parser.parse_args()

            self.__parse_terminal_parameters()
            self.__execute_events()

    def load_form(self, data, path=None):
        allparams = self.controls

        if hasattr(self, 'load_order'):
            for name in self.load_order:
                param = allparams[name]
                if name in data:
                    logger.debug("[%30s]: [%s]", param.label, data[name])
                    param.load_form(data[name])
        else:
            for name, param in allparams.items():
                if name in data:
                    logger.debug("[%30s]: [%s]", param.label, data[name])
                    param.load_form(data[name])


    def __parse_terminal_parameters(self):

        logger.debug('--------- LOADING TERMINAL PARAMS ---------')
        for fieldname, var in self.controls.items():
            name = var._name
            args = self._args.__dict__

            if name in args:
                value = args[name]

                if isinstance(var, ControlFile):
                    if value!=None and (value.startswith('http://') or value.startswith('https://')):
                        local_filename = value.split('/')[-1]
                        outputFileName = os.path.join('input', local_filename)
                        self.__downloadFile(value, outputFileName)
                        var.value = outputFileName
                    else:
                        var.value = value

                if isinstance(var, ControlDir):
                    var.value = value

                elif isinstance(var, ControlList):
                    if value is not None:
                        var.value = eval(value)
                    else:
                        var.value = None
                elif isinstance(var,  (ControlText, ControlCombo)):
                    var.value = value

                elif isinstance(var, ControlCheckBox):
                    var.value = value=='True' if value is not None and isinstance(value, str) else value

                elif isinstance(var, (ControlSlider, ControlNumber) ):
                    var.value = float(value) if value is not None and isinstance(value, (str, int) ) else value

                elif isinstance(var, ControlBoundingSlider):
                    var.value = eval(value) if isinstance(value, str) and value else value

                logger.debug("[%30s]: [%s]", var.label, var.value)

        logger.debug('--------- END LOADING TERMINAL PARAMS ---------')

        if self._args.load:
            logger.debug('--------- LOADING CONFIG JSON ---------')
            with open(self._args.load) as infile:
                data = json.load(infile)
                self.load_form(data, os.path.dirname(self._args.load))
            logger.debug('--------- END LOADING CONFIG JSON ---------')

        elif self._conf is not None:

            logger.debug('--------- LOADING DEFAULT CONFIG ---------')
            data = self._conf
            self.load_form(self._conf, '.')
            logger.debug('--------- END LOADING DEFAULT CONFIG ---------')

        logger.debug('--------- FIELDS FINAL VALUES ---------')
        for fieldname, var in self.controls.items():
            logger.debug("[%30s]: [%s]", fieldname, var.value)
        logger.debug('--------- END FIELDS FINAL VALUES ---------')
                    
            
    def __execute_events(self):
        for function in self._args.__dict__.get("exec{0}".format(self._controlsPrefix), []).split('|'):
            if len(function)>0: 
                getattr(self, function)()

        res = {}
        for controlName, control in self.controls.items(): 
            res[controlName] = {'value': control.value }
        with open('out-parameters.txt', 'w') as outfile:
            outfile.write( str(res) )


    def __downloadFile(self, url, outFilepath):
        chunksize = 512*1024
        r = requests.get(url, stream=True)
        with open(outFilepath, 'w') as f:
            for chunk in r.iter_content(chunk_size=chunksize): 
                if chunk: f.write(chunk); f.flush(); 
        


    def execute(self): pass


    def start_progress(self, total = 100):
        self._total_processing_count = total
        self._processing_initial_time = time.time()
        self._processing_count  = 1

    def update_progress(self):
        div = int(self._total_processing_count/400)
        if div==0: div = 1
        if (self._processing_count % div )==0:
            self._processing_last_time = time.time()  
            total_passed_time = self._processing_last_time - self._processing_initial_time
            remaining_time = ( (self._total_processing_count * total_passed_time) / self._processing_count ) - total_passed_time
            if remaining_time<0: remaining_time = 0
            time_remaining = datetime(1,1,1) + timedelta(seconds=remaining_time )
            time_elapsed = datetime(1,1,1) + timedelta(seconds=(total_passed_time) )

            values = ( 
                        time_elapsed.day-1,  time_elapsed.hour, time_elapsed.minute, time_elapsed.second, 
                        time_remaining.day-1, time_remaining.hour, time_remaining.minute, time_remaining.second, 
                        (float(self._processing_count)/float(self._total_processing_count))*100.0, self._processing_count, self._total_processing_count, 
                    )

            print("Elapsed: %d:%d:%d:%d; Remaining: %d:%d:%d:%d; Processed %0.2f %%  (%d/%d); |   \r" % values) 
            sys.stdout.flush()

        self._processing_count  += 1

    def end_progress(self):
        self._processing_count = self._total_processing_count
        self.update_progress()


    def __savePID(self, pid):
        try:
            with open('pending_PID.txt', 'w') as f:
                f.write(str(pid))
                f.write('\n')
        except (IOError) as e:
            raise e

    def __savePID(self, pid):
        try:
            with open('pending_PID.txt', 'w') as f:
                f.write(str(pid))
                f.write('\n')
        except (IOError) as e:
            raise e



    def message(self, msg, title=None, msg_type=None):
        print('*****', title.upper(), '*****')
        print(msg)

    def success(self,   msg, title=None):   self.message(msg, title, msg_type='success')
    def info(self,      msg, title=None):   self.message(msg, title, msg_type='info')
    def warning(self,   msg, title=None):   self.message(msg, title, msg_type='warning');
    def alert(self,     msg, title=None):   self.message(msg, title, msg_type='error')
    def critical(self,  msg, title=None):   self.message(msg, title, msg_type='error')
    def about(self,     msg, title=None):   self.message(msg, title, msg_type='about')
    def aboutQt(self,   msg, title=None):   self.message(msg, title, msg_type='aboutQt')


    def executeCommand(self, cmd, cwd=None, env=None):
        if cwd!=None: 
            currentdirectory = os.getcwd()
            os.chdir(cwd)
        
        print(" ".join(cmd))
        proc = subprocess.Popen(cmd)

        if cwd!=None: os.chdir(currentdirectory)
        self.__savePID(proc.pid)
        proc.wait()
        #(output, error) = proc.communicate()
        #if error: print 'error: ', error
        #print 'output: ', output
        return ''#output

    def exec_terminal_cmd(self, args, **kwargs):
        print('TERMINAL <<',' '.join(args) )
        sys.stdout.flush()
        proc = subprocess.Popen(args, **kwargs)
        self.__savePID(proc.pid)
        proc.wait()
        sys.stdout.flush()
        

    @property
    def controls(self):
        """
        Return all the form controls from the the module
        """
        result = {}
        for name, var in vars(self).items():
            if isinstance(var, ControlBase):
                var._name = self._controlsPrefix+"-"+name if len(self._controlsPrefix)>0 else name
                result[name] = var
        return result