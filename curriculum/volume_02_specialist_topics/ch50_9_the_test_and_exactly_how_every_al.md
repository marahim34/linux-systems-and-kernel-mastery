9. The test — and exactly how every alert in both volumes reaches your phone.

If you ever must run Postfix (send-only)
sudo apt install postfix # choose "Internet Site"
sudo postconf -e "inet_interfaces = loopback-only"
sudo postconf -e "relayhost = [smtp.eu.mailgun.org]:587"
echo test | mail -s "postfix test" you@mail.com
sudo tail -f /var/log/mail.log