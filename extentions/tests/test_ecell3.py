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

%load_ext ecell3

sim = theSimulator
rootSys = sim.getEntity('System::/')
DE1 = sim.createStepper('FixedODE1Stepper','DE1')

rootSys.StepperID = 'DE1'

SIZE = sim.createVariable('Variable')
SIZE.ID = 'SIZE'
SIZE.Value = 1e-18

S = sim.createVariable('Variable')
S.ID = 'S'
S.Value = 1000000

P = sim.createVariable('Variable')
P.ID = 'P'
P.Value = 0

E = sim.createVariable('Variable')
E.ID = 'E'
E.Value = 1000

P_E = sim.createProcess('MichaelisUniUniFluxProcess')
P_E.ID = 'E'
P_E.KmS = 1
P_E.KcF = 10

P_E.VariableReferenceList = (( 'S0', ':/:S', -1 ),( 'P0', ':/:P', 1 ),( 'C0', ':/:E', 0 ))

rootSys.registerEntity( SIZE )
rootSys.registerEntity( S )
rootSys.registerEntity( P )
rootSys.registerEntity( E )
rootSys.registerEntity( P_E )

S_Logger = createLoggerStub( 'Variable:/:S:Value' )
S_Logger.create()
S_Stub = createEntityStub( 'Variable:/:S' )

getCurrentTime()
S.Value
# S.MolarConc    ## can't get SIZE at t = 0
S.getProperty( 'Value' )
# S.getProperty( 'MolarConc' )    ## can't get SIZE at t = 0

sim.run(1000)

getCurrentTime()
S.Value
S.MolarConc
S.getProperty( 'Value' )
S.getProperty( 'MolarConc' )
