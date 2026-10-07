2. Scheduling Deep Dive — cron, anacron, at &
timers
cron — complete syntax mastery
# m h dom mon dow command
30 2 * * * /opt/scripts/backup.sh
*/10 * * * * /opt/scripts/healthcheck.sh
0 9-17 * * 1-5 /opt/scripts/business_hours.sh
0 3 1 * * /opt/scripts/monthly_report.sh
15 4 * * sun /opt/scripts/weekly.sh
@reboot /opt/scripts/on_boot.sh
@daily /opt/scripts/daily.sh