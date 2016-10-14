from kivy.app import App
from kivy.lang import Builder


KV = '''
ScreenManager:
    Screen:
        name: 'hello'
        BoxLayout:
            orientation: 'vertical'
            TextInput:
                id: ti
                size_hint_y: None
                height: '48dp'

            Button:
                text: 'push me'
                on_press: root.current = 'world'

    Screen:
        name: 'world'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'hello %s' % ti.text
            Button:
                text: 'back'
                on_press: root.current = 'hello'

'''


class Tutorial(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Tutorial().run()
