import telnetlib

tnports = {
    '192.168.13.1' : 5001,
    '192.168.13.2' : 5002,
    '192.168.13.3' : 5004,
    '192.168.13.4' : 5005,
}
for host,port in tnports.items():
    tn = telnetlib.Telnet("localhost",port)
    print(tn.read_very_eager().decode('ascii'))
    tn.write(b"\r")
    print(tn.read_very_eager().decode('ascii'))
    tn.write(b"terminal length 0\r")
    tn.read_very_eager()
    tn.write(b"conf t\r")
    tn.read_very_eager()
    tn.write(b"username cisco privilege 15 password cisco\r")
    tn.read_very_eager()
    tn.write(b"ip domain-name oefen.lab\r")
    tn.read_very_eager()
    tn.write(b"crypto key generate rsa mod 2048\r")
    tn.read_very_eager()
    tn.write(b"line vty 0 4\r")
    tn.read_very_eager()
    tn.write(b"login local\r")
    tn.read_very_eager()
    tn.write(b"transport input ssh telnet\r")
    tn.read_very_eager()
    tn.write(b"exit\r")
    tn.read_very_eager()
    tn.write(b"ip scp server enable\r")
    tn.read_very_eager()
    tn.write(b"archive\r")
    tn.read_very_eager()
    tn.write(b"path disk0:archive\r")
    tn.read_very_eager()
    tn.write(b"ip ssh pubkey-chain\r")
    tn.write(b"username cisco\r")
    tn.write(b"key-hash ssh-rsa 759C9A5D0620C1DD42AADBFCB28F512D dlansink@L-IT-LAPTOP01\r")
    tn.read_very_eager()
    tn.write(b"int fa0/0\r")
    tn.read_very_eager()
    tn.write(str.encode(f"ip address {host} 255.255.255.0\r"))
    tn.read_very_eager()
    tn.write(b"no shut\r")
    tn.read_very_eager()
    tn.write(b"end\r")