from kivy.app import App
from kivy.uix.label import Label


class Tutorial(App):
    def build(self):
        return Label(text='hello pycon!')


if __name__ == '__main__':
    Tutorial().run()
