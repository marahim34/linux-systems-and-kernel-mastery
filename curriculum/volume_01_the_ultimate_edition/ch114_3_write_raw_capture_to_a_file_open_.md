3. Write raw capture to a file — open it later in Wireshark on your laptop for full protocol dissection.

Bandwidth and quality
sudo apt install iperf3
iperf3 -s # on server
iperf3 -c server-ip # on client
mtr goodo.app