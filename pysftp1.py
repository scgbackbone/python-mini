#!/usr/bin/env python

import pysftp as sftp
import os
import colorama
from colorama import init, Fore, Back, Style
import sys

# this function return tuple where in position 0 is path to a file splitted on '/'
# and filename or directory on index 1
def normalizeAndSplit(path):
	path = os.path.normpath(path).split(os.sep)
	return path[:-1], path[-1]

def successfull_transmition(local, remote):
	print(Fore.GREEN + "Successfull transmition")
	print(Fore.GREEN + "{} ==> {}".format(local, remote))


def push_file(conn):
	colorama.init()
	local_path = sys.argv[2]
	remote_path = sys.argv[3]

	if os.path.isfile(local_path):
		try:
			conn.put(local_path, remote_path)
		except Exception as e:
			print(Fore.RED + str(e))
			return None
	elif os.path.isdir(local_path):
		print("Directory to be transmitted: {}".format(local_path))
		try:
			conn.put_r(local_path, remote_path)
		except Exception as e:
			print(Fore.RED + str(e))
			return None
	else:
		print(Fore.RED + "Not a file, not a directory.")
	conn.close()
	successfull_transmition(local_path, remote_path)

def pull_file(conn):
	colorama.init()
	local_path = sys.argv[3]
	remote_path = sys.argv[2]

	try:
		paths, fileORdir = normalizeAndSplit(remote_path)
		with conn.cd():
			for pathpart in paths:
				conn.chdir(pathpart)
			if conn.isfile(fileORdir):
				print("File to be pulled from remote host: {}".format(fileORdir))
				conn.get(fileORdir, local_path)
			elif conn.isdir(fileORdir):
				print("Directory to be pulled from remote host: {}".format(fileORdir))
				#if not os.path.isdir(local_path):
				#	dirname = os.path.basename(os.path.normpath(local_path))
				#	os.mkdir(dirname)
				#	print("Created directory: {}".format(local_path))
				conn.get_r(fileORdir, local_path)
			else: print("wtf")
	except Exception as e:
		print(Fore.RED + str(e))
		return None
	conn.close()
	successfull_transmition(remote_path, local_path)

def create_dir(conn, path):
	path = os.path.normpath(path).split(os.sep)
	# paths is a list, fileordir is a string
	paths, fileORdir = path[:-1], path[-1]
	with conn.cd():
		conn.makedirs(path)

def main():
	if sys.argv[1] == "push" or sys.argv[1] == "pull":
		s = sftp.Connection(host=os.environ.get("PYSFTP_HOST"),
							username=os.environ.get("PYSFTP_UNAME"),
							password=os.environ.get("PYSFTP_PASSWD"))

	else:
		print("push to a server: pysftp1 push local remote")
		print("pull from server: pysftp1 pull remote local")

	if sys.argv[1] == "push":
		push_file(s)
	elif sys.argv[1] == "pull":
		pull_file(s)

if __name__ == "__main__":
	main()
