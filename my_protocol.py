#################################################################
#  -----------------------------------------------------------  #
# | quit | source | destination | len of  message | message  |  #
# ------------------------------------------------------------  #
#################################################################


import socket

class MY_PROTOCOL:

    __packet = {'conn': None,
                'src':None,
                'dst':None,
                'len_of_msg':None,
                'message':None}


    def __format_IP(self,ip_as_str):
        IP = ip_as_str

        if(len(ip_as_str)<15):
            while(len(ip_as_str)<15):
                ip_as_str = ip_as_str + '*'

            IP = ip_as_str

        return IP
    

    def __format_len_of_message(self,message):
        leng = len(message)
        if(leng<10):
            return str(leng) + '*'

        return str(leng)


    def __prepare_packet(self,args):
        conn = args.pop('conn', False)
        if(conn):
            self.__packet['conn'] = conn
            self.__packet['src'] = conn.getsockname()[0]
            



        dst = args.pop('dst', False)
        if(dst):
            self.__packet['dst'] = self.__format_IP(dst)


        message = args.pop('message', False)
        if(message):
            self.__packet['message'] = message
            self.__packet['len_of_msg'] = self.__format_len_of_message(message)


    def send_message(self,**args):
        self.__prepare_packet(args)

        self.__packet['conn'].sendall(self.__packet['src'].encode('utf-8'))
        self.__packet['conn'].sendall(self.__packet['dst'].encode('utf-8'))
        self.__packet['conn'].sendall(self.__packet['len_of_msg'].encode('utf-8'))
        self.__packet['conn'].sendall(self.__packet['message'].encode('utf-8'))


    def receive_message(self, conn):
        src = conn.recv(15).decode('utf-8')
        dst = conn.recv(15).decode('utf-8')
        len_of_msg = conn.recv(2).decode('utf-8')
        message = conn.recv(int(len_of_msg)).decode('utf-8')

        return {'src': src, 'dst': dst, 'len_of_msg': len_of_msg, 'message':message}
