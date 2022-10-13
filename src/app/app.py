import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from pathlib import Path
import sys
from functools import partial

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # project home path
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


from src.utils.detect import runs


# templatepath = 'F:\\code\\printcheck\\tmp'
# testimgpath = 'F:\\code\\printcheck\\tmptest'
# pdfpath = 'F:\\code\\printcheck\\test.pdf'
    
# runs(pdfpath, templatepath, {})

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='select pdf'))
        self.pdfpath = TextInput(multiline=False)
        self.add_widget(self.pdfpath)
        self.add_widget(Label(text='select result save path'))
        self.resultpath = TextInput(multiline=False)
        self.add_widget(self.resultpath)
        self.button = Button(text='start')
        # on_press=partial(self.my_function, 'btn1')
        self.button.bind(on_press=partial(self.callback,self.pdfpath.text,self.resultpath.text))
        # self.button.bind(on_press=self.callback)
        self.add_widget(self.button)

    def callback(self, instance, pdfpath, resultpath):
        runs(self.pdfpath.text, self.resultpath.text, {})


class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
