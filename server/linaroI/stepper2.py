    from GPIOLibrary import GPIOProcessor
    import time
    import math

    GP = GPIOProcessor()
    import socket
    # import time

    MAGIC = "face600d"

    server_socket = socket.socket()
    server_host = '192.168.43.20'
    server_port = 5002
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)
    c,addr = server_socket.accept()


    try:
        # Stepper Motor Controls
        A1 = GP.getPin23()    # blue
        A2 = GP.getPin24()    # pink
        B1 = GP.getPin25()    # yellow
        B2 = GP.getPin26()    # orange

        A1.out()
        A2.out()
        B1.out()
        B2.out()

        # Delay time 
        T = 0.001

        # Stepper Sequence (Forward ; Reverse)
        SS = [[[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]],
             [[1,0,0,1],[0,0,1,1],[0,1,1,0],[1,1,0,0]]]

        # Step Angle
        SA = 0.18 #degrees per step
        y = 0

        while True:
           #0-forward
            FR = 0

            scanner_data = c.recv(1024)
            if scanner_data == "OPEN":
              y = 1
            
           
            y = input()     #gets input from server
       
            x = 75          #hard coded degrees 
       #     if x < 0:
       #         FR = 1
       #         x = abs(x)
       #     else:
       #         FR = 0
            
            if y == 1:
                x = int(x/SA)
            # Run Stepper Motor sequence
                for i in range(0,x):
                    A1.setValue(SS[FR][i%4][0])
                    time.sleep(T)
                    A2.setValue(SS[FR][i%4][1])
                    time.sleep(T)
                    B1.setValue(SS[FR][i%4][2])
                    time.sleep(T)
                    B2.setValue(SS[FR][i%4][3])
                    time.sleep(T)


                time.sleep(10)
                FR = 1 
                for j in range(0,x):
                    A1.setValue(SS[FR][j%4][0])
                    time.sleep(T)
                    A2.setValue(SS[FR][j%4][1])
                    time.sleep(T)
                    B1.setValue(SS[FR][j%4][2])
                    time.sleep(T)
                    B2.setValue(SS[FR][j%4][3])
                    time.sleep(T)
                y = 0
      #      print 'again? [y/n]'
      #      r = raw_input()
      #      if r == 'n':
      #          break

    finally:
        GP.cleanup()
        c.close()
        server_socket.close()
