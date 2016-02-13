from shields import pypi


generators = {
    'pypi': {
        'd': pypi.DownloadHandler,
        'download': pypi.DownloadHandler,
        'v': pypi.VersionHandler,
        'version': pypi.VersionHandler,
        'wheel': pypi.WheelHandler,
        'egg': pypi.EggHandler,
        'license': pypi.LicenseHandler,
        'format': pypi.FormatHandler,
        'py_versions': pypi.PythonVersionsHandler,
        'implementation': pypi.ImplementationHandler,
        'status': pypi.StatusHandler,
    }
}
