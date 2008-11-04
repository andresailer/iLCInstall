##################################################
#
# Mokka module
#
# Author: Jan Engels, DESY
# Date: Sep, 2007
#
##################################################

# custom imports
from baseilc import BaseILC
from util import *


class Mokka(BaseILC):
    """ Responsible for the Mokka configuration process. """
    
    def __init__(self, userInput):
        BaseILC.__init__(self, userInput, "Mokka", "Mokka")

        self.hasCMakeBuildSupport = False
        self.hasCMakeFindSupport = False

        self.download.supportedTypes = [ "cvs" ]
        # set some cvs variables
        # export CVSROOT=:pserver:anoncvs@pollin1.in2p3.fr:/home/flc/cvs
        self.download.accessmode = "pserver"
        self.download.server = "pollin1.in2p3.fr"
        self.download.root = "home/flc/cvs"

        self.reqfiles = [ ["bin/Linux-g++/Mokka"] ]
        self.reqmodules = [ "LCIO", "GEAR", "Geant4", "MySQL" ]


    def setMode(self, mode):
        BaseILC.setMode(self, mode)

        if( self.download.type != "cvs" ):
            self.download.type = "cvs"

        if( self.download.username == "anonymous" ):
            self.download.username = "anoncvs"
            self.download.password = "%ilc%"

    def compile(self):
        """ compile Mokka """

        os.chdir( self.installPath + "/source" )
        
        if self.rebuild:
            os.system( ". ${G4ENV_INIT}; unset G4UI_USE_XAW ; unset G4UI_USE_XM ; make clean 2>&1 | tee -a "+self.logfile )
            
        if( os.system( ". ${G4ENV_INIT}; unset G4UI_USE_XAW ; unset G4UI_USE_XM ; make 2>&1 | tee -a " \
                + self.logfile ) != 0 ):
            self.abort( "failed to compile!!" )

    def postCheckDeps(self):
        BaseILC.postCheckDeps(self)

        # if G4WORKDIR not set build mokka in installPath
        self.env.setdefault( 'G4WORKDIR', self.installPath )
        self.env.setdefault( 'G4UI_USE_TCSH', 1 )

        self.envpath["PATH"].append( self.installPath + "/bin/Linux-g++" )
        #self.envpath["LD_LIBRARY_PATH"].append( "$LCIO/lib" )
        self.envcmds.append(" . ${G4ENV_INIT} ")


