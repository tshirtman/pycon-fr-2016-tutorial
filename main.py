from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.uix.gridlayout import GridLayout
from csv import reader, writer


KV = '''
#:import F kivy.factory.Factory
#:import C kivy.utils.get_color_from_hex
#:set color_bg '#e3f2fd'
#:set color_button '#64b5f6'
#:set color_text '#0d47a1'
#:set color_important '#bf360c'
#:set color_important_active '#ffab91'

<RoundButton@ButtonBehavior+Label>:
    canvas.before:
        Color:
            rgba: C(color_important) if self.state == 'normal' else C(color_important_active)

        PushMatrix
        Scale:
            origin: self.center
            x: 1.1 if self.state == 'down' else 1
            y: 1.1 if self.state == 'down' else 1

        Ellipse:
            pos: self.pos
            size: self.size
        PopMatrix

<AutoButton@Button,AutoLabel@Label,AutoTextInput@TextInput,AutoSpinner@Spinner>:
    size_hint_y: None
    height: '48dp'
    color: C(color_text)
    font_size: '20dp'

<AutoButton,AutoSpinner>:
    background_color: C(color_button)
    color: C(color_bg)

<AutoSpinner>:
    option_cls: F.AutoButton

<AutoLabel>:
    size_hint_x: None
    width: self.texture_size[0]
    halign: 'right'

<AutoTextInput>:
    background_normal: self.background_active

ScreenManager:
    canvas.before:
        Color:
            rgba: C(color_bg)
        Rectangle:
            pos: self.pos
            size: self.size

    Screen:
        name: 'todolist'
        FloatLayout:
            ScrollView:
                GridLayout:
                    id: todos
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height

            RoundButton:
                text: '+'
                size_hint: None, None
                font_size: '50dp'
                size: '50dp', '50dp'
                right: self.width and root.width - 20
                y: 20
                on_release:
                    app.current_task = app.new_task()
                    root.transition.direction = 'left'
                    root.current = 'edit task'

    Screen:
        name: 'edit task'
        BoxLayout:
            orientation: 'vertical'
            ScrollView:
                GridLayout:
                    size_hint_y: None
                    height: self.minimum_height
                    cols: 2

                    AutoLabel:
                        text: 'Title'

                    AutoTextInput:
                        id: title
                        text: app.current_task.title
                        multiline: False
                        on_text_validate:
                            date.focus = True

                    AutoLabel:
                        text: 'Importance'

                    AutoSpinner:
                        id: importance
                        text: app.current_task.importance
                        values: 'high', 'medium', 'low'
                        on_text:
                            date.focus = True

                    AutoLabel:
                        text: 'Due date'

                    AutoTextInput:
                        id: date
                        multiline: False
                        text: app.current_task.date

                    AutoLabel:
                        text: 'Comment'
                        pos_hint: {'top': 1}

                    AutoTextInput:
                        size_hint_y: None
                        height:
                            max(self.minimum_height, 48)
                        id: comment
                        text: app.current_task.comment
            BoxLayout:
                size_hint_y: None
                height: '48dp'

                AutoButton:
                    text: 'Cancel'
                    on_press:
                        root.transition.direction = 'right'
                        root.current = 'todolist'

                AutoButton:
                    text: 'Save'
                    on_press:
                        app.current_task.title = title.text
                        app.current_task.importance = importance.text
                        app.current_task.date = date.text
                        app.current_task.comment = comment.text
                        if app.current_task not in app.todos: app.todos.append(app.current_task)
                        root.transition.direction = 'right'
                        root.current = 'todolist'

<TaskWidget>:
    rows: 1
    size_hint_y: None
    height: self.minimum_height
    AutoButton:
        text: '%s: %s' % (root.task.date, root.task.title)
        size_hint_y: None
        height: '48dp'
        on_press:
            app.current_task = root.task
            app.root.transition.direction = 'left'
            app.root.current = 'edit task'

    AutoButton:
        text: '-'
        size_hint_y: None
        size_hint_x: None
        size: '48dp', '48dp'
        on_press:
            app.todos.remove(root.task)
'''


class Task(EventDispatcher):
    title = StringProperty()
    date = StringProperty()
    importance = StringProperty()
    comment = StringProperty()


class TaskWidget(GridLayout):
    task = ObjectProperty(rebind=True)


class Tutorial(App):
    current_task = ObjectProperty(Task(), rebind=True)
    todos = ListProperty()

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        try:
            with open('tasks.csv') as f:
                csv_file = reader(f)
                for row in csv_file:
                    self.todos.append(
                        Task(
                            title=row[0],
                            importance=row[1],
                            date=row[2],
                            comment=row[3]))
        except IOError:
            pass

    def on_stop(self):
        with open('tasks.csv', 'w') as f:
            csv_file = writer(f)
            for t in self.todos:
                csv_file.writerow((t.title, t.importance, t.date, t.comment))

    def new_task(self, *args):
        return Task()

    def on_todos(self, *args):
        todos = self.root.ids.todos
        todos.clear_widgets()
        for t in self.todos:
            task = TaskWidget(task=t)
            todos.add_widget(task)

if __name__ == '__main__':
    Tutorial().run()
