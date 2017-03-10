from ansible.cli.adhoc import AdHocCLI as mycli
import sys
cli = mycli(['ansible', '10.46.4.33', '-m', 'ping'])
cli.parse()
exit_code = cli.run()

