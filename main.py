from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.uix.gridlayout import GridLayout
from csv import reader, writer


KV = '''
ScreenManager:
    Screen:
        name: 'todolist'
        FloatLayout:
            ScrollView:
                GridLayout:
                    id: todos
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height

            Button:
                text: '+'
                size_hint: None, None
                right: self.width and root.width - 20
                y: 20
                on_press:
                    app.current_task = app.new_task()
                    root.current = 'edit task'


    Screen:
        name: 'edit task'
        GridLayout:
            cols: 2

            Label:
                text: 'title'
            TextInput:
                id: title
                text: app.current_task.title
                multiline: False
                on_text_validate:
                    date.focus = True

            Label:
                text: 'importance'
            Spinner:
                id: importance
                text: app.current_task.importance
                values: 'high', 'medium', 'low'
                on_text:
                    date.focus = True

            Label:
                text: 'due date'
            TextInput:
                id: date
                multiline: False
                text: app.current_task.date

            Button:
                text: 'cancel'
                on_press:
                    root.current = 'todolist'

            Button:
                text: 'save'
                on_press:
                    app.current_task.title = title.text
                    app.current_task.importance = importance.text
                    app.current_task.date = date.text
                    if app.current_task not in app.todos: app.todos.append(app.current_task)
                    root.current = 'todolist'

<TaskWidget>:
    rows: 1
    size_hint_y: None
    height: self.minimum_height
    Button:
        text: '%s: %s' % (root.task.date, root.task.title)
        size_hint_y: None
        height: '48dp'
        on_press:
            app.current_task = root.task
            app.root.current = 'edit task'

    Button:
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


class TaskWidget(GridLayout):
    task = ObjectProperty(rebind=True)


class Tutorial(App):
    current_task = ObjectProperty(Task(), rebind=True)
    todos = ListProperty()

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        with open('tasks.csv') as f:
            csv_file = reader(f)
            for row in csv_file:
                self.todos.append(
                    Task(
                        title=row[0],
                        importance=row[1],
                        date=row[2]))

    def on_stop(self):
        with open('tasks.csv', 'w') as f:
            csv_file = writer(f)
            for t in self.todos:
                csv_file.writerow((t.title, t.importance, t.date))

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
