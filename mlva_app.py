import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from datetime import datetime
import subprocess
import sys
from widgets import ToggleSwitch


class MLVAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MultiLabel Video Annotator")
        self.root.geometry("1200x700")
        self.colors = {
            'primary': '#6366f1',
            'secondary': '#8b5cf6',
            'success': '#10b981',
            'background': '#f8fafc',
            'card': '#ffffff',
            'text': '#1e293b',
            'text_light': '#64748b',
            'border': '#e2e8f0'
        }
        self.root.configure(bg=self.colors['background'])
        self.labels_config = ["Confused", "Frustrated", "Optimistic", "Conflicted", "Curious", "Disengaged", "Surprised"]
        self.current_folder = None
        self.video_files = []
        self.current_video = None
        self.label_states = {}
        self.panel_orientation = "right"
        self.volume = 50
        self.show_home_page()

    def make_button(self, parent, text, command, width=15, font=("Segoe UI", 11, "bold")):
        """Create a consistently styled button: white bg, black text, hover raise, light-blue active."""
        btn = tk.Button(parent, text=text, command=command, width=width, font=font,
                        bg='white', fg='black', activebackground='#e6f7ff', bd=1, relief='flat', cursor='hand2')
        def on_enter(e):
            btn.config(bg='#f7f7f7', relief='raised')

        def on_leave(e):
            btn.config(bg='white', relief='flat')
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn

    def show_home_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        home_frame = tk.Frame(self.root, bg=self.colors['background'])
        home_frame.pack(expand=True, fill="both")
        content_frame = tk.Frame(home_frame, bg=self.colors['background'])
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        title = tk.Label(content_frame, text="MultiLabel Video Annotator",
                         font=("Segoe UI", 36, "bold"),
                         fg=self.colors['primary'],
                         bg=self.colors['background'])
        title.pack(pady=(0, 10))
        subtitle = tk.Label(content_frame, text="Annotate videos with custom labels",
                            font=("Segoe UI", 14),
                            fg=self.colors['text_light'],
                            bg=self.colors['background'])
        subtitle.pack(pady=(0, 40))
        card_frame = tk.Frame(content_frame, bg=self.colors['card'], relief="flat", bd=0)
        card_frame.pack(pady=20, padx=40)
        self.add_shadow(card_frame)
        card_inner = tk.Frame(card_frame, bg=self.colors['card'])
        card_inner.pack(padx=40, pady=30)
        tk.Label(card_inner, text="Configure Labels",
                 font=("Segoe UI", 18, "bold"),
                 fg=self.colors['text'],
                 bg=self.colors['card']).pack(pady=(0, 20))
        labels_container = tk.Frame(card_inner, bg=self.colors['card'])
        labels_container.pack(pady=10)
        list_frame = tk.Frame(labels_container, bg=self.colors['card'])
        list_frame.pack(side="left", padx=(0, 20))

        self.labels_listbox = tk.Listbox(list_frame, height=6, width=25,
                                         font=("Segoe UI", 12),
                                         bg="white",
                                         fg=self.colors['text'],
                                         selectbackground=self.colors['primary'],
                                         selectforeground="white",
                                         relief="solid",
                                         bd=1,
                                         highlightthickness=0)
        self.labels_listbox.pack(side="left", padx=5)

        scrollbar = tk.Scrollbar(list_frame, command=self.labels_listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.labels_listbox.config(yscrollcommand=scrollbar.set)

        for label in self.labels_config:
            self.labels_listbox.insert(tk.END, label)

        buttons_frame = tk.Frame(labels_container, bg=self.colors['card'])
        buttons_frame.pack(side="left")

        add_btn = self.make_button(buttons_frame, text="Add Label", command=self.add_label)
        add_btn.pack(pady=5, fill="x")

        rename_btn = self.make_button(buttons_frame, text="Rename Label", command=self.rename_label)
        rename_btn.pack(pady=5, fill="x")

        remove_btn = self.make_button(buttons_frame, text="Remove Label", command=self.remove_label)
        remove_btn.pack(pady=5, fill="x")

        open_btn = self.make_button(content_frame, text="Open Folder", command=self.open_folder, width=20,
                                    font=("Segoe UI", 16, "bold"))
        open_btn.config(height=2)
        open_btn.pack(pady=30)

    def add_shadow(self, widget):
        widget.config(highlightbackground=self.colors['border'], highlightthickness=1)

    def add_label(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Label")
        dialog.geometry("350x150")
        dialog.configure(bg=self.colors['background'])
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Label Name:",
                 font=("Segoe UI", 12),
                 bg=self.colors['background'],
                 fg=self.colors['text']).pack(pady=15)

        entry = tk.Entry(dialog, width=30, font=("Segoe UI", 11), relief="solid", bd=1)
        entry.pack(pady=5, ipady=5)
        entry.focus()

        def save():
            name = entry.get().strip()
            if name and name not in self.labels_config:
                self.labels_config.append(name)
                self.labels_listbox.insert(tk.END, name)
                dialog.destroy()

        entry.bind("<Return>", lambda e: save())
        self.make_button(dialog, text="Add", command=save, width=15).pack(pady=15)

    def rename_label(self):
        selection = self.labels_listbox.curselection()
        if not selection:
            return

        idx = selection[0]
        old_name = self.labels_config[idx]

        dialog = tk.Toplevel(self.root)
        dialog.title("Rename Label")
        dialog.geometry("350x150")
        dialog.configure(bg=self.colors['background'])
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="New Label Name:",
                 font=("Segoe UI", 12),
                 bg=self.colors['background'],
                 fg=self.colors['text']).pack(pady=15)

        entry = tk.Entry(dialog, width=30, font=("Segoe UI", 11), relief="solid", bd=1)
        entry.insert(0, old_name)
        entry.pack(pady=5, ipady=5)
        entry.focus()
        entry.select_range(0, tk.END)

        def save():
            name = entry.get().strip()
            if name and name not in self.labels_config:
                self.labels_config[idx] = name
                self.labels_listbox.delete(idx)
                self.labels_listbox.insert(idx, name)
                dialog.destroy()

        entry.bind("<Return>", lambda e: save())
        self.make_button(dialog, text="Rename", command=save, width=15).pack(pady=15)

    def remove_label(self):
        selection = self.labels_listbox.curselection()
        if selection:
            idx = selection[0]
            self.labels_config.pop(idx)
            self.labels_listbox.delete(idx)

    def open_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.current_folder = folder
            self.scan_video_files()
            if self.video_files:
                self.show_main_interface()
            else:
                messagebox.showinfo("No Videos", "No video files found in the selected folder.")

    def scan_video_files(self):
        extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
        self.video_files = []
        try:
            for file in os.listdir(self.current_folder):
                if any(file.lower().endswith(ext) for ext in extensions):
                    self.video_files.append(file)
        except Exception:
            self.video_files = []
        self.video_files.sort()

    def show_main_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg='#f0f4f8')

        self.main_container = ttk.PanedWindow(self.root, orient="horizontal")
        self.main_container.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.main_container, width=240, bg='#ffffff')
        self.main_container.add(self.left_frame, weight=0)

        header_frame = tk.Frame(self.left_frame, bg='#ffffff')
        header_frame.pack(fill="x", pady=10)

        tk.Label(header_frame, text="Video Files",
                 font=("Segoe UI", 13, "bold"),
                 fg='black',
                 bg='#ffffff').pack()

        listbox_frame = tk.Frame(self.left_frame, bg='#ffffff')
        listbox_frame.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")

        self.files_listbox = tk.Listbox(listbox_frame,
                                        yscrollcommand=scrollbar.set,
                                        font=("Segoe UI", 10),
                                        bg='white',
                                        fg='black',
                                        selectbackground='#e6f7ff',
                                        selectforeground='black',
                                        bd=0,
                                        highlightthickness=0)
        self.files_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.files_listbox.yview)

        for video in self.video_files:
            self.files_listbox.insert(tk.END, video)

        self.files_listbox.bind("<<ListboxSelect>>", self.on_video_select)

        self.middle_frame = tk.Frame(self.main_container, bg='#ffffff')
        self.main_container.add(self.middle_frame, weight=1)

        info_frame = tk.Frame(self.middle_frame, bg='white')
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.selected_label = tk.Label(info_frame, text="No video selected", font=("Segoe UI", 14, "bold"), bg='white', fg='black')
        self.selected_label.pack(pady=(30, 10))

        self.selected_path = tk.Label(info_frame, text="", font=("Segoe UI", 10), bg='white', fg='black')
        self.selected_path.pack()

        controls_frame = tk.Frame(self.middle_frame, bg='#ffffff')
        controls_frame.pack(fill="x", pady=5)

        self.make_button(controls_frame, text="Toggle Layout", command=self.toggle_layout).pack(side="left", padx=5)
        self.make_button(controls_frame, text="Home", command=self.show_home_page).pack(side="right", padx=5)
        self.setup_labels_panel()

    def setup_labels_panel(self):
        if hasattr(self, 'labels_panel_container') and self.labels_panel_container:
            try:
                self.main_container.forget(self.labels_panel_container)
            except Exception:
                pass
            try:
                self.labels_panel_container.destroy()
            except Exception:
                pass

        if self.panel_orientation == "right":
            self.labels_panel_container = tk.Frame(self.main_container, width=280, bg='#ffffff')
            self.main_container.add(self.labels_panel_container, weight=0)
        else:
            self.labels_panel_container = tk.Frame(self.root, bg='#ffffff')
            self.labels_panel_container.pack(side="bottom", fill="x", pady=5)

        header = tk.Frame(self.labels_panel_container, bg='#ffffff')
        header.pack(fill="x", pady=10)

        tk.Label(header, text="Labels",
                 font=("Segoe UI", 13, "bold"),
                 fg='black',
                 bg='#ffffff').pack()

        if self.panel_orientation == "right":
            labels_scroll_frame = tk.Frame(self.labels_panel_container, bg='#ffffff')
            labels_scroll_frame.pack(fill="both", expand=True, padx=10)

            canvas = tk.Canvas(labels_scroll_frame, bg='#ffffff', highlightthickness=0)
            scrollbar = tk.Scrollbar(labels_scroll_frame, orient="vertical", command=canvas.yview)
            self.labels_inner_frame = tk.Frame(canvas, bg='#ffffff')

            self.labels_inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=self.labels_inner_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            self.labels_inner_frame = tk.Frame(self.labels_panel_container, bg='#ffffff')
            self.labels_inner_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.label_switches = {}

        for label in self.labels_config:
            if label not in self.label_states:
                self.label_states[label] = 0

            frame = tk.Frame(self.labels_inner_frame, bg='#f7f9fb', relief="flat")
            if self.panel_orientation == "right":
                frame.pack(fill="x", pady=5, padx=5)
            else:
                frame.pack(side="left", padx=10, pady=5)

            inner_frame = tk.Frame(frame, bg='#f7f9fb')
            inner_frame.pack(padx=15, pady=12)

            label_text = tk.Label(inner_frame, text=label,
                                 font=("Segoe UI", 11, "bold"),
                                 fg='black',
                                 bg='#f7f9fb')
            if self.panel_orientation == "right":
                label_text.pack(side="left")
            else:
                label_text.pack()

            switch = ToggleSwitch(inner_frame, width=50, height=26,
                                 callback=lambda state, l=label: self.on_switch_toggle(l, state))
            if self.panel_orientation == "right":
                switch.pack(side="right", padx=(10, 0))
            else:
                switch.pack()
            switch.set_state(bool(self.label_states[label]))

            self.label_switches[label] = switch

        save_btn = self.make_button(self.labels_panel_container, text="Save Annotations", command=self.save_annotations, width=20)
        save_btn.config(padx=20, pady=10)
        save_btn.pack(pady=15, padx=10, fill="x")

    def on_switch_toggle(self, label, state):
        self.label_states[label] = 1 if state else 0

    def on_volume_change(self, value):
        self.volume = int(value)

    def on_seek(self, value):
        pass

    def update_timeline(self):
        pass

    def toggle_layout(self):
        self.panel_orientation = "bottom" if self.panel_orientation == "right" else "right"
        self.setup_labels_panel()

    def on_video_select(self, event):
        selection = self.files_listbox.curselection()
        if selection:
            video_name = self.files_listbox.get(selection[0])
            self.current_video = os.path.join(self.current_folder, video_name)
            self.update_selected_display()
            self.load_annotations()
            try:
                if sys.platform == 'darwin':
                    subprocess.Popen(['open', self.current_video])
                elif os.name == 'nt':
                    os.startfile(self.current_video)
                else:
                    subprocess.Popen(['xdg-open', self.current_video])
            except Exception:
                pass

    def load_annotations(self):
        if not self.current_video:
            return
        json_path = os.path.splitext(self.current_video)[0] + "_mlva.json"
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    labels = data.get('MLVA_labels', {})
                    for label in self.labels_config:
                        state = labels.get(label, 0)
                        self.label_states[label] = state
                        if label in self.label_switches:
                            self.label_switches[label].set_state(bool(state))
            except Exception:
                self.reset_labels()
        else:
            self.reset_labels()

    def reset_labels(self):
        for label in self.labels_config:
            self.label_states[label] = 0
            if label in self.label_switches:
                self.label_switches[label].set_state(False)

    def show_frame(self):
        pass

    def toggle_play(self):
        pass

    def start_audio(self):
        pass

    def stop_audio(self):
        pass

    def restart_audio(self):
        pass

    def play_video(self):
        pass

    def stop_video(self):
        pass

    def save_annotations(self):
        if not self.current_video:
            messagebox.showwarning("No Video", "Please select a video first.")
            return
        json_path = os.path.splitext(self.current_video)[0] + "_mlva.json"
        now = datetime.now()
        annotation_time = now.strftime("%H:%M:%S-%d/%m/%Y")
        labels_present = {label: 1 for label, state in self.label_states.items() if state}
        data = {
            "MLVA_labels": labels_present,
            "annotation_time": annotation_time
        }
        try:
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Saved", f"Annotations saved to:\n{json_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save annotations:\n{e}")

    def __del__(self):
        pass

    def update_selected_display(self):
        if self.current_video:
            name = os.path.basename(self.current_video)
            self.selected_label.config(text=name)
            self.selected_path.config(text=os.path.splitext(self.current_video)[0] + "_mlva.json")
        else:
            self.selected_label.config(text="No video selected")
            self.selected_path.config(text="")
