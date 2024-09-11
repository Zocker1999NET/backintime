# SPDX-FileCopyrightText: © 2008-2022 Oprea Dan
# SPDX-FileCopyrightText: © 2008-2022 Bart de Koning
# SPDX-FileCopyrightText: © 2008-2022 Richard Bailey
# SPDX-FileCopyrightText: © 2008-2022 Germar Reitze
# SPDX-FileCopyrightText: © 2021 Felix Stupp
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In Time" which is released under GNU
# General Public License v2 (GPLv2).
# See file LICENSE or go to <https://www.gnu.org/licenses/#GPL>.
"""Notify plugin module"""
import getpass
import dbus
import pluginmanager
import logger


class NotifyPlugin(pluginmanager.Plugin):
    """Plugin used to create notification bubbles in systray.

    The plugin use DBUS to send notifications. See its base class for more
    details.
    """

    def isGui(self):
        return True

    def message(self, profile_id, profile_name, level, message, timeout):
        try:
            notify_interface = dbus.Interface(
                object=dbus.SessionBus().get_object(
                    "org.freedesktop.Notifications",
                    "/org/freedesktop/Notifications"),
                dbus_interface="org.freedesktop.Notifications"
            )

        except dbus.exceptions.DBusException as exc:
            logger.error('Unexpected DBusException while initating '
                         f'dbus.Interface(): {exc}')
            return

        # 1 is ERROR, 0 is INFO
        if level != 1:
            # Dev note (2024-10, buhtz):
            # To my research (using "grep") BIT never use a level value
            # different from "1".
            # This level might be a "feature" that was planed but never used.
            # The level handling then should be removed from BIT.
            logger.error(
                f'Unexpected message level "{level}" in NotifyPlugin. The '
                f'message is: "{message}".')
            return

        if timeout > 0:
            timeout = 1000 * timeout
        else:
            # let timeout default to notification server settings
            timeout = -1

        title = f'Back In Time ({getpass.getuser()}) : {profile_name}'
        message = message.replace('\n', ' ')
        message = message.replace('\r', '')

        try:
            notify_interface.Notify(
                'Back In Time', 0, '', title, message, [], {}, timeout)

        except dbus.exceptions.DBusException as exc:
            logger.error(f'Unexpected DBusException while Notify(): {exc}')
