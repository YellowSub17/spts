def _init():
    import logging, sys

    global logger
    logger = logging.getLogger('spts')

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
