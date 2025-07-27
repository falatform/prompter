def require_package(pkg_name: str, import_name: str = None, extra: str = None):
    """
    Try to import a package, raise ImportError with a helpful message if not installed.
    :param pkg_name: The name to show in the error message (e.g. 'openai')
    :param import_name: The name to actually import (if different from pkg_name)
    :param extra: Optional pip extra to suggest (e.g. 'prompter[openai]')
    :return: The imported module
    """
    import importlib
    import_name = import_name or pkg_name
    try:
        return importlib.import_module(import_name)
    except (ImportError, ModuleNotFoundError):
        msg = f"The '{pkg_name}' package is required for this provider. "
        if extra:
            msg += f"Install with: pip install {extra}"
        else:
            msg += f"Install with: pip install {pkg_name}"
        raise ImportError(msg)
