#!/usr/bin/python3
import sys
import os
from socket import *
import time
from getpass import getpass
import readline
import signal

anonymous = "0"
def timer():	
	now = time.localtime(time.time())
	return now[5]

def speed(start, end, bytes):
	totaltime = end - start
	if(totaltime == 0):
		totaltime = 1
	speed = int(bytes/totaltime)
	print("Total bytes trasferred: {}".format(bytes))				
	print("speed {} bytes/sec".format(speed))
	return			
	
def file_info(filename):
	li = []
	try:
		size = "0"
		info = os.stat(filename)
		if(info != None):
			size = str(info.st_size)
			ack = "yes"
		else:
			ack = "no!"
		li.append(ack)
	except IOError:
		ack = "NO!"
		li.append(ack)
	li.append(size)		
	return li
def comm(ccsocket, datasocket):
	global anonymous
	hashflag = 0;
	history = ['open']
	prompt = "0"
	while(1):
		
		def handler(signum, frame):
			pass
		signal.signal(signal.SIGINT, handler)
		sentence= []
		print("ftp>",end= '')
		data = input()
		sentence = list(data.split(" "))
		sentence.append(anonymous)
		dataip = " ".join(sentence)
		sentence.pop()
		command = sentence[0]
		if(command != 'history'):
			history.append(command)
		if(command != "send" and command != "put"):
			ccsocket.send(dataip.encode())
		if(command == 'pwd'):
			ans = ccsocket.recv(1024).decode()	
			print(ans)
		elif(command == "hash"):
			if(hashflag == 0):
				hashflag = 1;
			else:
				hashflag = 0;
		elif(command == "history"):
			index = 1
			for i in history:
				print(index, end =" ")
				print(i)
				index += 1
		elif(command == "system"):
			ack = ccsocket.recv(1024).decode()
			li = list(ack.split(" "))
			for i in li:
				print(i)

		elif(command == "prompt"):
			if(prompt == "0"):
				prompt = "1"
				print("Interactive session off")
			else:
				prompt = "0"
				print("Interactive session on")
		elif(command == "cdup"):
			ack = ccsocket.recv(3).decode()
			if(ack == "yes"):
				print("Directory changed successfully")
			else:
				print("Directory cannot be changed")
		elif(command == "lcd"):
			try:
				os.chdir(data[4:])
				print("Directory changed successfully")
			except IOError:
				print("Directory does not exist!")
		elif(command == "cd"):
			ack = ccsocket.recv(1024).decode()
			if(ack == "yes"):
				print("Directory changed successfully!")
			else:
				print(ack)
		elif(command == "nlist"):
			if(len(sentence) > 1):
				ans = ccsocket.recv(1024).decode()
				if(ans != "no!"):
					li = list(ans.split(" "))
					for i in li:
						print(i)
				else:
					print("No such directory!")
			else:
				print("Mention Directory name")
		elif(command == "reget"):
			if(len(sentence) > 1):
				ack = ccsocket.recv(3).decode()
				li = file_info(sentence[1])
				reply = li[0]
				ccsocket.send(reply.encode())
				if(ack == "yes" and reply == "yes"):
					remotesize = ccsocket.recv(100).decode()
					ccsocket.send(li[1].encode())
					remotesize = int(remotesize)
					localsize = int(li[1])
				
					if(localsize < remotesize):
						count = ((remotesize - localsize)//1024) + 1					
						with open(sentence[1],'ab') as fd:
							while(count != 1):
								ans = datasocket.recv(1024)
								if(hashflag == 1):
									print("#",end = "")
								fd.write(ans)
								count = count - 1
							fd.close()
						if(hashflag == 1):
							print("")
						print("File {} downloaded successfully".format(sentence[1]))
					else:
						print("Whole file present, no need to download")	
				else:
					print("Error: File does not appear to exist.")
			else:
				print("Enter filename")
	
		elif(command == "ls" or command == "dir"):
			ack = ccsocket.recv(3).decode()
			if(ack == "yes"):
				size = ccsocket.recv(1024).decode()
				size = int(size)
				ans = datasocket.recv(size).decode()
				print(ans)
			else:
				print("Error: File does not appear to exist.")
		
		elif(command =='get' or command == "recv"):
			if(len(sentence) > 1):
				ack = ccsocket.recv(3).decode()
				if(ack == "yes"):
					start = timer()
					ack = ccsocket.recv(1024).decode()
					li = list(ack.split(" "))
					size = li[2]
					filename = li[1]
					val = int(size)
					count = val//1024
					count = count + 1
					with open(filename,'ab') as fd:
						while(count != 0):
							ans = datasocket.recv(1024)
							if(hashflag == 1):
								print("#",end = "")
							fd.write(ans)
							count = count - 1
						fd.close()
					if(hashflag == 1):
						print("")	
					end = timer()
					print("File {} downloaded successfully".format(filename))
					speed(start, end, val)
				else:
					print("Error: File does not appear to exist.")
			else:
				print("Enter filename")
		elif(command == 'mget'):
			if(len(sentence) > 1):
				files = sentence[1:]
				for i in files:
					print("123")
					ack = ccsocket.recv(3).decode()
					if(ack == "yes"):
						if(prompt == "0"):
							print("Do you want to download {}? y/n".format(i))
							ack = input()
						else:
							ack = "y"
						ccsocket.send(ack.encode())
						if(ack == "y"):
							start = timer()
							size = ccsocket.recv(1024).decode()
							val = int(size)
							count = val//1024
							count = count + 1
							with open(i, 'ab') as fd:
								while(count != 0):
									ans = datasocket.recv(1024)
									if(hashflag == 1):
										print("#",end = "")
									fd.write(ans)
									count = count - 1
								fd.close()
							if(hashflag == 1):
								print("")
							end = timer()
							print("File {} downloaded successfully".format(i))
							speed(start, end, val)
						else:
							pass
					else:
						print("Error:{} does not exist".format(i))
			else:
				print("Enter filenames")
		elif(command == 'put' or command == 'send'):
			if(len(sentence) > 1):
				filename = []
				filename = sentence[0:]
				if(len(filename) == 2):
					filename.append(filename[1])
				li = file_info(filename[1])
				filename.append(li[0])
				filename.append(li[1])
				filename.append(anonymous)
				ack = " ".join(filename)
				print(ack)
				ccsocket.send(ack.encode())
				if(anonymous == "0"):
					if(li[0] == "yes"):
						print("in ack")
						val = int(li[1])
						start = timer()
						f = open(filename[1],'rb')
						ans = f.read(1024)
						while(ans):
							datasocket.send(ans)
							if(hashflag == 1):
								print("#",end = "")
							ans = f.read(1024)
						f.close()
						if(hashflag == 1):
							print("")
						end = timer()
						print("File {} transferred successfully".format(filename[1]))
						speed(start, end, val)
					else:
						print("File does not appear to exist.")
				else:
					print("Anonymous user can not send files")	
			else:
				pass
		elif(command == 'mput'):
			if(len(sentence) > 1):
				if(anonymous == "0"):
					files = sentence[1:]
					for i in files:
						if(prompt == "0"):
							print("Do you want to send {}? y/n".format(i))
							ack = input()
						else:
							ack = "y"
						ccsocket.send(ack.encode())
						if(ack == "y"):
							time.sleep(1)
							li = file_info(i)
							ack = " ".join(li)
							if(li[0] == "yes"):
								val = int(li[1])
								start = timer()
								ccsocket.send(ack.encode())
								f = open(i,'rb')
								ans = f.read(1024)
								while(ans):
									datasocket.send(ans)
									if(hashflag == 1):
										print("#",end = "")
									ans = f.read(1024)
								f.close()
								if(hashflag == 1):
									print("")
								end = timer()
								print("File {} transferred successfully".format(i))
								speed(start, end, val)
							else:
								ccsocket.send(ack.encode())
								print("Error: {} does not exist".format(i))
						else:
							pass
				else:
					print("Anonymous user can not send files")
			else:
				print("Enter filename")
		elif(command == "quit" or command == 'exit' or command == 'bye' or command == "close"):
			print("Goodbye")
			datasocket.close()
			ccsocket.close()
			break
		elif(command == 'size'):
			if(len(sentence) > 1):
				ack = ccsocket.recv(3).decode()
				if(ack == "yes"):
					size = ccsocket.recv(1024).decode()
					size = int(size)
					if(size <= 1024):
						print("{}bytes".format(size))
					elif(size <= 1048576):
						size = size / 1024
						print("{}KB".format(round(size,2)))
					elif(size <= 1073741824):
						size = size / 1003188.92
						print("{}MB".format(round(size,2)))
					else:
						size = size / 981003114.11
						print("{}GB".format(round(size,2)))
				else:
					print("Error: File does not exist")
			else:
				print("Enter Filename")
		elif(command == 'delete' or command == 'mdelete'):
			if(len(sentence) > 1):
				if(anonymous == "0"):
					if(command == 'delete'):
				
						filename = sentence[1]
					else:
						files = sentence[1:]
					if(command == "delete"):
						ack = ccsocket.recv(3).decode()
						if(ack == "yes"):
							print("{} removed successfully".format(filename))
						else:
							print("{} does not appear to exist".format(filename))
					else:
						for i in files:
							if(prompt == "0"):
								print("Do you want to delete {}? y/n".format(i))
								ackprompt = input()
							else:
								ackprompt = "y"
							ccsocket.send(ackprompt.encode())
							if(ackprompt == "y"):
								ack = ccsocket.recv(3).decode()
								if(ack == "yes"):
									print("{} removed successfully".format(i))
								else:
									print("{} does not appear to exist".format(i))
							else:
								pass
				else:
					print("Permission denied")
			else:
				print("Enter Filename")
		elif(command == "modtime"):
			if(len(sentence) > 1):
				ans = ccsocket.recv(1024).decode()
				print(ans)			
			else:
				print("Enter Filename")
		elif(command == "rename"):
			if(len(sentence) > 2):
				if(anonymous == "0"):
					ack = ccsocket.recv(3).decode()
					if(ack == "yes"):
						print("File renamed successfully")
					else:
						print("Error: File does not appear to exist.")
				else:
					print("Permission denied")
			else:
				print("NO filename specified")
		elif(command == "mkdir"):
			if(len(sentence) > 1):
				if(anonymous == "0"):
					print("Directory created successfully")
				else:
					print("Permission denied")
			else:
				print("Enter Filename")
		elif(command == "rmdir"):
			if(len(sentence) > 1):
				if(anonymous == "0"):
					ack = ccsocket.recv(3).decode()
					if(ack == "yes"):
						length = ccsocket.recv(1).decode()
						if(length == '0'):
							print("Directory removed successfully!")
						else:
							ans = ccsocket.recv(55).decode()
							print(ans)
							reply = input()	
					
							if(reply == "y" or reply == "Y"):
								ack = "yes"
							else:
								ack = "no!"
							ccsocket.send(ack.encode())	
					else:
						print("Error: Directory does not exist.")		
				else:
					print("Permission denied")	
			else:
				print("Enter filename")
		elif(command == "mls" or command =="mdir"):
			if(len(sentence) > 1):
				files = sentence[1:]
				for i in files:
					ack = ccsocket.recv(3).decode()	
					ans = ccsocket.recv(10240).decode()
					if(ack == "yes"):
						li = list(ans.split(" "))
						print("Directory : {}".format(i))
						for j in li:						
							print(j)
					else:	
						print("Directory : {}".format(i))
						print(ans)
			else:
				print("Enter Filename")
		else:
			try:
				data = command[1:]
				print(os.system(data))
			except IOError:
				pass
			
def connection(ccsocket):
	global anonymous
	while(1):
		print("ftp>",end ='')
		command = input()
		if(command[0:4] == 'open'):
			username = input("Enter Username:")
			ccsocket.send(username.encode())
			if(username == "anonymous"):
				anonymous = "1"
			password = getpass("Enter Password:")
			ccsocket.send(password.encode())
			ack = ccsocket.recv(1024)
			if(ack.decode() == "0"):
				break
			else:
				print("Wrong username and password")
	
	dataport = int(ccsocket.recv(1024).decode())
	clientsocket = socket(AF_INET,SOCK_STREAM)
	clientsocket.bind(('',dataport))
	clientsocket.listen(10)
	datasocket, addr = clientsocket.accept()
	comm(ccsocket, datasocket)

if __name__== "__main__":
	li = list(sys.argv)
	servername = str(li[1])
	serverport = int(li[2])
	ccsocket = socket(AF_INET,SOCK_STREAM)
	ccsocket.connect((servername,serverport))
	connection(ccsocket)
