import json
import re
import urllib.request
import subprocess


class RouteParser:
    def __init__(self):
        self.as_regex = re.compile(r'\bAS\d+')
        self.ip_regex = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        self.addresses = []

    def parse(self, route):
        for line in route.split('\n')[2:]:
            ip = re.search(self.ip_regex, line)
            if ip is not None:
                self.addresses.append(ip.group(0))
        if len(self.addresses) == 0:
            raise Exception("проверьте корректность введенного ip и подключение к интернету")
        print("№" + " "*4 + "IP" + " "*20 + "AS" + " "*20 + "Country" + " "*20 + "Provider")
        number = 0
        for address in self.addresses:
            number += 1
            self.find_as(address, number)

    def find_as(self, address, number):
        response = urllib.request.urlopen(f'https://ipinfo.io/{address}/json')
        data = json.loads(response.read())
        a_s = ''
        country = ''
        provider = ''
        if 'country' in data:
            country = data['country']
        if 'org' in data:
            match_as = re.search(self.as_regex, data['org'])
            a_s = match_as.group(0)[2:] if match_as is not None else ''
            provider = data['org'].replace(a_s, '') if match_as is not None else data['org']
        self.print_result(address, number, a_s, country, provider)

    def print_result(self, address, number, a_s, country, provider):
        number_tab = 5 - len(str(number))
        ip_tab = 22 - len(str(address))
        as_tab = 22 - len(str(a_s))
        country_tab = 27 - len(str(country))
        print(str(number) + " "*number_tab + str(address) + " "*ip_tab +
              a_s + " "*as_tab + country + " "*country_tab + provider)


def main():
    answer = input("Для того чтобы запустить скрипт введите: ip" + "\n")
    max_count_hobs = 40
    parser = RouteParser()
    traceroute = subprocess.Popen(['tracert', '-d', '-h', str(max_count_hobs), answer], stdout=subprocess.PIPE)
    route = traceroute.communicate()[0].decode('866')
    parser.parse(route)


if __name__ == '__main__':
    main()
