import os
import socket
import subprocess
import re
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class WifiScanner(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')
        scan_button = Button(text='Scan Wi-Fi Networks', on_press=self.scan_wifi_networks)
        self.result_label = Label(text='', halign='center')
        layout.add_widget(scan_button)
        layout.add_widget(self.result_label)
        return layout

    def scan_wifi_networks(self, instance):
        result = subprocess.check_output(['iwlist', 'wlan0', 'scan'])
        networks = re.findall(r'ESSID:"(.+?)"', result.decode('utf-8'))
        ip_addresses = []

        for network in networks:
            try:
                ip_address = socket.gethostbyname(network)
                ip_addresses.append(f'{network}: {ip_address}')
            except socket.gaierror:
                pass

        self.result_label.text = '\n'.join(ip_addresses)

if __name__ == '__main__':
    WifiScanner().run()
