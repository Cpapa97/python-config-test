"""
Configuration package/module for minnie. Experimental version.
"""

from . import adapters
from . import externals

import datajoint as dj

# Also important to run the dj flags at SOME point during normal datajoint initialization, probably don't want to have this in every config though?
from . import utils
utils.enable_datajoint_flags()

# IMPORTANT: You can organize several schemas' config files (or folders) however you want as long as
# the correct schema configurations are plugged in for the enum variations (obviously).

from enum import Enum

class SCHEMAS(Enum):
    MINNIE65 = 'microns_minnie65_02'


def register_externals(stores_config: dict):
    """
    Registers the external stores for a schema in this module.
    """
    
    if 'stores' not in dj.config:
        dj.config['stores'] = stores_config
    else:
        dj.config['stores'].update(stores_config)


def register_adapters(adapter_objects: dict, context=None):
    """
    Imports the adapters for a schema into the global namespace.
    
    This function is probably not necessary, but standardization is nice.
    """
    
    if context is None:
        # if context is missing, use the calling namespace
        import inspect
        frame = inspect.currentframe().f_back
        context = frame.f_locals
        del frame
    
    for name, adapter in adapter_objects.items():
        context[name] = adapter


# Typing annotation hints not strictly necessary. This import is also not necessary if you only specify one type.
from typing import Union

def create_vm(schema: Union[SCHEMAS, str]):
    """
    Creates a virtual module after registering the external stores, and includes the adapter objects in the vm.
    """
    
    # Steps that create_vm should take for each schema:
    # 1. Register externals with dj.config
    # 2. Choose which schema's config to load.
    # 3. Load a dict with the relevant adapters into the adapter object field of a virtual module.
    
    schema = SCHEMAS(schema)
    
    if schema is SCHEMAS.MINNIE65:
        schema_name = schema.value # MAKE SURE YOU PASS THE VALUE OF THE ENUM TO dj.create_virtual_module and NOT the ACTUAL ENUM.
        register_externals(externals.stores_config) # This would be the stores_config for a specific schema.
        vm = dj.create_virtual_module(schema_name, schema_name, add_objects=adapters.adapter_objects) # This would be the adapter_objects for a specific schema.
    else:    
        raise NotImplementedError("Another schema ({schema}) would go here if there were more.")
    
    return vm
