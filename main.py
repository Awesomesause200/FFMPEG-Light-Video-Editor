import tkinter as tk
import tkinter.filedialog

import ttkbootstrap as ttk
import os
import subprocess


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename='superhero')
        self.geometry("800x900")
        self.wm_title("FFMPEG Light Video Editor")

        # Define frames
        self.primary_frame = ttk.Frame()
        self.input_field_frame = ttk.Frame(self.primary_frame)
        # Additional frames per option selector
        self.time_selector_frame = ttk.Frame(self.primary_frame)
        self.crop_selector_frame = ttk.Frame(self.primary_frame)
        self.resize_frame = ttk.Frame(self.primary_frame)
        self.scale_video_frame = ttk.Frame(self.primary_frame)
        self.rotate_frame = ttk.Frame(self.primary_frame)
        self.flip_frame = ttk.Frame(self.primary_frame)
        self.saturation_brightness_contrast_frame = ttk.Frame(self.primary_frame)
        self.operation_frame = ttk.Frame(self.primary_frame)
        self.test_frame = ttk.Frame(self.primary_frame)

        # Define widgets
        self.file_input_var = tk.StringVar()
        self.file_input = ttk.Entry(self.input_field_frame, textvariable=self.file_input_var)
        self.file_input_select = ttk.Button(self.input_field_frame, text="Select input file",
                                            command=lambda: self.select_file(self.file_input_var))
        self.file_output_var = tk.StringVar()
        self.file_output_var.set(os.getcwd())
        self.file_output_select = ttk.Button(self.input_field_frame, text="Select output file",
                                             command=lambda: self.select_directory(self.file_output_var))
        self.file_output = ttk.Entry(self.input_field_frame, textvariable=self.file_output_var)
        # self.test_button = ttk.Button(self.test_frame)

        self.time_selector = OptionSelectorTimeBased(self.time_selector_frame, ['start time', 'duration'],
                                                     "Truncate time")
        self.crop_selector = OptionSelector(self.crop_selector_frame,
                                            ['Width (pixels)', 'Height (pixels)', 'Top left X', 'Top left Y'],
                                            "Crop Video")
        # self.resize_selector = OptionSelector(self.resize_frame, ['width (pixels)', 'height (pixels)'], "Resize")
        self.scale_video_selector = OptionSelector(self.scale_video_frame, ['width (pixels)', 'height (pixels)'],
                                                   "Scale video down/up, leaving a box blank will fit to match the aspect ratio")
        self.rotate_selector = OptionSelectorComboBox(self.rotate_frame, [
            ['counterclockwise & vertical flip', 'clockwise', 'counterclockwise', 'clockwise & vertical flip']],
                                                      ['transpose'], "Rotate")
        self.flip_selector = OptionSelectorComboBox(self.flip_frame, [['horizontal flip', 'vertical flip']],
                                                    ['flip option'], "Flip Video")
        self.saturation_brightness_contrast = OptionSelectorMeter(self.saturation_brightness_contrast_frame,
                                                                  ['brightness', 'contrast', 'saturation'],
                                                                  "Additional Filters")

        self.convert_video_button = ttk.Button(self.operation_frame, text="Make video edits",
                                               command=self.make_video_edits)

        # Pack frame
        self.primary_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.input_field_frame.pack(expand=False, fill=tk.X, padx=5, pady=5)
        self.time_selector_frame.pack(expand=False, fill=tk.X, padx=5, pady=5)
        self.crop_selector_frame.pack(expand=False, fill=tk.X, padx=5, pady=5)
        # self.resize_frame.pack(expand=False, fill=tk.X, pady=5, padx=5)
        self.scale_video_frame.pack(expand=False, fill=tk.X, padx=5, pady=5)
        self.rotate_frame.pack(expand=False, fill=tk.X, padx=5, pady=5)
        self.flip_frame.pack(expand=False, fill=tk.X, padx=5, pady=5)
        self.saturation_brightness_contrast_frame.pack(expand=False, fill=tk.X, padx=5, pady=5)
        self.operation_frame.pack(expand=False, fill=tk.X, padx=5, pady=5)
        self.test_frame.pack(expand=False, fill=tk.X, padx=5, pady=5)

        # Pack widgets
        self.file_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10, pady=5)
        self.file_input_select.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)
        self.file_output.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10, pady=5)
        self.file_output_select.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)
        self.convert_video_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10, pady=5)
        # self.test_button.pack()

        self.place_window_center()
        self.mainloop()

    def create_toplevel_window(self, label_message, height: int = 300, width: int = 200):
        top_level_window = tk.Toplevel(self)
        top_level_window.title("Toplevel Window")
        top_level_window.geometry(f"{height}x{width}")

        self.place_window_center_toplevel(top_level_window)

        label = ttk.Label(top_level_window, text=label_message)
        label.pack(pady=10)

        top_level_window.attributes("-topmost", True)

        self.wait_window(top_level_window)

    def place_window_center_toplevel(self, window):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window.winfo_reqwidth()) // 2
        y = (screen_height - window.winfo_reqheight()) // 2

        # Place the window at the calculated coordinates
        window.geometry("+{}+{}".format(x, y))

    @staticmethod
    def select_file(text_field: tk.StringVar):
        """
        :param text_field: text field string to output the file path string to
        """
        filename = tkinter.filedialog.askopenfilename(title="Select the input file",
                                                      filetypes=[
                                                          ("Video files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv;*.flv;*.webm;"
                                                                          "*.mpg;*.mpeg;*.m4v;*.ogv;*.3gp;*.3g2;*.ts;"
                                                                          "*.mts;*.m2ts"),
                                                          ("All files", "*.*")
                                                      ])

        if filename:
            text_field.set(filename)

    @staticmethod
    def select_directory(text_field: tk.StringVar):
        """
        :param text_field: text field string to output the directory string to

        This allows the user to select an output directory
        The filename itself always outputs the video file input as the new file extensions
        """

        directory = tkinter.filedialog.askdirectory(title="Select the output directory")

        if directory:
            text_field.set(directory)

    def make_video_edits(self):
        # Gather activation status
        time_selector_items = self.time_selector.get_item_states()
        crop_selector_items = self.crop_selector.get_item_states()
        scale_video_items = self.scale_video_selector.get_item_states()
        rotate_selector_items = self.rotate_selector.get_item_states()
        flip_selector_items = self.flip_selector.get_item_states()
        sat_bri_con_items = self.saturation_brightness_contrast.get_item_states()

        # concat all selected items, filtering as we go
        time_values = []
        video_filters = []
        if not time_selector_items[0] and not time_selector_items[1]:
            # catch invalid input error
            self.create_toplevel_window(
                "Time selector has an invalid input, ensure you're only using numbers or unselect truncate time", 600)
        elif time_selector_items[0]:
            start_time, duration = time_selector_items[1]

            # Require start time
            if not start_time:
                self.create_toplevel_window("You did not input a start time")
                return False
            else:
                time_values.append(f"-ss {start_time}")

            # If we have a duration, add that in
            if duration != '00:00:00':
                time_values.append(f"-t {duration}")

        if crop_selector_items[0]:
            crop_width, crop_height, crop_top_x, crop_top_y = crop_selector_items[1]

            # If missing width/height, the modifiers are malformed
            if not crop_width or not crop_height:
                self.create_toplevel_window("Either width, or height is not inputted. Please input values or unselect "
                                            "the crop video modifier", 600, 300)
                return False

            # Define the base string we'll append data to
            crop_modifier_string = f"crop={crop_width}:{crop_height}"

            # Only append data if we have either x/y defined
            if crop_top_x or crop_top_y:
                if crop_top_x:
                    crop_modifier_string += f":{crop_top_x}"
                else:
                    crop_modifier_string += ":"

                if crop_top_y:
                    crop_modifier_string += f":{crop_top_y}"

            # Append the final string
            video_filters.append(f'{crop_modifier_string}')

        if scale_video_items[0]:
            resize_width, resize_height = scale_video_items[1]

            if resize_width or resize_height:
                # If we have a width/height output that, otherwise put a generic w:h
                first_string = f"scale={resize_width if resize_width else 'w'}:{resize_height if resize_height else 'h'}"
                video_filters.append(f'{first_string}')
            else:
                self.create_toplevel_window("Please define width or height to use resize modifier or unselect it.", 500)

        if rotate_selector_items[0]:
            rotate_translation: dict = {'counterclockwise & vertical flip': "0",
                                        'clockwise': "1",
                                        'counterclockwise': "2",
                                        'clockwise & vertical flip': "3"}
            if rotate_selector_items[1][0]:
                first_string = "transpose=" + rotate_translation.get(rotate_selector_items[1][0])
                video_filters.append(f'{first_string}')
            else:
                self.create_toplevel_window(
                    "Please select which rotation you would like or unselect the rotate modifier", 500)

        if flip_selector_items[0]:
            flip_translation: dict = {
                'horizontal flip': 'hflip',
                'vertical flip': 'vflip'
            }
            if flip_selector_items[1][0]:
                # if we have a transpose command, we'll append this one to it instead
                if any(['transpose' in x for x in video_filters]):
                    # Find the index where transpose is
                    transpose_index = next(
                        (i for i, filter_text in enumerate(video_filters) if 'transpose' in filter_text), None)

                    # Splitting string since f-strings can't contain the same quote types
                    original_string = video_filters[transpose_index].strip('"')
                    new_string_part = ',' + flip_translation[flip_selector_items[1][0]]

                    # Append new string
                    video_filters[transpose_index] = f'{original_string + new_string_part}'
                else:
                    video_filters.append(f'"{flip_translation[flip_selector_items[1][0]]}"')
            else:
                self.create_toplevel_window("Select flip modifier (horizontal/vertical), otherwise unselect it")

        if sat_bri_con_items[0]:
            # Divide it by 100
            brightness, contrast, saturation = [int(x) / 100 for x in sat_bri_con_items[1]]

            video_filters.append(f'eq=brightness={brightness}:contrast={contrast}:saturation={saturation}')

        # Craft the command
        if not time_values and not video_filters:
            return False

        command = []

        if time_values:
            command.append(" ".join(time_values))

        if video_filters:
            command.append('-vf')
            command.append(f'"{",".join(video_filters)}"')

        # Pre-pend input, post-pend output
        command.insert(0, f'FFMPEG -i {self.file_input_var.get()}')

        # Parse input file to create output filename
        input_file_name = self.file_input_var.get().split('/')[-1]
        base_name, extension = os.path.splitext(input_file_name)
        new_filename = f"{base_name}_edit{extension}"

        command.append(f'{os.path.join(self.file_output_var.get(), new_filename)}')

        # print(' '.join(command))
        subprocess.call(' '.join(command), shell=False)

        """
        Time video
        ffmpeg -i input.mp4 -ss [start_time] -t [duration] -c:a copy output.mp4

        Crop video
        ffmpeg -i input.mp4 -vf "crop=out_w:out_h:x:y" output.mp4

        Resize video
        ffmpeg -i input.mp4 -vf "scale=w:h" output.mp4

        Rotate video
        ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

        Flip/Mirror video
        ffmpeg -i input.mp4 -vf "hflip" output.mp4
        
        Rotate & Flip
        ffmpeg -i input.mp4 -vf "transpose=1,hflip"

        Adjust brightness/Contrast/Saturation
        ffmpeg -i input.mp4 -vf "eq=brightness=value:contrast=value:saturation=value" output.mp4

        ADDITIONAL NOTES:
        multiple commands can be comma seperated
        """


# Option selector BUT uses spin boxes instead for time selection
class OptionSelectorTimeBased:
    def __init__(self, parent_frame: tk.Frame, entry_box_names: list, frame_text: str, toggle_text: str = 'Toggle'):
        self.parent_frame = parent_frame
        self.frame_text = frame_text
        self.entry_box_names = entry_box_names
        self.toggle_text = toggle_text
        self.box_inputs = []

        self.local_frame = ttk.Labelframe(self.parent_frame, text=self.frame_text)

        self.input_var = tk.IntVar()
        self.input_var.set(0)
        self.check_box = ttk.Checkbutton(self.local_frame, text=self.toggle_text, variable=self.input_var, onvalue=1,
                                         offvalue=0)
        self.check_box.pack(side=tk.LEFT)

        for box_name in self.entry_box_names:
            new_frame = ttk.Labelframe(self.local_frame, text=box_name)
            box_hour_frame = ttk.Labelframe(new_frame, text='hour')
            box_minute_frame = ttk.Labelframe(new_frame, text='minute')
            box_second_frame = ttk.Labelframe(new_frame, text='second')
            box_hour = ttk.Spinbox(box_hour_frame, from_=0, to=99, width=5)
            box_minute = ttk.Spinbox(box_minute_frame, from_=0, to=60, width=5)
            box_second = ttk.Spinbox(box_second_frame, from_=0, to=60, width=5)

            # Pack out stuff
            box_hour.pack(side=tk.LEFT, padx=2, pady=5)
            box_minute.pack(side=tk.LEFT, padx=2, pady=5)
            box_second.pack(side=tk.LEFT, padx=2, pady=5)
            new_frame.pack(side=tk.LEFT, padx=5, pady=5)
            box_hour_frame.pack(side=tk.LEFT, padx=3, pady=1)
            box_minute_frame.pack(side=tk.LEFT, padx=5, pady=1)
            box_second_frame.pack(side=tk.LEFT, padx=3, pady=1)

            # Add to inputs for grabbing them later
            self.box_inputs.append([box_hour, box_minute, box_second])

            # Set values to default 0
            box_hour.set(0)
            box_minute.set(0)
            box_second.set(0)

        self.test_button = ttk.Button(self.local_frame, text="test", command=lambda: print(self.get_item_states()))
        # self.test_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.local_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)

    def get_item_states(self) -> tuple[bool, list[str]]:
        # Slightly modify this as we'll be outputting timestamp values (00:00:00)
        active_boolean: bool = True if self.input_var.get() == 1 else False
        local_box_inputs: list = []

        for box_input in self.box_inputs:
            try:
                h_val, m_val, s_val = [int(x.get()) for x in box_input]
                h_max, m_max, s_max = [x.cget('to') for x in box_input]
            except ValueError:
                # meant to catch if someone inputs a string instead of number input
                return False, []

            # Validate values don't exceed maxes, otherwise pass it on to the next input second > minute > hour
            if s_val > s_max:
                excess_minutes, s_val = divmod(s_val, s_max)
                m_val = m_val + excess_minutes
            if m_val > m_max:
                excess_hours, m_val = divmod(m_val, m_max)
                h_val = h_val + excess_hours

            local_box_inputs.append(f"{h_val:02d}:{m_val:02d}:{s_val:02d}")

        return active_boolean, local_box_inputs


class OptionSelector:
    def __init__(self, parent_frame: tk.Frame, entry_box_names: list, frame_text: str, toggle_text: str = 'Toggle'):
        self.parent_frame = parent_frame
        self.frame_text = frame_text
        self.entry_box_names = entry_box_names
        self.toggle_text = toggle_text
        self.box_inputs = []

        self.local_frame = ttk.Labelframe(self.parent_frame, text=self.frame_text)

        self.input_var = tk.IntVar()
        self.input_var.set(0)
        self.check_box = ttk.Checkbutton(self.local_frame, text=self.toggle_text, variable=self.input_var, onvalue=1,
                                         offvalue=0)
        self.check_box.pack(side=tk.LEFT)

        for box_name in self.entry_box_names:
            new_frame = ttk.Labelframe(self.local_frame, text=box_name)
            new_frame.pack(side=tk.LEFT, padx=5, pady=5)
            new_entry = ttk.Entry(new_frame)
            self.box_inputs.append(new_entry)
            new_entry.pack(side=tk.LEFT)

        self.test_button = ttk.Button(self.local_frame, text="test", command=self.get_item_states)
        # self.test_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.local_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)

    def get_item_states(self) -> tuple[bool, list[str]]:
        return True if self.input_var.get() == 1 else False, [x.get().strip() for x in self.box_inputs]


class OptionSelectorComboBox:
    def __init__(self, parent_frame: tk.Frame, combo_box_options: list[list[str]], combo_box_names: list,
                 frame_text: str, toggle_text: str = 'Toggle'):
        self.parent_frame = parent_frame
        self.frame_text = frame_text
        self.combo_box_options = combo_box_options
        self.toggle_text = toggle_text
        self.combobox_inputs = []

        if len(self.combo_box_options) != len(combo_box_names):
            raise SyntaxError("You failed to define an equal amount of combo box options to the combo box names. You "
                              "must have the same number of options to match the new names")

        self.local_frame = ttk.Labelframe(self.parent_frame, text=self.frame_text)

        self.input_var = tk.IntVar()
        self.input_var.set(0)
        self.check_box = ttk.Checkbutton(self.local_frame, text=self.toggle_text, variable=self.input_var, onvalue=1,
                                         offvalue=0)
        self.check_box.pack(side=tk.LEFT)

        for box_name, combo_box_option in zip(combo_box_names, self.combo_box_options):
            new_frame = ttk.Labelframe(self.local_frame, text=box_name)
            new_frame.pack(side=tk.LEFT, padx=5, pady=5)
            new_combo = ttk.Combobox(new_frame, validate="focusout", justify="center", values=combo_box_option,
                                     width=len(combo_box_option) * 7)
            self.combobox_inputs.append(new_combo)
            new_combo.pack(side=tk.LEFT)

        self.test_button = ttk.Button(self.local_frame, text="test", command=self.get_item_states)
        # self.test_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.local_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)

    def get_item_states(self) -> tuple[bool, list[str]]:
        return True if self.input_var.get() == 1 else False, [x.get().strip() for x in self.combobox_inputs]


class OptionSelectorMeter:
    def __init__(self, parent_frame: tk.Frame, meter_text_names: list, frame_text: str, toggle_text: str = 'Toggle'):
        self.parent_frame = parent_frame
        self.frame_text = frame_text
        self.meter_text_names = meter_text_names
        self.toggle_text = toggle_text
        self.meter_inputs = []

        self.local_frame = ttk.Labelframe(self.parent_frame, text=self.frame_text)

        self.input_var = tk.IntVar()
        self.input_var.set(0)
        self.check_box = ttk.Checkbutton(self.local_frame, text=self.toggle_text, variable=self.input_var, onvalue=1,
                                         offvalue=0)
        self.check_box.pack(side=tk.LEFT)

        for meter_name in self.meter_text_names:
            new_meter = ttk.Meter(self.local_frame, amounttotal=300, metertype='semi', subtext=meter_name,
                                  textfont="-size 20 -weight bold", interactive=True, amountused=100)
            self.meter_inputs.append(new_meter)
            new_meter.pack(side=tk.LEFT)

        self.test_button = ttk.Button(self.local_frame, text="test", command=self.get_item_states)
        # self.test_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.local_frame.pack(side=tk.LEFT, expand=False, fill=tk.Y)

    def get_item_states(self) -> tuple[bool, list[str]]:
        return True if self.input_var.get() == 1 else False, [x.amountusedvar.get() for x in self.meter_inputs]


if __name__ == '__main__':
    app = App()

    """
    Time video
    ffmpeg -i input.mp4 -ss [start_time] -t [duration] -c:v copy -c:a copy output.mp4
    
    Crop video
    ffmpeg -i input.mp4 -vf "crop=out_w:out_h:x:y" output.mp4
    
    Resize video
    ffmpeg -i input.mp4 -vf "scale=w:h" output.mp4
    
    Rotate video
    ffmpeg -i input.mp4 -vf "transpose=1" output.mp4
    
    Flip/Mirror video
    ffmpeg -i input.mp4 -vf "hflip" output.mp4
    
    Adjust brightness/Contrast/Saturation
    ffmpeg -i input.mp4 -vf "eq=brightness=value:contrast=value:saturation=value" output.mp4
    
    ADDITIONAL NOTES:
    multiple commands can be comma seperated
    """
