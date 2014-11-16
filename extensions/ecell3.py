# -*- coding: utf-8 -*-
"""
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

       This file is part of the E-Cell System

       Copyright (C) 1996-2014 Keio University
       Copyright (C) 2008-2014 RIKEN
       Copyright (C) 2005-2009 The Molecular Sciences Institute

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


 E-Cell System is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public
 License as published by the Free Software Foundation; either
 version 2 of the License, or (at your option) any later version.
 
 E-Cell System is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 See the GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public
 License along with E-Cell System -- see the file COPYING.
 If not, write to the Free Software Foundation, Inc.,
 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 
END_HEADER

 written by Yasuhiro Naito <ynaito@sfc.keio.ac.jp>,
 E-Cell Project.
"""

import ecell.config
import ecell.ecs
import ecell.emc
from ecell.Session import Session, createScriptContext

from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

try:
    from PySide import QtCore, QtGui
except ImportError:
    from PyQt4 import QtCore, QtGui

def model_chooser( dir = None ):
    """
    Choose a eml file via a dialog
    """
    if dir is None: dir ='./'
    
    model_file = QtGui.QFileDialog.getOpenFileName(
        None,
        "Choose a model file...", 
        dir, 
        filter = "Model files (*.em *.eml)" )
    
    return str( model_file )

def FullID_matcher( event, session ):
    prefix = event.line.split( "'" )[ -1 ]
    prefix = prefix.split( '"' )[ -1 ]
    return [ id for id in session.getModelEntityList() if id.startswith( prefix ) ]

def load_ipython_extension( ipython ):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    
    aSimulator = ecell.emc.Simulator()
    aSimulator.setDMSearchPath( aSimulator.DM_SEARCH_PATH_SEPARATOR.join( ecell.config.dm_path ) )
    aSession = Session( aSimulator )
    
    ipython.push( createScriptContext( aSession, {} ) )
    
    def FullID_completer( self, event ):
        # Completer for createLoggerStub
        return FullID_matcher( event, aSession )
    
    ipython.set_hook('complete_command', FullID_completer, re_key = r'.*createEntityStub\(\s*[\'\"]')
    ipython.set_hook('complete_command', FullID_completer, re_key = r'.*createLoggerStub\(\s*[\'\"]')
    
    @register_cell_magic
    def loadModel( line, cell ):
        model_file = model_chooser()
        loadModel( model_file )
        print '{} is loaded.'.format( model_file )



def unload_ipython_extension( ipython ):
    # If you want your extension to be unloadable, put that logic here.
    pass
