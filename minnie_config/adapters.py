"""
Adapter module.
"""

import datajoint as dj
import numpy as np
import h5py
import os

from collections import namedtuple


class MeshAdapter(dj.AttributeAdapter):
    # Initialize the correct attribute type (allows for use with multiple stores)
    def __init__(self, attribute_type):
        self.attribute_type = attribute_type
        super().__init__()

    attribute_type = '' # this is how the attribute will be declared

    TriangularMesh = namedtuple('TriangularMesh', ['segment_id', 'vertices', 'faces'])
    
    def put(self, filepath):
        # save the filepath to the mesh
        filepath = os.path.abspath(filepath)
        assert os.path.exists(filepath)
        return filepath

    def get(self, filepath):
        # access the h5 file and return a mesh
        assert os.path.exists(filepath)

        with h5py.File(filepath, 'r') as hf:
            vertices = hf['vertices'][()].astype(np.float64)
            faces = hf['faces'][()].reshape(-1, 3).astype(np.uint32)
        
        segment_id = os.path.splitext(os.path.basename(filepath))[0]

        return self.TriangularMesh(
            segment_id=int(segment_id),
            vertices=vertices,
            faces=faces
        )
    

class DecimatedMeshAdapter(dj.AttributeAdapter):
    # Initialize the correct attribute type (allows for use with multiple stores)
    def __init__(self, attribute_type):
        self.attribute_type = attribute_type
        super().__init__()

    attribute_type = '' # this is how the attribute will be declared
    has_version = False # used for file name recognition

    TriangularMesh = namedtuple('TriangularMesh', ['segment_id', 'version', 'decimation_ratio', 'vertices', 'faces'])
    
    def put(self, filepath):
        # save the filepath to the mesh
        filepath = os.path.abspath(filepath)
        assert os.path.exists(filepath)
        return filepath

    def get(self, filepath):
        # access the h5 file and return a mesh
        assert os.path.exists(filepath)

        with h5py.File(filepath, 'r') as hf:
            segment_id = hf['segment_id'][()].astype(np.uint64)
            version = hf['version'][()].astype(np.uint8)
            decimation_ratio = hf['decimation_ratio'][()].astype(np.float64)
            vertices = hf['vertices'][()].astype(np.float64)
            faces = hf['faces'][()].reshape(-1, 3).astype(np.uint32)
        
        return self.TriangularMesh(
            segment_id=int(segment_id),
            version=version,
            decimation_ratio=decimation_ratio,
            vertices=vertices,
            faces=faces
        )


import bz2
import pickle
from pathlib import Path

# Load any compressed pickle file
def decompress_pickle(filename):
    """
    Example: 
    data = decompress_pickle('example_cp.pbz2') 
    """
    if not isinstance(filename, Path):
        filename = Path(filename)
    if filename.suffix != ".pbz2":
        filename = filename.with_suffix(".pbz2")

    data = bz2.BZ2File(filename, 'rb') # Possibly slow (or it could be the datajoint UUID checks)
    data = pickle.load(data)
    return data


from enum import Enum

class SkeletonVersion(Enum):
    "Skeleton version adapater."
    V3 = 'v3'
    V4 = 'v4'


class FacesAdapter(dj.AttributeAdapter):
    # Initialize the correct attribute type (allows for use with multiple stores)
    def __init__(self, attribute_type, version: SkeletonVersion = SkeletonVersion.V3):
        self.attribute_type = attribute_type
        self.version = version
        super().__init__()

    attribute_type = '' # this is how the attribute will be declared

    def put(self, filepath):
        # save the filepath to the mesh
        filepath = os.path.abspath(filepath)
        assert os.path.exists(filepath)
        return filepath

    def get(self, filepath):
        # access the h5 file and return a mesh
        assert os.path.exists(filepath)

        if self.version == SkeletonVersion.V3:
            return decompress_pickle(filepath)
        elif self.version == SkeletonVersion.V4:
            with np.load(filepath) as f:
                skeleton = f['data']
            return skeleton



class SkeletonAdapter(dj.AttributeAdapter):
    # Initialize the correct attribute type (allows for use with multiple stores)
    def __init__(self, attribute_type, version: SkeletonVersion = SkeletonVersion.V4):
        self.attribute_type = attribute_type
        self.version = version
        super().__init__()

    attribute_type = '' # this is how the attribute will be declared

    def put(self, filepath):
        # save the filepath to the mesh
        filepath = os.path.abspath(filepath)
        assert os.path.exists(filepath)
        return filepath

    def get(self, filepath):
        # access the h5 file and return a mesh
        assert os.path.exists(filepath)

        if self.version == SkeletonVersion.V3:
            return decompress_pickle(filepath)
        elif self.version == SkeletonVersion.V4:
            with np.load(filepath) as f:
                skeleton = f['data']
            return skeleton


# Decompositions
class DecompositionAdapter(dj.AttributeAdapter):
    # Initialize the correct attribute type (allows for use with multiple stores)
    def __init__(self, attribute_type):
        self.attribute_type = attribute_type
        super().__init__()
    
    attribute_type = '' # this is how the attribute will be declared
    
    has_version = False # used for file name recognition
    
    def put(self, filepath):
        # save the filepath to the mesh
        filepath = os.path.abspath(filepath)
        assert os.path.exists(filepath)
        return filepath
    
    def get(self,filepath):
        """
        1) Get the filepath of the decimated mesh
        2) Make sure that both file paths exist
        3) use the decompress method
        """

        #1) Get the filepath of the decimated mesh
        filepath = Path(filepath)
        assert os.path.exists(filepath)
        """Old way where used the file path
        dec_filepath = get_decimated_mesh_path_from_decomposition_path(filepath)
        assert os.path.exists(dec_filepath)
        print(f"Attempting to get the following files:\ndecomp = {filepath}\ndec = {dec_filepath} ")
        """
        """
        ---- 4/26 Change that will only send back the filepath
        """
        return filepath


# IMPORTANT: The adapter_objects dict must have the same names as keys as the actual adapters used in the table definitions (same for the instantiations of the adapters below, but that part only matters when they're imported standalone into the global namespace).

# instantiate for use as a datajoint type
mesh = MeshAdapter('filepath@meshes')
decimated_mesh = DecimatedMeshAdapter('filepath@decimated_meshes')
faces = FacesAdapter('filepath@faces')
skeleton = SkeletonAdapter('filepath@skeleton')
decomposition = DecompositionAdapter('filepath@decomposition')

# also store in one object for ease of use with virtual modules
adapter_objects = {
    'mesh': mesh,
    'decimated_mesh': decimated_mesh,
    'faces': faces,
    'skeleton': skeleton,
    'decomposition': decomposition
}

__all__ = ['mesh', 'decimated_mesh', 'faces', 'skeleton', 'decomposition']