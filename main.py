from kivy.app import App
from kivy.lang import Builder


KV = '''
ScreenManager:
    Screen:
        name: 'hello'
        Button:
            text: 'push me'
            on_press: root.current = 'world'

    Screen:
        name: 'world'
        Label:
            text: 'world'
'''


class Tutorial(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Tutorial().run()
