import gradio as gr
from .tab import SettingTab, InputTab
from .network import MySession

class MainBlock:
    block: gr.Blocks
    setting_tab: SettingTab
    input_tab: InputTab
    session: MySession

    def __init__(self):
        self.session = MySession()
        with gr.Blocks(title="Boost LLM", js="()=>{document.getElementsByTagName('footer')[0].remove();}") as self.block:
            gr.Markdown("# Boost LLM")
            self.setting_tab = SettingTab(self.session)
            self.input_tab = InputTab(self.session)