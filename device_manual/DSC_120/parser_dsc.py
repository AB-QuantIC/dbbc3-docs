import socket
import datetime
import _struct

MCAST_GRP = '224.0.0.255'
MCAST_PORT = 25000
IS_ALL_GROUPS = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if IS_ALL_GROUPS:
    # on this port, receives ALL multicast groups
    sock.bind(('', MCAST_PORT))
else:
    # on this port, listen ONLY to MCAST_GRP
    sock.bind((MCAST_GRP, MCAST_PORT))
mreq = _struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    # print(sock.recv(1024))
    valueArray = sock.recv(16384)
    offset = 0
    versionString = valueArray[offset:offset+32].decode("utf-8")
    print(datetime.datetime.utcnow())
    print(versionString)
    offset = offset + 32

    # Present/Active IFs
    presentIFs = valueArray[offset]
    activeIFs = valueArray[offset+1]
    offset = offset + 2
    print("Present IFs: {:08b}".format(presentIFs))
    print("Active  IFs: {:08b}".format(activeIFs))
    
    # GCoMo values
    for i in range(0, 8):
        shortArray = _struct.unpack('HHHH', valueArray[offset+i*8:offset+i*8+8])
        if shortArray[0] == 0:
            print(str(i+1) + " man" + str(shortArray))
        else:
            print(str(i+1) + " agc" + str(shortArray))
            
    offset = offset + (8 * 8)
           
    # Downconverter Values        
    for i in range(0, 8):
        shortArray = _struct.unpack('HHHH', valueArray[offset+i*8:offset+i*8+8])
        print(str(shortArray))
        
    offset = offset + (8 * 8)
        
    # ADB3L Values
    for i in range(0, 8):
        powerArray = _struct.unpack('IIII', valueArray[offset:offset+16])
        print(str(powerArray))
        offset = offset + 16

        offsetArray = _struct.unpack('IIII', valueArray[offset:offset+16])
        print(str(offsetArray))
        offset = offset + 16

        corrArray = _struct.unpack('IIII', valueArray[offset:offset+16])
        print(str(corrArray))
        offset = offset + 16

    # Core3H Values    
    for i in range(0, 8):
        secondValue = _struct.unpack('I', valueArray[offset:offset+4])
        epochValue = _struct.unpack('I', valueArray[offset+4:offset+8])
        ppsDelayValue = _struct.unpack('I', valueArray[offset+8:offset+12])
        print("Board["+str(i+1)+"], Epoch: " + str(epochValue[0]) + ", Second: " + str(secondValue[0]) + ", 1PPS Delay: " + str(ppsDelayValue))
        offset = offset + 12

        powerSampler1 = _struct.unpack('I', valueArray[offset:offset+4])
        powerSampler2 = _struct.unpack('I', valueArray[offset+4:offset+8])
        powerSampler3 = _struct.unpack('I', valueArray[offset+8:offset+12])
        powerSampler4 = _struct.unpack('I', valueArray[offset+12:offset+16])
        print("Sampler 0: " + str(powerSampler1))
        print("Sampler 1: " + str(powerSampler2))
        print("Sampler 2: " + str(powerSampler3))
        print("Sampler 3: " + str(powerSampler4))
        offset = offset + 16

        for j in range(0, 4):
            print("Sampler " + str(j) + " BStat: ")
            for k in range(0, 4):
                core3hbstat = _struct.unpack('I', valueArray[offset:offset+4])
                print(str(core3hbstat[0]) + ": " + str(core3hbstat[0] / 640000))
                offset = offset + 4

    #
    #     ppsDelayValue = _struct.unpack('I', valueArray[offset:offset+4])
    #     print("pps_delay["+str(i)+"] " +str(ppsDelayValue))
    #     offset = offset + 4
    #
    #     tpS0_0Value = _struct.unpack('I', valueArray[offset:offset+4])
    #     print("tpS0_0["+str(i)+"] " +str(tpS0_0Value))
    #     offset = offset + 4
    #
    #     tpS0_1Value = _struct.unpack('I', valueArray[offset:offset+4])
    #     print("tpS0_1["+str(i)+"] " +str(tpS0_1Value))
    #     offset = offset + 4
    #
    #     tsysValue = _struct.unpack('I', valueArray[offset:offset+4])
    #     print("Tsys["+str(i)+"] " + str(tsysValue))
    #     offset = offset + 4
    #
    #     sefdValue = _struct.unpack('I', valueArray[offset:offset+4])
    #     print("Sefd["+str(i)+"] " + str(sefdValue))
    #     offset = offset + 4
        
    # BBC Values
    # for i in range(0,128):
    #     bbcValue = _struct.unpack('IBBBBIIIIHHHHHHHH', valueArray[offset:offset+40])
    #     offset = offset + 40
    #     if (i < 16) or (63 < i < 80):
    #         print("[" + str(i+1) + "]" + str(bbcValue[0]//524288) + "," + str(bbcValue[1])+ "," + str(bbcValue[2])+ "," + str(bbcValue[3])+ "," + str(bbcValue[4])+ "," + str(bbcValue[5])+ "," + str(bbcValue[6])+ "," + str(bbcValue[7])+ "," + str(bbcValue[8])+ ",",end='')
    #         print(str(bbcValue[9])+ ","+ str(bbcValue[10])+ "," + str(bbcValue[11])+ "," + str(bbcValue[12])+ "," + str(bbcValue[13])+ "," +str(bbcValue[14])+ "," +str(bbcValue[15])+ "," +str(bbcValue[16]))
