import time
from jsonfile import *
from query import find_all_ips_for_domain


results = dict()

multiple_dns = read_json()

for dns in multiple_dns.values():
    ipv4_ips = find_all_ips_for_domain(dns)
    results[dns] = ipv4_ips
    time.sleep(0.5)

write_json(results)

input("Press any key to quit....")