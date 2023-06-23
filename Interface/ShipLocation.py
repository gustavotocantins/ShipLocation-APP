import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.config import Config

#Utilizando o navegador
#import navegador.controlador as navegar

def tamanho_tela():
    from screeninfo import get_monitors
    monitors = get_monitors()
    screen_width = monitors[0].width
    screen_height = monitors[0].height
    return screen_width, screen_height

class Tela1(Screen):
    def entrar_tela1(self):
        self.manager.current = 'tela2'

class Tela2(Screen):
    def on_enter(self):
        #Alterar tamanho da janela
        screen_width, screen_height = tamanho_tela()
        Window.size = (screen_width*0.3, screen_height*0.96)

        #Fixar no canto
        Window.left = screen_width-screen_width*0.3
        Window.top = 0

    def entrar_tela2(self):
        self.manager.current = 'tela1'

class Tela3(Screen):
    pass

class GerenciarTela(ScreenManager):
    pass

class MeuApp(App):
    def build(self):
        #Tamanho da janela
        Window.size = (1100,600)
        Config.set('kivy', 'icon', 'logo1.png')
        gerenciador = GerenciarTela(transition=FadeTransition())
        gerenciador.add_widget(Tela1(name='tela1'))
        gerenciador.add_widget(Tela2(name='tela2'))
        gerenciador.add_widget(Tela3(name='tela3'))
        return gerenciador


if __name__ == '__main__':
    MeuApp().run()