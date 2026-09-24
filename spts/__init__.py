def _init():
    import logging, sys

    # Set up the logger first, before anything that could raise (e.g. a
    # missing hdf5plugin below) -- otherwise an exception here leaves `spts`
    # partially imported with no `logger` attribute, which surfaces
    # downstream as a confusing "module 'spts' has no attribute 'logger'"
    # AttributeError instead of the real (e.g. ModuleNotFoundError) cause.
    global logger
    logger = logging.getLogger('spts')

    # Registers hdf5plugin's bundled filter plugins (blosc/lz4/zstd/etc.) with
    # HDF5's plugin search path as an import-time side effect. Without this,
    # reading datasets written with a non-builtin compression filter fails with
    # "Can't synchronously read data (can't open directory .../hdf5/plugin)".
    import hdf5plugin

    # import pkg_resources
    # global __version__
    # __version__ = pkg_resources.require("spts")[0].version

    from importlib.metadata import version, PackageNotFoundError

    global __version__
    try:
        __version__ = version("spts")
    except PackageNotFoundError:
            # Fallback if the package is not installed (e.g. running from source)
        __version__ = "unknown"

    
_init()
