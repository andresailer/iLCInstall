##################################################
#
# JAIDA module
#
# Author: Jan Engels, DESY
# Date: Jan, 2007
#
##################################################

# custom imports
from baseilc import BaseILC
from util import *


class JAIDA(BaseILC):
    """ Responsible for the JAIDA configuration process. """
    
    def __init__(self, userInput):
        BaseILC.__init__(self, userInput, "JAIDA", "JAIDA")

        self.reqfiles = [ ["bin/aida-setup.sh"] ]

        # no cmake build support
        self.hasCMakeBuildSupport = False

        # Java is required for JAIDA
        self.reqmodules = [ "Java" ]

        self.download.supportHEAD = False
        self.download.supportedTypes = [ "wget" ]

        # binary distribution of JAIDA is downloaded
        self.skipCompile = True

    def setMode(self, mode):
        BaseILC.setMode(self, mode)

        self.download.url = "ftp://ftp.slac.stanford.edu/software/freehep/JAIDA/v%s/JAIDA-%s.tar.gz" \
                % (self.version, self.version)

        if( self.mode == "install" ):
            if( Version( self.version ) >= '3.3' or Version( self.version ) < '3.2' ):
                self.abort( "ilcinstall only supports installation of JAIDA 3.2.x versions!" )

    def postCheckDeps(self):
        BaseILC.postCheckDeps(self)

        self.env["JAIDA_HOME"] = self.installPath
        
        # get the jar names in ${JAIDA_HOME}/lib
        jars_fp = glob.glob( self.installPath + "/lib/*.jar" )
        jars = [ i.split('/')[-1] for i in jars_fp ]

        for jar in jars:
            self.envpath["CLASSPATH"].append( "$JAIDA_HOME/lib/" + jar + ".jar" )
