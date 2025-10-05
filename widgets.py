import tkinter as tk

class ToggleSwitch(tk.Canvas):
    def __init__(self, parent, width=60, height=30, callback=None):
        super().__init__(parent, width=width, height=height, bg='white', highlightthickness=0)
        self.width = width
        self.height = height
        self.callback = callback
        self.state = False
        
        self.bg_off = "#cccccc"
        self.bg_on = "#4cd964"
        self.circle_color = "white"
        
        self.background = self.create_rectangle(0, 0, width, height, fill=self.bg_off, outline="", tags="bg")
        self.circle = self.create_oval(2, 2, height-2, height-2, fill=self.circle_color, outline="", tags="circle")
        
        self.bind("<Button-1>", self.toggle)
        self.bind("<Enter>", lambda e: self.config(cursor="hand2"))
        
    def toggle(self, event=None):
        self.state = not self.state
        self.animate()
        if self.callback:
            self.callback(self.state)
    
    def set_state(self, state):
        if self.state != state:
            self.state = state
            self.animate()
    
    def animate(self):
        if self.state:
            self.itemconfig("bg", fill=self.bg_on)
            target_x = self.width - self.height + 2
        else:
            self.itemconfig("bg", fill=self.bg_off)
            target_x = 2
        
        coords = self.coords(self.circle)
        current_x = coords[0]
        
        steps = 10
        dx = (target_x - current_x) / steps
        
        def move_step(step=0):
            if step < steps:
                self.move(self.circle, dx, 0)
                self.after(10, lambda: move_step(step + 1))
        
        move_step()
