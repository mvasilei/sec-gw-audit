#! /usr/bin/env python
import getpass, paramiko, time, re

show_interface_counters_errors = 'sho int counters errors | exclude  0           0            0            0          0|0          0          0          0         0           0|0         0         0          0         0         0         0\n'
show_interface_transceiver = 'sho interfaces transceiver\n'
show_route_map = 'sho route-map ENCR\n'
show_ip_access_list = 'sho ip access-lists | sec Extended IP access list 1[01].\n'
show_ip_route = 'show ip route\n'
show_module = 'show module\n'

device_list_odd = ['XAN-CA-01','XCY-CA-01','XEH-CA-01','XER-CA-01','XGL-CA-01','XGR-CA-01',
			 'XKS-CA-01','XLD-CA-01','XMS-CA-01','XOM-CA-01','XRM-CA-01','XSN-CA-01','XSY-CA-01']
device_list_even = ['XAN-CA-02','XCY-CA-02','XEH-CA-02','XER-CA-02','XGL-CA-02','XGR-CA-02',
			 'XKS-CA-02','XLD-CA-02','XMS-CA-02','XOM-CA-02','XRM-CA-02','XSN-CA-02','XSY-CA-02']

def connection_establishment():
   try:
      print 'Processing HOST: ', host
      client = paramiko.SSHClient()
      client.load_system_host_keys()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(host, 22, username=USER, password=PASS)
      channel = client.invoke_shell()
      out = channel.recv(1)
      channel.send('term len 0\n')
   except paramiko.AuthenticationException as error:
      print 'Authentication Error'
      exit()
   return (channel,client)

def connection_teardown(client):
   client.close()

def sami_count(out):
   modules = []
   for line in out.splitlines():
       line = line.rstrip()
       pattern = re.compile(r'^ *(?P<module>\d+)')
       m = pattern.match(line)
   
       if m:
          modules.append(m.group(0).strip())

   return(modules)

def execute_command(command, channel,wait):
   channel.send(command)
   time.sleep(wait)
   out = channel.recv(65535)
   file.write(out)
   return (out)

USER = raw_input('Username: ')
PASS = getpass.getpass(prompt='Password: ')

with open(time.strftime("%Y%m%d-%H%M%S")+'-even.log', 'w') as file:
   for host in device_list_even:
      channel,client = connection_establishment()
      out = execute_command('show module services\n',channel,0.2)
      modules = sami_count(out)
      execute_command(show_interface_counters_errors, channel,0.2)
      execute_command(show_interface_transceiver, channel,0.2)
      execute_command(show_route_map, channel,0.2)
      execute_command(show_ip_access_list, channel,0.2)
      execute_command(show_ip_route, channel,0.2)
      execute_command(show_module,channel,0.2)

      for m in modules:
         execute_command('session slot ' + m +' process 3\n',channel,5)
         execute_command('show crypto throughput\n',channel,0.2)
         execute_command('exit\n',channel,0.2)

      connection_teardown(client)

with open(time.strftime("%Y%m%d-%H%M%S")+'-odd.log', 'w') as file:
   for host in device_list_odd:
      channel,client = connection_establishment()
      out = execute_command('show module services\n',channel,0.2)
      modules = sami_count(out)
      execute_command(show_interface_counters_errors, channel,0.2)
      execute_command(show_interface_transceiver, channel,0.2)
      execute_command(show_route_map, channel,0.2)
      execute_command(show_ip_access_list, channel,0.2)
      execute_command(show_ip_route, channel,0.2)
      execute_command(show_module,channel,0.2)

      for m in modules:
         execute_command('session slot ' + m +' process 3\n',channel,5)
         execute_command('show crypto throughput\n',channel,0.2)
         execute_command('exit\n',channel,0.2)

      connection_teardown(client)
