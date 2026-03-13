import customtkinter
import requests
from PIL import Image
from io import BytesIO


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x600")
        self.title("news searching app")
        customtkinter.set_appearance_mode("dark")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Введите запрос")
        self.entry.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

        self.search_button = customtkinter.CTkButton(
            self, command=self.search_click, text="Search"
        )
        self.search_button.grid(row=0, column=1, padx=20, pady=10)

        self.scroll_frames = customtkinter.CTkScrollableFrame(
            self, label_text="Results of search"
        )
        self.scroll_frames.grid(row=1, column=0, sticky="nsew", padx=20)
        self.scroll_frames.grid_columnconfigure(0, weight=1)

        self.scaling_slider = customtkinter.CTkSlider(
            self, from_=0.7, to=2.0, command=self.change_scaling
        )
        self.scaling_slider.grid(row=2, column=0, sticky="ew", pady=20)

        self.scaling_label = customtkinter.CTkLabel(self, text="Маштаб 100%")
        self.scaling_label.grid(row=2, column=1, padx=20)

    def change_scaling(self, n_scale: float):
        self.scaling_label.configure(text=f"Маштаб: {int(n_scale * 100)}%")
        customtkinter.set_widget_scaling(n_scale)
        customtkinter.set_window_scaling(n_scale)

    def search_click(self):
        for frame in self.scroll_frames.winfo_children():
            frame.destroy()

        input = self.entry.get()
        if not input:
            input = []

        url = f"""https://newsdata.io/api/1/latest?apikey=pub_b8d5bbba560c41cc82dd7505125a9db7&q={input}"""

        try:
            response = requests.get(url, timeout=5).json()
            news_data = response.get("results", [])
            for i, article in enumerate(news_data):
                title = article.get("title", "No title")

                btn = customtkinter.CTkButton(
                    self.scroll_frames,
                    border_width=1,
                    border_color="white",
                    fg_color="transparent",
                    anchor="w",
                    command=lambda i=i: self.news_details(news_data, i),
                    text=f"{title}",
                )
                btn.grid(row=i, column=0, pady=5, padx=5, sticky="ew")
        except:
            print("Error with loading data")

    def news_details(self, data, i):
        article = data[i]
        title = article.get("title", "No title")
        description = article.get("description", "No description")
        link = article.get("link", "No link")
        img_url = article.get("image_url", None)

        detailed_window = customtkinter.CTkToplevel(self)
        detailed_window.geometry("800x700")
        detailed_window.title("News details")

        detailed_window.resizable(False, False)

        main_scroll = customtkinter.CTkScrollableFrame(
            detailed_window, fg_color="transparent"
        )
        main_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        main_scroll.columnconfigure(0, weight=1)

        title_label = customtkinter.CTkLabel(
            main_scroll,
            text=title,
            font=("Arial", 20, "bold"),
            wraplength=700,
            justify="center",
        )
        title_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 20))

        details_text = customtkinter.CTkTextbox(
            main_scroll, wrap="word", font=("Arial", 14)
        )
        details_text.insert("0.0", text=f"{description}\n\nSource link:\n{link}")
        details_text.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        target_width = 750
        img = self.load_image(img_url, width=target_width)

        img_label = customtkinter.CTkLabel(main_scroll, text="")
        if img:
            img_label.configure(image=img)
        else:
            img_label.configure(text="[ Image not available ]", text_color="gray")

        img_label.grid(row=2, column=0, pady=(10, 30), padx=20)

    def load_image(self, url, width=None, height=None):
        if not url:
            return None

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            img_bytes = BytesIO(response.content)
            pil_img = Image.open(img_bytes)

            original_width, original_height = pil_img.size

            if width and not height:
                ratio = width / float(original_width)
                height = int(float(original_height) * float(ratio))
            elif height and not width:
                ratio = height / float(original_height)
                width = int(float(original_width) * float(ratio))
            elif not width and not height:
                width = original_width
                height = original_height

            pil_img_resized = pil_img.resize((width, height), Image.Resampling.LANCZOS)

            return customtkinter.CTkImage(
                light_image=pil_img_resized,
                dark_image=pil_img_resized,
                size=(width, height),
            )
        except Exception as e:
            print(f"Error loading image from {url}: {e}")
            return None


app = App()
app.mainloop()
