DESCRIPTION:
This "ftp server" is a mini project developed in python for NAWP course for academic year 2019-2020.
It is designed to transfer the file among the same network hosts.
ftp_server.py contains the implementaion code for server and ftp_client.py contains the implementation code for client(s).

INSTALLATION:
$sudo apt update
$sudo apt install python3-pip
$pip install --upgrade pip
$pip3 install pam


WORKING:
Intially the server must be switched on hence the ftp_server.py must be excuted as- $python3 ftp_server.py (portno)
once the server is set client side code must be executed by- $python3 ftp_client.py (IP address or localhost) (portno)
example:
$python3 ftp_server.py 1608
$python3 ftp_client.py 127.0.0.1 1608
When the ftp prompts opens at client , client must open a connection with command open and must enter its username and password for authentication.Futher client(s) may proceed with ftp operations.
Multiple clients can establish connections with server.

COMMANDS:
FTP consist of various commands to carry out various operations with files over network like to get the file from server to the client. 
List of commands includes:
open -> open ; opens a new connection betwwn client and server , authenticates the client on its username and password.
ls /dir -> ls or dir ; enlists the content of current workingg directory.
cd -> cd (directory name) ; changes to the path to specified directory.
pwd -> pwd ;displays the path of cureent working directory.
hash -> hash ; displays the hashes while downloading or uploading.
history -> history ; enlist all the entered commands till and it can also be accessed at upper arrow key.
system -> system ; displays the system specifications.
prompt -> prompt ;sets the interactive sessions on or off.
cdup -> cdup ; changes directory to its parent directory.
lcd -> lcd (directory name) ; chnages the directory to specified directory at client side.
nlist -> nlist (directory name) ; outputs the content of specified directory
reget -> reget (filename) ;It checks whether the complete file is downloaded , in case a file is partially downloaded it downloades the further part of file.
get / recv -> get (filename) or get (filename) (another filename) or recv (filename) ; downloads single file from server to client. It may also change the name of file to another filename while saving it at client side.
mget -> mget (filename(s)) ; downloads multiple files from server to client.
put / send -> put (filename) or send (filename) ; uploads single file to server from client.
mput -> mput (filename(s)) ; uploads multiple files to server from client.
size -> size (filename) ; displays the size of file in KB ,MB and GB.
delete / mdelete -> delete (filename) or mdelete (filename(s)).
modtime -> modtime (filename); displays the last modified time of a file.
rename -> rename (this filename) (that filename) ; renames the first filename or directory name as the another file or directory name. 
mkdir -> mkdir (directory name) ; creates a directory of name specified.
rmdir -> rmdir (directory name) ;removes the specified directory and it also handles deletion of parent directory.
mls / mdir -> mls (directory name(s)) ; enlists the the content of multiple directories.
quit/ exit/ bye/ close -> quit or exit or bye or close ; It says goodbye and closes the connection with server.

Anonymous ftp where user can login as anonymous can only download files these users can not send files, delete files, rename files or can not make directory at server side. The user who login as anonymous need to enter their email id in password. Server maintain records of user who logged in as anonymous. Anonymous ftp implemented in this project.
Ctrl+c interrupt in handled. 



 

 



 
