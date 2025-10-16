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

        # Checks if the button's method is wtihin the CommandHandler class
        func = getattr(command_handler, button.component_id, None)
        try:
            func(button)
        except TypeError:
            print(f"❌ The button '{button.component_id}' has no associated action")

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

    def button(self, text="Button", button_type="default", button_style=None, component_id=None, **kwargs):
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
            text=text,
            font=("Arial", 16),
            width=200, height=40,
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

    def password_entry_field(self, placeholder_text="Password", **kwargs):
        component = Components(self.screen_manager, self.frame_manager)

        component.default.entry_field(placeholder_text=placeholder_text, show="*")

    def main_menu_button(self, **kwargs):
        component = Components(self.screen_manager, self.frame_manager)

        component.default.button(text="Main menu", button_type="grey")
    
    def sign_out_button(self, **kwargs):
        component = Components(self.screen_manager, self.frame_manager)

        component.default.button(text="Sign out", button_type="red")

class ComponentCommandHandler:
    def __init__(self, screen_manager, frame_manager):
        self.screen_maanger = screen_manager
        self.frame_manager = frame_manager
    
    def login(self, component):
        new_component = Components(self.screen_maanger, self.frame_manager)

        username = self.frame_manager.find_component("username").get()
        password = self.frame_manager.find_component("password").get()

        account = Account()
        result = account.login(username, password)

        if result["sucess"]:
            # Sucessful login
            self.screen_maanger.show_screen("main_menu")
        else:
            # Failed login
            new_component.default.message_box(message_box_type="warning", message=result["message"])    

    def create_account_menu(self, component):
        self.screen_maanger.show_screen("create_account")

    def make_the_account(self, component):
        new_component = Components(self.screen_maanger, self.frame_manager)

        display_name = self.frame_manager.find_component("display_name").get()
        new_username = self.frame_manager.find_component("new_username").get()
        new_password = self.frame_manager.find_component("new_password").get()
        confirm_password = self.frame_manager.find_component("confirm_password").get()

        account = Account()
        result = account.create_account(display_name, new_username, new_password, confirm_password)

        if result["sucess"]:
            # Sucessfully created an account
            self.screen_maanger.show_screen("login")
            new_component.default.message_box(message_box_type="info", message=result["message"]) 
        else:
            # Failed to create an account
            new_component.default.message_box(message_box_type="warning", message=result["message"])    

    def cancel_create_account(self, component):
        self.screen_maanger.show_screen("login")

    def sign_out(self, component):
        account = Account()
        account.sign_out()

        self.screen_maanger.show_screen("login")

        new_component = Components(self.screen_maanger, self.frame_manager)
        new_component.default.message_box(message_box_type="info", message="Successfully signed out")

    def coming_soon(self, component):
        self.screen_maanger.show_screen("coming_soon")

    def main_menu(self, component):
        self.screen_maanger.show_screen("main_menu")
    
    def quiz_menu(self, component):
        self.screen_maanger.show_screen("quiz_menu")

    def notes(self, component):
        self.screen_maanger.show_screen("notes")