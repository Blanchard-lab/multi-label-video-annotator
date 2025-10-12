from mlva_app import MLVAApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = MLVAApp(root)
    root.mainloop()
    
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
        
        tk.Button(dialog, text="Add", command=save, 
                 font=("Segoe UI", 11, "bold"),
                 bg=self.colors['success'],
                 fg='white',
                 width=15,
                 bd=0,
                 cursor='hand2',
                 relief='flat').pack(pady=15)
    
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
        
        tk.Button(dialog, text="Rename", command=save, 
                 font=("Segoe UI", 11, "bold"),
                 bg=self.colors['primary'],
                 fg='white',
                 width=15,
                 bd=0,
                 cursor='hand2',
                 relief='flat').pack(pady=15)
    
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
        for file in os.listdir(self.current_folder):
            if any(file.lower().endswith(ext) for ext in extensions):
                self.video_files.append(file)
        self.video_files.sort()
    
    def show_main_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.configure(bg='#1e1e1e')
        
        self.main_container = ttk.PanedWindow(self.root, orient="horizontal")
        self.main_container.pack(fill="both", expand=True)
        
        self.left_frame = tk.Frame(self.main_container, width=200, bg='#2d2d2d')
        self.main_container.add(self.left_frame, weight=0)
        
        header_frame = tk.Frame(self.left_frame, bg='#2d2d2d')
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(header_frame, text="Video Files", 
                font=("Segoe UI", 13, "bold"), 
                fg='white',
                bg='#2d2d2d').pack()
        
        listbox_frame = tk.Frame(self.left_frame, bg='#2d2d2d')
        listbox_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.files_listbox = tk.Listbox(listbox_frame, 
                                        yscrollcommand=scrollbar.set, 
                                        font=("Segoe UI", 10),
                                        bg='#1e1e1e',
                                        fg='white',
                                        selectbackground=self.colors['primary'],
                                        selectforeground='white',
                                        bd=0,
                                        highlightthickness=0)
        self.files_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        for video in self.video_files:
            self.files_listbox.insert(tk.END, video)
        
        self.files_listbox.bind("<<ListboxSelect>>", self.on_video_select)
        
        self.middle_frame = tk.Frame(self.main_container, bg='#1e1e1e')
        self.main_container.add(self.middle_frame, weight=1)
        
        self.video_label = tk.Label(self.middle_frame, text="Select a video to play", 
                                    background="black", foreground="white",
                                    font=("Segoe UI", 14))
        self.video_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        timeline_frame = tk.Frame(self.middle_frame, bg='#2d2d2d')
        timeline_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self.time_label = tk.Label(timeline_frame, text="00:00 / 00:00", 
                                   font=("Segoe UI", 9),
                                   fg='white', bg='#2d2d2d')
        self.time_label.pack(side="left", padx=5)
        
        self.timeline_var = tk.DoubleVar()
        self.timeline_scale = tk.Scale(timeline_frame, from_=0, to=100, 
                                       orient="horizontal",
                                       variable=self.timeline_var,
                                       showvalue=False,
                                       bg='#2d2d2d',
                                       fg='white',
                                       highlightthickness=0,
                                       troughcolor='#1e1e1e',
                                       activebackground=self.colors['primary'],
                                       command=self.on_seek)
        self.timeline_scale.pack(side="left", fill="x", expand=True, padx=5)
        
        controls_frame = tk.Frame(self.middle_frame, bg='#2d2d2d')
        controls_frame.pack(fill="x", pady=5)
        
        btn_style = {
            'font': ("Segoe UI", 10, "bold"),
            'bd': 0,
            'fg': 'white',
            'cursor': 'hand2',
            'relief': 'flat',
            'padx': 15,
            'pady': 8
        }
        
        self.play_button = tk.Button(controls_frame, text="Play", 
                                     bg=self.colors['success'],
                                     activebackground='#059669',
                                     command=self.toggle_play, **btn_style)
        self.play_button.pack(side="left", padx=5)
        
        volume_frame = tk.Frame(controls_frame, bg='#2d2d2d')
        volume_frame.pack(side="left", padx=15)
        
        tk.Label(volume_frame, text="Volume", font=("Segoe UI", 12),
                fg='white', bg='#2d2d2d').pack(side="left", padx=5)
        
        self.volume_var = tk.IntVar(value=self.volume)
        volume_scale = tk.Scale(volume_frame, from_=0, to=100, 
                               orient="horizontal",
                               variable=self.volume_var,
                               showvalue=True,
                               length=100,
                               bg='#2d2d2d',
                               fg='white',
                               highlightthickness=0,
                               troughcolor='#1e1e1e',
                               activebackground=self.colors['primary'],
                               command=self.on_volume_change)
        volume_scale.pack(side="left")
        
        tk.Button(controls_frame, text="Toggle Layout", 
                 bg=self.colors['primary'],
                 activebackground='#4f46e5',
                 command=self.toggle_layout, **btn_style).pack(side="left", padx=5)
        
        tk.Button(controls_frame, text="Home", 
                 bg='#64748b',
                 activebackground='#475569',
                 command=self.show_home_page, **btn_style).pack(side="right", padx=5)
        
        self.setup_labels_panel()
    
    def setup_labels_panel(self):
        if hasattr(self, 'labels_panel_container'):
            self.labels_panel_container.destroy()
        
        if self.panel_orientation == "right":
            self.labels_panel_container = tk.Frame(self.main_container, width=280, bg='#2d2d2d')
            self.main_container.add(self.labels_panel_container, weight=0)
        else:
            self.labels_panel_container = tk.Frame(self.root, bg='#2d2d2d')
            self.labels_panel_container.pack(side="bottom", fill="x", pady=5)
        
        header = tk.Frame(self.labels_panel_container, bg='#2d2d2d')
        header.pack(fill="x", pady=10)
        
        tk.Label(header, text="Labels", 
                font=("Segoe UI", 13, "bold"), 
                fg='white',
                bg='#2d2d2d').pack()
        
        if self.panel_orientation == "right":
            labels_scroll_frame = tk.Frame(self.labels_panel_container, bg='#2d2d2d')
            labels_scroll_frame.pack(fill="both", expand=True, padx=10)
            
            canvas = tk.Canvas(labels_scroll_frame, bg='#2d2d2d', highlightthickness=0)
            scrollbar = tk.Scrollbar(labels_scroll_frame, orient="vertical", command=canvas.yview)
            self.labels_inner_frame = tk.Frame(canvas, bg='#2d2d2d')
            
            self.labels_inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=self.labels_inner_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            self.labels_inner_frame = tk.Frame(self.labels_panel_container, bg='#2d2d2d')
            self.labels_inner_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.label_switches = {}
        
        for label in self.labels_config:
            if label not in self.label_states:
                self.label_states[label] = 0
            
            frame = tk.Frame(self.labels_inner_frame, bg='#3d3d3d', relief="flat")
            frame.pack(fill="x", pady=5, padx=5) if self.panel_orientation == "right" else frame.pack(side="left", padx=10, pady=5)
            
            inner_frame = tk.Frame(frame, bg='#3d3d3d')
            inner_frame.pack(padx=15, pady=12)
            
            label_text = tk.Label(inner_frame, text=label, 
                                 font=("Segoe UI", 11, "bold"), 
                                 fg='white',
                                 bg='#3d3d3d')
            label_text.pack(side="left" if self.panel_orientation == "right" else "top", pady=(0, 5) if self.panel_orientation == "bottom" else 0)
            
            switch = ToggleSwitch(inner_frame, width=50, height=26, 
                                 callback=lambda state, l=label: self.on_switch_toggle(l, state))
            switch.pack(side="right" if self.panel_orientation == "right" else "top", padx=(10, 0) if self.panel_orientation == "right" else 0)
            switch.set_state(bool(self.label_states[label]))
            
            self.label_switches[label] = switch
        
        save_btn = tk.Button(self.labels_panel_container, text="Save Annotations", 
                            command=self.save_annotations,
                            font=("Segoe UI", 11, "bold"),
                            bg=self.colors['secondary'],
                            activebackground='#7c3aed',
                            fg='white',
                            bd=0,
                            cursor='hand2',
                            relief='flat',
                            padx=20,
                            pady=10)
        save_btn.pack(pady=15, padx=10, fill="x")
    
    def on_switch_toggle(self, label, state):
        self.label_states[label] = 1 if state else 0
    
    def on_volume_change(self, value):
        self.volume = int(value)
        if self.audio_process and self.audio_process.poll() is None:
            self.restart_audio()
    
    def on_seek(self, value):
        if self.cap and not self.is_seeking:
            self.is_seeking = True
            frame_pos = int((float(value) / 100) * self.total_frames)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            self.show_frame()
            
            if self.audio_process and self.audio_process.poll() is None:
                self.audio_process.terminate()
                self.audio_process = None
            
            self.root.after(100, lambda: setattr(self, 'is_seeking', False))
    
    def update_timeline(self):
        if self.cap and self.cap.isOpened() and not self.is_seeking:
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            progress = (current_frame / self.total_frames) * 100 if self.total_frames > 0 else 0
            self.timeline_var.set(progress)
            
            current_time = current_frame / self.fps if self.fps > 0 else 0
            total_time = self.total_frames / self.fps if self.fps > 0 else 0
            
            current_str = time.strftime('%M:%S', time.gmtime(current_time))
            total_str = time.strftime('%M:%S', time.gmtime(total_time))
            self.time_label.config(text=f"{current_str} / {total_str}")
    
    def toggle_layout(self):
        self.panel_orientation = "bottom" if self.panel_orientation == "right" else "right"
        self.setup_labels_panel()
    
    def on_video_select(self, event):
        selection = self.files_listbox.curselection()
        if selection:
            self.stop_video()
            self.stop_audio()
            video_name = self.files_listbox.get(selection[0])
            self.current_video = os.path.join(self.current_folder, video_name)
            self.load_video()
            self.load_annotations()
    
    def load_video(self):
        if self.cap:
            self.cap.release()
        
        self.cap = cv2.VideoCapture(self.current_video)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.is_playing = False
        self.play_button.config(text="Play")
        self.timeline_var.set(0)
        self.show_frame()
        self.update_timeline()
    
    def load_annotations(self):
        json_path = os.path.splitext(self.current_video)[0] + ".json"
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
            except:
                self.reset_labels()
        else:
            self.reset_labels()
    
    def reset_labels(self):
        for label in self.labels_config:
            self.label_states[label] = 0
            if label in self.label_switches:
                self.label_switches[label].set_state(False)
    
    def show_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                label_width = self.video_label.winfo_width()
                label_height = self.video_label.winfo_height()
                
                if label_width > 1 and label_height > 1:
                    h, w = frame.shape[:2]
                    aspect = w / h
                    
                    if label_width / label_height > aspect:
                        new_height = label_height
                        new_width = int(aspect * new_height)
                    else:
                        new_width = label_width
                        new_height = int(new_width / aspect)
                    
                    frame = cv2.resize(frame, (new_width, new_height))
                
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk, text="")
    
    def toggle_play(self):
        if not self.cap:
            return
        
        self.is_playing = not self.is_playing
        self.play_button.config(text="Pause" if self.is_playing else "Play")
        
        if self.is_playing:
            self.start_audio()
            threading.Thread(target=self.play_video, daemon=True).start()
        else:
            self.stop_audio()
    
    def start_audio(self):
        if not self.current_video:
            return
        
        self.stop_audio()
        
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        start_time = current_frame / self.fps if self.fps > 0 else 0
        
        try:
            ffplay_path = shutil.which('ffplay')
            ffmpeg_path = shutil.which('ffmpeg')
            afplay_path = shutil.which('afplay')

            if sys.platform != 'darwin' and ffplay_path:
                if sys.platform == 'win32':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    self.audio_process = subprocess.Popen(
                        [ffplay_path, '-nodisp', '-autoexit', '-ss', str(start_time),
                         '-volume', str(self.volume), self.current_video],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        startupinfo=startupinfo
                    )
                else:
                    self.audio_process = subprocess.Popen(
                        [ffplay_path, '-nodisp', '-autoexit', '-ss', str(start_time),
                         '-volume', str(self.volume), self.current_video],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True
                    )
            elif sys.platform == 'darwin' and ffmpeg_path and afplay_path:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                tmp_path = tmp.name
                tmp.close()
                try:
                    cmd = [ffmpeg_path, '-hide_banner', '-loglevel', 'error',
                           '-ss', str(start_time), '-i', self.current_video,
                           '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2',
                           '-y', tmp_path]
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    self.audio_process = subprocess.Popen([afplay_path, tmp_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                    self._audio_tempfile = tmp_path
                except Exception:
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass
                    self._audio_tempfile = None
                    self.audio_process = None
            elif ffplay_path:
                self.audio_process = subprocess.Popen(
                    [ffplay_path, '-nodisp', '-autoexit', '-ss', str(start_time),
                     '-volume', str(self.volume), self.current_video],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
            else:
                self.audio_process = None
        except FileNotFoundError:
            pass
    
    def stop_audio(self):
        if self.audio_process and self.audio_process.poll() is None:
            try:
                self.audio_process.terminate()
            except Exception:
                try:
                    self.audio_process.kill()
                except Exception:
                    pass
            finally:
                self.audio_process = None
        if hasattr(self, '_audio_tempfile') and self._audio_tempfile:
            try:
                os.unlink(self._audio_tempfile)
            except Exception:
                pass
            finally:
                self._audio_tempfile = None
    
    def restart_audio(self):
        if self.is_playing:
            self.start_audio()
    
    def play_video(self):
        while self.is_playing and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                label_width = self.video_label.winfo_width()
                label_height = self.video_label.winfo_height()
                
                if label_width > 1 and label_height > 1:
                    h, w = frame.shape[:2]
                    aspect = w / h
                    
                    if label_width / label_height > aspect:
                        new_height = label_height
                        new_width = int(aspect * new_height)
                    else:
                        new_width = label_width
                        new_height = int(new_width / aspect)
                    
                    frame = cv2.resize(frame, (new_width, new_height))
                
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
                
                self.update_timeline()
                
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                time.sleep(1/fps if fps > 0 else 0.033)
            else:
                self.is_playing = False
                self.play_button.config(text="Play")
                self.stop_audio()
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.update_timeline()
                break
    
    def stop_video(self):
        self.is_playing = False
        self.stop_audio()
        if hasattr(self, 'play_button'):
            self.play_button.config(text="Play")
    
    def save_annotations(self):
        if not self.current_video:
            messagebox.showwarning("No Video", "Please select a video first.")
            return
        
        json_path = os.path.splitext(self.current_video)[0] + ".json"
        
        now = datetime.now()
        annotation_time = now.strftime("%H:%M:%S-%d/%m/%Y")
        
        data = {
            "MLVA_labels": {label: self.label_states.get(label, 0) for label in self.labels_config},
            "annotation_time": annotation_time
        }
        
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        messagebox.showinfo("Saved", f"Annotations saved to:\n{json_path}")
    
    def __del__(self):
        self.stop_audio()
        if self.cap:
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = MLVAApp(root)
    root.mainloop()