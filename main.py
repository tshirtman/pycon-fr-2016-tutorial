from kivy.app import App
from kivy.uix.button import Button


class Tutorial(App):
    def build(self):
        b = Button(text='push me')
        b.bind(on_press=self.hello)

        return b

    def hello(self, *args):
        print "hello pycon"


if __name__ == '__main__':
    Tutorial().run()
