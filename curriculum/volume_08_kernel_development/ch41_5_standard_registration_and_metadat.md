5. Standard registration and metadata.

Building and testing it





make
sudo insmod notepad.ko
echo "Assalamu alaikum" | sudo tee /dev/notepad
sudo cat /dev/notepad
sudo rmmod notepad