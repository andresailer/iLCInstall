##################################################
#
# CLHEP module
#
# Author: Jan Engels, DESY
# Date: Jan, 2007
#
##################################################
                                                                                                                                                            
# custom imports
from baseilc import BaseILC
from util import *


class CLHEP(BaseILC):
    """ Responsible for the CLHEP installation process. """
    
    def __init__(self, userInput):
        BaseILC.__init__(self, userInput, "CLHEP", "CLHEP")

        # no cmake build support
        self.hasCMakeBuildSupport = False

        self.download.supportHEAD = False
        self.download.supportedTypes = ["wget"]

        self.reqfiles = [ ["lib/libCLHEP.a", "lib/libCLHEP.so", "lib/libCLHEP.dylib"] ]

    def setMode(self, mode):
        BaseILC.setMode(self, mode)
        
        if( self.mode == "install" ):
            if( Version( self.version ) < "1.9.1.1" ):
                self.abort( "ilcinstall only supports installation of CLHEP 1.9.1.1 or greater!" )
            if( Version( self.version ) == "2.0.3.0" and not isinPath( "xiar" )):
                self.abort( "CLHEP 2.0.3.0 requires xiar, that wasn't found in your system!" )

            # download url
            if( Version( self.version ) == "1.9.1.1" or Version( self.version ) == "2.0.1.1" ):
                self.download.url = "http://proj-clhep.web.cern.ch/proj-clhep/export/share/CLHEP/%s/clhep-%s.tgz" \
                        % (self.version, self.version)
            else:
                self.download.url = "http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/distributions/clhep-%s.tgz" \
                        % (self.version,)
    
    def downloadSources(self):
        BaseILC.downloadSources(self)

        # create build directory
        trymakedir( self.installPath + "/build" )
    
    def compile(self):
        """ compile CLHEP """

        os.chdir( self.installPath + "/build" )

        if( os.system( "../CLHEP/configure --prefix=" + self.installPath + " 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to configure!!" )

        if( os.system( "make ${MAKEOPTS} 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to compile!!" )

        if( os.system( "make install 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to install!!" )
    
    def cleanupInstall(self):
        BaseILC.cleanupInstall(self)
        os.chdir( self.installPath + "/build" )
        os.system( "make clean" )

    def postCheckDeps(self):
        BaseILC.postCheckDeps(self)

        self.envorder = [ "CLHEP" ]
        self.env["CLHEP"] = self.installPath

        self.env["CLHEP_BASE_DIR"] = "$CLHEP"
        self.env["CLHEP_INCLUDE_DIR"] = "$CLHEP/include"
        
        self.envpath["PATH"].append( "$CLHEP_BASE_DIR/bin" )
        self.envpath["LD_LIBRARY_PATH"].append( "$CLHEP_BASE_DIR/lib" )
