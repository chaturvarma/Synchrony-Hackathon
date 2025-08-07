import customtkinter as ctk
import copy
import threading
from controller import get_command_output

# --- CustomTkinter GUI Application ---

ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")

class ChatShellApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CmdCraft")
        self.geometry("1200x750")

        self.colors = {
            "bg_light": "#eaf4f8", "sidebar": "#d9e7f0", "text_dark": "#1c1c1c",
            "text_light": "#f2f2f2", "brand": "#005f99", "user_bubble": "#a9d6e5",
            "chat_btn": "#a9d6e5", "chat_btn_hover": "#89c2d9", "chat_btn_active": "#468faf"
        }
        
        self.configure(bg=self.colors["bg_light"])
        self.chat_sessions = []
        self.current_chat_index = -1
        self.build_ui()

    def build_ui(self):
        self.chat_font = ctk.CTkFont(family="Segoe UI", size=15)
        self.response_font = ctk.CTkFont(family="Segoe UI", size=14)
        self.title_font = ctk.CTkFont(family="Segoe UI Semibold", size=30)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color=self.colors["sidebar"])
        self.sidebar.pack(side="left", fill="y")
        self.sidebar_title = ctk.CTkLabel(self.sidebar, text="CmdCraft", font=self.title_font, text_color=self.colors["brand"])
        self.sidebar_title.pack(pady=(20, 10), padx=10)
        self.new_chat_button = ctk.CTkButton(self.sidebar, text="➕ New Chat", command=self.start_new_chat, width=180)
        self.new_chat_button.pack(pady=(10, 20))
        self.chat_listbox = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", width=180, height=600)
        self.chat_listbox.pack(pady=(0, 10), padx=10, fill="y", expand=True)
        self.chat_buttons = []

        # Right frame
        self.right_frame = ctk.CTkFrame(self, fg_color=self.colors["bg_light"])
        self.right_frame.pack(side="left", fill="both", expand=True)
        self.chat_frame = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent")
        self.chat_frame.pack(pady=(10, 5), padx=20, fill="both", expand=True)
        self.inner_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        self.inner_frame.pack(fill="x", expand=True)

        self.prompt_entry = ctk.CTkEntry(
            self.right_frame, placeholder_text="Type your prompt here...", width=720, height=50,
            font=self.chat_font, corner_radius=999, border_width=1.5, border_color=self.colors["brand"] #type: ignore
        )
        self.prompt_entry.pack(pady=(10, 25), padx=30, side="bottom")
        self.prompt_entry.focus()
        self.prompt_entry.bind("<Return>", self.process_command_threaded)

        self.start_new_chat()

    def process_command_threaded(self, event=None):
        """Handles the user input in a separate thread to keep the UI responsive."""
        command = self.prompt_entry.get().strip()
        if not command:
            return

        self.display_message("You", command)
        self.chat_sessions[self.current_chat_index].append(("You", command))
        
        # MODIFIED: Only disable the entry. Do not delete text here.
        # The prompt will be fully reset after the response is received.
        self.prompt_entry.configure(state="disabled", placeholder_text="Processing...")

        # Run the API call in a new thread
        thread = threading.Thread(target=self.fetch_api_response, args=(command,))
        thread.start()

    def fetch_api_response(self, command):
        """Worker function that calls the API."""
        result = get_command_output(command)
        # Schedule the UI update back on the main thread
        self.after(0, self.update_ui_with_response, result)

    def update_ui_with_response(self, result):
        """Updates the GUI with the API response on the main thread."""
        self.display_message("CmdCraft", result.strip())
        self.chat_sessions[self.current_chat_index].append(("CmdCraft", result.strip()))
        
        # MODIFIED: Fully restore the prompt entry to its initial state here.
        self.prompt_entry.configure(
            state="normal",
            placeholder_text="Type your prompt here..."
        )
        self.prompt_entry.delete(0, "end") # Clear the previous command
        self.prompt_entry.focus()         # Set focus for the next command
        
        self.update_idletasks()
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    # --- Other UI Methods (Unchanged) ---
    def start_new_chat(self):
        if self.current_chat_index != -1:
            self.chat_sessions[self.current_chat_index] = copy.deepcopy(self.chat_sessions[self.current_chat_index])
        self.chat_sessions.append([])
        self.current_chat_index = len(self.chat_sessions) - 1
        self.add_chat_button(self.current_chat_index)
        self.load_chat(self.current_chat_index)

    def add_chat_button(self, index):
        btn = ctk.CTkButton(
            self.chat_listbox, text=f"Chat {index + 1}", width=160,
            fg_color=self.colors["chat_btn"], hover_color=self.colors["chat_btn_hover"],
            text_color=self.colors["text_dark"], command=lambda idx=index: self.load_chat(idx)
        )
        btn.pack(pady=5)
        self.chat_buttons.append(btn)

    def load_chat(self, index):
        self.current_chat_index = index
        for i, button in enumerate(self.chat_buttons):
            button.configure(fg_color=self.colors["chat_btn_active"] if i == index else self.colors["chat_btn"])
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        for sender, message in self.chat_sessions[index]:
            self.display_message(sender, message)

    def display_message(self, sender, message):
        if sender == "You":
            bubble_frame = ctk.CTkFrame(self.inner_frame, fg_color=self.colors["user_bubble"], corner_radius=999)
            label = ctk.CTkLabel(bubble_frame, text=message, font=self.chat_font, text_color=self.colors["text_dark"], justify="left", wraplength=600)
            label.pack(padx=15, pady=10)
            bubble_frame.pack(anchor="e", pady=8, padx=10)
        else:
            label = ctk.CTkLabel(self.inner_frame, text=message, font=self.response_font, text_color=self.colors["text_dark"], anchor="w", justify="left", wraplength=880, bg_color="transparent")
            label.pack(anchor="w", pady=(8, 6), padx=10)

if __name__ == "__main__":
    app = ChatShellApp()
    app.mainloop()