# Copyright (c) 2017, Lawrence Livermore National Security, LLC. Produced at
# the Lawrence Livermore National Laboratory.
# Written by J.-L. Fattebert, D. Osei-Kuffuor and I.S. Dunn.
# LLNL-CODE-743438
# All rights reserved.
# This file is part of MGmol. For details, see https://github.com/llnl/mgmol.
# Please also read this link https://github.com/llnl/mgmol/LICENSE
#
# read_hdf5.cc -> read_hdf5.py

''' Libraries '''
import sys
import copy
import argparse
import h5py
import numpy as np
import struct

''' Variables / Constants '''
##################
## Don't Modify ##
##################

# Bohr to Angstroem
bohr2ang = 0.529177

# Maximum String Length
MaxStrLength = 10

''' Classes '''
class mystruct:
    def FixedLengthString(self):
        self.mystring = [''] * MaxStrLength
s = mystruct()
s.FixedLengthString()
# s.mystring

########################################
## Maps in C++, can be implemented as ## 
## Dictionaries in Python             ##
########################################

''' Variables (Dictionaries) '''
cov_radii = {}      # C++ - map <key = int, value = double> cov_radii
ball_radii = {}     # C++ - map <key = int, value = double> ball_radii
colors = {}         # C++ - map <key = int, value = string> colors

''' Functions '''
# Void Function (set_maps())
# Set Covalent Radii, Ball Radii, and Colors for Chemical Element
def set_maps():

    # (H) Hydrogen
    cov_radii.update( {1 : 0.6} )
    ball_radii.update( {1 : 0.4} )
    colors.update( {1 : 'White'} )

    # Lithium
    cov_radii.update( {3 : 2.7} )
    ball_radii.update( {3 : 1.6} )
    colors.update( {3 : 'Ochre'} )

    # Beryllium
    cov_radii.update( {4 : 2.0} )
    ball_radii.update( {4 : 1.1} )
    colors.update( {4 : 'Ochre'} )

    # Carbon
    cov_radii.update( {6 : 1.8} )
    ball_radii.update( {6 : 0.7} )
    colors.update( {6 : 'Cyan'} )

    # Nitrogen
    cov_radii.update( {7 : 1.8} )
    ball_radii.update( {7 : 0.6} )
    colors.update( {7 : 'Blue'} )

    # Oxygen
    cov_radii.update( {8 : 1.8} )
    ball_radii.update( {8 : 0.5} )
    colors.update( {8 : 'Red'} )

    # F (Fluorine)
    cov_radii.update( {9 : 1.8} )
    ball_radii.update( {9 : 0.4} )
    colors.update( {9 : 'Green'} )

    # Na (Sodium)
    cov_radii.update( {11 : 3.2} )
    ball_radii.update( {11 : 1.9} )
    colors.update( {11 : 'Ochre'} )

    # Mg (Magnesium)
    cov_radii.update( {12 : 2.9} )
    ball_radii.update( {12 : 1.5} )
    colors.update( {12 : 'Ochre'} )

    # Al (Aluminium)
    cov_radii.update( {13 : 2.5} )
    ball_radii.update( {13 : 1.2} )
    colors.update( {13 : 'Ochre'} )

    # Si (Silicon)
    cov_radii.update( {14 : 2.3} )
    ball_radii.update( {14 : 1.1} )
    colors.update( {14 : 'Ochre'} )

    # P (Phosphorus)
    cov_radii.update( {15 : 2.3} )
    ball_radii.update( {15 : 1.1} )
    colors.update( {15 : 'Tan'} )

    # S (Sulfur)
    cov_radii.update( {16 : 2.2} )
    ball_radii.update( {16 : 1.1} )
    colors.update( {16 : 'Yellow'} )

    # Cl (Chlorine)
    cov_radii.update( {17 : 2.2} )
    ball_radii.update( {17 : 1.1} )
    colors.update( {17 : 'Ochre'} )

    return

# Read dataset in hdf5 file.
# Returns a pointer to an array containing the data.
def get_function(filename, datasetname, dims, origin,
                 lattice, attributes, dima):

    ''' Variables '''
    filename = ''.join(filename)
    datasetname = ''.join(datasetname)
    
    #####################################################################
    ### data = []                                                     ###
    ### herr_t status   htri_t ishdf                                  ###
    ### hid_t file_id, dset_id, filespace, attribute_id, attdataspace ###
    ### hsize_t maxdims = [0] * 3; hsize_t dimsa = [0] * 2;           ###
    ### int rank; char attname = [''] * 50;                           ###
    ### Variables Initialized by Default Later on Code                ###
    #####################################################################

    # Numpy Array Must be C-Contiguous for h5py.h5a.AttrID.read Method
    origin = np.ascontiguousarray(origin)
    lattice = np.ascontiguousarray(lattice)

    # If Above Method Fails, Stop
    if( not(lattice.flags['C_CONTIGUOUS']) and
        not(origin.flags['C_CONTIGUOUS']) ):

        print('\nlattice or origin are not C-Contiguous. Stop.')
        return 0.0

    # Check If File is in HDF5 Format
    try:

        # If h5py.is_hdf Method Fails, Stop
        ishdf = h5py.is_hdf5(filename)

    except Exception:

        print('\nh5py.is_hdf5 unsucessful')
        return None
    
    # If File is not in HDF5 Format, Stop
    if( not(ishdf) ):
        print('\nInput File ' + filename + ' not in HDF5 Format. Stop.')
        return None

    # If Everything Goes Fine, Proceed
    else:
        
        # Open HDF5 File
        try:
            
            file_id = h5py.h5f.open(bytes(filename),
                          h5py.h5f.ACC_RDONLY, h5py.h5p.DEFAULT)
            
        except Exception:

            print('\nHDF5 File: ' + filename + ' Failed to Open')
            return None

        # Open Dataset  
        try:
            
            dset_id = h5py.h5d.open(file_id, bytes(datasetname))

        except Exception:

            print('\nHDF5 Dataset: ' + datasetname + ' Failed to Open')
            return None

        # Copy of Dataspace for Dataset 
        try:

            filespace = dset_id.get_space()
            # filespace = h5py.h5d.DatasetID.get_space()

        except Exception:

            print('\ndset_id.get_space() Failed.')
            return None

        ## Get Dataspace Size ################################################

        # Get Dataspace Dimension -> INT
        rank = filespace.get_simple_extent_ndims()
        
        # Shape of Dataspace (dims) -> TUPLE shape
        dims = dims.tolist()
        dims = filespace.get_simple_extent_dims()

        # Maximum Shape of Dataspace (maxdims) -> TUPLE shape
        maxdims = filespace.get_simple_extent_dims(maxdims = True)
        
        # rank = h5py.h5s.SpaceID.get_simple_extent_dims(maxdims = True)

        # Close Filespace
        # filespace._close()
        # h5py.h5s.SpaceID._close()

        # If Dataspace Dimension Rank is not 3, Stop.
        if( not(rank == 3) ):

            print('\nProblem with Dataspace Dimension, rank = ' + str(rank))
            return None

        # If Dataspace Dimension Rank is 3, Proceed.
        else:

            print('\nDataspace: Dimension ' + str( int(dims[0]) ) + ' x '
                                            + str( int(dims[1]) ) + ' x '
                                            + str( int(dims[2])) )

            print('\nSize: ' + str( int(dims[0] * dims[1] * dims[2]) ))

        # If Size < 1, Stop.
        if( int( dims[0] * dims[1] * dims[2] ) < 1 ):
            return None

        # Read data -> data
        data = np.array(0.0, h5py.h5t.NATIVE_DOUBLE)
        data.resize( int(dims[0] * dims[1] * dims[2]) , refcheck = False)

        # Dump Data into Numpy Array (data)
        try:

            status = dset_id.read(h5py.h5s.ALL, h5py.h5s.ALL, data)
        
            # status = dset_id.read(h5py.h5s.ALL, h5py.h5s.ALL, data,
            # h5py.h5t.NATIVE_DOUBLE, h5py.h5p.DEFAULT)

        except Exception:

            print('\ndataset_id.read Failed.')
            return 0

        ### Read Lattice Parameters ##########################################
        attname = "Lattice parameters"

        # Open a Dataset Attribute
        try:
            
            attribute_id = h5py.h5a.open(dset_id, bytes(attname))

        except Exception:

            print('\nh5py.h5a.open Failed for ' + attname)
            return None

        # Read Data from Attribute and Store in Numpy Array (lattice)
        try:

            status = attribute_id.read(lattice)
            # status = h5py.h5a.AttrID.read( ... )

        except Exception:

            print('\nh5py.h5a.AttrID.read Failed for ' + attname)
            return None

        '''
        # Close Attribute ID
        try:

            status =  attribute_id._close()
            # status = h5py.h5a.AttrID._close()
                           
        except Exception:

            print('\nh5py.h5a.AttrID._close() Failed.')
            return None
        '''

        print('\nLattice parameters: ' + str( lattice[0] ) + ' x '
                                       + str( lattice[1] ) + ' x '
                                       + str( lattice[2] ))
        
        ### Read Origin Parameters ##########################################
        attname = "Cell origin"

        # Open a Dataset Attribute
        try:
            
            attribute_id = h5py.h5a.open(dset_id, bytes(attname))

        except Exception:

            print('\nWARNING: h5py.h5a.open Failed for ' + attname)
            print('\n' + 0.0 + '\t' + 0.0 + '\t' + 0.0 + ' // cell origin')
            return None

        # Read Data from Attribute and Store in Numpy Array (origin)
        try:

            status = attribute_id.read(origin)
            # status = h5py.h5a.AttrID.read( ... )

        except Exception:

            print('\nh5py.h5a.AttrID.read Failed for ' + attname)
            return None
        
        '''
        # Close Attribute ID
        try:

            status =  attribute_id._close()
            # status = h5py.h5a.AttrID._close()

        except Exception:

            print('\nh5py.h5a.AttrID._close() Failed.')
            return None
        '''

        print('\nCell origin: ' + str( origin[0] ) + ' , '
                                + str( origin[1] ) + ' , '
                                + str( origin[2] ))
        
        print('\nMesh: ' + str( int(dims[0]) ) + '\t' + str( int(dims[1]) ) +
              '\t' + str( int(dims[2]) ))

        ### Dataset's Name Starts with F, Proceed #############################
        #not working at present time, so change 'F' to 'f' to turn it off
        if( datasetname[0] == 'f' ):

            # Read Orbitals Centers and Radii
            attname = "List of centers and radii"

            try:
            
                attribute_id = h5py.h5a.open(dset_id, bytes(attname))

            except Exception:

                print('\nWARNING: h5py.h5a.open Failed for ' + str( attname ))
                return None

            # Get a Copy of Attribute's Dataspace
            attdataspace = attribute_id.get_space()
            # attdataspace = h5py.h5a.AttrID.get_space()

            # Get Dataspace Dimension -> INT
            rank = attdataspace.get_simple_extent_ndims()

            # Shape of Dataspace (dims) -> TUPLE shape
            dimsa = attdataspace.get_simple_extent_dims()

            # Maximum Shape of Dataspace (maxdims) -> TUPLE shape
            del maxdims
            maxdims = attdataspace.get_simple_extent_dims(maxdims = True)
            
            # h5py.h5s.SpaceID.get_simple_extent_dims( ... )

            if( not(rank == 2) ):
                print('\nProblem with attdataspace dimension, rank = ' +
                      str( rank ) )
                return None

            if( not( int(dimsa[1]) == 4 ) ):
                print('\nProblem with attdataspace dimension, dimsa = ' +
                      str( int(dimsa[1]) ))

            ''' More Variables '''
            dima = dimsa[0]
            # attributes = np.array(0.0, dtype = h5py.h5t.NATIVE_DOUBLE)
            attributes.resize( 4 * dimsa[0], refcheck = False )

            # Numpy Array Must be C-Contiguous for h5py.h5a.AttrID.read Method
            attributes = np.ascontiguousarray(attributes)
            print('dim0=' + str(dima) )
            print('dim1=' + str(dimsa[1]) )

            # If Above Method Fails, Stop
            if( not(attributes.flags['C_CONTIGUOUS']) ):

                print('\nattributes is not C-Contiguous. Stop.')
                return 0.0

            # Read Data from Attribute and Store in Numpy Array (attributes)
            try:
                
                status = attribute_id.read(attributes)

            except Exception:

                print('\nh5py.h5a.AttrID.read Failed for attributes')
                return None
            
            '''
            # Close Attribute's Dataspace
            try:

                status = attdataspace._close()

            except Exception:

                print('\nh5py.h5s.SpaceID._close() Failed.')
                return None

            # Close Attribute's ID
            try:

                status = attribute_id._close()

            except Exception:

                print('\nh5py.h5a.AttrID._close() Failed.')
                return None
            '''

            print('\n' + str( int(dima) ) + ' Orbital centers')
            for i in range(0, int(dima)):
                print('\nOrbital center: ( ' + str( attributes[4 * i] ) + ' , '
                                             + str( attributes[4 * i + 1] ) + ' , '
                                             + str( attributes[4 * i + 2] ) + ' )'
                                             + ', radius = '
                                             + str( attributes[4 * i + 3] ))

        '''      
        ### Close/Release Resources #########################################
        try:
            
            dset_id._close()

        except Exception:

            print('\nh5py.h5d.DatasetID._close() Failed.')
            return None

        try:

            file_id._close()

        except Exception:

            print('\nh5py.h5f.FileID._close() Failed.')
            return None
        '''
    
    return ( data, dims )

# Read Ionic Positions Dataset in File - Function
def read_ionic_positions_hdf5(file_id):

    print('\nRead Ionic Positions from HDF5 File')

    # Open Datatset
    try:

        dataset_id = h5py.h5d.open(file_id, bytes('/Ionic_positions'))

    except Exception:

        print('\nIons::read_positions_hdf5() --- h5py.h5d.open Failed!!!')
        return None

    # Get Size of the Dataset Inside of File
    dim = int( dataset_id.get_storage_size() ) / dataset_id.dtype.itemsize 

    # Numpy Array for Storing Data
    data = np.arange(0.0)
    data.resize(dim, refcheck = False)

    # Numpy Array Must be C-Contiguous for h5py.h5d.DatasetID.read Method
    data = np.ascontiguousarray(data)

    # If Above Method Fails, Stop
    if( not(data.flags['C_CONTIGUOUS']) ):

        print('\ndata is not C-Contiguous. Stop.')
        return None

    # Ion i: data[3 * i], data[3 * i + 1], data[3 * i + 2]
    try:

        status = dataset_id.read(h5py.h5s.ALL, h5py.h5s.ALL, data,
                                 h5py.h5t.NATIVE_DOUBLE, h5py.h5p.DEFAULT)

    except Exception:

        print('\nread_ionic_positions_hdf5() --- dataset_id.read Failed!!!')
        return None

    # Close Dataset ID
    # dataset_id._close()
    # print(h5py.h5d.DatasetID._close(dataset_id))

    return data

def read_atomic_numbers_hdf5(file_id):

    print('\nRead Atomic Numbers from HDF5 File')

    # Open Datatset
    try:

        dataset_id = h5py.h5d.open(file_id, bytes('/Atomic_numbers'))

    except Exception:

        print('\nIons::read_atomic_numbers_hdf5() --- h5py.h5d.open Failed!!!')
        return 0
    
    # Get dim for Reading Atomic Numbers
    dim = int( dataset_id.get_storage_size() ) / int( (h5py.h5t.NATIVE_INT32).get_size() )

    # Create Numpy Array for Storing Data
    data = np.array(0, dtype = h5py.h5t.NATIVE_INT32)
    data.resize(dim, refcheck = False)
    
    # Numpy Array Must be C-Contiguous for h5py.h5d.DatasetID.read Method
    data = np.ascontiguousarray(data)

    # If Above Method Fails, Stop
    if( not(data.flags['C_CONTIGUOUS']) ):

        print('\ndata is not C-Contiguous. Stop.')
        return 0

    print('\nRead ' + str(dim) + ' Atomic Numbers from HDF5 File')

    # 
    try:

        status = dataset_id.read(h5py.h5s.ALL, h5py.h5s.ALL, data)
        # h5py.h5t.NATIVE_INT32, h5py.h5p.DEFAULT)

    except Exception:

        print('\nread_ionic_positions_hdf5() --- dataset_id.read Failed!!!')
        return 0

    # Close Dataset ID
    # dataset_id._close()

    # Return Data as a List
    # data = data.tolist()                                
    
    return ( dim, data )

# int Function - Read Atomic Names HDF5
def read_atomic_names_hdf5(file_id, data):

    print('\nRead Atomic Names from HDF5 File')

    # Open the Dataset
    try:
        
        dataset_id = h5py.h5d.open(file_id, bytes('/Atomic_names'))

    except Exception:

        print('\nIons::read_atomic_names_hdf5() --- h5py.h5d.open Failed!!!')
        return 0

    # Create Type for Strings of Length MaxStrLength
    strtype = h5py.h5t.TypeID.copy(h5py.h5t.C_S1)

    strtype.set_size( MaxStrLength )
    # h5py.h5t.TypeID.set_size( strtype, MaxStrLength )

    # Amount of Names to be Read from HDF5 File
    dim = int( dataset_id.get_storage_size() ) / strtype.get_size()

    print('\nRead ' + str( dim ) + ' Atomic Names from HDF5 File')

    # Vector - tc (Using Numpy Arrays)
    tc = np.array( [s.mystring] * dim )

    try:

        # Read Data into Numpy Array
        status = dataset_id.read(h5py.h5s.ALL, h5py.h5s.ALL, tc, strtype,
                                 h5py.h5p.DEFAULT)
        # status = h5py.h5d.DatasetID.read(

    except Exception:

        print('\nread_atomic_names_hdf5() --- dataset_id.read Failed!!!')
        return 0

    # For Loop - Add Strings to Data
    count=0
    for i in range(0, len(tc)):
        t = ''.join(tc[i])
        data.append(t)
        if len(t)>0:
          count=count+1

    # Close Dataset ID
    # dataset_id._close()

    return count

# Writes Text on .bov File
def writeBOVheader(bov_filename, data_filename, origin, ll, mesh):

    # HMESH Constant
    HMESH = [ ll[0] / mesh[0], ll[1] / mesh[1], ll[2] / mesh[2] ] 
    # HMESH = hmesh( ll, mesh )

    # Start Writing Information on .bov File
    with open(bov_filename, 'w') as tfile:

        print('\nWrite down BOV header...')

        # Append All Neccessary Text to File
        tfile.write('TIME: 0.0')
        tfile.write('\nDATA_FILE: ' + data_filename)
        tfile.write('\nDATA_SIZE: ' + str(mesh[0]) + ' ' + str(mesh[1])
                    + ' ' + str(mesh[2]))
        tfile.write('\nDATA_FORMAT: FLOAT')
        tfile.write('\nVARIABLE: data')
        tfile.write('\nDATA_ENDIAN: LITTLE')
        tfile.write('\nCENTERING: zonal')

        ## Shift by -0.5 * h Because VisIt Assumes Cell Centered Data ##
        tfile.write('\nBRICK_ORIGIN: ' +
                    str( (origin[0] - 0.5 * HMESH[0]) * bohr2ang ) +
                    ' ' + 
                    str( (origin[1] - 0.5 * HMESH[1]) * bohr2ang ) +
                    ' ' +
                    str( (origin[2] - 0.5 * HMESH[2]) * bohr2ang ) )
        
        tfile.write( '\nBRICK_SIZE: ' +
                    str( (ll[0]) * bohr2ang ) + " " + 
                    str( (ll[1]) * bohr2ang ) + " " +
                    str( (ll[2]) * bohr2ang ) )

def map3d_header(tfile, origin, ll):

    print('\nWrite Down map3d Header...')

    tfile.write(' 600 600              // pixels')

    tfile.write('\n 0  -100    40        // viewPoint')

    tfile.write('\n' + str(origin[0] + 0.5 * ll[0]) + '\t'
                     + str(origin[1] + 0.5 * ll[1]) + '\t'
                     + str(origin[2] + 0.5 * ll[2]) + ' // screenCenter')

    tfile.write('\n 1     0     0        // horizontal direction')

    tfile.write('\n 100 -100 100 0.2 0.5 // lightSource,ambient,diff')

    tfile.write('\n 8.000000 8.000000    // hScreenSize, vScreenSize')

    tfile.write('\n LightBlue 0.6 1.0    // background color')

    tfile.write('\n 0.3  White           // bondradius, bond color')

# Void Function
def write_map3d_header(tfile, filename, origin, lattice):

    ''' Variables '''
    filename = ''.join(filename)

    # Check If File is in HDF5 Format
    try:

        # If h5py.is_hdf Method Fails, Stop
        ishdf = h5py.is_hdf5(filename)

    except Exception:

        print('\nh5py.is_hdf5 unsucessful')
        return

    # If File isn't an HDF5 File, Stop
    if( not(ishdf) ):

        print('\nInput File ' + filename + ' not in HDF5 Format. Stop.')
        return

    # If File is an HDF5 File, Proceed
    else:

        try:
                
            file_id = h5py.h5f.open(bytes(filename),
                          h5py.h5f.ACC_RDONLY, h5py.h5p.DEFAULT)
        
        except Exception:

            print('\nh5py.h5f.open(...) Failed For ' + filename)
            return

    # Vector - at_numbers (Lists)
    # at_numbers = np.array(...)

    # If Datasets, Atomic_numbers or Ionic_positions, are not Present
    try: 

        # Call read_atomic_numbers_hdf5
        n, at_numbers = read_atomic_numbers_hdf5(file_id)
        n = int(n)

        # Read Ionic Positions
        coord = read_ionic_positions_hdf5(file_id)

    except Exception:

        # if( n <= 0 or np.any(at_numbers) <= 0 or np.any(coord) == None ):
        print('\nread_atomic_numbers_hdf5() or read_ionic_positions_hdf5() '
              + '--- Read Failed')
        return -1

    # Call map3d_header
    map3d_header(tfile, origin, lattice)

    tfile.write('\n' + str(n) + '  // natoms')

    for i in range(0, n):

        ''' Variable '''
        at = int(at_numbers[i])
            
        tfile.write( '\n' + str( coord[3 * i] ) + '\t'
                         + str( coord[3 * i + 1] ) + '\t'
                         + str( coord[3 * i + 2] ) + '\t'
                         + str( ball_radii[at] ) + '\t'
                         + str( cov_radii[at] ) + '\t'
                         + str( colors[at] ) )

    tfile.write('\n1  // nfunctions')

    tfile.write('\n' + str(origin[0]) + '\t'
                     + str(origin[1]) + '\t'
                     + str(origin[2]) + '  // origin')

    tfile.write('\n' + str(lattice[0]) + '\t'
                     + str(lattice[1]) + '\t'
                     + str(lattice[2]) + '  // lattice')

    tfile.write('\nSteelBlue         // color')

    tfile.write('\n0.0004  0.        // flevel,thresh')

# Writes Text on .xyz File
def writeAtomsXYZ(xyz_filename, filename, origin, lattice):

    # Start Writing Information on .xyz File
    with open(xyz_filename, 'w') as tfile:

        ''' Variables '''
        # file_id = None

        # Check If Statement Executes Sucessfully
        try:
            
            ## File in HDF5 Format? ##
            ishdf = h5py.is_hdf5(filename)

        # If Error Occurs | File Doesn't Exist, Exit
        except Exception:

            print('\nh5py.is_hdf5 unsuccessful')
            return

        # If File isn't in HDF5 Format, Exit
        if( not(ishdf) ):

            print('\nInput File ' + filename + ' not in HDF5 Format. Stop')
            return

        # If File Exists, Get File's ID
        else:

            try:
                
                file_id = h5py.h5f.open(bytes(filename),
                              h5py.h5f.ACC_RDONLY, h5py.h5p.DEFAULT)

            except Exception:

                print('\nh5py.h5f.open(...) Failed For ' + filename)
                return

        # Make a Set with Chemical Elements (Unordered - Python)
        atomicsp = set()
        atomicsp.add('H')
        atomicsp.add('Li')
        atomicsp.add('Be')
        atomicsp.add('B')
        atomicsp.add('C')
        atomicsp.add('N')
        atomicsp.add('O')
        atomicsp.add('F')
        atomicsp.add('Na')
        atomicsp.add('Mg')
        atomicsp.add('Al')
        atomicsp.add('Si')
        atomicsp.add('P')
        atomicsp.add('S')
        atomicsp.add('Cl')
        atomicsp.add('K')
        atomicsp.add('Ca')
        atomicsp.add('Ni')
        atomicsp.add('Cu')
        atomicsp.add('Ga')
        atomicsp.add('Ge')
        atomicsp.add('Au')
        atomicsp.add('Zn')

        # Vector - at_names (Using Lists)
        at_names = []

        # Amount of Atomic Names Inside HDF5 File
        natoms = read_atomic_names_hdf5(file_id, at_names)

        # Get Data of Ionic Positions
        coord = read_ionic_positions_hdf5(file_id)

        # Number of Atoms
        tfile.write(str(natoms) + '\n')

        # If Datasets, Atomic_numbers or Ionic_positions, are not Present
        if( natoms <= 0 or np.any(coord) == None ):
            print('\nread_atomic_names_hdf5() or read_ionic_positions_hdf5() '
                  + '--- Read Failed')
            return -1

        # Iterate Through at_names List
        i=-1
        for name in at_names:

            i=i+1

            # Slicing List (substr (C++) - Slicing (Python))
            if len(name)==0:
              continue
            sp = name[0 : 2]

            # Iterator (in - Boolean)
            # p = sp in atomicsp   ->   (NOT NEEDED)

            # If Sliced Specie is the Same as Last Specie, Get First Letter
            # of New Specie
            #if( sp == list(atomicsp)[len(atomicsp) - 1] ):
            if sp not in atomicsp:

                sp = name[0 : 1]
                
            #
            if sp in atomicsp:
              x = coord[3 * i] 
              y = coord[3 * i + 1] 
              z = coord[3 * i + 2] 
              #move atoms into cell using periodicity
              if x<origin[0]:
                x = x + lattice[0]
              if y<origin[1]:
                y = y + lattice[1]
              if z<origin[2]:
                z = z + lattice[2]
              if x>origin[0]+lattice[0]:
                x = x - lattice[0]
              if y>origin[1]+lattice[1]:
                y = y - lattice[1]
              if z>origin[2]+lattice[2]:
                z = z - lattice[2]
              tfile.write('\n' + sp + '\t' +
                        str( x* bohr2ang ) +
                        '\t' +
                        str( y* bohr2ang ) +
                        '\t' +
                        str( z* bohr2ang ) +
                        '\t')


''' MAIN '''
# *argv (sys.argv in Python) - Takes an Arbitrary Number of Paramters
# and Stores Them in a List

# USAGE:
# ssh -l user cab.llnl.gov (If Using Cab System)
# python read_hdf5.py [ -bov | -map3d ] file.hdf5 datasetName

def main():

    ''' Variables '''
    datasetname = [''] * 50
    h5filename = [''] * 50
    buf = [''] * 255
    dims = np.arange(0, dtype = h5py.h5t.NATIVE_INT32)  # Turns Into a TUPLE
    dima = 1
    mapNum = 0
    xyzNum = 0

    # Lattice (Numpy Array)
    lattice = np.arange(0.0, dtype = h5py.h5t.NATIVE_DOUBLE)
    lattice.resize(3, refcheck = False)

    # Origin (Numpy Array)
    origin = np.arange(0.0, dtype = h5py.h5t.NATIVE_DOUBLE)
    origin.resize(3, refcheck = False)

    # Attributes (Numpy Array)
    attributes = np.arange(0.0, dtype = h5py.h5t.NATIVE_DOUBLE)

    tmap3d = False
    tbov = False

    if( len(sys.argv) > 1 ):
        tmap3d = not( (  sys.argv[1] > '-map3d' ) - ( sys.argv[1] < '-map3d' ) )
        tbov = not( ( sys.argv[1] > '-bov' ) - ( sys.argv[1] < '-bov' ) )

    index = 1

    if( tmap3d or tbov ):
        index = 2

    h5filename = copy.deepcopy( ''.join( sys.argv[index] ) )
    datasetname = copy.deepcopy( ''.join( sys.argv[index + 1] ) )

    print('\nDataset: ' + datasetname)

    # Get data - Call get_function
    try:
        
        data, dims = get_function(h5filename, datasetname, dims, origin,
                                         lattice, attributes, dima)
    except Exception:

        print('\nRead Failed. \nEither the HDF5 File ' +
              'or the Dataset are not Present. Stop. (TypeError)\n')
        return None

    # If data Empty, Stop.
    if( data == None or dims == None ):
        print('\nRead Failed.')
        return -1

    # From List of Strings to String Variable
    base_filename = ''.join( map( str, h5filename ) )

    # Remove File Extension ( .hdf5 )
    base_filename = base_filename.split('.')[0].strip()

    # Use base_filename to Make .dat Filename
    output_data_filename = base_filename
    output_data_filename += '_' + datasetname + '.dat'
    print('\noutput_data_filename = ' + output_data_filename)
    
    # New Array for Storing dims
    dim = [ int(dims[0]), int(dims[1]), int(dims[2]) ]

    # More Variables
    incx = dim[1] * dim[2]
    incy = dim[2]

    # Header, Including Atoms List
    if( tmap3d ):
        
        set_maps()
        header_filename = base_filename
        header_filename = header_filename + '_header.map3d'

        with open(header_filename, 'w') as tfile:

            mapNum = write_map3d_header(tfile, h5filename, origin, lattice)

        if( mapNum == -1 ):
            print('\nAtomic_numbers or Ionic_positions Datasets --- ' +
                  'Read Failed. map3d_header File not Completed')

    else:

        xyz_filename = base_filename
        xyz_filename = xyz_filename + '_atoms.xyz'

        xyzNum = writeAtomsXYZ(xyz_filename, h5filename, origin, lattice)

        if( xyzNum == -1 ):
            print('\nAtomic_names or Ionic_positions Datasets --- ' +
                  'Read Failed. _atoms.xyz File not Completed')

        if( tbov ):

            bov_filename = base_filename
            bov_filename = bov_filename + '.bov'
            print('\nbov_filename = ' + bov_filename)
            writeBOVheader(bov_filename, output_data_filename,
                                          origin, lattice, dim)

    ''' Function '''
    if( tbov ):

        # More Variables
        inczf = dim[1] * dim [0]
        incyf = dim[0]

        print('\nTranspose data...\n')

        fdata = np.array(0.0, np.float32)
        fdata.resize( (dim[0] * dim[1] * dim[2]), refcheck = False )

        # Transpose Data
        for i in range( dim[0] ):
            for j in range( dim[1] ):
                for k in range( dim[2] ):
                    index1 = (k * inczf) + (j * incyf) + i
                    index2 = (i * incx) + (j * incy) + k
                    fdata[index1] = float( data[index2] )
        
        print('\nWrite BOV data...\n')

        # Open Binary File and Write Data (If File Doesn't Exist,
        # Create a New One)
        with open(output_data_filename, 'wb') as binary:

            # Format of Data to be Written as Binary
            fmt = 'f' * len( fdata )

            # Pack *fdata, According to format string fmt, and Return Bytes  
            fbin = struct.pack( fmt, *fdata )

            # Write Bytes to File
            binary.write(fbin)

    else:

        print('\nWrite data...\n')

        with open(output_data_filename, 'w') as tfile:

            if( not( tmap3d ) ):

                tfile.write('\n' + str( origin[0] ) + '\t'
                                 + str( origin[1] ) + '\t'
                                 + str( origin[2] ) + '\t'
                                 + str( origin[0] + lattice[0] ) + '\t'
                                 + str( origin[1] + lattice[1] ) + '\t'
                                 + str( origin[2] + lattice[2] )
                                 + '  // cell corners')

            tfile.write(str(dim[0]) + '\t' + str(dim[1]) + '\t'
                        + str(dim[2]) + ' // mesh')

            for i in range( dim[0] ):
                for j in range( dim[1] ):
                    for k in range( dim[2] ):
                        row = (i * incx) + (j * incy) + k
                        tfile.write('\n' + str( data[row] ))

    # Release Data and Attributes
    del data
    del attributes
        
    return 0

# Executes Main Function
if __name__ == '__main__':

    main()
