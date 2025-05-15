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
    reset_camera,
    sculpture_change_complete
)

in_development = True


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
        from kivy.clock import Clock
        import os

        Window.size = (1800, 940)
        Window.left = 50
        Window.top = 50

        print("Python used:", sys.executable)

        self.color_settings_data = self.get_saved_settings()
        Window.clearcolor = (0.16, 0.44, 0.79, 1)

        root = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        left_panel = BoxLayout(orientation='vertical', spacing=10)

        scroll = ScrollView()
        layout = GridLayout(cols=8, padding=10, spacing=10,
                            row_default_height=40, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        def wrap_button(btn):
            btn.halign = 'center'
            btn.valign = 'middle'
            btn.bind(
                size=lambda instance, value: setattr(instance, 'text_size',
                                                     (instance.width, None)))
            return btn

        layout.add_widget(Label(text='RPM:', color=(1, 1, 1, 1)))
        rpm_entry = TextInput()
        layout.add_widget(rpm_entry)

        layout.add_widget(Label(text='Direction:', color=(1, 1, 1, 1)))
        direction_spinner = Spinner(text="forward",
                                    values=["forward", "backward"])
        layout.add_widget(direction_spinner)

        layout.add_widget(Label(text='Color:', color=(1, 1, 1, 1)))
        color_spinner = Spinner(text="white", values=[c["color_name"] for c in
                                                      self.color_settings_data])
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
            lbl = Label(
                text=f"{setting.replace('_', ' ').title()} ({min_val}-{max_val})",
                halign='center', valign='middle', color=(1, 1, 1, 1))
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

        layout.add_widget(wrap_button(Button(
            text="Send Command to\nNovatrope",
            on_press=lambda x: on_send(rpm_entry, color_value_entry,
                                       direction_spinner, shutter_entry,
                                       setting_inputs),
            background_normal='', background_color=(0, 0.5, 0, 1),
            color=(1, 1, 1, 1)
        )))

        layout.add_widget(wrap_button(Button(
            text="Save Current\nSettings",
            on_press=lambda x: on_save(color_spinner, color_value_entry,
                                       rpm_entry, direction_spinner,
                                       shutter_entry, comments_entry,
                                       setting_inputs),
            background_normal='', background_color=(0, 0.5, 0, 1),
            color=(1, 1, 1, 1)
        )))

        for _ in range(12):
            layout.add_widget(Label())

        layout.add_widget(Label(text='Time Left (free):', color=(1, 1, 1, 1)))
        free_timer = TextInput()
        layout.add_widget(free_timer)

        layout.add_widget(
            Label(text='Time Left (priority):', color=(1, 1, 1, 1)))
        priority_timer = TextInput()
        layout.add_widget(priority_timer)

        layout.add_widget(wrap_button(Button(
            text="Update\nTimers",
            on_press=lambda x: update_timers(free_timer, priority_timer),
            background_normal='', background_color=(0.5, 0, 0.5, 1),
            color=(1, 1, 1, 1)
        )))

        for _ in range(14):
            layout.add_widget(Label())

        color_spinner.bind(
            text=lambda instance, value: self.on_color_change(color_spinner,
                                                              color_value_entry,
                                                              rpm_entry,
                                                              direction_spinner,
                                                              shutter_entry,
                                                              setting_inputs))
        self.on_color_change(color_spinner, color_value_entry, rpm_entry,
                             direction_spinner, shutter_entry, setting_inputs)

        layout.add_widget(wrap_button(Button(
            text="Start Twitch/\nYoutube Python Server",
            on_press=lambda x: run_server_script(),
            background_normal='', background_color=(0.57, 0.27, 1, 1),
            color=(1, 1, 1, 1)
        )))

        layout.add_widget(wrap_button(Button(
            text="Start\nStream Apps",
            on_press=lambda x: run_streamerbot_script()
        )))

        for _ in range(5):
            layout.add_widget(Label())

        layout.add_widget(wrap_button(Button(
            text="Restart\nSculpture",
            on_press=lambda x: sculpture_change_complete(),
            background_normal='', background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1)
        )))
        layout.add_widget(wrap_button(Button(
            text="Change the\nSculpture", on_press=lambda x: stop_sculpture(),
            background_normal='', background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1)
        )))
        layout.add_widget(wrap_button(Button(
            text="Reset\nArduino", on_press=lambda x: reset_arduinos(),
            background_normal='', background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1)
        )))
        layout.add_widget(wrap_button(Button(
            text="Clear Timer\nVariables",
            on_press=lambda x: reset_timer_variables(),
            background_normal='', background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1)
        )))

        for _ in range(5):
            layout.add_widget(Label())

        layout.add_widget(wrap_button(Button(
            text='Restart HDMI\nStream:', on_press=lambda x: reset_camera(),
            background_normal='', background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1)
        )))

        console_output = TextInput(
            text='', multiline=True, readonly=True,
            background_color=(0, 0, 0, 1), foreground_color=(1, 1, 1, 1),
            size_hint_y=None, height=200
        )
        sys.stdout = TextRedirector(console_output)
        sys.stderr = TextRedirector(console_output)

        scroll.add_widget(layout)
        left_panel.add_widget(scroll)
        left_panel.add_widget(console_output)
        root.add_widget(left_panel)

        # === RIGHT SIDE JSON VIEWER ===
        settings_path = r"A:\Desktop\Novatropes Stream\sculpture_settings"
        self.json_sources = {}

        for filename in os.listdir(settings_path):
            if filename.lower().endswith(".json"):
                full_path = os.path.join(settings_path, filename)
                try:
                    with open(full_path, "r") as f:
                        data = json.load(f)
                    name = os.path.splitext(filename)[0]
                    self.json_sources[name] = data
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

        if not self.json_sources:
            self.json_sources["No Files Found"] = {}

        first_key = list(self.json_sources.keys())[0]

        right_panel = BoxLayout(orientation='vertical', size_hint=(0.4, 1),
                                spacing=10)

        json_selector = Spinner(
            text='',
            values=list(self.json_sources.keys()),
            size_hint=(1, None),
            height=40
        )

        json_viewer = TextInput(
            readonly=True,
            size_hint=(1, 1),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1)
        )

        def on_json_select(spinner, text):
            selected = self.json_sources.get(text, {})
            json_viewer.text = json.dumps(selected, indent=4)
            self.color_settings_data = selected

            if 'rpm' in selected:
                rpm_entry.text = str(selected['rpm'])
            if 'color' in selected:
                color_value_entry.text = selected['color']
            if 'direction' in selected:
                direction_spinner.text = selected['direction']
            if 'shutter_instructions' in selected:
                shutter_entry.text = selected['shutter_instructions']

            for setting, entry in setting_inputs.items():
                if setting in selected:
                    entry.text = str(selected[setting])

        json_selector.bind(text=on_json_select)

        right_panel.add_widget(json_selector)
        right_panel.add_widget(json_viewer)
        root.add_widget(right_panel)

        def trigger_initial_json(dt):
            json_selector.text = first_key

        Clock.schedule_once(trigger_initial_json, 0)

        if not in_development:
            run_streamerbot_script()
            run_server_script()

        return root







