#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

from gi.repository import GObject

from datetime import datetime

import dbus
import dbus.mainloop.glib
from optparse import OptionParser, make_option
import bluezutils

compact = False
devices = {}


def get_distance(txPower, rssi):
	if (rssi == 0):
		return -1.0 #; // if we cannot determine accuracy, return -1.
	
	ratio_db = txPower - rssi

	ratio_linear = pow (10, ratio_db / 10)

	r = pow (ratio_linear, 0.5)

	return r


def print_compact(address, properties):
	name = ""
	address = "<unknown>"
	RSSI = -1

	timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	for key, value in properties.iteritems():
		if type(value) is dbus.String:
			value = unicode(value).encode('ascii', 'replace')
		if (key == "Name"):
			name = value
		elif (key == "Address"):
			address = value
		elif (key == "RSSI"):
			RSSI = value

	if ("AprilBeacon" in name):
 		print("%s,%s,%s,%d,%d" % (timestamp, address, name, RSSI, get_distance(-67,RSSI)))	

	properties["Logged"] = True


def print_normal(address, properties):
	print("[ " + address + " ]")

	for key in properties.keys():
		value = properties[key]
		if type(value) is dbus.String:
			value = unicode(value).encode('ascii', 'replace')
		if (key == "Class"):
			print("    %s = 0x%06x" % (key, value))
		else:
			print("    %s = %s" % (key, value))

	print()

	properties["Logged"] = True

def skip_dev(old_dev, new_dev):
	if not "Logged" in old_dev:
		return False
	if "Name" in old_dev:
		return True
	if not "Name" in new_dev:
		return True
	return False

def interfaces_added(path, interfaces):
	properties = interfaces["org.bluez.Device1"]
	if not properties:
		return

	if path in devices:
		dev = devices[path]

		if compact and skip_dev(dev, properties):
			return
		devices[path] = dict(devices[path].items() + properties.items())
	else:
		devices[path] = properties

	if "Address" in devices[path]:
		address = properties["Address"]
	else:
		address = "<unknown>"

	if compact:
		print_compact(address, devices[path])
	else:
		print_normal(address, devices[path])

def properties_changed(interface, changed, invalidated, path):
	if interface != "org.bluez.Device1":
		return

	if path in devices:
		dev = devices[path]

		if compact and skip_dev(dev, changed):
			return
		devices[path] = dict(devices[path].items() + changed.items())
	else:
		devices[path] = changed

	if "Address" in devices[path]:
		address = devices[path]["Address"]
	else:
		address = "<unknown>"

	if compact:
		print_compact(address, devices[path])
	else:
		print_normal(address, devices[path])

def property_changed(name, value):
	if (name == "Discovering" and not value):
		mainloop.quit()

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

	bus = dbus.SystemBus()

	option_list = [
			make_option("-i", "--device", action="store",
					type="string", dest="dev_id"),
			make_option("-c", "--compact",
					action="store_true", dest="compact"),
			]
	parser = OptionParser(option_list=option_list)

	(options, args) = parser.parse_args()

	adapter = bluezutils.find_adapter(options.dev_id)

	if options.compact:
		compact = True;

	bus.add_signal_receiver(interfaces_added,
			dbus_interface = "org.freedesktop.DBus.ObjectManager",
			signal_name = "InterfacesAdded")

	bus.add_signal_receiver(properties_changed,
			dbus_interface = "org.freedesktop.DBus.Properties",
			signal_name = "PropertiesChanged",
			arg0 = "org.bluez.Device1",
			path_keyword = "path")

	bus.add_signal_receiver(property_changed,
					dbus_interface = "org.bluez.Adapter1",
					signal_name = "PropertyChanged")

	om = dbus.Interface(bus.get_object("org.bluez", "/"),
				"org.freedesktop.DBus.ObjectManager")
	objects = om.GetManagedObjects()
	for path, interfaces in objects.iteritems():
		if "org.bluez.Device1" in interfaces:
			devices[path] = interfaces["org.bluez.Device1"]

	adapter.StartDiscovery()

	mainloop = GObject.MainLoop()
	mainloop.run()