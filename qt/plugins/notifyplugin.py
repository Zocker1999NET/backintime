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
import os
import dbus
import pluginmanager


class NotifyPlugin(pluginmanager.Plugin):
    def __init__(self):
        self.user = ''

        try:
            self.user = os.getlogin()
        except:
            pass

        if not self.user:
            try:
                self.user = os.environ['USER']
            except:
                pass

        if not self.user:
            try:
                self.user = os.environ['LOGNAME']
            except:
                pass

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

        except dbus.exceptions.DBusException:
            return

        if 1 == level:

            if timeout > 0:
                timeout = 1000 * timeout
            else:
                timeout = -1 # let timeout default to notification server settings

            title = "Back In Time (%s) : %s" % (self.user, profile_name)
            message = message.replace("\n", ' ')
            message = message.replace("\r", '')

            try:
                notify_interface.Notify(
                    "Back In Time", 0, "", title, message, [], {}, timeout)

            except dbus.exceptions.DBusException:
                pass

        return
