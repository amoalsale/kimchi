#
# Project Kimchi
#
# Copyright IBM, Corp. 2013
#
# Authors:
#  Aline Manera <alinefm@br.ibm.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import libvirt
import os

import config

ISO_STREAM_XML = """
<domain type='kvm'>
  <name>ISO_STREAMING</name>
  <uuid>c7a5fdbd-edaf-9455-926a-d65c16db1809</uuid>
  <memory unit='KiB'>1048576</memory>
  <currentMemory unit='KiB'>1048576</currentMemory>
  <vcpu placement='static'>1</vcpu>
  <os>
    <type arch='x86_64' machine='pc-1.2'>hvm</type>
    <boot dev='cdrom'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices>
    <emulator>/usr/bin/kvm</emulator>
    <disk type='network' device='cdrom'>
      <driver name='qemu' type='raw'/>
      <source protocol='%(protocol)s' name='/url/path/to/iso/file'>
        <host name='host.name' port='1234'/>
      </source>
      <target dev='hdc' bus='ide'/>
      <readonly/>
      <alias name='ide0-1-0'/>
      <address type='drive' controller='0' bus='1' target='0' unit='0'/>
    </disk>
    <controller type='usb' index='0'/>
    <controller type='pci' index='0' model='pci-root'/>
    <controller type='ide' index='0'/>
    <memballoon model='virtio'/>
  </devices>
</domain>"""

class FeatureTests(object):

    @staticmethod
    def is_iso_stream_supported(protocol):
        xml = ISO_STREAM_XML % {'protocol': protocol}

        try:
            conn = libvirt.open('qemu:///system')
            dom = conn.defineXML(xml)
            dom.undefine()
            return True
        except libvirt.libvirtError:
            return False