#! /usr/bin/env python
import getpass, paramiko, time

show_interface_counters_errors = 'sho int counters errors | exclude  0           0            0            0          0|0          0          0          0         0           0|0         0         0          0         0         0         0\n'
show_interface_transceiver = 'sho interfaces transceiver\n'
show_route_map = 'sho route-map ENCR\n'
show_ip_access_list = 'sho ip access-lists | sec Extended IP access list 10.\n'

device_list_odd = ['XAN-CA-01','XCY-CA-01','XEH-CA-01','XER-CA-01','XGL-CA-01','XGR-CA-01',
			 'XKS-CA-01','XLD-CA-01','XMS-CA-01','XOM-CA-01','XRM-CA-01','XSN-CA-01','XSY-CA-01']
device_list_even = ['XAN-CA-02','XCY-CA-02','XEH-CA-02','XER-CA-02','XGL-CA-02','XGR-CA-02',
			 'XKS-CA-02','XLD-CA-02','XMS-CA-02','XOM-CA-02','XRM-CA-02','XSN-CA-02','XSY-CA-02']
			 
USER = raw_input('Username: ')
PASS = getpass.getpass(prompt='Password: ')
def execute_command():
   try:
      print (host)
      client = paramiko.SSHClient()
      client.load_system_host_keys()
      client.set_missing_host_key_policy(paramiko.WarningPolicy())

      client.connect(host, 22, username=USER, password=PASS)
      channel = client.invoke_shell()
      
      channel.send('term len 0\n')
      channel.send(show_interface_counters_errors)
      time.sleep(2)
      out1 = channel.recv(65535)
      print (out1)
      channel.send(show_interface_transceiver)
      time.sleep(2)
      out2 = channel.recv(65535)
      print (out2)
      channel.send(show_route_map)
      time.sleep(2)
      out3 = channel.recv(65535)
      print (out3)
      channel.send(show_ip_access_list)
      time.sleep(2)
      out4 = channel.recv(65535)
      print (out4)
   finally:
      client.close()

   return(out1,out2,out3,out4)

with open('even.log', 'w') as file:
   for host in device_list_even:
      out1,out2,out3,out4 = execute_command()
      file.write(out1)
      file.write(out2)
      file.write(out3)
      file.write(out4)

with open('odd.log', 'w') as file:
   for host in device_list_odd:
      out1,out2,out3,out4 = execute_command()
      file.write(out1)
      file.write(out2)
      file.write(out3)
      file.write(out4)
