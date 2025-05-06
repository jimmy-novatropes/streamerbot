from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import json
import sys
from support_functions import (
    on_send,
    on_save,
    run_server_script,
    run_streamerbot_script,
    stop_sculpture,
    reset_arduinos,
    update_timers,
    reset_timer_variables,
    restart_sculpture,
    sculpture_change_complete
)

# class TextRedirector:
#     def __init__(self, text_input):
#         self.text_input = text_input
#
#     def write(self, text):
#         self.text_input.text += text
#         self.text_input.cursor = (0, len(self.text_input.text.split('\n')))
#
#     def flush(self):
#         pass


class TextRedirector:
    def __init__(self, text_input):
        self.text_input = text_input

    def write(self, text):
        self.text_input.text += text
        self.text_input.cursor = (0, len(self.text_input.text.split('\n')))
        self.flush()

    def flush(self):
        # Force redraw
        self.text_input._refresh_text(self.text_input.text, self.text_input.cursor)


class NovatropeControlApp(App):
    def get_saved_settings(self):
        with open("A:/Desktop/Novatropes Stream/server_settings.json", "r") as f:
            return json.load(f)

    def on_color_change(self, spinner, color_value_entry, rpm_entry, direction_spinner, shutter_entry, setting_inputs):
        selected_color = spinner.text.lower()
        match = next((c for c in self.color_settings_data if c["color_name"] == selected_color), None)
        if not match:
            return
        color_value_entry.text = match["color"]
        rpm_entry.text = match["rpm"]
        direction_spinner.text = match["direction"]
        shutter_entry.text = match["shutter_instructions"]
        setting_inputs["exposure_time_absolute"].text = match["exposure"]
        setting_inputs["white_balance_automatic"].text = match["white_balance_auto"]
        setting_inputs["white_balance_temperature"].text = match["white_balance"]
        setting_inputs["brightness"].text = match["brightness"]
        setting_inputs["contrast"].text = match["contrast"]
        setting_inputs["saturation"].text = match["saturation"]
        setting_inputs["hue"].text = match["hue"]

    def build(self):
        Window.size = (1800, 940)
        Window.left = 50  # X position from left of screen
        Window.top = 50  # Y position from top of screen

        print("Python used:", sys.executable)

        self.color_settings_data = self.get_saved_settings()
        Window.clearcolor = (0.16, 0.44, 0.79, 1)

        root = BoxLayout(orientation='vertical', padding=20, spacing=10)
        scroll = ScrollView()
        layout = GridLayout(cols=8, padding=10, spacing=10, row_default_height=40, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Separate button layout row
        button_layout = GridLayout(cols=4, spacing=10, size_hint_y=None, height=140)
        layout.add_widget(Label(text='RPM:', color=(1, 1, 1, 1)))
        rpm_entry = TextInput()
        layout.add_widget(rpm_entry)

        layout.add_widget(Label(text='Direction:', color=(1, 1, 1, 1)))
        direction_spinner = Spinner(text="forward", values=["forward", "backward"])
        layout.add_widget(direction_spinner)

        layout.add_widget(Label(text='Color:', color=(1, 1, 1, 1)))
        color_spinner = Spinner(text="white", values=[c["color_name"] for c in self.color_settings_data])
        layout.add_widget(color_spinner)

        layout.add_widget(Label(text='Color Value:', color=(1, 1, 1, 1)))
        color_value_entry = TextInput()
        layout.add_widget(color_value_entry)

        layout.add_widget(Label(text='Shutter:', color=(1, 1, 1, 1)))
        shutter_entry = TextInput()
        layout.add_widget(shutter_entry)


        camera_settings = {
            "exposure_time_absolute": (1, 5000),
            "white_balance_automatic": (0, 1),
            "white_balance_temperature": (2800, 6500),
            "brightness": (-64, 64),
            "contrast": (0, 64),
            "saturation": (0, 128),
            "hue": (-40, 40),
        }

        setting_inputs = {}
        for setting, (min_val, max_val) in camera_settings.items():
            # layout.add_widget(Label(
            #     text=f"{setting.replace('_', ' ').title()} ({min_val}-{max_val})",
            #     text_size=(200, None),  # set fixed width
            #     halign='center',
            #     color=(1, 1, 1, 1)))
            # entry = TextInput()
            # layout.add_widget(entry)
            lbl = Label(
                text=f"{setting.replace('_', ' ').title()} ({min_val}-{max_val})",
                halign='center',
                valign='middle',
                color=(1, 1, 1, 1)
            )
            lbl.bind(
                size=lambda instance, value: setattr(instance, 'text_size',
                                                     (instance.width, None)))
            layout.add_widget(lbl)

            entry = TextInput()
            layout.add_widget(entry)

            setting_inputs[setting] = entry

        layout.add_widget(Label(text='Comments:', color=(1, 1, 1, 1)))
        comments_entry = TextInput(multiline=True)
        layout.add_widget(comments_entry)

        # layout.add_widget(Button(text="Send Command to Novatrope", on_press=lambda x: on_send(
        #     rpm_entry, color_value_entry, direction_spinner, shutter_entry, setting_inputs),
        #                          background_normal='',
        #                          background_color=(0, 0.5, 0, 1),
        #                          color=(1, 1, 1, 1)           ))

        btn = Button(
            text="Send Command to Novatrope",
            on_press=lambda x: on_send(
                rpm_entry, color_value_entry, direction_spinner, shutter_entry, setting_inputs
            ),
            background_normal='',
            background_color=(0, 0.5, 0, 1),  # Dark green
            color=(1, 1, 1, 1),               # White text
            halign='center',
            valign='middle'
        )
        btn.bind(size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        layout.add_widget(btn)



        layout.add_widget(Button(text="Save Current Settings", on_press=lambda x: on_save(
            color_spinner, color_value_entry, rpm_entry, direction_spinner, shutter_entry, comments_entry, setting_inputs),
                background_normal='',
                background_color=(0, 0.5, 0, 1),  # Dark green
                color=(1, 1, 1, 1)    ))

        for _ in range(12):
            layout.add_widget(Label())

        layout.add_widget(Label(text='Time Left (free):', color=(1, 1, 1, 1)))
        free_timer = TextInput()
        layout.add_widget(free_timer)

        layout.add_widget(Label(text='Time Left (priority):', color=(1, 1, 1, 1)))
        priority_timer = TextInput()
        layout.add_widget(priority_timer)

        layout.add_widget(Button(
            text="Update Timers",
            on_press=lambda x: update_timers(free_timer, priority_timer),
            background_normal='',
            background_color=(0.5, 0, 0.5, 1),  # Purple
            color=(1, 1, 1, 1)
        ))

        for _ in range(14):
            layout.add_widget(Label())

        color_spinner.bind(text=lambda instance, value: self.on_color_change(
            color_spinner, color_value_entry, rpm_entry, direction_spinner, shutter_entry, setting_inputs))
        self.on_color_change(color_spinner, color_value_entry, rpm_entry, direction_spinner, shutter_entry, setting_inputs)

        btn = Button(
            text="Start Twitch/Youtube Python Server",
            on_press=lambda x: run_server_script(),
            halign='center',
            valign='middle',
            background_normal='',
            background_color=(0.57, 0.27, 1, 1),  # Purple
            color=(1, 1, 1, 1),
        )
        btn.bind(size=lambda instance, value: setattr(instance, 'text_size',
                                                      (instance.width, None)))
        layout.add_widget(btn)


        layout.add_widget(Button(text="Start Stream Apps", on_press=lambda x: run_streamerbot_script()))

        for _ in range(5):
            layout.add_widget(Label())

        layout.add_widget(Button(text="Restart Sculpture",
                                 on_press=lambda x: sculpture_change_complete(),
                                 background_normal='',
                                 background_color=(1, 0, 0, 1),
                                 # Red background
                                 color=(1, 1, 1, 1)))
        layout.add_widget(Button(text="Change the Sculpture", on_press=lambda x: stop_sculpture(),  background_normal='',
    background_color=(1, 0, 0, 1),  # Red background
    color=(1, 1, 1, 1) ))
        layout.add_widget(Button(text="Reset Arduino", on_press=lambda x: reset_arduinos(),  background_normal='',
    background_color=(1, 0, 0, 1),  # Red background
    color=(1, 1, 1, 1) ))
        layout.add_widget(Button(text="Clear Timer Variables", on_press=lambda x: reset_timer_variables(),  background_normal='',
    background_color=(1, 0, 0, 1),  # Red background
    color=(1, 1, 1, 1) ))

        # Console output window
        console_output = TextInput(text='', multiline=True, readonly=True, background_color=(0, 0, 0, 1), foreground_color=(1, 1, 1, 1), size_hint_y=None, height=200)
        sys.stdout = TextRedirector(console_output)
        sys.stderr = TextRedirector(console_output)
        root.add_widget(console_output)

        scroll.add_widget(layout)
        root.add_widget(button_layout)
        root.add_widget(scroll)

        run_streamerbot_script()
        run_server_script()
        return root


