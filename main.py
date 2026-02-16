from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Static, TextArea, Tree, Footer, ProgressBar, Switch, Select
from textual.widgets.text_area import TextAreaTheme
from textual.screen import Screen
from textual.binding import Binding
from textual import events, work
from textual.theme import Theme
from time import time, sleep
from rich.style import Style
from pathlib import Path
from textual import on
import threading
import datetime
import random
import shutil
import json
import sys
import os


version = 1.9
autosave = False
hide_footer = False
expand_tree = False
hide_root_tree = True
safety_backup_s = True
default_theme = "textral-dark"
double_click_to_open = True
show_progressbar = True
leaf_color = "green"
folder_color = "blue"
opened_file = ""
file_to_open_path = None
saved_file = True
isTreeHidden = False
settings_open = False
syntax_language = "Textral"
temp_len = 0

root_dir = os.getcwd()

if os.path.exists("./.settings.json"):
    try:
        with open("./.settings.json", "r") as f:
            settings = json.load(f)
    except Exception as e:
        print(f"[.settings.json] is damaged or incorrect:\n[[{e}]]")
        exit(0)
       
    autosave = settings["autosave"]
    hide_footer = settings["hide_footer"]
    double_click_to_open = settings["double_click_to_open"]
    hide_root_tree = settings["hide_root_tree"]
    safety_backup_s = settings["safety_file_backup_s"]
    default_theme = settings["default_theme"]
else:
    with open("./.settings.json", "w") as f:
        json.dump({
            "autosave": False,
            "hide_footer": False,
            "double_click_to_open": True,
            "hide_root_tree": True,
            "safety_file_backup_s": True,
            "default_theme": "textral-dark"
        }, f, indent=4)
        

# WINDOWS THREAD! : python -m nuitka --onefile --output-filename=Textral --windows-icon-from-ico=development.ico --include-package=textual --include-package=tree_sitter_python --include-package=tree_sitter --include-package=pygments --include-package=rich --include-data-file=style.tcss=./ main.py
#SAFE : pyinstaller --clean -y --onefile -n Textral --icon=development.ico --collect-all textual --collect-all tree_sitter_css --collect-all tree_sitter_bash --collect-all tree_sitter_go --collect-all tree_sitter_html --collect-all tree_sitter_java --collect-all tree_sitter_javascript --collect-all tree_sitter_json --collect-all tree_sitter_markdown --collect-all tree_sitter_regex --collect-all tree_sitter_rust --collect-all tree_sitter_sql --collect-all tree_sitter_toml --collect-all tree_sitter_xml --collect-all tree_sitter_yaml --collect-all tree_sitter_python --collect-all tree_sitter --collect-all pygments --collect-all rich --add-data=style.tcss:. main.py
# pip install "textual[syntax]"
# pip install textual
# pip install tree-sitter-python

syntax_languages = {
  ".py": "python",
  ".md": "markdown",
  ".json": "json",
  ".toml": "toml",
  ".yaml": "yaml",
  ".yml": "yaml",
  ".html": "html",
  ".htm": "html",
  ".xml": "xml",
  ".css": "css",
  ".js": "javascript",
  ".mjs": "javascript",
  ".cjs": "javascript",
  ".rs": "rust",
  ".go": "go",
  ".sql": "sql",
  ".java": "java",
  ".sh": "bash",
  ".bash": "bash",
  # Experimental languages mapped to closest supported syntax
  ".lua": "javascript",
  ".c": "java",
  ".h": "java",
  ".cpp": "java",
  ".cc": "java",
  ".cxx": "java",
  ".hpp": "java",
  ".vb": "java",
  ".vbs": "java",
  ".r": "python",
  ".pl": "bash",
  ".pm": "bash",
  ".f": "rust",
  ".for": "rust",
  ".f90": "rust",
  ".php": "javascript",
  ".sb": "javascript",
  ".sb2": "javascript",
  ".sb3": "javascript",
  ".adb": "java",
  ".ads": "java",
  ".m": "python",
  ".asm": "bash",
  ".s": "bash",
  ".tcss": "css",
  ".bat": "bash",
  ".vbs1": "java",
  ".ps1": "bash",
  ".spec": "yaml",
  ".cmd": "bash",
  ".cfg": "toml",
  ".ini": "toml",
  ".properties": "toml",
  ".gitconfig": "toml"
}


Textral_DARK = Theme(
    name="textral-dark",
    primary="#6339f9",
    secondary="#ff66c4",
    accent="#ff66c4",
    foreground="#e0e0e0",
    background="#161625",
    surface="#1a1a2e",
    panel="#252545",
    boost="#3b3b75",
)

Textral_LIGHT = Theme(
    name="textral-light",
    primary="#6339f9",
    secondary="#ff66c4",
    accent="#6339f9",
    foreground="#1a1a2e",
    background="#ffffff",
    surface="#fdfdfd",
    panel="#f0f0f5",
    boost="#e6e6f2",
)

GITHUB_DARK = Theme(
    name="github-dark",
    primary="#2f81f7",    # GitHub Blue
    secondary="#30363d",  # Muted border/gray
    accent="#2ea043",     # Success Green
    foreground="#c9d1d9", # Main text
    background="#0d1117", # Deep dark background
    surface="#161b22",    # Slightly lighter surface
    panel="#161b22",      # Secondary containers
    boost="#21262d",      # Hover/Highlight states
)

GITHUB_LIGHT = Theme(
    name="github-light",
    primary="#0969da",    # GitHub Link Blue
    secondary="#afb8c1",  # Muted gray
    accent="#1a7f37",     # GitHub Green
    foreground="#1f2328", # Deep gray/black text
    background="#ffffff", # Pure white
    surface="#f6f8fa",    # Light gray surface
    panel="#f6f8fa",      # Secondary containers
    boost="#ebeff2",      # Hover/Highlight states
)

HARLEQUIN = Theme(
    name="harlequin", 
    primary="#e6ff88", # The vibrant yellow used for "Run Query" and SQL keywords
    secondary="#52ffcc", # The mint/aqua used for the selected row (Hamilton)
    accent="#70e2e2", # The soft blue/cyan used for 'f1', 'Help', and 'avg' functions
    foreground="#f8f8f2", # Off-white/yellowish text color
    background="#080808", # True black background from the IDE
    surface="#121212", # The slightly lighter gray-black used for the sidebar/panels
    panel="#262626", # Used for borders and inactive tabs
    boost="#1c1c1c", # The highlight color for the current line in the editor
)

themes_list = [
    "textral-dark",
    "textral-light",
    "github-dark",
    "github-light",
    "harlequin",
    "nord",
    "gruvbox",
    "catppuccin-mocha",
    "dracula",
    "tokyo-night",
    "monokai",
    "flexoki",
    "catppuccin-latte",
    "solarized-dark",
    "rose-pine",
    "rose-pine-moon",
    "rose-pine-dawn",
    "atom-one-dark",
    "atom-one-light",
    "textual-dark",
    "textual-light"
]

eastercats = [
    "=^..^=",
    "=^･ω･^=",
    "=^._.^=",
    "=^. .^=",
    "=^･ω･^=",
    "=^･ｪ･^=",
    "=^･ω･^",
    "=^ ^=",
    "=^･ω･^=",
    "=♡ω♡=",
    "=ＴェＴ=",
    # "=ↀωↀ=",
    # "=✧ω✧=",
    "(=^･ﻌ･^=)",
    "=^･ﻌ･^=",
    "=^･ﻌ･^=",
    "≧◔◡◔≦﻿",
    "=^◔ω◔^=",
    "◔ω◔",
    "{◔ω◔}",
    "(=◔ω◔=)",
    "=oωo=",
    "=OωO=",
    "=TωT=",
    "=IωI=",
    "\\(OwO)",
    "(OwO)/",
    "{◔ω◔}/",
    "\\{◔ω◔}",
    "\\{◔ω◔}/",
    "◔ω◔/",
    "\\◔ω◔",
    "\\◔ω◔/",
    ",,UwU,,",
    ".UwU.",
    ".^uwu^.",
    "/^uwu^\\",
    "/^UwU^\\",
    "/◔ω◔\\"
]
eastercat = random.choice(eastercats)
dummy_infobar = "[white]|[white] 03:09 [white]|[white] [green]Python[green] [white]|[white] [purple]len: 10[purple] [white]|[white] [red]UNSAVED[red] [white]|[white] [pink]\\(OwO)[pink] [white]|[white]"


welcome_message = f'''
___________              __                .__   
\__    ___/___ ___  ____/  |_____________  |  |  
  |    |_/ __ \\  \/  /\   __\_  __ \__   \ |  |  
  |    |\  ___/ >    <  |  |  |  |\/ / __ \|  |__
  |____| \___  >__/\_ \ |__|  |__|  (____  /____/
             \/      \/                  \/      
- Version: {version}

* HELP
- To refresh [File Tree]: ctrl + R
- To save file from [Code Editor]: ctrl + S
- To hide [File Tree]: ctrl + T
- To open [Settings]: ctrl + U
- To open [Palette]: ctrl + P


* OH NO!
- You've lost your file/s and your progress
  because of an accident or a bug!
- Then No worries! there is [Safety Backup] Enabled by default
  all your progress should be backed up in "./.temp/backup" ;)
'''
 

def info_bar_clock(self):
    while True:
        global temp_len
        codeEditorLen = len(self.codeEditor.text)
        if codeEditorLen > temp_len or codeEditorLen < temp_len:
            global saved_file
            saved_file = False
            temp_len = codeEditorLen
        else:
            temp_len = codeEditorLen
        
        update_infobar(self)
        self.fileExplorer.show_root = not hide_root_tree
        classd = "fileExplorerHidden" if hide_footer == True else "Footer"
        for footer in self.query(Footer):
            footer.classes = classd
        sleep(0.5)


def update_infobar(self):
    # w = "[white]|[/white]"
    w = "[grey]∣[/grey]"
    if saved_file:
        is_saved = "[#19ff56]⦿[/#19ff56]"
    else:
        is_saved = "[#ff1952]⦿[/#ff1952]"
    
    length = f"[#7d19ff]l:{len(self.codeEditor.text)}[/#7d19ff]"
    
    if syntax_language == "":
        syntax = f"[grey]N/A[/grey]"
    else:
        syntax = f"[orange]{syntax_language}[/orange]"
    
    time_now = datetime.datetime.now()
    time_split = [time_now.strftime("%I"), time_now.strftime("%M")]
    
    # 🕑⌚ ◄─hello─►
    render = f"[grey]❮[/grey] {os.path.basename(opened_file)} {w} ⌚ {time_split[0]}:{time_split[1]} {w} {length} {w} {syntax} {w} {is_saved} [grey]❯[/grey]"
    self.infoBar.content = render
    self.infoBarLeft.content = f"[grey]❮[/grey][pink] {eastercat} [/pink][grey]❯[/grey]"


def get_language(self, path):
    file_name = os.path.basename(path)
    file_name_extension = os.path.splitext(file_name)
    file_name_extension = file_name_extension[-1].replace(" ", "")
    # self.notify(message=f"gotlang: {file_name_extension}")
    return syntax_languages.get(file_name_extension, "")
    
    
def do_a_safety_backup(path):
    if safety_backup_s == True:
        # check if folders exist
        folders = ["./.temp", "./.temp/backup"]
        for folder in folders:
            if os.path.exists(folder) == False:
                os.mkdir(folder)
        
        path = Path(path)
        if os.path.isdir(path) == False:
            time_now = datetime.datetime.now()
            time_now = f"[{time_now.day}-{time_now.month}-{time_now.year}  {(time_now.hour - 12)}-{time_now.minute}]"
            shutil.copyfile(path, f"./.temp/backup/{os.path.splitext(os.path.basename(path))[0]} {time_now}{os.path.splitext(os.path.basename(path))[-1]}")
    return


def save_settings(target, value):
    with open("./.settings.json", "r") as f:
        data = json.load(f)
    data[target] = value
    with open("./.settings.json", "w") as f:
        json.dump(data, f, indent=4)


class ExtraCodeEditor(TextArea):
    def _on_key(self, event: events.Key) -> None:
        match event.character:
            case "(":
                self.insert("()")
                self.move_cursor_relative(columns=-1)
                event.prevent_default()
            
            case "{":
                self.insert("{}")
                self.move_cursor_relative(columns=-1)
                event.prevent_default()
                
            case "[":
                self.insert("[]")
                self.move_cursor_relative(columns=-1)
                event.prevent_default()
            
            case '"':
                self.insert('""')
                self.move_cursor_relative(columns=-1)
                event.prevent_default()
                
            case "'":
                self.insert("''")
                self.move_cursor_relative(columns=-1)
                event.prevent_default()


class Settings(Screen):
    BINDINGS = [
        Binding(key="escape", action="close", description="Close", key_display="-")
    ]
    
    
    def action_close(self) -> None:
        global settings_open
        settings_open = False
        app.pop_screen()
        
    
    def compose(self) -> ComposeResult:
        self.settingsBody = VerticalScroll(id="settings")
        with self.settingsBody:
            with Vertical(classes="category", id="general"):
                with Horizontal(classes="switch"):
                    yield Static(f"AutoSave:", classes="label")
                    yield Switch(animate=False, value=autosave, id="autosave")
            
                with Horizontal(classes="switch"):
                    yield Static(f"Hide Footer:", classes="label")
                    yield Switch(animate=False, value=hide_footer, id="hide_footer")
                    
                with Horizontal(classes="switch"):
                    yield Static(f"Default Theme:", classes="label")
                    yield Select((line, line) for line in themes_list)

            # with Horizontal(classes="switch"):
                # yield Static(f"Cursor Style:", classes="label")
                # yield Select.from_values(("Bar |", "Block █", "Underline _"), classes="selectCursor")
            
            with Vertical(classes="category", id="filetree"):
                with Horizontal(classes="switch"):
                    yield Static(f"Hide Root Tree: ", classes="label")
                    yield Switch(animate=False, value=hide_root_tree, id="hide_root_tree")

                with Horizontal(classes="switch"):
                    yield Static(f"Double click:", classes="label")
                    yield Switch(animate=False, value=double_click_to_open, id="double_click_to_open")
            
            with Vertical(classes="category", id="safetybackup"):
                with Horizontal(classes="switch"):
                    yield Static(f"Safety File Backup:", classes="label")
                    yield Switch(animate=False, value=safety_backup_s, id="safety_file_backup")
            
        yield Footer(classes="Footer")

    
    @on(Select.Changed) 
    def select_changed(self, event: Select.Changed) -> None:
        if event.value == Select.BLANK:
            return
        
        global default_theme 
        default_theme = event.value
        self.app.theme = event.value
        save_settings("default_theme", event.value)


    def on_switch_changed(self, event: Switch.Changed) -> None:
        change = True if event.value == True else False
        match event.control.id:
            case "hide_footer":
                global hide_footer
                hide_footer = change
                classd = "fileExplorerHidden" if hide_footer == True else "Footer"
                for footer in self.query(Footer):
                    footer.classes = classd
                save_settings("hide_footer", change)
                    
            case "safety_file_backup":
                global safety_backup_s
                safety_backup_s = change
                save_settings("safety_file_backup_s", change)

            case "double_click_to_open":
                global double_click_to_open
                double_click_to_open = change
                save_settings("double_click_to_open", change)
                
            case "hide_root_tree":
                global hide_root_tree
                hide_root_tree = change
                save_settings("hide_root_tree", change)
                
            case "autosave":
                global autosave
                autosave = change
                save_settings("autosave", change)
  
    
    def on_mount(self) -> None:
        self.settingsBody.border_title = "Settings"
        
        classd = "fileExplorerHidden" if hide_footer == True else "Footer"
        for footer in self.query(Footer):
            footer.classes = classd
            
        self.query_one(Select).value = default_theme
        
        for vertical in self.query(Vertical):
            match vertical.id:
                case "general":
                    vertical.border_title = "General"
                case "filetree":
                    vertical.border_title = "File Tree"
                case "safetybackup":
                    vertical.border_title = "NOT RECOMMENDED"
    

class Textral(App):
    CSS_PATH = "style.tcss"
    SCREENS = {"settings": Settings}
    BINDINGS = [
        Binding(key="ctrl+s", action="Save Opened File", description="Save", key_display="▼"),
        Binding(key="ctrl+r", action="Refresh File Tree", description="Refresh", key_display="⟳"),
        Binding(key="ctrl+t", action="show/hide File Tree", description="Hide", key_display="|<"),
        Binding(key="ctrl+u", action="open_settings", description="Settings", key_display="*")
    ]
    
    
    def action_open_settings(self) -> None:
        global settings_open
        if settings_open == False:
            settings_open = True
            app.push_screen('settings')
    

    def compose(self) -> ComposeResult:
        # Dont like this SyntaxTheme
        AYU_DARK_BG = "#0B0E14"      # Deep, ink-black
        AYU_DARK_FG = "#B3B1AD"      # Soft grey foreground
        AYU_KEYWORD = "#FF8F40"     # Vibrant orange
        AYU_STRING = "#A6CC70"      # Earthy green
        AYU_FUNCTION = "#FFB454"    # Golden yellow
        AYU_COMMENT = "#5C6773"     # Steel grey
        AYU_OPERATOR = "#F29668"    # Salmon/Orange
        AYU_NUMBER = "#D2A6FF"      # Light violet
        AYU_MARKUP = "#39BAE6"      # Bright cyan

        ayu_dark = TextAreaTheme(
            name="ayu-dark",
            base_style=Style(color=AYU_DARK_FG, bgcolor=AYU_DARK_BG),
            cursor_style=Style(color=AYU_DARK_BG, bgcolor="#E6B450"),
            cursor_line_style=Style(bgcolor="#151A1E"),
            selection_style=Style(bgcolor="#253340"),
            # syntax_styles={
                # "keyword": Style(color=AYU_KEYWORD, bold=True),
                # "string": Style(color=AYU_STRING),
                # "comment": Style(color=AYU_COMMENT, italic=True),
                # "operator": Style(color=AYU_OPERATOR),
                # "function": Style(color=AYU_FUNCTION),
                # "number": Style(color=AYU_NUMBER),
                # "type": Style(color=AYU_MARKUP),
                # "parameter": Style(color="#D5FF80"),
                # "method": Style(color=AYU_FUNCTION),
                # "boolean": Style(color=AYU_KEYWORD),
            # },
        )
        
        with Vertical(id="main_layout"):
            with Horizontal(id="top_row"):
                self.fileExplorer = Tree(rf"{root_dir}")
                self.fileExplorer.root.expand()
                if hide_root_tree:
                    self.fileExplorer.show_root = False
                yield self.fileExplorer

                self.codeEditor = ExtraCodeEditor.code_editor(welcome_message, language="python", theme="css")
                # self.codeEditor.register_theme(ayu_dark)
                yield self.codeEditor

            self.fileTreeProgressBar = ProgressBar(classes="fileExplorerHidden")
            yield self.fileTreeProgressBar
            
            with Horizontal(id="infoBarGroup"):
                self.infoBarLeft = Static("EasterEgg", classes="infoBarLeft")
                self.infoBar = Static(dummy_infobar, classes="infoBar")
                yield self.infoBarLeft
                yield self.infoBar
        
        yield Footer(classes="fileExplorerHidden")

    def on_mount(self) -> None:
        global temp_len, opened_file, syntax_language, saved_file
        
        self.fileExplorer.classes = "fileExplorer"
        self.fileExplorer.border_title = "File Tree"
        
        self.codeEditor.classes = "codeEditor"
        self.codeEditor.border_title = "Code Editor"
        # self.codeEditor.theme = "ayu-dark"
        
        self.refresh_file_tree()
        
        temp_len = len(self.codeEditor.text)
        
        infoBarClock = threading.Thread(target=info_bar_clock, args=(self,), daemon=True)
        infoBarClock.start()
        
        self.register_theme(Textral_DARK)
        self.register_theme(Textral_LIGHT)
        self.register_theme(GITHUB_DARK)
        self.register_theme(GITHUB_LIGHT)
        self.register_theme(HARLEQUIN)
        self.theme = default_theme
        
        classd = "fileExplorerHidden" if hide_footer == True else "Footer"
        for footer in self.query(Footer):
            footer.classes = classd
        
        if file_to_open_path != None:
            do_a_safety_backup(file_to_open_path)
            try:
                with open(file_to_open_path, "r", encoding="utf-8") as f:
                    self.codeEditor.text = f.read()
                    syntax_language = get_language(self, file_to_open_path)
                    self.codeEditor.language = syntax_language
                    temp_len = len(self.codeEditor.text)
                    opened_file = file_to_open_path
            except PermissionError:
                pass
            except Exception as e:
                opened_file = ""
                self.notify(message=f"File could not be read! \n\n [[{e}]]", title="Code Editor", severity='error', timeout=3)
                
            saved_file = True
            update_infobar(self)
        
    
    def on_key(self, event: events.Key) -> None:
        match event.key:
            case "ctrl+q" | "ctrl+s":
                self.save_code_editor()
            case "ctrl+r":
                self.refresh_file_tree()
            case "ctrl+t":
                self.toggle_file_tree()
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_click_time = 0
        self.last_node = None


    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        if event.node.data == None:
            return
            
        if double_click_to_open:
            if os.path.isdir(event.node.data) == True:
                self.on_double_click(event)
                return
            
            current_time = time()
            if current_time - self.last_click_time < 0.5 and event.node == self.last_node:
                self.on_double_click(event)
            
            self.last_click_time = current_time
            self.last_node = event.node
        else:
            self.on_double_click(event)


    def on_double_click(self, event: Tree.NodeSelected) -> None:
        global opened_file, syntax_language, saved_file, temp_len
        
        # self.notify(f"Double-clicked: {event.node.label} => {event.node.data}")
        
        if opened_file == "" or not autosave and not os.path.isdir(event.node.data):
            opened_file = event.node.data
        elif not os.path.isdir(event.node.data):
            self.save_code_editor()
            opened_file = event.node.data
        
        try:
            # Backup the file that will be opened
            do_a_safety_backup(event.node.data)
            # Open
            with open(event.node.data, "r", encoding="utf-8") as f: # Load file to CodeEditor
                self.codeEditor.text = f.read()
                syntax_language = get_language(self, event.node.data)
                self.codeEditor.language = syntax_language
                temp_len = len(self.codeEditor.text)
        except PermissionError:
            if os.path.isdir(event.node.data) and event.node.is_expanded:
                self.refresh_file_tree(treeNodeRoot=event.node, source_dir=event.node.data)
            else:
                pass # maybe raise PermissionError
        except Exception as e:
            opened_file = ""
            self.notify(message=f"File could not be read! \n\n [[{e}]]", title="Code Editor", severity='error', timeout=3)
            
        saved_file = True
        update_infobar(self)


    def add_to_tree(self, root, directory) -> None:
        try:
            entries = os.listdir(directory)
        except PermissionError:
            pass
        except OSError:
            pass

        folders = []
        files = []

        for entry in entries:
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                folders.append((entry, full_path))
            else:
                files.append((entry, full_path))

        # Setup Progress Bar
        if show_progressbar:
            self.call_from_thread(self.fileTreeProgressBar.update, total=len(entries))
            self.fileTreeProgressBar.classes = "fileTreeProgressBar" # Note: classes is usually safe, but call_from_thread is safer

        # 1. Add all files
        for file, full_path in sorted(files):
            # We wrap the widget-modifying methods
            self.call_from_thread(root.add_leaf, f"[{leaf_color}]{file}[/{leaf_color}]", data=full_path)
            if show_progressbar:
                self.call_from_thread(self.fileTreeProgressBar.advance, 1)

        # 2. Add all folders
        for folder, full_path in sorted(folders):
            new_folder = self.call_from_thread(
                root.add, 
                f"[{folder_color}]{folder}[/{folder_color}]", 
                expand=expand_tree, 
                data=full_path
            )
            # Recursively call within the same thread
            # self.add_to_tree(new_folder, full_path)
            if show_progressbar:
                self.call_from_thread(self.fileTreeProgressBar.advance, 1)


    # Inside your Class
    @work(exclusive=True, thread=True)
    def refresh_file_tree(self, source_dir=None, treeNodeRoot=None) -> None:
        if not treeNodeRoot:
            self.notify(title="File Tree", message="Refreshing ⟳", severity='information', timeout=2)
        
        root = self.fileExplorer.root
        # UI updates from a thread must use call_from_thread
        if not source_dir:
            self.call_from_thread(root.remove_children)
        
        # Start the recursive addition
        if not source_dir:
            self.add_to_tree(root=root, directory=root_dir)
        else:
            treeNodeRoot.remove_children()
            self.add_to_tree(root=treeNodeRoot, directory=source_dir)

        if show_progressbar:
            self.fileTreeProgressBar.classes = "fileExplorerHidden"
        
        return
    
       
    def save_code_editor(self) -> None:
        global opened_file, saved_file, temp_len
        
        file_name = os.path.basename(opened_file)
        # self.notify(message = opened_file)
        try:
            if opened_file != "" and self.codeEditor.text != "" and not os.path.isdir(opened_file):
                ### Backup the file opened
                do_a_safety_backup(opened_file)
                
                with open(opened_file, "w", encoding="utf-8") as f:
                    f.write(self.codeEditor.text)
                self.notify(title="Code Editor", message=f"Saved to {file_name}", severity='information', timeout=2)
                
                temp_len = len(self.codeEditor.text)
                saved_file = True
                update_infobar(self)
            else:
                self.notify(title="Code Editor", message="Cannot save", severity='warning', timeout=2)
        except Exception as e:
                    self.notify(title="Code Editor", message=f"Failed to save to file {file_name}!\n\n[[{e}]]", severity='error', timeout=3)
        sleep(0.1)
        
        
    def toggle_file_tree(self) -> None:
        global isTreeHidden
        
        root = self.fileExplorer
        if not isTreeHidden:
            root.classes = "fileExplorerHidden"
            isTreeHidden = True
        else:
            root.classes = "fileExplorer"
            isTreeHidden = False


 
if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_to_open_path=sys.argv[1]
    app = Textral()
    app.run()