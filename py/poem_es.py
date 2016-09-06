import sys
import socket
import os
import subprocess as sp


class Server:

    def __init__(self,port, model = 0, beam_size = 10):
        self.host = socket.gethostname()
        self.port = port
        self.model = model
        self.root_dir = os.path.abspath(__file__ + "/../../")
        model_names = ["lyrics.tl.nn.es"]
        self.lm = False
        self.model_path = os.path.join(os.path.join(self.root_dir,'models/'), model_names[self.model])
        self.rnn = os.path.join(self.root_dir,"a.out")
        self.fsa_path = "fsa_path"
        self.source_path = "source_path"
        self.print_beam = 1

        self.cmd = [self.rnn]
        self.cmd += "--interactive 1".split()
        self.cmd += "--adjacent-repeat-penalty -2.0 --repeat-penalty -3.0".split()
        self.cmd += "-b {}".format(beam_size).split()
        self.cmd += "-L 160".split()
        
        if self.lm:
            self.cmd += "-k 1 {} kbest{}.txt".format(self.model_path, self.port).split()
        else:
            self.cmd += "-k 1 {} {} kbest{}.txt".format(self.source_path, self.model_path, self.port).split()
        
        self.cmd += "--fsa {}".format(self.fsa_path).split()
        self.cmd += "--print-beam {}".format(self.print_beam).split()
        self.cmd += "--dec-ratio 0.0 100.0".split()
        #self.cmd += "--encourage-list dummy --encourage-weight 1.0 --encourage-partially 1".split()
        
        self.cmd = " ".join(self.cmd)
            
    def start_server(self):
        print "loading the model"
        print self.cmd
        cmd = self.cmd.split()
        master,slave = os.openpty()
        backend = sp.Popen(cmd,bufsize=0,stdout=slave, stdin=sp.PIPE)
        poem_stdout = os.fdopen(master)
        while True:
            line = poem_stdout.readline()
            print line,
            if line.startswith("Please input"):
                break
        print "model is loaded"
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
        try:
            s.bind((self.host, self.port))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        print 'Socket bind complete'
 
        s.listen(0)
        print 'Socket now listening on {}:{}'.format(self.host, self.port)

        while True:
            conn, addr = s.accept()
            conn.sendall("Accept")
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            data = conn.recv(1024)
            print data   
            result = ""
            backend.stdin.write(data)
            while True:
                line = poem_stdout.readline()
                print line,
                if line.startswith('[END]'):
                    break
                result += line

            while True:
                line = poem_stdout.readline()
                print line,
                if line.startswith("Please input"):
                    break

            conn.sendall(result)
            conn.close()

        s.close()


def start_server_thread(port,model,bs):
    server = Server(port,model,bs)
    server.start_server()

from multiprocessing import Process

p1 = Process(target=start_server_thread, args=(10030,0,50))
#p2 = Process(target=start_server_thread, args=(10031,2,200))


p1.start()
#p2.start()




