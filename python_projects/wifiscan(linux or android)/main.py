import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from plyer import wifi, bluetooth

kivy.require('2.0.0')

Builder.load_string("""
<WifiBluetoothItem>:
    orientation: 'vertical'
    Button:
        text: root.text
        on_press: root.on_item_press()

<RV>:
    viewclass: 'WifiBluetoothItem'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        spacing: dp(2)
        
<WifiBluetoothScanner>:
    orientation: 'vertical'
    RV:
        id: wifi_list
    RV:
        id: bluetooth_list
""")

class WifiBluetoothItem(ButtonBehavior, BoxLayout):
    text = StringProperty('')

    def on_item_press(self):
        print(f'Selected: {self.text}')

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

class WifiBluetoothScanner(BoxLayout):
    def __init__(self, **kwargs):
        super(WifiBluetoothScanner, self).__init__(**kwargs)
        self.wifi_list = self.ids['wifi_list']
        self.bluetooth_list = self.ids['bluetooth_list']
        self.scan_wifi()
        self.scan_bluetooth()

    def scan_wifi(self):
        wifi_scan_result = wifi.get_access_points()
        wifi_networks = [{'text': result['ssid']} for result in wifi_scan_result]
        self.wifi_list.data = wifi_networks

    def scan_bluetooth(self):
        paired_devices = bluetooth.get_bonded_devices()
        bluetooth_devices = [{'text': device['name']} for device in paired_devices]
        self.bluetooth_list.data = bluetooth_devices

class WifiBluetoothScannerApp(App):
    def build(self):
        return WifiBluetoothScanner()

if __name__ == '__main__':
    WifiBluetoothScannerApp().run()
