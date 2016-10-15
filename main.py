from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.uix.gridlayout import GridLayout
from csv import reader, writer


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
