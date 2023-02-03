#!/usr/bin/env python3
########################################################################
# File:plate_map_converter.py
#  executable: plate_map_converter.py commandGroup commandArgs
# Purpose:
#
# Author:       Akshar Lohith
# History:      AL 08/03/2022 Created
#
#
########################################################################
import pandas as pd
import numpy as np
import sys, os
import gui

class CommandLine(object) :
    '''
    Handle the command line, usage and help requests.

    CommandLine uses argparse, now standard in 2.7 and beyond.
    it implements a standard command line argument parser with various argument options,
    a standard usage and help, and an error termination mechanism do-usage_and_die.

    attributes:
    myCommandLine.args is a dictionary which includes each of the available command line arguments as
    myCommandLine.args['option']

    methods:
    do_usage_and_die()
    prints usage and help and terminates with an error.
    '''

    def __init__(self, inOpts=None) :
        '''
        CommandLine constructor.
        Implements a parser to interpret the command line argv string using argparse.
        '''
        import argparse
        self.parser = argparse.ArgumentParser(\
            description = 'This program will convert plate maps. Square-form <=> Long-form',\
            add_help = True, #default is True
            prefix_chars = '-', usage = '%(prog)s')
        self.subparsers = self.parser.add_subparsers(dest='command',\
            help='Possible command group options.')
        self.subparsers.required = True

        # create subparser for performing operations on directory tree
        self.dirProcess = self.subparsers.add_parser("dirProcess",\
            aliases=['dir'],\
            help='Process sets of NanoString data.\n'+\
            'Should be unique folders with just the replicates from one 96-well compound plate')

        self.dirProcess.add_argument("path", action = 'store',\
            type=os.path.abspath,\
            help='Path to dir to work in. Files will be saved here. '+\
            'Should be 1 level above individual replicates.\n'+\
            'Each set of files should be in folder containing data set '+\
            'name with "2reps" in the title.')
        self.dirProcess.add_argument("--dead","-d", action='store_true',\
            help="Return list of indiviual replicates considered 'dead'.\n"+\
            "Dead consideration is Normed count for both EEF1A1 and SIRT6 below "+\
            "50%% SD(housekeeping Gene).")
        self.dirProcess.add_argument('--merge','-m',action='store_true',\
            help='Option to return all data sets concatenated into 1 file as well.')
        self.dirProcess.add_argument('--repsOut',action='store_true',\
            help='Option to also export/save each individual replicate, after '+\
            'outlier mask, at penultimate step.')
        self.dirProcess.add_argument('--noMasks',action='store_true',\
            help='Option to not oerform outlier mask before merge.')
        self.dirProcess.add_argument("--outName","-o", action="store",\
            help='Specific Outname stem to be given to concatenated calculation output.')
        # self.dirProcess.add_argument("rep1", action = 'store',\
        #     type=argparse.FileType('r', encoding='unicode_escape'),\
        #     help='NanoString ERCC_75thNeg Normalized Custom Export for rep1.')
        # self.dirProcess.add_argument("rep2", action = 'store',\
        #     type=argparse.FileType('r', encoding='unicode_escape'),\
        #     help='NanoString ERCC_75thNeg Normalized Custom Export for rep2.')
        # self.dirProcess.add_argument("--outNames","-o", action="store",\
        #     help='List of '))

        # create subparser for performing operations on single set of replicates
        self.plateProcess = self.subparsers.add_parser("singleProcess",\
            aliases=['single'],\
            help='Process single set of NanoString data.\n'+\
            'Should be direct paths to specific replicate files.')

        self.plateProcess.add_argument("path", action = 'store',\
            type=os.path.abspath,\
            help='Path to dir to work in. Files will be save here.')
        self.plateProcess.add_argument("rep1", action = 'store',\
            type=argparse.FileType('r', encoding='unicode_escape'),\
            help='NanoString ERCC_75thNeg Normalized Custom Export for rep1.\n'+\
            "(Comma-seperated-value format)")
        self.plateProcess.add_argument("rep2", action = 'store',\
            type=argparse.FileType('r', encoding='unicode_escape'),\
            help='NanoString ERCC_75thNeg Normalized Custom Export for rep2.\n'+\
            "(Comma-seperated-value format)")
        self.plateProcess.add_argument("--outName","-o", action="store",\
            help='Specific Outname to be given to single calculation output.\n'+\
            "(Default: Infer from rep1 filename.)")
        self.plateProcess.add_argument("--dead","-d", action='store_true',\
            help="Return list of indiviual replicates considered 'dead'.\n"+\
            "Dead consideration is Normed count for both EEF1A1 and SIRT6 below "+\
            "50%% SD(housekeeping Gene).")
        self.plateProcess.add_argument('--repsOut',action='store_true',\
            help='Option to also export/save each individual replicate, after '+\
            'outlier mask, at penultimate step.')
        self.plateProcess.add_argument('--noMasks',action='store_true',\
            help='Option to not oerform outlier mask before merge.')
        # self.parser.add_argument('searchList', action = 'store',\
        #     type=argparse.FileType('r',encoding='unicode_escape'),\
        #     help="Text file with list of MX names to filter/process")
        # self.parser.add_argument("headersSearch", action = 'store',\
        #     type=argparse.FileType('r', encoding='unicode_escape'),\
        #     help='Text file with the list of feature headers to excise out.')

        if inOpts is None :
            self.args = vars(self.parser.parse_args()) # parse the CommandLine options
        else:
            self.args = vars(self.parser.parse_args(inOpts)) # parse the input options



    def __del__ (self) :
        '''
        CommandLine destructor.
        '''
        # do something if needed to clean up before leaving
        pass

    def do_usage_and_die (self, str) :
        '''
        If a critical error is encountered, where it is suspected that the program is not being called with consistent parameters or data, this
        method will write out an error string (str), then terminate execution of the program.
        '''
        import sys
        print(str, file=sys.stderr)
        self.parser.print_usage()
        return 2

class Usage(Exception):
    '''
    Used to signal a Usage error, evoking a usage statement and eventual exit when raised.
    '''
    def __init__(self, msg):
        self.msg = msg

class Reformat(object):
    ''' Super Class for the reformat functions
    '''
    def __init__(self, current_map_form, well_type):
        self.well_type= well_type
        self.current_map_form = current_map_form
        # self.long = long
        # self.square = square
        pass

    def square_to_long(self, square_map):
        ''' General method to melt square platemap to long form.
            If alphanumeric Well dataFrame is not in the square map, numerical 
            Well_X,Well_Y coordinates are needed
            to map each square form data column to long-from.
        '''
        long_out = pd.DataFrame({col:square_map[col].to_numpy().flatten() for
                                 col in square_map.keys()})
        if 'Well' not in square_map:
            long_out['Well'] = ['%s%02d' % (chr(r), c) 
                                for r in range(65,65+np.max(long_out['Well_X']))
                                for c in range(1, np.max(long_out['Well_Y']+1))]
            
        return long_out

    def long_to_square(self, square_map, dimensions):
        ''' General method to stack long platemap into square form.
            will return dictionary for each column, with the key as the column header,
            and the value a square pd.DataFrame of the given dimensions.
            if no Well column included, a dataFrame called "Well" will be added 
            to the return dict containing well names in alphanumeric'''
        dim_x, dim_y = dimensions
        fieldArrays = dict().fromkeys(square_map.columns.to_list())
        for field in fieldArrays:
            if 'Well' not in fieldArrays:
                squareForm = pd.DataFrame(np.array(['%s%02d' % (chr(r), c) 
                                                    for r in range(65,65+dim_x) 
                                                    for c in range(1, dim_y)]).\
                                                        reshape(dim_x,dim_y),
                                  index=[chr(r) for r in range(65,65+dim_x)],
                                  columns=[c for c in range(1,dim_y)])
                fieldArrays['Well'] = squareForm
            fieldArrays[field] = pd.DataFrame(square_map[field].to_numpy().\
                reshape(dim_x,dim_y),
                index=[chr(r) for r in range(65,65+dim_x)],
                columns=[c for c in range(1,dim_y)])
            
        return fieldArrays

    def well_translate(self):
        return NotImplementedError

    def validate_form(self):
        return NotImplementedError

class Well96 (Reformat):
    ''' Object with operations starting from 96 well form. 
    SquareForm ouputs/starting:
        Each sheet refers to one column in a long form platemap.
        so structure should be a dictionary:
        {compoundName:pd.DataFrame (shape = (8,12)),
         concentraion:pd.DataFrame ....}
        '''

    def __init__(self, current_map_form, plate_map):
        self.current_map_form = self.validate_form(plate_map)
        super().__init__(self.current_map_form, "96well")
        self.plate_map = plate_map

    def validate_form(self,x):
        ''' Determine the form (square or long) of the given platemap to be converted.
            Then determine if number of wells listed is in a valid form (96-wells)
            Default is to make it long format.
        '''
        if x.shape[0] == 8:
            return "square"
        elif x.shape[0] > 8:
            return "long"
        else:
            CommandLine.do_usage_and_die(
                "96 PlateMap not in an acceptable format (8x12 or long-form)")
            # SystemExit

    def well_translate(self, direction, form_change="long"):
        ''' function that will look at the direction to convert the 96well coord
            to the appropriate 384well coord.
            output will default to long_map form unless otherwise specified.
        '''
        
        if direction == 'Q1':
            # Q1 wells from 384 = [print('%s%02d' % (chr(r), c)) 
            # for r in range(65,81,2) for c in range(1, 25,2)]
            well_convert = {well1:(well2,well2[0],well2[1:]) 
                            for well1,well2 in zip(
            ['%s%02d' % (chr(r), c) for r in range(65,65+8) 
                                    for c in range(1, 13)],
            ['%s%02d' % (chr(r), c) for r in range(65,81,2) 
                                    for c in range(1, 25,2)])}
        elif direction == 'Q2':
            # Q2 wells from 384 = [print('%s%02d' % (chr(r), c)) 
            # for r in range(65,81,2) for c in range(2, 25,2)]
            well_convert = {well1:(well2,well2[0],well2[1:]) 
                            for well1,well2 in zip(
            ['%s%02d' % (chr(r), c) for r in range(65,65+8) 
                                    for c in range(1, 13)],
            ['%s%02d' % (chr(r), c) for r in range(65,81,2) 
                                    for c in range(2, 25,2)])}
        elif direction == 'Q3':
            # Q3 wells from 384 = [print('%s%02d' % (chr(r), c)) 
            # for r in range(66,81,2) for c in range(1, 25,2)]
            well_convert = {well1:(well2,well2[0],well2[1:]) 
                            for well1,well2 in zip(
            ['%s%02d' % (chr(r), c) for r in range(65,65+8) 
                                    for c in range(1, 13)],
            ['%s%02d' % (chr(r), c) for r in range(66,81,2) 
                                    for c in range(1, 25,2)])}
        elif direction == 'Q4':
            # Q4 wells from 384 = [print('%s%02d' % (chr(r), c)) 
            # for r in range(66,81,2) for c in range(2, 25,2)]
            well_convert = {well1:(well2,well2[0],well2[1:]) 
                            for well1,well2 in zip(
            ['%s%02d' % (chr(r), c) for r in range(65,65+8) 
                                    for c in range(1, 13)],
            ['%s%02d' % (chr(r), c) for r in range(66,81,2) 
                                    for c in range(2, 25,2)])}
        
        if self.current_map_form == 'square' and form_change == 'long':
            self.plate_map = self.square_to_long(self.plate_map)
            self.current_map_form == 'long'
            
        elif self.current_map_form == 'long' and form_change == 'square':
            self.plate_map = self.long_to_square(self.plate_map,(8,12))
            self.current_map_form == 'square'
            
        if self.current_map_form == 'square':
            return_map = self.plate_map['Well'].\
                applymap(lambda well: well_convert[well])
        
        elif self.current_map_form == 'long':
            return_map = self.plate_map.copy()
            return_map['Well'] = return_map['Well'].\
                map(well_convert,na_action='ignore')
            
        return return_map

class Well384(Reformat):
    ''' Object with operations starting from 384 well form.
    SquareForm ouputs/starting:
        Each sheet refers to one column in a long form platemap.
        so structure should be a dictionary:
        {compoundName:pd.DataFrame (shape = (16,24)),
         concentraion:pd.DataFrame ....}
    
    '''

    def __init__(self, current_map_form, plate_map):
        self.current_map_form = self.validate_form(plate_map)
        super().__init__(self.current_map_form, "384well")
        self.plate_map = plate_map

    def validate_form(self,x):
        ''' Determine the form (square or long) of the given platemap to be converted.
            Then determine if number of wells listed is in a valid form (384-wells)
            Default is to make it long format.
        '''
        if x.shape[0] == 16:
            return "square"
        elif x.shape[0] > 16:
            return "long"
        else:
            print(
                "384 PlateMap not in an acceptable format (16x24 or long-form)",
                file=sys.stderr)
            SystemExit

    def well_translate(self, direction, form_change="long"):
        ''' function that will look at the direction to convert the 96well coord
            to the appropriate 384well coord.
            output will default to long_map form unless otherwise specified.
        '''

        pass

def main(myCommandLine =None):
    if myCommandLine is None:
        myCommandLine = CommandLine()
    else :
        myCommandLine = CommandLine(['-h'])
    parseCmd =myCommandLine.args
    # print(parseCmd,file=sys.stderr)
    if 'single' in parseCmd['command']:
        processedData = DataEvaluation(\
            path = parseCmd['path'], mode = parseCmd['command'],\
            normCounts = (parseCmd['all_reps'], parseCmd['nameMap']),\
            outName = parseCmd['outName'], returnReps = parseCmd['repsOut'], \
            deadOut = parseCmd['dead'], disableMask=parseCmd['noMasks'])
    elif 'dir' in parseCmd['command']:
        processedData = DataEvaluation(\
            path = parseCmd['path'], mode = parseCmd['command'],\
            normCounts = parseCmd['data_sets'], merge = parseCmd['merge'],\
            returnReps = parseCmd['repsOut'], deadOut = parseCmd['dead'],
            outName = parseCmd['outName'], disableMask=parseCmd['noMasks'])

if __name__ == "__main__":
    # if program is launched alone, this is true and is exececuted. if not, nothing is\
    # executedf rom this program and instead objects and variables are made available \
    # to the program that imports this.
    main();
    raise SystemExit

gui.run_gui()

# Q1 wells from 384 = [print('%s%02d' % (chr(r), c)) for r in range(65,81,2) for c in range(1, 25,2)]
# Q2 wells from 384 = [print('%s%02d' % (chr(r), c)) for r in range(65,81,2) for c in range(2, 25,2)]
# Q3 wells from 384 = [print('%s%02d' % (chr(r), c)) for r in range(66,81,2) for c in range(1, 25,2)]
# Q4 wells from 384 = [print('%s%02d' % (chr(r), c)) for r in range(66,81,2) for c in range(2, 25,2)]
# 96 wellIDs = [print('%s%02d' % (chr(r), c)) for r in range(65,73) for c in range(1, 13)]
