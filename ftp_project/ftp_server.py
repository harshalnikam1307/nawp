#!/usr/bin/python3
import platform
import sys
import os
import time
from socket import *
from _thread import *
import threading
import pam
import shutil
anonymous_client_list = []

def file_size(filename):
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
		li.append(size)
		if(ack == "yes"):
			connectionsocket.send(ack.encode())
		return li
	except IOError:
		ack = "No!"
		connectionsocket.send(ack.encode())
		li.append(ack)
		return li
def command(connectionsocket, sdsocket):
	while(1):
		datainput = connectionsocket.recv(1024).decode()
		sentence = list(datainput.split(" "))
		anonymous = sentence.pop()
		data = " ".join(sentence)
		if(len(sentence) > 0):
			command = sentence[0]
		else:
			break
		if(command == "pwd"):
			ans = os.getcwd()
			connectionsocket.send(ans.encode())

		elif(command == 'cd'):
			try:
				os.chdir(data[3:])
				ack = "yes"
				connectionsocket.send(ack.encode())
			except IOError:
				ack = "Error: File does not appear to exist."
				connectionsocket.send(ack.encode())
		elif(command == "system"):
			ack = []
			ack.append(os.name)
			ack.append(platform.system())
			ack.append(platform.release())
			ack = " ".join(ack)
			connectionsocket.send(ack.encode())
		elif(command == "cdup"):
			try:			
				data = ".."		
				os.chdir(data)
				ack = "yes"
				connectionsocket.send(ack.encode())
			except:
				ack = "no!"
				connectionsocket.send(ack.encode())
		elif(command == "nlist"):
			if(len(sentence) > 1):
				try:
					dirname = sentence[1]
					ans = os.listdir(dirname)
					if(len(ans) != 0):
						ans = " ".join(ans)	
						connectionsocket.send(ans.encode())
				except IOError:
					ans = "no!"
					connectionsocket.send(ans.encode())
	
		elif(command == 'ls' or command =='dir'):
			data = data + "> store.txt"
			os.system(data)
			info = os.stat("store.txt")
			size = str(info.st_size)
			if(size != '0'):
				ack = "yes"
				connectionsocket.send(ack.encode())
				time.sleep(0.10)
				connectionsocket.send(size.encode())
				f = open("store.txt","r+")
				size = int(size)
				ans = f.read(size - 1)
				sdsocket.send(ans.encode())
				f.close()
			else:
				ack = "Error: File does not appear to exist."
				connectionsocket.send(ack.encode())

		elif(command == "reget"):
			if(len(sentence) > 1):
				li = file_size(sentence[1])
				ack = li[0]
				print("ack:",ack)
			
				reply = connectionsocket.recv(3).decode()
				if(ack == "yes" and reply == "yes"):
					connectionsocket.send(li[1].encode())
					localsize = connectionsocket.recv(100).decode()
					remotesize = int(li[1])
					localsize = int(localsize)
				
					if(localsize < remotesize):
						count = ((remotesize - localsize)// 1024) + 1
						f = open(sentence[1],'rb')
						skip = f.read(localsize)
						ans = f.read(1024)
						while(count != 0):
							sdsocket.send(ans)
							ans = f.read(1024)
							count -= 1
						f.close()
						print("end")
					else:
						pass
				else:
					pass
			else:
				pass
		elif(command =='get' or command == "recv"):
			if(len(sentence) > 1):
				filename = []
				filename = sentence[1:]
				if(len(filename)== 1):
					filename.append(filename[0])
				li = file_size(filename[0])
				if(li[0] == "yes"):
					size = li[1]
					f = open(filename[0],'rb')
					filename.append(size)
					ack = " ".join(filename)
					connectionsocket.send(ack.encode())
					ans = f.read(1024)		
					while(ans):
						sdsocket.send(ans)
						ans = f.read(1024)
					f.close()
				else:
					pass
			else:
				pass
		elif(command == 'mget'):
			if(len(sentence) > 1):
				files = sentence[1:]
				for i in files:
					li = file_size(i)
					if(li[0] == "yes"):
						ackprompt = connectionsocket.recv(1).decode()
						if(ackprompt == "y"):
							size = li[1]
							connectionsocket.send(size.encode())
							time.sleep(0.10)
							f = open(i,'rb')
							ans = f.read(1024)
							while(ans):
								sdsocket.send(ans)
								ans = f.read(1024)
							f.close()
						else:
							pass
					else:
						pass
			else:
				pass	
		elif(command == 'put' or command == 'send'):
			if(len(sentence) > 1):
				filename = sentence[2]
				ack = sentence[3]
				print("ack {}".format(ack))
				if(anonymous == "0"):
					if(ack == "yes"):
						size = sentence[4]
						val = int(size)
						count = val//1024	
						count = count + 1
		
						with open(filename,'ab') as fd:
							while(count != 0):
								ans = sdsocket.recv(1024)
								fd.write(ans)
								count = count - 1
							fd.close()
					else:
						pass
				else:
					pass	
			else:
				pass
		elif(command == 'mput' and anonymous == "0"):
			if(len(sentence)> 1):
				files = sentence[1:]
				for i in files:
					ackprompt = connectionsocket.recv(1).decode()
					if(ackprompt == "y"):
						acknowledge = connectionsocket.recv(1024).decode()
						li = list(acknowledge.split())
						ack = li[0]
						print("ack {}".format(ack))
						if(ack == "yes"):
							size = li[1]
							val = int(size)
							count = val//1024
							count = count + 1
							with open(i,'ab') as fd:
								while(count != 0):
									ans = sdsocket.recv(1024)
									fd.write(ans)
									count = count - 1
								fd.close()
						else:
							pass
					else:
						pass
			else:
				pass
		
		elif(command == "modtime"):
			try:
				filename = sentence[1]
				info = os.stat(filename)
				if(info != None):
					ans = str(time.ctime(info.st_mtime))
					connectionsocket.send(ans.encode())
			except IOError:
				ans = "No such file exist!"
				coneectionsocket.send(ans.encode())
		elif(command =='chmod'):
			li = list(data.split())
			mode = int(li[1])
			os.chmod(li[2],mode)
		elif(command == 'size'):
			if(len(sentence) > 1):
				filename = sentence[1]
				li = file_size(filename)
				if(li[0] == "yes"):
					size = li[1]
					connectionsocket.send(size.encode())	
			else:
				pass
		elif(command == 'rename' and anonymous == "0"):
			if(len(sentence) > 2):
				try:
					li = list(data.split())
					oldfile = li[1]
					newfile = li[2]
					os.rename(oldfile, newfile)
					ack = "yes"
				except IOError:
					ack = "no!"
				connectionsocket.send(ack.encode())
			else:
				pass
		elif(command == 'delete' or command == 'mdelete'):
			if(len(sentence) > 1):
				if(anonymous == "0"):
					if(command == 'delete'):
						filename = sentence[1]
					else:
						files = sentence[1:]
					if(command == "delete"):
						try:
							filename = str(filename)
							os.remove(filename)
							ack = "yes"
						except IOError:
							ack = "no!"
						connectionsocket.send(ack.encode())
					else:
						for i in files:
							ackprompt = connectionsocket.recv(1).decode()
							if(ackprompt == "y"):
								try:
									os.remove(i)
									ack = "yes"
								except IOError:		
									print(IOError)
									ack = "no!"
								connectionsocket.send(ack.encode())
								print("ack:",ack)
							else:
								pass
				else:
					pass
			else:
				pass
		elif(command == "mkdir" and anonymous == "0"):
			if(len(sentence) > 1):
				dirname = sentence[1]
				os.mkdir(dirname)
		elif(command == "rmdir" and anonymous == "0"):
			if(len(sentence) > 1):
				dirname = sentence[1]
				boo = os.path.isdir(dirname)
				if(boo == True):
					ack = "yes"
				else:
					ack = "no!"
				connectionsocket.send(ack.encode())
				if(ack == "yes"):
				
					li = os.listdir(dirname)
					length = str(len(li))
					connectionsocket.send(length.encode())
					if(length == '0'):
						os.rmdir(dirname)
					else:
						sentence = "Directory is not empty..! Do you still want delete? y/n"
						connectionsocket.send(sentence.encode())
						ack = connectionsocket.recv(3).decode()
						if(ack == "yes"):
							shutil.rmtree(dirname)
						else:
							pass				
				else:
					pass
			else:
				pass
		elif(command == "mls" or command =="mdir"):
			if(len(sentence) > 1):
				files = sentence[1:]
				for i in files:
					boo = os.path.isdir(i)
					if(boo == True):
						ack = "yes"
					else:
						ack = "no!"
					connectionsocket.send(ack.encode())
					if(ack == "yes"):
						li = os.listdir(i)
						ans = " ".join(li)
					else:
						ans = "Error:Entered directory is not present!"
					connectionsocket.send(ans.encode())
			else:
				pass
		
def threading(connectionsocket,addr):
	global anonymous_client_list
	
	while True:
		try:
			username = connectionsocket.recv(1024).decode()
			print(username)
			password = connectionsocket.recv(1024).decode()
			print(password)
			if(username == "anonymous"):
				anonymous_client_list.append(password)
				res = True
			else:	
				res = p.authenticate(username,password)
			if(res == True):
				ack = "0"
				connectionsocket.send(ack.encode())
				break
			else:
				ack = "1"
				connectionsocket.send(ack.encode())	
		except:
			continue
	
	if(ack == '0'):
		print("connection established with {}".format(username))
	print(addr)
	clientip = str(addr[0])
	dataport = int(addr[1]+5)
	portno = str(dataport)
	connectionsocket.send(portno.encode())
	time.sleep(1)
	sdsocket = socket(AF_INET, SOCK_STREAM)
	sdsocket.connect((clientip,dataport))
	command(connectionsocket, sdsocket)

if __name__== "__main__":
	li = list(sys.argv)
	p=pam.pam()
	serverport = int(li[1])
	serversocket = socket(AF_INET,SOCK_STREAM)
	serversocket.bind(('',serverport))
	serversocket.listen(10)
	print("The Server is ready to receive")
	while True:
		connectionsocket, addr = serversocket.accept()
		
		start_new_thread(threading,(connectionsocket,addr,))
	connectionsocket.close()
	serversocket.close()


