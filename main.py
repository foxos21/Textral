from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, TextArea, Tree, Footer, ProgressBar
from textual.widgets.text_area import TextAreaTheme
from textual.binding import Binding
from textual import events, work
from textual.theme import Theme
from time import time, sleep
from rich.style import Style
from pathlib import Path
import threading
import datetime
import random
import sys
import os


version = 1.8
autosave = False
expand_tree = False
hide_root_tree = True
double_click_to_open = False
show_progressbar = True
leaf_color = "green"
folder_color = "blue"
opened_file = ""
file_to_open_path = None
saved_file = True
isTreeHidden = False
syntax_language = "Textral"
temp_len = 0

root_dir = os.getcwd()

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
        sleep(0.5)          


def update_infobar(self):
    # w = "[white]|[/white]"
    w = "[grey]|[/grey]"
    if saved_file:
        is_saved = "[#19ff56]⦿[/#19ff56]"
    else:
        is_saved = "[#ff1952]⦿[/#ff1952]"
    
    length = f"[#7d19ff]l:{len(self.codeEditor.text)}[/#7d19ff]"
    
    if syntax_language == "":
        syntax = f"[grey]N/A[/grey]"
    else:
        syntax = f"[orange]{syntax_language}[/orange]"
    
    time = datetime.datetime.now()
    time = [time.strftime("%I"), time.strftime("%M")]
    
    # 🕑⌚
    render = f"{w} {os.path.basename(opened_file)} {w} ⌚ {time[0]}:{time[1]} {w} {length} {w} {syntax} {w} {is_saved} {w}"
    self.infoBar.content = render
    self.infoBarLeft.content = f"{w}[pink] {eastercat} [/pink]{w}"


def get_language(self, path):
    file_name = os.path.basename(path)
    file_name_extension = os.path.splitext(file_name)
    file_name_extension = file_name_extension[-1].replace(" ", "")
    # self.notify(message=f"gotlang: {file_name_extension}")
    return syntax_languages.get(file_name_extension, "")


class ExtraCodeEditor(TextArea):
    def _on_key(self, event: events.Key) -> None:
        if event.character == "(":
            self.insert("()")
            self.move_cursor_relative(columns=-1)
            event.prevent_default()
            
        if event.character == "{":
            self.insert("{}")
            self.move_cursor_relative(columns=-1)
            event.prevent_default()
            
        if event.character == "[":
            self.insert("[]")
            self.move_cursor_relative(columns=-1)
            event.prevent_default()
        
        if event.character == '"':
            self.insert('""')
            self.move_cursor_relative(columns=-1)
            event.prevent_default()
            
        if event.character == "'":
            self.insert("''")
            self.move_cursor_relative(columns=-1)
            event.prevent_default()


class Textral(App):
    CSS_PATH = "style.tcss"
    BINDINGS = [
        Binding(key="ctrl+s", action="Save Opened File", description="Save", key_display="▼"),
        Binding(key="ctrl+r", action="Refresh File Tree", description="Refresh", key_display="⟳"),
        Binding(key="ctrl+t", action="show/hide File Tree", description="Hide", key_display="|<")
    ]
    

    def compose(self) -> ComposeResult:
        yield Footer()
        
        with Vertical(id="main_layout"):
            with Horizontal(id="top_row"):
                self.fileExplorer = Tree(rf"{root_dir}")
                self.fileExplorer.root.expand()
                if hide_root_tree:
                    self.fileExplorer.show_root = False
                yield self.fileExplorer

                self.codeEditor = ExtraCodeEditor.code_editor(welcome_message, language="python", theme="css")
                #self.codeEditor = TextArea.code_editor(welcome_message, language="python")
                yield self.codeEditor

            self.fileTreeProgressBar = ProgressBar(classes="fileExplorerHidden")
            yield self.fileTreeProgressBar
            
            with Horizontal(id="infoBarGroup"):
                self.infoBarLeft = Static("EasterEgg", classes="infoBarLeft")
                self.infoBar = Static(dummy_infobar, classes="infoBar")
                yield self.infoBarLeft
                yield self.infoBar


    def on_mount(self) -> None:
        global temp_len, opened_file, syntax_language, saved_file
        
        self.fileExplorer.classes = "fileExplorer"
        self.fileExplorer.border_title = "File Tree"
        
        self.codeEditor.classes = "codeEditor"
        self.codeEditor.border_title = "Code Editor"
        
        self.refresh_file_tree()
        
        temp_len = len(self.codeEditor.text)
        
        infoBarClock = threading.Thread(target=info_bar_clock, args=(self,), daemon=True)
        infoBarClock.start()
        
        self.register_theme(Textral_DARK)
        self.register_theme(Textral_LIGHT)
        self.theme = "textral-dark"
        
        if file_to_open_path != None:
            try:
                with open(file_to_open_path, "r") as f:
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
        if event.key == "ctrl+q" or event.key == "ctrl+s":
            self.save_code_editor()
        if event.key == "ctrl+r":
            self.refresh_file_tree()
        if event.key == "ctrl+t":
            self.toggle_file_tree()
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_click_time = 0
        self.last_node = None


    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        self.on_double_click(event)
        if double_click_to_open:
            current_time = time()
            if current_time - self.last_click_time < 0.5 and event.node == self.last_node:
                self.on_double_click(event)
            
            self.last_click_time = current_time
            self.last_node = event.node


    def on_double_click(self, event: Tree.NodeSelected) -> None:
        global opened_file, syntax_language, saved_file, temp_len
        
        # self.notify(f"Double-clicked: {event.node.label} => {event.node.data}")
        
        if opened_file == "" or not autosave and not os.path.isdir(event.node.data):
            opened_file = event.node.data
        elif not os.path.isdir(event.node.data):
            self.save_code_editor()
            opened_file = event.node.data
        
        try:
            with open(event.node.data, "r") as f: # Load file to CodeEditor
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


    def add_to_tree(self, root, directory):
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
    
       
    def save_code_editor(self) -> None:
        global opened_file, saved_file, temp_len
        
        file_name = os.path.basename(opened_file)
        # self.notify(message = opened_file)
        try:
            if opened_file != "" and self.codeEditor.text != "" and not os.path.isdir(opened_file):
                with open(opened_file, "w") as f:
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