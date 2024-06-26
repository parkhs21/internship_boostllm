from ..network import MySession
from ..service import InputService
import gradio as gr
from pathlib import Path

class InputTab:
    service: InputService
    tab: gr.Tab
    model_dd: gr.Dropdown
    rag_dd: gr.Dropdown
    ft_dd: gr.Dropdown
    sample_check: gr.Checkbox
    temperature_slider: gr.Slider
    topp_slider: gr.Slider
    token_slider: gr.Slider
    input_box: gr.Textbox
    output_box: gr.Textbox
    output_raw: gr.JSON
    clear_btn: gr.Button
    submit_btn: gr.Button
    hidden_btn: gr.Button
    input_example: gr.Examples
    
    def __init__(self, session: MySession):
        self.service = InputService(session)
        with gr.Tab("챗봇") as self.tab:
            with gr.Blocks() as block:
                gr.Markdown("- RAG 및 FineTuning 옵션은 추후 업데이트 예정입니다.")
                gr.Markdown("- Max New Token 옵션은 토큰 수가 많아질 수록 많은 양을 생성합니다. 다만, 그에 따라 응답 시간이 증가합니다.")
                gr.Markdown("- do Sample 체크 시, Temperature(높을수록 다채롭지만 부정확한 답변 출력), Top_p(높을수록 일반적인 단어 사용) 옵션이 반영됩니다.")
                
                with gr.Row():
                    with gr.Column():
                        with gr.Row():
                            self.model_dd = gr.Dropdown(label="Model", interactive=True)
                            self.rag_dd = gr.Dropdown(label="RAG", interactive=True)
                            self.ft_dd = gr.Dropdown(label="FineTuning", interactive=True)
                        
                        self.input_box = gr.Text(label="Input", show_copy_button=True, lines=8)
                        
                        with gr.Row():
                            self.clear_btn = gr.Button("Clear")
                            self.submit_btn = gr.Button("Submit", variant="primary")
                            
                    with gr.Column():
                        with gr.Row():
                            self.sample_check = gr.Checkbox(label="설정 변경", interactive=True, elem_id='sample_check')
                            self.temperature_slider = gr.Slider(
                                minimum=0,
                                maximum=1,
                                value=1,
                                step=0.05,
                                label="Temperature",
                                interactive=False,
                                scale=3
                                )
                            self.topp_slider = gr.Slider(
                                minimum=0,
                                maximum=1,
                                value=1,
                                step=0.05,
                                label="Top p",
                                interactive=False,
                                scale=2
                                )
                            self.token_slider = gr.Slider(
                                minimum=96,
                                maximum=4096,
                                value=512,
                                step=16,
                                label="Max New Token",
                                interactive=True,
                                scale=3
                                )
                            
                        self.output_box = gr.Text(label="Ouptut", show_copy_button=True, lines=8, interactive=False, elem_id="output_box")

                        # with gr.Accordion("Output_Raw", open=False):
                        #     self.output_raw = gr.JSON(show_label=False, elem_id="output_raw")

                # self.input_example = gr.Examples([])
                # self.hidden_btn = gr.Button(visible=False, elem_id="hidden_btn")

            block.load(
                fn=self.service.initial_render,
                outputs=[
                    self.model_dd,
                    self.rag_dd,
                    self.ft_dd
                ],
                show_progress=False
            )
            
            self.sample_check.select(
                fn=self.service.sample_check_toggle,
                inputs=[
                    self.sample_check
                ],
                outputs=[
                    self.temperature_slider,
                    self.topp_slider
                ]
            )
            
            self.clear_btn.click(
                fn=self.service.clear_text,
                outputs=[
                    self.input_box,
                    self.output_box,
                    # self.output_raw
                ]
            )
            
            self.submit_btn.click(
                fn=self.service.completion_stream,
                inputs=[
                    self.model_dd,
                    self.rag_dd,
                    self.ft_dd,
                    self.sample_check,
                    self.temperature_slider,
                    self.topp_slider,
                    self.token_slider,
                    self.input_box
                ],
                outputs=[
                    self.output_box
                ],
                show_progress="minimal"
            )