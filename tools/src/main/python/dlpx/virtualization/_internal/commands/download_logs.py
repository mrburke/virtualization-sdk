#
# Copyright (c) 2019 by Delphix. All rights reserved.
#

import logging

from dlpx.virtualization._internal import delphix_client, package_util
from dlpx.virtualization.common.util import to_bytes, to_str

logger = logging.getLogger(__name__)


def download_logs(engine, plugin_config, user, password, directory):
    """
    Download plugin logs from a Delphix Engine.

    Args:
        engine: Delphix Engine hostname or IP address
        plugin_config: Config file to fetch plugin name
        user: User to log in to the Delphix Engine
        password: Password for the user to log in to the Delphix Engine
        directory: Directory of where plugin logs should be downloaded

    Raises specifically:
        UserError
        HttpError
        UnexpectedError
    """
    logger.debug('Download parameters include'
                 ' engine: {},'
                 ' plugin_config: {}'
                 ' user: {},'
                 ' directory: {}'.format(engine, plugin_config, user,
                                         directory))
    logger.info('Downloading plugin logs from {} to: {}'.format(
        engine, directory))

    engine = to_str(engine)
    plugin_config = to_str(plugin_config)
    user = to_str(user)
    password = to_str(password)
    directory = to_str(directory)

    # Create a new delphix session.
    client = delphix_client.DelphixClient(engine)
    client.login(package_util.get_engine_api_version(), user, password)
    client.download_plugin_logs(directory, plugin_config)
