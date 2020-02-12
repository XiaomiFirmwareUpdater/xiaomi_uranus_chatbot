""" MIUI Updates utilities """


async def get_branch(version):
    """
    get MIUI branch based on MIUI version
    :param version: MIUI version, stable/weekly
    :return: branch
    """
    return 'Stable' if version.startswith('V') else 'Weekly'


async def get_region(filename, codename, version):
    """ Get the region of an update """
    if 'eea_global' in filename or 'eea_global' in codename or 'EU' in version:
        region = 'EEA'
    elif 'id_global' in filename or 'id_global' in codename or 'ID' in version:
        region = 'Indonesia'
    elif 'in_global' in filename or 'in_global' in codename or 'IN' in version:
        region = 'India'
    elif 'ru_global' in filename or 'ru_global' in codename or 'RU' in version:
        region = 'Russia'
    elif 'global' in filename or 'global' in codename or 'MI' in version:
        region = 'Global'
    else:
        region = 'China'
    return region


async def get_type(update):
    """ Get the type of an update """
    return 'Fastboot' if '.tgz' in update else 'Recovery'
