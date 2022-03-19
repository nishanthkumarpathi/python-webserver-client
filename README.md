# Project Details

Computer Networking MCIS 6163
Project 1 : Simple Web Server & Client

# Project Objectives

- To understand Client-Server communication via sockets
- To gain exposure to the basic operations of a Web Server and Client
- To explore basic structures of HTTP messages

# About Project 

We have written a simple commandline based multithreaded web server and client written in python. 

This repository Contains 4 Files

- README.md : This file is what you are reading. This file has all necessary Instructions to Execute this code.
- server.py : This is the Webserver File, Acting as the Server
- index.html : This is a Simple HTML file, which is served by server.py
- client.py: This is the Command line based Client Application to interact with Server

# Pre-requisites

To exectue this project, we need the following Softwares.

- Python2.7 : Python2.7 Programming Language is used to write the Code.
- VSCode IDE : VSCode Integrated Development Environment is used to develop the Code.
- Ubuntu 20.04 : Any Version of Ubuntu is fine, however at the time of development Ubuntu 20.04 is used.

# Instructions to Use the Files.

Step 1: Download the files from the Github Repository, by cloning the Git Repository

```bash
git clone <<repository-url>>
```

Step 2: Traverse into the Folder

```bash
```

Step 3: Make Python Files Executable

```bash
chmod +x *.py
```

Step 4: Execute the Server Python file via the Terminal

```bash
python2.7 server.py 8080
```

Step 5: Go to Browser and open http://localhost:8080


Step 6: You can also use python client file to interact with Web Server.
 
For example : python2.7 client.py webserver_host webserver_port requested_filename

```bash
python2.7 client.py localhost 8080 index.html
```


