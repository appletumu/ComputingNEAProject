import customtkinter as tk
import tkinter.messagebox as messagebox
from tkinter.messagebox import askyesno, askokcancel, askyesnocancel, askretrycancel
from recallr.backend import DatabaseManager
from recallr.objects import Account, AppSettings, Notes

class ComponentManager:
    def __init__(self, screen_manager, frame_manager):
        self.screen_manager = screen_manager
        self.frame_manager = frame_manager

        self.window_manager = screen_manager.window_manager

    def button_click(self, button):
        command_handler = ComponentCommandHandler(screen_manager=self.screen_manager, frame_manager=self.frame_manager)

        # Checks to see if the button has an associated command first
        # If not, it will use the button's component_id to find the method
        if hasattr(button, 'associated_command'):
            button_command = button.associated_command
        else:
            button_command = button.component_id

        # Uncomment if you need to check the button_command variable
        #print(button_command)

        # Checks if the button's method is wtihin the CommandHandler class
        func = getattr(command_handler, button_command, None)
        try:
            func(button)
        except TypeError as e:
            print(f"❌ The button '{button.component_id}' has no associated action, or has run into an error.\n\t> {e}")

            # Uncomment this if you need to find the error from here
            #raise e

class Components:
    def __init__(self, screen_manager, frame_manager):
        self.screen_manager = screen_manager
        self.frame_manager = frame_manager
        self.default = DefaultComponents(screen_manager, frame_manager)
        self.custom = CustomComponents(screen_manager, frame_manager)

class DefaultComponents:
    def __init__(self, screen_manager, frame_manager):
        self.screen_manager = screen_manager
        self.frame_manager = frame_manager

        self.app_settings = AppSettings()
        self.font = self.app_settings.font
        self.title_size = self.app_settings.text_sizes['title']
        self.content_size = self.app_settings.text_sizes['content']
        self.colors = self.app_settings.colors

    def title(self, text=None, component_id="title", **kwargs):
        if text == None:
            text = self.app_settings.app_name

        self.frame_manager.create_component(
            tk.CTkLabel, 
            text=text, 
            component_id=component_id, 
            font=(self.font, self.title_size), 
            **kwargs
        )

    def content(self, component_id="content", **kwargs):
        self.frame_manager.create_component(
            tk.CTkLabel, 
            component_id=component_id, 
            font=(self.font, self.content_size), 
            **kwargs
        )

    def check_box(self, component_id=None, check_box_style="default", disabled=False, selected=False, **kwargs):
        button_colors = self.app_settings.colors

        if check_box_style not in button_colors:
            raise ValueError(f"Unknown check_box style '{check_box_style}'. Available types: {list(button_colors.keys())}")

        selected_colour = check_box_style

        if disabled == True:
            state = tk.DISABLED
            border_color="#A0A0A0"
        else:
            state = tk.NORMAL
            border_color = None

        check_box_instance = self.frame_manager.create_component(
            tk.CTkCheckBox, 
            component_id=component_id, 
            font=(self.font, self.content_size), 
            border_color=border_color,
            fg_color=button_colors[selected_colour]['fg_color'],
            hover_color=button_colors[selected_colour]['hover_color'],
            border_width=2,
            state=state,
            **kwargs
        )

        if selected == True:
            check_box_instance.select()

    def entry_field(self, component_id=None, **kwargs):
        component_size = self.app_settings.component_configs["entryField"]

        self.frame_manager.create_component(
            tk.CTkEntry, 
            component_id=component_id, 
            font=(self.font, self.content_size), 
            width=200, 
            height=40, 
            **kwargs
        )

    def text_box(self, component_id=None, textbox_size="content", width=None, height=None, **kwargs):
        text_size = self.app_settings.text_sizes[textbox_size]

        # textbox_size is a key: 'title' or 'content'

        if width is None:
            width = 700 if textbox_size == "title" else 700
        if height is None:
            height = 70 if textbox_size == "title" else 300

        wrap = "word"

        # If font size is a title, disable wrapping
        if text_size == self.title_size:
            wrap = "none"
        
        text_box = self.frame_manager.create_component(
            tk.CTkTextbox, 
            component_id=component_id, 
            font=(self.font, text_size), 
            width=width, height=height,
            wrap=wrap,
            **kwargs
        )

        return text_box

    def button(self, text="Button", button_type="default", button_style=None, component_id=None, padding=True, command=None, **kwargs):
        component_size = self.app_settings.component_configs["button"]

        if button_type not in self.colors:
            raise ValueError(f"Unknown button style or type '{button_type}'. Available styles: {list(self.colors.keys())}")

        if button_style == None:
            selected_button_colour = button_type
        else:
            selected_button_colour = button_style

        button_instance = self.frame_manager.create_component(
            tk.CTkButton,
            component_id=component_id,
            padding=padding,
            text=text,
            font=(self.font, self.content_size),
            width=200, height=40,
            command=command,
            fg_color=self.colors[selected_button_colour]['fg_color'],
            hover_color=self.colors[selected_button_colour]['hover_color'],
            **kwargs
        )

        # If the button is disabled, makes the fg_color as selected.
        state = button_instance.cget("state")
        if state == "disabled":
            button_instance.configure(fg_color=self.colors[selected_button_colour]['hover_color'])

        component_manager = ComponentManager(screen_manager=self.screen_manager, frame_manager=self.frame_manager)

        # Connects the button to the ComponentCommandHandler class
        # Allows code to be executed when the button is pressed
        button_instance.configure(command=lambda b=button_instance: component_manager.button_click(b))

        # If this is a primary button, binds it to the Enter/Return key
        if button_type == "primary":
            try:
                root = self.screen_manager.winfo_toplevel()
            except Exception:
                root = getattr(self.screen_manager, 'master', None)

            if root is not None:
                # store the primary button reference on the root
                try:
                    setattr(root, '_primary_button', button_instance)
                except Exception:
                    try:
                        root._primary_button = button_instance
                    except Exception:
                        pass

                # define the handler that will invoke the current primary
                def _primary_key_handler(event, r=root):
                    btn = getattr(r, '_primary_button', None)
                    if btn:
                        try:
                            btn.invoke()
                        except Exception:
                            pass

                # bind once on the root
                try:
                    if not getattr(root, '_primary_keybound', False):
                        root.bind_all('<Return>', _primary_key_handler)
                        setattr(root, '_primary_keybound', True)
                except Exception:
                    pass

    def message_box(self, component_id="message_box", message_box_type="info", title=None, message="", **kwargs):
        if title == None:
            title = self.app_settings.app_name

        result = None

        if message_box_type == "info":
            messagebox.showinfo(f"{title}", message)
        elif message_box_type == "warning":
            messagebox.showwarning(f"{title} - Warning", message)
        elif message_box_type == "error":
            messagebox.showerror(f"{title} - Error", message)
        elif message_box_type == "confirm":
            if message == "":
                message = "Are you sure you want to do this?"
            result = askokcancel(f"{title} - Confirm", message)
        else:
            raise ValueError(f"Unknown message_box_type '{message_box_type}'. Available types: ['info', 'warning', 'error', 'confirm']")

        return result


class CustomComponents:
    def __init__(self, screen_manager, frame_manager):
        self.screen_manager = screen_manager
        self.frame_manager = frame_manager

        self.window_manager = screen_manager.window_manager
    
    def view_note_button(self, **kwargs):
        component = Components(self.screen_manager, self.frame_manager)
        note_id = kwargs.pop('note_id', 1)

        # Get the note / title from the database
        note = Notes().get_notes(note_ids=[note_id])[0]

        note_title = note['title']
        note_content = note['content']

        note_title = note['title'] or "Untitled"
        note_content = note['content'] or  "No preview available"

        # Collapse newlines and repeated spaces for both title and content
        title_max = kwargs.pop('title_max_chars', 18)
        preview_max = kwargs.pop('preview_max_chars', 18)

        def make_preview(text, max_chars):
            s = ' '.join(str(text).split())
            if len(s) > max_chars:
                return s[:max_chars].rstrip() + '...'
            return s

        title_preview = make_preview(note_title, title_max)
        content_preview = make_preview(note_content, preview_max)

        component.default.button(text=f"{title_preview}\n{content_preview}", padding=False, button_type="grey", command="view_note", **kwargs)
    
    def view_note_textbox(self, note_id, **kwargs):
        account = Account()
        component = Components(self.screen_manager, self.frame_manager)

        note = Notes().get_notes(note_ids=[note_id])[0]

        # Gets note info from db
        note_title = note['title']
        note_content = note['content']

        # If it equals None, makes it "" to prevent an _tkinter.TclError
        if note_title == None:
            note_title = ""
        if note_content == None:
            note_content = ""

        #if note_title == None:
            #note_title = "Untitled"

        # Display Components
        component.default.text_box(component_id=f"notes_title_textbox_{note_id}", textbox_size="title", **kwargs)
        component.default.text_box(component_id=f"notes_content_textbox_{note_id}", **kwargs)
        component.default.button(text="Save note", component_id=f"save_note_{note_id}", button_type="default", command="save_note")
        component.default.button(text="Delete note", component_id=f"delete_note_{note_id}", button_type="red", command="delete_note")
        component.custom.go_to_notes_selection_button(note_id=note_id)
        #component.custom.main_menu_button()

        title = self.frame_manager.find_component(f"notes_title_textbox_{note_id}")
        content = self.frame_manager.find_component(f"notes_content_textbox_{note_id}")

        # Inserts the note title and content into the text box
        title.insert("0.0", note_title)
        content.insert("0.0", note_content)

    def go_to_notes_selection_button(self, note_id, **kwargs):
        component = Components(self.screen_manager, self.frame_manager)
        component.default.button(text="Go back", component_id=f"go_to_notes_selection_from_{note_id}", button_type="grey", command="go_to_notes_selection")

    def password_entry_field(self, placeholder_text="Password", **kwargs):
        component = Components(self.screen_manager, self.frame_manager)

        component.default.entry_field(placeholder_text=placeholder_text, show="*", **kwargs)

    def main_menu_button(self, **kwargs):
        component = Components(self.screen_manager, self.frame_manager)

        component.default.button(text="Main menu", button_type="grey", **kwargs)
    
    def sign_out_button(self, **kwargs):
        component = Components(self.screen_manager, self.frame_manager)

        component.default.button(text="Sign out", button_type="red", **kwargs)

    def change_page_blurting_button(self, text, page, button_state, selected_notes, **kwargs):
        component = Components(self.screen_manager, self.frame_manager)
        
        component.default.button(
            text=text, 
            component_id=f"blurting_selection_page_{page}", 
            command="change_page_blurting_selection", 
            button_type="default", 
            state=button_state,
            padding=False
        )

    def reveal_blurting_note_button(self, state=tk.NORMAL, button_style="green", **kwargs):
        component = Components(self.screen_manager, self.frame_manager)
        
        component.default.button(text="Reveal note", component_id="reveal_blurting_note", state=state, button_type="primary", button_style=button_style)

    def start_countdown(self, seconds=10, **kwargs):
        # Gets the time remaining
        if not hasattr(self, "time_left"):
            self.time_left = seconds
        if self.time_left is None:
            self.time_left = seconds

        component = self.frame_manager.find_component("countdown_timer")

        # Create the component if missing
        if component is None:
            new_component = Components(self.screen_manager, self.frame_manager)
            new_component.default.title(text=str(self.time_left), component_id="countdown_timer")
            new_component.default.content(text="seconds remaining")
            new_component.custom.reveal_blurting_note_button(state=tk.DISABLED, button_style="grey")
            component = self.frame_manager.find_component("countdown_timer")

        component.configure(text=str(self.time_left))

        # Schedules the next tick if there is time left
        if self.time_left > 0:
            self.time_left -= 1
            self.window_manager.after(1000, lambda: self.start_countdown(self.time_left))
        else:
            self.screen_manager.show_screen("blurting_game", blurting_notes=self.screen_manager.selected_notes, current_note_index=self.screen_manager.current_note_index, step="times_up")
            self.time_left = None
    
"""    def start_countdown(self, seconds=10, **kwargs):
        component = self.frame_manager.find_component("countdown_timer")

        if component == None:
            self.time_left = seconds
            new_component = Components(self.screen_manager, self.frame_manager)
            new_component.default.title(text=str(self.time_left), component_id="countdown_timer")
        elif self.time_left >= 0:
            component.configure(text=str(self.time_left), component_id="countdown_timer")

            # Schedule the next tick
            self.window_manager.after(1000, self.start_countdown)

            self.time_left -= 1
        else:
            print("timer finished")"""

class ComponentCommandHandler:
    def __init__(self, screen_manager, frame_manager):
        self.screen_manager = screen_manager
        self.frame_manager = frame_manager
    
    def login(self, component):
        new_component = Components(self.screen_manager, self.frame_manager)

        username = self.frame_manager.find_component("username").get()
        password = self.frame_manager.find_component("password").get()

        account = Account()
        result = account.login(username, password)

        if result["success"]:
            # successful login
            self.screen_manager.show_screen("main_menu")
        else:
            # Failed login
            new_component.default.message_box(message_box_type="warning", message=result["message"])    

    def create_account_menu(self, component):
        self.screen_manager.show_screen("create_account")

    def make_the_account(self, component):
        new_component = Components(self.screen_manager, self.frame_manager)

        display_name = self.frame_manager.find_component("display_name").get()
        new_username = self.frame_manager.find_component("new_username").get()
        new_password = self.frame_manager.find_component("new_password").get()
        confirm_password = self.frame_manager.find_component("confirm_password").get()

        account = Account()
        result = account.create_account(display_name, new_username, new_password, confirm_password)

        if result["success"]:
            # successfully created an account
            self.screen_manager.show_screen("login")
            new_component.default.message_box(message_box_type="info", message=result["message"]) 
        else:
            # Failed to create an account
            new_component.default.message_box(message_box_type="warning", message=result["message"])    

    def cancel_create_account(self, component):
        self.screen_manager.show_screen("login")

    def sign_out(self, component):
        account = Account()
        account.sign_out()

        self.screen_manager.show_screen("login")

        new_component = Components(self.screen_manager, self.frame_manager)
        new_component.default.message_box(message_box_type="info", message="Successfully signed out")

    def coming_soon(self, component):
        new_component = Components(self.screen_manager, self.frame_manager)
        new_component.default.message_box(message_box_type="warning", message="Coming Soon") 

    def main_menu(self, component):
        self.screen_manager.show_screen("main_menu")
    
    def quiz_menu(self, component):
        self.screen_manager.show_screen("quiz_menu")

    def notes(self, component):
        self.screen_manager.show_screen("notes")

    def blurting(self, component):
        self.screen_manager.show_screen("blurting_menu_selection")
    
    def create_note(self, component):
        note_id = Notes().create_note()

        self.screen_manager.show_screen("notes", view_note_id=note_id)

    def save_note(self, component):
        notes = Notes()
        note_data = notes.get_note_data_from_components(component, self.frame_manager)
        notes.save_note(note_data['id'], note_data['title'], note_data['content'])

        self.screen_manager.show_screen("notes", view_note_id=note_data['id'])
        new_component = Components(self.screen_manager, self.frame_manager)
        new_component.default.message_box(message_box_type="info", message=f"Saved the note '{note_data['title']}' with the note ID '{note_data['id']}'.")

    def delete_note(self, component):
        new_component = Components(self.screen_manager, self.frame_manager)

        # Gets the note ID from the component ID
        note_id = component.component_id.split("_")[-1]
        note_info = Notes().delete_note(note_id)

        # Confirmation
        result = new_component.default.message_box(message_box_type="confirm", message=f"Are you sure you want to delete this note?\n\nTitle: '{note_info['title']}'\nID: {note_id}")

        if result == False:
            return False

        self.screen_manager.show_screen("notes")
        #new_component.default.message_box(message_box_type="info", message=f"Deleted the note '{note_info['title']}' with the note ID '{note_id}'.")
    
    def go_to_notes_selection(self, component):
        new_component = Components(self.screen_manager, self.frame_manager)
        notes = Notes()
        result = True

        # Only shows confirmation prompt if any changes have been made
        current_note_data = notes.get_note_data_from_components(component, self.frame_manager)
        current_note_title = current_note_data['title']
        current_note_content = current_note_data['content']

        db_note = Notes().get_notes(note_ids=[int(current_note_data['id'])])[0]
        db_note_title = db_note['title']
        db_note_content = db_note['content']
        
        if current_note_title != db_note_title or current_note_content != db_note_content:
            result = new_component.default.message_box(message_box_type="confirm", message=f"You have unsaved changes. Are you sure you want to exit this note?")

        if result == True:
            self.screen_manager.show_screen("notes")

    def view_note(self, component):
        # Gets the note ID from the component ID
        note_id = component.component_id.split("_")[-1]

        self.screen_manager.show_screen("notes", view_note_id=note_id)

    def settings_pane(self, component):
        self.screen_manager.show_screen("settings")
    
    def change_page_blurting_selection(self, component):
        self.screen_manager.selected_notes = Notes().select_notes_blurt(self.frame_manager, self.screen_manager.selected_notes)
        
        page_number = component.component_id.split("_")[-1]
        self.screen_manager.show_screen("blurting_menu_selection", page_number=page_number, notes_selected=self.screen_manager.selected_notes)
    
    def select_blurting_notes(self, component):
        self.screen_manager.selected_notes = Notes().select_notes_blurt(self.frame_manager, self.screen_manager.selected_notes)
        
        new_component = Components(self.screen_manager, self.frame_manager)

        if len(self.screen_manager.selected_notes) > 0:
            #new_component.default.message_box(message_box_type="info", message=f"Selected the following notes:\n\n{self.screen_manager.selected_notes}")
            self.screen_manager.show_screen("blurting_game", blurting_notes=self.screen_manager.selected_notes)
        else:
            new_component.default.message_box(message_box_type="warning", message=f"You need to select at least one note to blurt.")
    
    def go_back_to_blurting_selection(self, component):
        new_component = Components(self.screen_manager, self.frame_manager)
        
        if component.component_id.endswith("noconfirm"):
            result = True
        else:
            result = new_component.default.message_box(message_box_type="confirm")

        if result == True:
            self.screen_manager.show_screen("blurting_menu_selection")

    def start_blurting_timer(self, component):
        self.screen_manager.show_screen("blurting_game", blurting_notes=self.screen_manager.selected_notes, current_note_index=self.screen_manager.current_note_index, step="blurting")
    
    def reveal_blurting_note(self, component):
        self.screen_manager.show_screen("blurting_game", blurting_notes=self.screen_manager.selected_notes, current_note_index=self.screen_manager.current_note_index, step="reveal_note")
    
    def next_blurting_note(self, component):
        self.screen_manager.current_note_index += 1

        self.screen_manager.show_screen("blurting_game", blurting_notes=self.screen_manager.selected_notes, current_note_index=self.screen_manager.current_note_index, step="blurting")