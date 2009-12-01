##################################################
#
# Marlin module
#
# Author: Jan Engels, DESY
# Date: Jan, 2007
#
##################################################

# custom imports
from baseilc import BaseILC
from util import *


class Marlin(BaseILC):
    """ Responsible for the Marlin software installation process. """
    
    def __init__(self, userInput):
        BaseILC.__init__(self, userInput, "Marlin", "Marlin")

        self.reqfiles = [ ["lib/libMarlin.a", "lib/libMarlin.so", "lib/libMarlin.dylib"], ["bin/Marlin"] ]

        # LCIO is required for building Marlin
        self.reqmodules = [ "LCIO" ]

        # optional modules
        self.optmodules = [ "GEAR", "CLHEP", "LCCD", "CondDBMySQL", "AIDA" ]

        # supported cmake modules
        self.cmakebuildmodules = [ "LCIO", "GEAR", "CLHEP", "LCCD", "CondDBMySQL", "AIDA" ]

        self.envcmake['MARLIN_GUI']='OFF'
    
    def compile(self):
        """ compile Marlin """
        
        os.chdir( self.installPath )

        os.chdir( "build" )

        if( self.rebuild ):
            tryunlink( "CMakeCache.txt" )

        # build software
        if( os.system( "cmake " + self.genCMakeCmd() + " .. 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to configure!!" )
        
        if( os.system( "make ${MAKEOPTS} 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to compile!!" )

        if( os.system( "make install 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to install!!" )

    def preCheckDeps(self):
        BaseILC.preCheckDeps(self)
        if( self.mode == "install" ):
            # for compatibility of older cfg files
            if( self.env.has_key("MARLIN_GUI") and str(self.env["MARLIN_GUI"]) == "1" ):
                self.envcmake["MARLIN_GUI"]="ON"

            if( str(self.envcmake["MARLIN_GUI"]) == "1" or self.envcmake["MARLIN_GUI"] == "ON" ):
                self.addExternalDependency( ["QT"] )
                self.reqfiles.append(["bin/MarlinGUI"])
    
    def postCheckDeps(self):
        BaseILC.postCheckDeps(self)

        self.env["MARLIN"] = self.installPath
        self.envpath["PATH"].append( '$MARLIN/bin' )

        if( self.mode == "install" ):
            # check for QT 4
            if( "QT" in self.reqmodules_external ):
                qt = self.parent.module("QT")
                if( qt != None and Version( qt.version ) < '4.0' ):
                    self.abort( "you need QT 4!! QT version " + qt.version + " found..." )
