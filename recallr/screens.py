import customtkinter as tk
from recallr.frames import FrameManager, Frames
from recallr.components import Components
from recallr.objects import UserSettings, AppSettings, Account, Notes
from recallr.backend import DatabaseManager
from paginate import Page

def setup_screen(screen_type="menu"):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            # Call the decorated screen method
            func(self, *args, **kwargs)
        return wrapper
    return decorator

class ScreenManager(tk.CTkFrame):
    def __init__(self, window_manager, **kwargs):
        super().__init__(window_manager, **kwargs)

        # Sets up the screen
        self.configure(fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.window_manager = window_manager

        self.frames = []

    def create_frame(self, frame_name="centred"):
        frame_manager = FrameManager(self)

        frame = Frames(frame_manager)
        frame_manager.id = frame_name

        func = getattr(frame, frame_name, None)

        # Runs the code within the Frames class
        func()

        self.frames.append(frame_manager)
        return Components(self, frame_manager)
    
    def show_screen(self, function_name, **kwargs):
        # Clear any primary-button reference stored in the toplevel
        try:
            root = self.winfo_toplevel()
            if hasattr(root, '_primary_button'):
                try:
                    root._primary_button = None
                except Exception:
                    try:
                        delattr(root, '_primary_button')
                    except Exception:
                        pass
        except Exception:
            pass

        # Clears any content from the previous screen
        for frame in self.frames:
            frame.destroy()
        self.frames.clear() 
        
        frame_manager = FrameManager(self)

        screens = Screens(self.window_manager, frame_manager)
        # Checking to see if the function is apart of the Screens class
        func = getattr(screens, function_name, None)
        if callable(func):
            func(**kwargs)
        else:
            raise NameError(f"Function '{function_name}' is not a valid subroutine for the '{screens.__class__.__name__}' class.")

        print("-"*30)
        # If func is apart of the Screens class, loads the components
        for frame in self.frames:
            frame.load_components()

            print(f"🎞️ '{frame.id}' frame has been loaded.")
        
        print(f"🔲 '{function_name}' screen has been loaded.")

class Screens:
    def __init__(self, window_manager, frame_manager):
        self.window_manager = window_manager
        self.screen_manager = frame_manager.master
        self.frame_manager = frame_manager

    @setup_screen(screen_type="menu")
    def login(self):
        main = self.screen_manager.create_frame()
        main.default.title()
        main.default.content(text="Please fill in your login details!")
        main.default.entry_field(placeholder_text="Username")
        main.custom.password_entry_field()
        main.default.button(text="Login", button_type="primary")
        main.default.button(text="Create account", button_type="grey", component_id="create_account_menu")

    @setup_screen(screen_type="menu")
    def create_account(self):
        main = self.screen_manager.create_frame() 
        main.default.title(text="Create Account")
        main.default.content(text="Please fill in the following details!")
        main.default.entry_field(placeholder_text="What is your name?", component_id="display_name")
        main.default.entry_field(placeholder_text="New Username")
        main.custom.password_entry_field(placeholder_text="New Password")
        main.custom.password_entry_field(placeholder_text="Confirm Password")
        main.default.button(text="Create account", button_type="primary", button_style="green", component_id="make_the_account")
        main.default.button(text="Cancel", button_type="red", component_id="cancel_create_account")

    @setup_screen(screen_type="menu")
    def main_menu(self):
        account = Account()

        main = self.screen_manager.create_frame()
        main.default.title()
        main.default.content(text=f"Hello, {account.display_name}!")
        main.default.button(text="Notes")
        main.default.button(text="Test yourself", component_id="quiz_menu")
        main.default.button(text="Settings", button_type="grey", component_id="settings_pane")
        main.custom.sign_out_button()

    @setup_screen(screen_type="menu")
    def settings(self, view_setting_id=None, **kwargs):
        user_settings = UserSettings()
        main = self.screen_manager.create_frame()

        # Checks if a setting is being viewed
        if view_setting_id == None:
            main.default.title()
            main.default.content(text="Select a setting from the sidebar!")

        else:
            setting_id = view_setting_id
            main.custom.view_setting_properties(setting_id=setting_id)

        # Checks if a setting is being viewed
        selected_setting_id = view_setting_id

        sidebar = self.screen_manager.create_frame("sidebar")
        for setting in user_settings.list:
            setting_values = next(iter(setting.values()))
            setting_id = next(iter(setting.keys()))

            # If the button is selected, then it greys it out
            button_state = "normal"
            if setting_id == selected_setting_id:
                button_state = "disabled"

            if setting_values['settingsType'] != "buttons":
                content_preview = f"'{user_settings.get_current_setting_value(setting_id)}'"
            else:
                content_preview = setting_values["description"]

            sidebar.custom.sidebar_button(component_id=f"setting_{setting_id}", title=setting_values['name'], content=content_preview, command="view_setting", state=button_state, **kwargs)
        sidebar.custom.main_menu_button(button_type="default")

    @setup_screen(screen_type="menu")
    def quiz_menu(self, **kwargs):
        main = self.screen_manager.create_frame()
        main.default.title(text="Quiz Menu")
        main.default.content(text="Please pick which mode you would like to do!")
        main.default.button(text="Flashcards")
        main.default.button(text="Multiple choice", component_id="coming_soon")
        main.default.button(text="Blurting")
        main.custom.main_menu_button()

    @setup_screen(screen_type="menu")
    def notes(self, **kwargs):
        view_note_id = kwargs.get("view_note_id", None)
        main = self.screen_manager.create_frame()

        # Checks if a note is being viewed
        if view_note_id == None:
            main.default.title()
            main.default.content(text="Select a note from the sidebar!")
            main.custom.main_menu_button()
        else:
            note_taking = self.screen_manager.create_frame("note_taking")
            note_taking.custom.view_note_textbox(note_id=int(view_note_id))

        sidebar = self.screen_manager.create_frame("sidebar")
        all_notes = Notes().get_note_ids()

        # Checks if a note is being viewed
        selected_note_id = None
        if view_note_id != None:
            selected_note_id = int(view_note_id)

        for note in all_notes:
            note_id = note

            # If the button is selected, then it greys it out
            button_state = "normal"
            if note_id == selected_note_id:
                button_state = "disabled"

            sidebar.custom.view_note_button(note_id=note_id, component_id=f"view_note_{note_id}", state=button_state)
        sidebar.default.button(text="Create note")

    @setup_screen(screen_type="menu")
    def flashcards_menu_setup(self, **kwargs):
        main = self.screen_manager.create_frame()
        main.default.title(text="Flashcards")

        # The settings with their options
        flashcard_config = [
            {"title": "What should be visible?", "options": ["Title", "Content"]},
            {"title": "What order should flashcards be in?", "options": ["Chronological order", "Randomised"]},
        ]

        # The options that have been chosen, this uses the same index position as 'flashcard_config'
        # Checks to see if either is an attribute of ScreenManager, if not then its likely this screen has only just been loaded
        try:
            self.screen_manager.selected_options
        except AttributeError:
            self.screen_manager.selected_options = ["Title", "Chronological order"]
        try:
            self.screen_manager.selected_notes
        except AttributeError:
            self.screen_manager.selected_notes = []

        # Displays the components
        index = 0
        for setting in flashcard_config:
            main.default.content(text=f"{index+1}) {setting['title']}")

            for button_name in setting["options"]:
                if button_name == self.screen_manager.selected_options[index]:
                    button_state = "disabled"
                else:
                    button_state = "normal"
                main.default.button(text=button_name, component_id=f"flashcards_config_{index}_{button_name}", command="edit_flashcards_config",button_style="default", padding=False, state=button_state)

            index += 1

        main.default.content(text="When you are ready, click the start button below!")
        main.default.button(text="Start", component_id="start_flashcards_game", button_type="primary", button_style="green", padding=False)
        

    @setup_screen(screen_type="menu")
    def blurting_menu_selection(self, page_number=1, **kwargs):
        # Checks to see if selected_notes is an attribute, if not then its likely this screen has only just been loaded
        try:
            self.screen_manager.selected_notes
        except AttributeError:
            self.screen_manager.selected_notes = []
        try:
            self.screen_manager.current_note_index
        except AttributeError:
            self.screen_manager.current_note_index = 0

        main = self.screen_manager.create_frame()
        main.default.title(text="Blurting")
        main.default.content(text="Please which notes you would like to blurt today!")

        # Gets the ntoes
        notes = Notes().get_notes()
        items_per_page = 10

        # Creates pagination
        page = Page(
            notes,
            page=page_number,
            items_per_page=items_per_page,
            item_count=len(notes)
        )

        # Displays the page
        for item in page:
            title = item['title']
            title_preview = Notes().make_preview(title, max_chars=50)
            note_id = int(item['id'])

            # Checks if the note has already been selected
            selected = False
            if note_id in self.screen_manager.selected_notes:
                selected = True
            
            main.default.check_box(text=title_preview, component_id = f"note_{item['id']}",padding=False, selected=selected)
        # Adds placeholders if there were less items than in the max 'items_per_page'
        remaining = max(0, min(items_per_page, items_per_page - len(page)))
        for i in range(remaining):
            main.default.check_box(text=" ", disabled=True, padding=False)

        # Checks the next and previous page numbers, to see if it needs to disabled any of the buttons
        next_button_state = tk.NORMAL
        if page.next_page == None:
            next_button_state = tk.DISABLED
        previous_button_state = tk.NORMAL
        if page.previous_page == None:
            previous_button_state = tk.DISABLED

        
        main.default.button(f"Page {page.page} / {page.page_count}", button_type="grey", state=tk.DISABLED)
        # Component IDs either end with the next/previous page, or "None"
        main.custom.change_page_blurting_button(
            text="Next page",
            page=page.next_page,
            button_state=next_button_state,
            selected_notes=self.screen_manager.selected_notes
        )
        main.custom.change_page_blurting_button(
            text="Previous page",
            page=page.previous_page,
            button_state=previous_button_state,
            selected_notes=self.screen_manager.selected_notes
        )

        main.default.button(text="Start blurting!", component_id="select_blurting_notes", button_type="primary", button_style="green")
        main.custom.main_menu_button() 
    
    def blurting_game(self, blurting_notes=[], current_note_index=0, step="waiting", **kwargs):
        main = self.screen_manager.create_frame()
        notes_obj = Notes()
        note = notes_obj.get_notes(note_ids=[blurting_notes[current_note_index]])[0]

        title = notes_obj.make_preview(note['title'], max_chars=30)
        main.default.title(f"Blurt: {title}")
        main.default.content(text=f"Note: {blurting_notes.index(note['id'])+1}/{len(blurting_notes)}")

        # This section changes based on what 'step' you are on
        # waiting: Waiting to start the next timer
        # blurting: Countdown timer where you are blurting
        # times_up / reveal_note: Finished blurting the note, ready to go to the next one

        if step == "waiting":
            main.default.content(text="When you are ready, press the green button below to begin!")
            main.default.button(text="Start timer", component_id="start_blurting_timer", button_type="primary", button_style="green")
        elif step == "blurting":
            user_settings = UserSettings()
            time_limit = user_settings.get_current_setting_value("blurtingRecallNotesTimeLimit")
            main.custom.start_countdown(seconds=int(time_limit))
        elif step == "times_up":
            main.default.title(text="Time's up!")
            main.default.content(text="When you are ready, click the green button below to reveal your note.")
            main.custom.reveal_blurting_note_button()
        elif step == "reveal_note":
            textbox = main.default.text_box(component_id="blurting_content_textbox")
            textbox.insert("0.0", note['content'])
            textbox.configure(state=tk.DISABLED)

            if current_note_index+1 < len(blurting_notes):
                main.default.button(text="Next note", component_id="next_blurting_note", button_type="primary")
            else:
                main.default.button(text="Finish blurting", component_id="go_back_to_blurting_selection_noconfirm", command="go_back_to_blurting_selection", button_type="primary")
                return

        main.default.button(text="Exit", component_id="go_back_to_blurting_selection", button_type="red")