import socket
from brute import brute 


host = "127.0.0.1"
port = 9999

# try and connect to a bind shell
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))

	try :
		print "[+] Connected to bind shell!\n"
                result = s.recv(2048).strip()
                print result
     		while 1:
      			cmd = raw_input("> ")

                        if cmd == 'brute':
                            for b in brute(length=7, letters=True, numbers=True, symbols=False):
                                s.send(b + "\n")
                                result = s.recv(2048).strip()
                            # print(result)
                                if 'Unrecognized satellite: ' in result:
                                    print "No"
                                    c = b
                                else:
                                    print "Something special!!!!!!!!!!!!!!!!!!"
                                    print "b: " + b
                                    print "c: " + c
                                    break

                            s.send('\n')
                            result = s.recv(2048).strip()
                            print result
                            continue
      			s.send(cmd + "\n");
      			result = s.recv(2048).strip();
      			if not len(result) :
	         		print "[+] Empty response. Dead shell / exited?"
            			s.close();
         			break;
        		print(result);

	except KeyboardInterrupt:
		print "\n[+] ^C Received, closing connection"
     		s.close();
	except EOFError:
		print "\n[+] ^D Received, closing connection"
     		s.close();

except socket.error:
	print "[+] Unable to connect to bind shell."

