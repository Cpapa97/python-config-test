def enable_datajoint_flags():
    """
    Enable experimental datajoint features
    
    These flags are required by 0.12.0+ (for now).
    """
    import datajoint as dj
    
    dj.config['enable_python_native_blobs'] = True
    dj.errors._switch_filepath_types(True)
    dj.errors._switch_adapted_types(True)
