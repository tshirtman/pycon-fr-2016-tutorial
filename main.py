from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class Tutorial(App):
    def build(self):
        return Button(text='push me', on_press=self.hello)

    def hello(self, *args):
        p = Popup(title='hello pycon', size_hint=(.5, .5))
        p.add_widget(Button(text='close', on_press=p.dismiss))
        p.open()


if __name__ == '__main__':
    Tutorial().run()
