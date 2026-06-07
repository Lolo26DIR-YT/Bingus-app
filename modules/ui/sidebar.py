import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, categories, on_category_selected, on_target_selected, **kwargs):
        super().__init__(parent, fg_color="#131820", **kwargs)
        self.on_category_selected = on_category_selected
        self.on_target_selected = on_target_selected
        self.categories = categories
        self.active_category = None
        self.target_buttons = []

        self.columnconfigure(0, weight=1)

        header = ctk.CTkLabel(self, text="CATEGORIES", font=ctk.CTkFont(size=14, weight="bold"), text_color="#66fcf1")
        header.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.category_frame = ctk.CTkFrame(self, fg_color="#0b0f16")
        self.category_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.category_frame.columnconfigure(0, weight=1)

        self.category_buttons = {}
        for index, category in enumerate(categories):
            button = ctk.CTkButton(
                self.category_frame,
                text=category["label"],
                command=lambda c=category: self.select_category(c["key"]),
                fg_color="#1f2833",
                hover_color="#0b5f5f",
                text_color="#c5c6c7",
                anchor="w",
            )
            button.grid(row=index, column=0, sticky="ew", padx=8, pady=4)
            self.category_buttons[category["key"]] = button

        self.target_label = ctk.CTkLabel(self, text="CIBLES", font=ctk.CTkFont(size=14, weight="bold"), text_color="#66fcf1")
        self.target_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 6))

        self.target_scroll = ctk.CTkScrollableFrame(self, fg_color="#0b0f16")
        self.target_scroll.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.target_scroll.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

    def select_category(self, key):
        category = next((c for c in self.categories if c["key"] == key), None)
        if not category:
            return
        self.active_category = category
        self.on_category_selected(category)
        self._render_targets(category["targets"])
        for button_key, button in self.category_buttons.items():
            button.configure(fg_color="#1f2833" if button_key != key else "#45a29e")

    def _render_targets(self, targets):
        for widget in self.target_scroll.winfo_children():
            widget.destroy()
        self.target_buttons.clear()

        for index, target in enumerate(targets):
            button = ctk.CTkButton(
                self.target_scroll,
                text=f"{target['name']}",
                command=lambda t=target: self.on_target_selected(t),
                fg_color="#18212b",
                hover_color="#0b5f5f",
                text_color="#c5c6c7",
                anchor="w",
            )
            button.grid(row=index, column=0, sticky="ew", padx=8, pady=4)
            self.target_buttons.append(button)
