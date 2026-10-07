6. Reverse: name for an IP.

Record TTLs explain 'the DNS change hasn't worked yet': resolvers cache answers for the TTL. Before
migrations, drop TTL to 300 a day early; raise it back after.

Traffic inspection — tcpdump essentials
sudo tcpdump -i any -nn port 8000 -c 20
sudo tcpdump -i any -nn 'tcp[tcpflags] & tcp-syn != 0' -c 10
sudo tcpdump -i any -nn -w capture.pcap port 5432