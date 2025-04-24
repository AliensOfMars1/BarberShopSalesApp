import customtkinter as ctk
from PIL import Image, ImageTk
import os


class SetupView(ctk.CTkFrame):
    def __init__(self, master, proceed_callback):
        super().__init__(master)
        self.configure(fg_color="#222222")
        self.proceed_callback = proceed_callback

        # Background image overlay
        bg_path = os.path.join(os.path.dirname(__file__), "setup_bg.png")
        if os.path.exists(bg_path):
            img = Image.open(bg_path)
            self.bg_image = ImageTk.PhotoImage(img)
            bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
  
        # Title inside rounded frame
        title_frame = ctk.CTkFrame(self, fg_color="#333333", corner_radius=0)
        title_frame.place(relx=0.5, rely=0.2, anchor="center")

        title_label = ctk.CTkLabel(
            title_frame,
            text="Enter Barber Names (comma separated)",
            text_color="white", fg_color="transparent"
        )
        title_label.pack(padx=12, pady=6)

        # Entry for barber names
        self.entry = ctk.CTkEntry(
            self,
            width=300, height=40,
            fg_color="#333333", text_color="white",
            placeholder_text="e.g., Mike, Alex, Sasha",
            placeholder_text_color="gray", corner_radius= 0
        )
        self.entry.place(relx=0.5, rely=0.4, anchor="center")


        # Proceed button
        self.proceed_btn = ctk.CTkButton(
            self, text="Proceed", command=self.on_proceed,
              width=150, height=40, corner_radius=0,
            font=ctk.CTkFont(size=16, weight="bold"),
              border_width=2, border_color="#555555"
        )
        self.proceed_btn.place(relx=0.5, rely=0.6, anchor="center")

    def on_proceed(self):
        import sys
        print("View.on_proceed invoked, proceed_callback is", self.proceed_callback, file=sys.stdout, flush=True)
        try:
            self.proceed_callback()
        except Exception as e:
            print("Error in proceed_callback:", e, file=sys.stdout, flush=True)

    def get_barber_name(self):
        return self.entry.get()




