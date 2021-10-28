"""
External storage configuration module.

Example is using microns_minnie65_02's external storage.
"""

# IMPORTANT: The way the external store paths are defined here isn't really important. The main thing this example is showing is the actual stores_config dictionary updating dj.config['stores'].

from pathlib import Path

segmentation_m65 = 2
segmentation_m65_str = '{:02d}'.format(segmentation_m65)

_schema_base_name = 'microns_minnie65_'
schema_name_m65 = _schema_base_name + segmentation_m65_str

path_obj = Path() / '/mnt' / 'dj-stor01'

external_store_basepath = path_obj / 'platinum' / 'minnie65'
external_segmentation_path = path_obj / external_store_basepath / segmentation_m65_str
external_mesh_path = external_segmentation_path / 'meshes'
external_decimated_mesh_path = external_segmentation_path / 'decimated_meshes'
external_skeletons_path = external_segmentation_path / 'skeletons'
external_faces_path = external_segmentation_path / 'glia_nuclei_faces'
external_skeleton_path = external_segmentation_path / 'compartment_skeletons'
external_closest_distance_path = external_segmentation_path / 'closest_distance'
external_decomposition_path = external_segmentation_path / 'decomposition'

def make_store_dict(path):
    return {
        'protocol': 'file',
        'location': str(path),
        'stage': str(path)
    }
    
# External filepath referrencing.
stores_config = {
    'minnie65': make_store_dict(external_store_basepath),
    'meshes': make_store_dict(external_mesh_path),
    'decimated_meshes': make_store_dict(external_decimated_mesh_path),
    'skeletons': make_store_dict(external_skeletons_path),
    'faces': make_store_dict(external_faces_path),
    'skeleton': make_store_dict(external_skeleton_path),
    'closest_distance': make_store_dict(external_closest_distance_path),
    'decomposition': make_store_dict(external_decomposition_path),
}

# # The above could also be done like so, though the above is a bit more flexible if one of the external store configs needs to be different.
# stores_config = [
#     ('minnie65', external_store_basepath),
#     ('meshes', external_mesh_path),
#     ('decimated_meshes', external_decimated_mesh_path),
#     ('skeletons', external_skeletons_path),
#     ('faces', external_faces_path),
#     ('skeleton', external_skeleton_path),
#     ('closest_distance', external_closest_distance_path),
#     ('decomposition', external_decomposition_path),
# ]
# stores_config = {key: make_store_dict(path) for key, path in stores_config}
