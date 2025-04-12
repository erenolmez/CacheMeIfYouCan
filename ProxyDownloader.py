from socket import *
# Only socket module is used for the assignment. 
# sys module used for running the python code with port number. 
# os module ussed for to guarantee that downloaded files are at 
# the same directory with the python script
import sys
import os

def find_string_between_host_and_user_agent(input_string):
    start_index = input_string.find("Host:") + len("Host:")
    end_index = input_string.find("User-Agent:")
    if start_index == -1 or end_index == -1:
        return None
    else:
        return input_string[start_index:end_index].strip()

def get_remaining_string(input_string):
    last_slash_index = input_string.rfind("/")
    if last_slash_index == -1 or last_slash_index == len(input_string) - 1:
        return None
    else:
        return input_string[last_slash_index+1:]

#  Receiving port number as an input from teminal, i.e., making it the function variable
if len(sys.argv ) <= 1:
	sys.exit(2)

# Formation of server sockets for listening HTTP Proxy: localhost, Port: 12345 
server_socket = socket(AF_INET, SOCK_STREAM)
HTTP_Proxy = 'localhost'
Port_Number = int(sys.argv[1])
server_socket.bind((HTTP_Proxy, Port_Number))
server_socket.listen(100)
print('....ProxyDownloader started to run....')

while True:
	print('Retrieved request from Firefox:')
	client_socket, addr = server_socket.accept()
	print('Received a connection from:', addr)
	message = client_socket.recv(1024)
	print(message.decode())
	send_addr = message.split()[1].decode().partition("//")[2]

	# Since the length of URL addresses lines can change (hence, URL can hold 
	# multiple lines) I used functions that identify the necessary variables by looking
	# between inidcator titles intead of just using simple split functions and assigning a 
	# specific line to the supposed variable.

	# storing IP and Port number from GET repsonse in case of they become needed
	ip_addr = addr[0]
	port_no = int(addr [1])
	
	# extracting the host and filename
	host = find_string_between_host_and_user_agent(message.decode())
	filename = send_addr.replace(host, '')

	port = 80

	intermediary_socket = socket(AF_INET, SOCK_STREAM)
	intermediary_socket.connect((host, port))
	print("Successfully connected!\n")

	str = "GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" % (filename, host)
	print(str)

	intermediary_socket.sendall(str.encode('utf-8'))
	txt_name = get_remaining_string(filename)

	first_iteration = True
	# Filtering the Firefox Requests according to assignment
	if host == 'www.cs.bilkent.edu.tr':
		while True:
			# code needs to run differently at the first iterarion. 
			# Because of that if the file exists it can overwrite it 
			# instead of appending the file which is undesired. It also 
			# manages to receive the status code corectlly and only once
			# for each file.
			if first_iteration:
				print("Downloading file " + "‘" + txt_name + "’" + "...")
				buffer_storage = intermediary_socket.recv(4096)
				# finding status code
				status_code  = buffer_storage.split()[1].decode() + " " + buffer_storage.split()[2].decode()
				print("Retrieved: " + status_code)
				if status_code != "200 OK":
					print("Error at receiving data, response is negative")
					sys.exit(1)
				if not len(buffer_storage):
					break
				print("Saving file… ")
				start_index = buffer_storage.decode('utf-8').find('Content-Type:')
				end_index = buffer_storage.decode('utf-8').find('\n', start_index)
				next_line_start_index = buffer_storage.decode('utf-8').find('\n', end_index)
				next_line_end_index = buffer_storage.decode('utf-8').find('\n', next_line_start_index+1)

				text = buffer_storage.decode('utf-8')[next_line_end_index+1:]
				with open(os.path.join(sys.path[0], txt_name), "w") as file:
					file.write(text)
				first_iteration = False
			else:
				buffer_storage = intermediary_socket.recv(4096)
				if not len(buffer_storage):
					break
				with open(os.path.join(sys.path[0], txt_name), "a") as file:
					file.write(buffer_storage.decode('utf-8'))
			
		print("(Continue with next website)")
		intermediary_socket.close()

# never trigger because of while loop, normally these code block was used.  But since it was requried in 
# the manual that this code needs to be run all the time, it became commented.
client_socket.close() 
server_socket.close()