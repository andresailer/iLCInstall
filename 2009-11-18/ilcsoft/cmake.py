##################################################
#
# CMake module
#
# Author: Jan Engels, DESY
# Date: Jan, 2007
#
##################################################
                                                                                                                                                            
# custom imports
from baseilc import BaseILC
from util import *


class CMake(BaseILC):
    """ Responsible for the CMake installation process. """
    
    def __init__(self, userInput="auto"):
        BaseILC.__init__(self, userInput, "CMake", "CMake")

        self.download.supportHEAD = False
        self.hasCMakeBuildSupport = False
        self.hasCMakeFindSupport = False
        self.download.supportedTypes = ["wget"]

        self.reqfiles = [ ["bin/cmake"], ["bin/cpack"], ["bin/ctest"] ]

        if( userInput == "auto" ):
            self.autoDetect()

    def autoDetectPath(self):
        """ tries to auto detect cmake dir from system settings.
            - returns empty string in case of failure
            - otherwise returns cmake dir """

        # look for SL afs installation
        if os.path.exists( self.ilcHome ):
            if self.os_ver.isSL():
                for v in [ '2.6.2', '2.4.6' ]:
                    cpath = fixPath( self.ilcHome+'/'+self.alias+'/'+v )
                    if os.path.exists( cpath ):
                        return cpath

        # else try to get from cmake
        if( isinPath("cmake")):
            out = getoutput("which cmake").strip()
            ind = out.find("/bin/cmake")
            return out[:ind]

        return ''

    def autoDetectVersion(self):
        """ tries to auto detect version by parsing the output of cmake --version.
            - returns empty string in case of failure
            - otherwise returns cmake version """

        try:
            v = Version( getoutput( self.realPath() + '/bin/cmake --version' ).replace( 'patch ','' ), strict=True)
        except ValueError:
            return ''
        else:
            return str(v)

    def setMode(self, mode):
        BaseILC.setMode(self, mode)

        self.download.url = "http://www.cmake.org/files/v%s/cmake-%s.tar.gz" % (self.version[:3], self.version)
        
    def downloadSources(self):
        BaseILC.downloadSources(self)

        # move sources to a subdirectory
        os.renames( self.version, self.name )
        os.renames( self.name, self.version + "/" + self.name )

        # create build directory
        os.makedirs( self.installPath + "/build" )


    def compile(self):
        """ compile CMake """

        os.chdir( self.installPath + "/build" )

        if( self.rebuild ):
            os.system( "make clean" )

        if( os.system( "../" + self.name + "/configure --prefix=" + self.installPath + \
            " 2>&1 | tee -a " + self.logfile ) != 0 ):
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
        self.envpath["PATH"].append( self.installPath+"/bin" )
