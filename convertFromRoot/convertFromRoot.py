#!/usr/bin/env python
# encoding: utf-8
'''
convertFromRoot -- converts the root files produced with the deepJet ntupler to the data format used by keras for the DNN training

convertFromRoot is a small program that converts the root files produced with the deepJet ntupler to the data format used by keras for the DNN training


@author:     jkiesele

'''

import sys
import os

from argparse import ArgumentParser

__all__ = []
__version__ = 0.1
__date__ = '2017-02-22'
__updated__ = '2017-02-22'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2017 user_name (organization_name)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    
    #try:
        # setup option parser

    parser = ArgumentParser('program to convert root tuples to traindata format')
    parser.add_argument("-i", help="set input sample description (output from the check.py script)", metavar="FILE")
    parser.add_argument("-o",  help="set output path", metavar="PATH")
    parser.add_argument("-c",  help="set output class [TrainData_deepCSV, TrainData_deepCMVA_ST, TrainData_deepCSV_ST, TrainData_veryDeepJet]", metavar="Class")
    parser.add_argument("-r",  help="set path to snapshot that got interrupted", metavar="FILE", default='')
    parser.add_argument("--testdatafor", default='')

    
    # process options
    args=parser.parse_args()
    infile=args.i
    outPath=args.o
    Class=args.c
    Recover=args.r
    testdatafor=args.testdatafor

    if infile:
        print("infile = %s" % infile)
    if outPath:
        print("outPath = %s" % outPath)

    # MAIN BODY #
    
    
    from DataCollection import DataCollection
    from TrainData import TrainData
    from TrainData_deepCSV import TrainData_deepCSV
    from TrainData_veryDeepJet import TrainData_veryDeepJet
    from TrainData_deepCSV_ST import TrainData_deepCSV_ST,TrainData_deepCMVA_SST,TrainData_deepCMVA_ST,TrainData_deepCSV_ST_broad
    from TrainData_deepCSV_PF import  TrainData_deepCSV_PF,TrainData_deepCSV_miniPF
    from TrainData_deepJet_Fla_PT import TrainData_deepCMVA_Fla_PT
    dc=DataCollection()
    traind=TrainData
    if Class == 'TrainData_deepCSV':
        traind=TrainData_deepCSV
    elif Class == 'TrainData_veryDeepJet':
        traind=TrainData_veryDeepJet
    elif Class == 'TrainData_deepCMVA_Fla_PT':
        traind=TrainData_deepCMVA_Fla_PT
    elif Class ==  'TrainData_deepCSV_ST':
        traind=TrainData_deepCSV_ST
    elif Class ==  'TrainData_deepCSV_PF':
        traind=TrainData_deepCSV_PF
    elif Class ==  'TrainData_deepCSV_miniPF':
        traind=TrainData_deepCSV_miniPF
    elif Class == 'TrainData_deepCMVA_ST':
        traind=TrainData_deepCMVA_ST
    elif Class == 'TrainData_deepCMVA_SST':
        traind=TrainData_deepCMVA_SST
    elif Class == 'TrainData_deepCSV_ST_broad':
        traind=TrainData_deepCSV_ST_broad
    elif len(Recover)<1 and len(testdatafor)<1:
        raise Exception('wrong class selecton')
    
    if len(testdatafor):
        print('converting test data, no weights applied')
        dc.createTestDataForDataCollection(testdatafor,infile,outPath)
    
    elif len(Recover)>0:
        dc.recoverCreateDataFromRootFromSnapshot(Recover)
    else:
        notdone=True
        while notdone:
            
            # testdata for.. and then pass DataCollection (for means and norms)
            
            dc.convertListOfRootFiles(infile, traind(), outPath)
            notdone=False
            #except Exception as e:
            #    print('for recovering run: convertFromRoot.py -r '+outPath+'/snapshot.dc')
            #    raise e
   

    


#if __name__ == "__main__":
if DEBUG:
    sys.argv.append("-h")
if TESTRUN:
    import doctest
    doctest.testmod()
if PROFILE:
    import cProfile
    import pstats
    profile_filename = 'convertFromRoot_profile.txt'
    cProfile.run('main()', profile_filename)
    statsfile = open("profile_stats.txt", "wb")
    p = pstats.Stats(profile_filename, stream=statsfile)
    stats = p.strip_dirs().sort_stats('cumulative')
    stats.print_stats()
    statsfile.close()
    sys.exit(0)
sys.exit(main())
