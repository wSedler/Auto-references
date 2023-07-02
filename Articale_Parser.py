from string import ascii_lowercase, ascii_uppercase, digits, punctuation

#from PIL import Image

from tkinter import messagebox, END
import customtkinter as CTk
import parser


class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("460x370")
        self.title("Password generator")
        self.resizable(False, False)

        #self.logo = CTk.CTkImage(dark_image=Image.open("img.png"), size=(460, 150))
        #self.logo_label = CTk.CTkLabel(master=self, text="", image=self.logo)
        #self.logo_label.grid(row=0, column=0)

        self.password_frame = CTk.CTkFrame(master=self, fg_color="transparent")
        self.password_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.entry_text = CTk.CTkTextbox(master=self.password_frame, width=300, height=112)
        self.entry_text.grid(row=0, column=0, padx=(0, 20))

        self.btn_generate = CTk.CTkButton(master=self.password_frame, text="Add Source", width=100, command=self.add_sourse)
        self.btn_generate.grid(row=0, column=1)

        self.appearance_mode_option_menu = CTk.CTkOptionMenu(self,
                                                             values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=3, column=0, columnspan=4, pady=(10, 10))

        self.appearance_mode_option_menu.set("System")

    def change_appearance_mode_event(self, new_appearance_mode):
        CTk.set_appearance_mode(new_appearance_mode)

    def add_sourse(self):
        header_artical = self.entry_text.get('1.0', END)
        try:
            parser.add_sourse(header_artical=header_artical)
            messagebox.showinfo(title='info', message='Source added')
        except:
            messagebox.showerror(title='Error', message='Something went wrong')
        finally:
            self.entry_text.delete("0.0", END)


if __name__ == "__main__":
    app = App()
    app.mainloop()