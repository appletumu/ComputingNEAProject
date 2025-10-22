import customtkinter as tk
import tkinter.messagebox as messagebox
import sqlite3
from recallr.backend import DatabaseManager, JsonManager
from recallr.objects import Account

class ComponentManager:
    def __init__(self, screen_manager, frame_manager):
        self.screen_manager = screen_manager
        self.frame_manager = frame_manager

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
            print(f"❌ The button '{button.component_id}' has no associated action")

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

    def title(self, component_id=None, **kwargs):
        self.frame_manager.create_component(tk.CTkLabel, component_id=component_id, font=("Arial", 68), **kwargs)

    def content(self, component_id=None, **kwargs):
        self.frame_manager.create_component(tk.CTkLabel, component_id=component_id, font=("Arial", 16), **kwargs)

    def entry_field(self, component_id=None, **kwargs):
        self.frame_manager.create_component(tk.CTkEntry, component_id=component_id, font=("Arial", 14), width=200, height=40, **kwargs)

    def button(self, text="Button", button_type="default", button_style=None, component_id=None, padding=True, command=None, **kwargs):
        button_colors = {
            "primary": {"fg_color": "#104A99", "hover_color": "#1E90FF"},
            "default": {"fg_color": "#104A99", "hover_color": "#1E90FF"},
            "green": {"fg_color": "#218c3a", "hover_color": "#27ae60"},
            "red": {"fg_color": "#FF3333", "hover_color": "#FF6666"},
            "grey": {"fg_color": "#666666", "hover_color": "#808080"},
        }

        if button_type not in button_colors:
            raise ValueError(f"Unknown button_type '{button_type}'. Available types: {list(button_colors.keys())}")

        if button_style == None:
            selected_button_colour = button_type
        else:
            selected_button_colour = button_style

        button_instance = self.frame_manager.create_component(
            tk.CTkButton,
            component_id=component_id,
            padding=padding,
            text=text,
            font=("Arial", 16),
            width=200, height=40,
            command=command,
            fg_color=button_colors[selected_button_colour]['fg_color'],
            hover_color=button_colors[selected_button_colour]['hover_color'],
            **kwargs
        )

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
    
    def text_box(self, component_id=None, **kwargs):
        self.frame_manager.create_component(
            tk.CTkTextbox, 
            component_id=component_id, 
            font=("Arial", 14), 
            width=400, height=200,
            wrap="word",
            **kwargs
        )

    def message_box(self, component_id=None, message_box_type="info", title="Recallr", message="", **kwargs):
        if message_box_type == "info":
            messagebox.showinfo("Recallr", message)
        elif message_box_type == "warning":
            messagebox.showwarning("Recallr - Warning", message)
        elif message_box_type == "error":
            messagebox.showerror("Recallr - Error", message)
        else:
            raise ValueError(f"Unknown message_box_type '{message_box_type}'. Available types: ['info', 'warning', 'error']")


class CustomComponents:
    def __init__(self, screen_manager, frame_manager):
        self.screen_manager = screen_manager
        self.frame_manager = frame_manager
    
    def view_note_button(self, **kwargs):
        account = Account()
        component = Components(self.screen_manager, self.frame_manager)
        note_id = kwargs.pop('note_id', 1)

        note = DatabaseManager().query(
            "SELECT title, content FROM notes WHERE note_id = ? AND owner_username = ?",
            (note_id, account.username)
        )

        note_title = note[0][0]
        note_content = note[0][1]

        # Get the note / title from the database
        if note and len(note) > 0 and len(note[0]) >= 2:
            note_title = note[0][0] or "Untitled"
            note_content = note[0][1] or  "No preview available"
        else:
            note_title = "Untitled"
            note_content = "No preview available"

        # Collapse newlines and repeated spaces for both title and content
        title_max = kwargs.pop('title_max_chars', 22)
        preview_max = kwargs.pop('preview_max_chars', 22)

        def make_preview(text, max_chars):
            s = ' '.join(str(text).split())
            if len(s) > max_chars:
                return s[:max_chars].rstrip() + '...'
            return s

        title_preview = make_preview(note_title, title_max)
        content_preview = make_preview(note_content, preview_max)

        component.default.button(text=f"{title_preview}\n{content_preview}", padding=False, button_type="grey", **kwargs)
    
    def view_note_textbox(self, note_id, **kwargs):
        account = Account()
        component = Components(self.screen_manager, self.frame_manager)

        note = DatabaseManager().query(
            "SELECT title, content FROM notes WHERE note_id = ? AND owner_username = ?",
            (note_id, account.username)
        )

        # Gets note info from db
        note_title = note[0][0]
        note_content = note[0][1]

        # If it equals None, makes it "" to prevent an _tkinter.TclError
        if note_title == None:
            note_title = ""
        if note_content == None:
            note_content = ""

        #if note_title == None:
            #note_title = "Untitled"

        # Display Components
        component.default.text_box(component_id=f"notes_title_textbox_{note_id}", **kwargs)
        component.default.text_box(component_id=f"notes_content_textbox_{note_id}", **kwargs)
        component.default.button(text="Delete note", component_id=f"delete_note_{note_id}", button_type="red", command="delete_note")
        component.custom.main_menu_button()

        title = self.frame_manager.find_component(f"notes_title_textbox_{note_id}")
        content = self.frame_manager.find_component(f"notes_content_textbox_{note_id}")

        # Inserts the note title and content into the text box
        title.insert("0.0", note_title)
        content.insert("0.0", note_content)

    def password_entry_field(self, placeholder_text="Password", **kwargs):
        component = Components(self.screen_manager, self.frame_manager)

        component.default.entry_field(placeholder_text=placeholder_text, show="*", **kwargs)

    def main_menu_button(self, **kwargs):
        component = Components(self.screen_manager, self.frame_manager)

        component.default.button(text="Main menu", button_type="grey", **kwargs)
    
    def sign_out_button(self, **kwargs):
        component = Components(self.screen_manager, self.frame_manager)

        component.default.button(text="Sign out", button_type="red", **kwargs)

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

        if result["sucess"]:
            # Sucessful login
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

        if result["sucess"]:
            # Sucessfully created an account
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
        self.screen_manager.show_screen("coming_soon")

    def main_menu(self, component):
        self.screen_manager.show_screen("main_menu")
    
    def quiz_menu(self, component):
        self.screen_manager.show_screen("quiz_menu")

    def notes(self, component):
        self.screen_manager.show_screen("notes")
    
    def create_note(self, component):
        account = Account()

        DatabaseManager().query(
            "INSERT INTO notes (owner_username, title, content) VALUES (?, ?, ?)",
            (account.username, "New Note", "- This is a new note!\n- You can write your content here.\n- Test your knowledge by using the Blurting feature.")
        )

        get_note_id = DatabaseManager().query(
            "SELECT MAX(note_id) FROM notes WHERE owner_username = ?",
            (account.username,)
        )

        note_id = get_note_id[0][0]

        self.screen_manager.show_screen("notes", view_note_id=note_id)
        #new_component = Components(self.screen_manager, self.frame_manager)
        #new_component.default.message_box(message_box_type="info", message=f"Created a new note for the account '{account.username}'")

    def delete_note(self, component):
        account = Account()

        # Gets the note ID from the component ID
        note_id = component.component_id.split("_")[-1]

        note = DatabaseManager().query(
            "SELECT title, content FROM notes WHERE note_id = ? AND owner_username = ?",
            (note_id, account.username)
        )

        note_title = note[0][0]

        DatabaseManager().query(
            "DELETE FROM notes WHERE note_id = ? AND owner_username = ?",
            (note_id, account.username)
        )

        self.screen_manager.show_screen("notes")
        new_component = Components(self.screen_manager, self.frame_manager)
        new_component.default.message_box(message_box_type="info", message=f"Deleted the note '{note_title}' with the note ID '{note_id}'.")

    def view_note(self, component):
        account = Account()

        # Gets the note ID from the component ID
        note_id = component.component_id.split("_")[-1]

        note = DatabaseManager().query(
            "SELECT title, content FROM notes WHERE note_id = ? AND owner_username = ?",
            (note_id, account.username)
        )

        # Gets note info from db
        note_title = note[0][0]
        note_content = note[0][1]

        new_component = Components(self.screen_manager, self.frame_manager)
        #new_component.default.message_box(message_box_type="info", title=note[0][0], message=f"Title: {note_title}\nNote ID: {note_id}\n\n{note_content}")
        self.screen_manager.show_screen("notes", view_note_id=note_id)