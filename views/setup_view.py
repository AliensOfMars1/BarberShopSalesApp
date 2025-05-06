import customtkinter as ctk
from PIL import Image
import os
from customtkinter import CTkImage

class SetupView(ctk.CTkFrame):
    def __init__(self, master, proceed_callback):
        super().__init__(master)
        self.proceed_callback = proceed_callback
        self.configure(fg_color="#222222")

        # ───── Left: full‑height image covers 60% width ─────
        img_frame = ctk.CTkFrame(self, fg_color="transparent")
        img_frame.place(relx=0, rely=0, relwidth=0.6, relheight=1)
        img_frame.pack_propagate(False)

        bg_path = os.path.join(os.path.dirname(__file__), "view_images", "login_bg.png")
        if os.path.exists(bg_path):
            pil_img = Image.open(bg_path)
            self.left_img = CTkImage(pil_img, size=(400, 800))
            lbl = ctk.CTkLabel(img_frame, image=self.left_img, text="")
            lbl.place(relx=0.5, rely=0.5, anchor="center")

            def resize(evt):
                w, h = evt.width, evt.height
                self.left_img = CTkImage(pil_img, size=(w, h))
                lbl.configure(image=self.left_img)
            img_frame.bind("<Configure>", resize)

        # ───── Right: form in remaining 40% ─────
        form = ctk.CTkFrame(self, fg_color="transparent")
        form = ctk.CTkFrame(self, fg_color="#334A6E", corner_radius=0)
        form.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)
        form.lift()

        # Barber names
        ctk.CTkLabel(
            form,
            text="Enter Barber Names\n(comma-separated)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",
            justify="left"
        ).pack(anchor="w", pady=(60,20), padx=20)

        self.entry = ctk.CTkEntry(
            form,
            placeholder_text="e.g., Mike, Alex, Sasha",
            fg_color="#333333", text_color="white",
            width=240, corner_radius=8
        )
        self.entry.pack(anchor="w", pady=(0,30), padx=20)

        # Proceed button
        self.proceed_btn = ctk.CTkButton(
            form,
            text="Proceed",
            command=self.on_proceed,
            width=150, height=40,
            corner_radius=8,
            fg_color="#4CAF50", hover_color="#45a049",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.proceed_btn.pack(anchor="w", padx=40)

    def on_proceed(self):
        names = [n.strip() for n in self.entry.get().split(",") if n.strip()]
        if not names:
            ctk.messagebox.showerror(
                "Error",
                "Please enter at least one barber name.",
                parent=self
            )
            return
        self.proceed_callback(names)

    def get_barber_name(self):
        return self.entry.get()