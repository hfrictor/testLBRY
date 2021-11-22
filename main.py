import kivy
import requests
import pprint

from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import  Window
from kivy.clock import Clock
from kivy.uix.filechooser import FileChooser


LBRY_DAEMON_URL = "http://localhost:5279"

class BookNetApp(App):

    def check_lbry_status(self, dt):
        status_args_dict = {"method": "status", "params": {}}
        try:
            response = requests.post(LBRY_DAEMON_URL, json=status_args_dict)
        except requests.exceptions.RequestException:
            status_bool = False

        else:
            if response.status_code == 200:
                status_bool = True
            else:
                status_bool = False
        self.update_staus_label(status_bool)

    def update_staus_label(self, status_bool=False):
        lbry_status_str = "online" if status_bool else "down"
        status_line_str = f'[status {lbry_status_str}]'
        self.status_label.text = status_line_str

    def build(self):

        Clock.schedule_once(self.check_lbry_status, 1)

        layout = FloatLayout(size=Window.size)
        form_layout = BoxLayout(orientation='vertical')
        layout.add_widget(form_layout)

        booknet_label = Label(text=f'LBRY Booknet')
        form_layout.add_widget(booknet_label)



        #file_field_widget = FileChooser()
        #layout.add_widget(file_field_widget)

        file_field_btn = Button(text='Choose Files(s)', font_size=14)
        form_layout.add_widget(file_field_btn)

        title_field_input = TextInput(text="Title")
        form_layout.add_widget(title_field_input)

        FORMAT_VALUE_CHOICES = (
            'epub', 'mobi', 'pdf'
        )
        format_field_input = Spinner(text=FORMAT_VALUE_CHOICES[0], values=FORMAT_VALUE_CHOICES)
        form_layout.add_widget(format_field_input)


        author_field_input = TextInput(text="Author")
        form_layout.add_widget(author_field_input)

        GENRE_VALUE_CHOICES = (
            'Scifi', 'True Crime', 'Some really long genre that someone might put in.'
        )
        genre_field_input = Spinner(text=GENRE_VALUE_CHOICES[0], values=GENRE_VALUE_CHOICES)
        form_layout.add_widget(genre_field_input)

        othertags_field_input = TextInput(text="Other Tags")
        form_layout.add_widget(othertags_field_input)

        self.status_label = Label(text="", valign="bottom", halign="right", text_size=layout.size)
        layout.add_widget(self.status_label)

        self.update_staus_label()
        return layout
    #some minor change



if __name__ == '__main__':
    BookNetApp().run()