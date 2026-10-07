4. Test...
5. ...and mail.log tells you exactly what happened to every message (the deliverability debugger).





Deliverability minimum for a custom From-domain
Sending as anything@yourdomain.fi requires DNS records or Gmail/Outlook will junk it: SPF (TXT: which
servers may send for the domain), DKIM (your provider gives a signing record), DMARC (policy record). All
three are copy-paste values from your relay provider's dashboard — ten minutes that decide whether alerts
arrive or vanish.
PRACTICE EXERCISES