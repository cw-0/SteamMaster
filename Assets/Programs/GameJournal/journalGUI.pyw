import math
from howlongtobeatpy import HowLongToBeat
import re
from pathlib import Path
import tkinter as tk
from tkinter import ttk, RAISED, SUNKEN, messagebox
from PIL import ImageTk, Image
from configparser import ConfigParser

config = ConfigParser(interpolation=None)

p = Path(__file__).parent / "Journal Assets" / "config.ini"

ICON_PATH = Path(__file__).parent / "Journal Assets" / "GameJournal.ico"

class GUI:
    
    if not p.exists():
        config.add_section("IN PROGRESS")
        # config.set("IN PROGRESS")

        config.add_section("INCOMPLETE")
        # config.set("INCOMPLETE")

        config.add_section("COMPLETED")
        # config.set("COMPLETE")

        config.add_section("REVIEWS")
        # config.set("REVIEWS")

        with open(p, "w") as configfile:
            config.write(configfile)
        messagebox.showinfo(title="Game Journal", message="Welcome to Game Journal a Config File has just been created for you!")
    
    def __init__(self):
        # --- THEMES ---
        # bg fg bg2 btn_bg btn_fg btn2_bg btn3_bg, btn4_bg

        # self.theme_default = [
        #     "black", "#00FF00", "grey", "white", "green", "red", "orange", "blue"
        #     ]
        self.theme_default = [
            "#373737", "#3F9BFC", "#DBDBDB", "#1B1F20", "#28C940", "#FF6058", "orange", "#A681D4"
            ]
    
        # --- Init Root ---
        self.theme = self.get_theme()
        self.root = tk.Tk()
        self.root.geometry("1000x800")
        self.root.minsize(600, 725)
        self.root.title("Game Journal")
        self.root.config(bg=self.theme[0])
        self.header = tk.Label(self.root,
                               text="Game Journal",
                               font=("Luckiest Guy", 38),
                               fg=self.theme[1],
                               bg=self.theme[2],
                               bd=10,
                               relief=SUNKEN
                               )
        self.header.pack(ipadx=15, pady=10)

        icon_image = Image.open(ICON_PATH)
        icon_photo = ImageTk.PhotoImage(icon_image)

        self.root.iconphoto(True, icon_photo)

        style = ttk.Style()
        style.theme_use("clam")

        # Configure the Notebook tab and frame styles
        style.configure("TNotebook", background=self.theme[0], borderwidth=5)
        style.configure("TNotebook.Tab", background=self.theme[1], foreground=self.theme[2], padding=[10, 5])
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.theme[4])],
            foreground=[("selected", self.theme[0])]
        )

        # --- Make Notebook ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(ipadx=150, ipady=200)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Games in Progress")
        self.notebook.add(self.tab2, text="Incomplete Games")
        self.notebook.add(self.tab3, text="Completed Games")

        # --- TAB 1 - Games in Progress ---
        self.tab1_label = tk.Label(self.tab1,
                                   text="Games in Progress",
                                   font=("Courier", 18, "bold"),
                                   fg=self.theme[3],
                                   bg=self.theme[2]
                                   )
        self.tab1_label.pack()
        
        self.progress_list = tk.Listbox(self.tab1, font=("Helvetica", 22, "bold"), fg="#FF8800", bg=self.theme[3], justify="center")
        self.progress_list.pack(expand=True, fill="both")
        
        btn_frame = tk.Frame(self.tab1)
        btn_frame.columnconfigure(0, weight=1)

        self.add_game = tk.Button(btn_frame,
                                  text="Add Game in Progress",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[4],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda :self.add_game_function("in progress"))
        self.add_game.grid(row=0, column=0, sticky=tk.W+tk.E)

        self.status_game = tk.Button(btn_frame,
                                  text="Change Game Status",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[6],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda : self.change_status_function("In Progress"))
        self.status_game.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.remove_game = tk.Button(btn_frame,
                                  text="Remove Game in Progress",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[5],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda : self.remove_game_function("In Progress"))
        self.remove_game.grid(row=2, column=0, sticky=tk.W+tk.E)

        self.timetobeat_btn = tk.Button(btn_frame,
                                  text="How Long To Beat",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[7],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda : self.time_to_beat_function("In Progress"))
        self.timetobeat_btn.grid(row=3, column=0, sticky=tk.W+tk.E)

        btn_frame.pack(fill="x")

        # --- TAB 2 - Incomplete Games ---
        self.tab2_label = tk.Label(self.tab2,
                                   text="Incomplete Games",
                                   font=("Courier", 18, "bold"),
                                   fg=self.theme[3],
                                   bg=self.theme[2]
                                   )
        self.tab2_label.pack()
        
        self.incomplete_list = tk.Listbox(self.tab2, font=("Helvetica", 22, "bold"), fg="#E52527", bg=self.theme[3], justify="center")
        self.incomplete_list.pack(expand=True, fill="both")
        
        btn_frame = tk.Frame(self.tab2)
        btn_frame.columnconfigure(0, weight=1)

        self.add_game = tk.Button(btn_frame,
                                  text="Add Incomplete Game",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[4],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda :self.add_game_function("incomplete"))
        self.add_game.grid(row=0, column=0, sticky=tk.W+tk.E)
        
        self.status_game = tk.Button(btn_frame,
                                  text="Change Game Status",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[6],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda : self.change_status_function("Incomplete"))
        self.status_game.grid(row=1, column=0, sticky=tk.W+tk.E)
        
        self.remove_game = tk.Button(btn_frame,
                                  text="Remove Incomplete Game",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[5],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda : self.remove_game_function("Incomplete"))
        self.remove_game.grid(row=2, column=0, sticky=tk.W+tk.E)
    
        self.timetobeat_btn = tk.Button(btn_frame,
                                  text="How Long To Beat",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[7],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda : self.time_to_beat_function("Incomplete"))
        self.timetobeat_btn.grid(row=3, column=0, sticky=tk.W+tk.E)


        btn_frame.pack(fill="x")

        # --- TAB 3 - Completed Games ---
        self.tab3_label = tk.Label(self.tab3,
                                   text="Completed Games",
                                   font=("Courier", 18, "bold"),
                                   fg=self.theme[3],
                                   bg=self.theme[2]
                                   )
        self.tab3_label.pack()
        
        self.completed_list = tk.Listbox(self.tab3, font=("Helvetica", 22, "bold"), fg="#00FF00", bg=self.theme[3], justify="center")
        self.completed_list.pack(expand=True, fill="both")
        
        btn_frame = tk.Frame(self.tab3)
        btn_frame.columnconfigure(0, weight=1)

        self.add_game = tk.Button(btn_frame,
                                  text="Add Completed Game",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[4],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda :self.add_game_function("completed"))
        self.add_game.grid(row=0, column=0, sticky=tk.W+tk.E)
        
        self.status_game = tk.Button(btn_frame,
                                  text="Change Game Status",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[6],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda : self.change_status_function("Completed"))
        self.status_game.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.remove_game = tk.Button(btn_frame,
                                  text="Remove Completed Game",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[5],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda : self.remove_game_function("Completed"))
        self.remove_game.grid(row=2, column=0, sticky=tk.W+tk.E)

        self.view_review = tk.Button(btn_frame,
                                  text="View Game Review",
                                  font=("Arial", 16),
                                  fg=self.theme[3],
                                  bg=self.theme[7],
                                  relief=RAISED,
                                  bd=5,
                                  command=lambda : self.view_review_function())
        self.view_review.grid(row=3, column=0, sticky=tk.W+tk.E)

        btn_frame.pack(fill="x")

        self.load_games()
        self.run = self.root.mainloop()

    def get_theme(self):
        return self.theme_default

    def load_games(self):
        config.read(p)
        try:
            for game in sorted(config["IN PROGRESS"]):
                self.progress_list.insert(tk.END, game.title())
            for game in sorted(config["INCOMPLETE"]):
                    self.incomplete_list.insert(tk.END, game.title())
            for game in sorted(config["COMPLETED"]):
                    self.completed_list.insert(tk.END, game.title())
        except Exception as e:
            print(f"Error loading games: {e}")

    def add_game_function(self, add_location):
        self.add_location = add_location
        popup = tk.Toplevel(self.root)
        popup.geometry("600x300")
        popup.minsize(300, 200)
        popup.config(bg=self.theme[0])

        label = tk.Label(popup,
                         text="Enter Name of Game".upper(),
                         font=("Luckiest Guy", 22),
                         fg=self.theme[1],
                         bg=self.theme[2],
                         relief=SUNKEN,
                         bd=3)
        label.pack(ipadx=10, pady=5)

        enter_game = tk.Entry(popup, width=50, relief=SUNKEN, bd=5)
        enter_game.pack(pady=25)
        
        def submit_game():
             item = enter_game.get()
             if not enter_game.get().strip():
                 messagebox.showerror(title="Error", message="Must insert Game Name")
                 return
             config.read(p)

             if self.add_location == "in progress":
                if messagebox.askyesno(title="Confirm Submission", message=f"Would you like to add:\n'{enter_game.get()}'\nto Games in Progress"):
                    config.set("IN PROGRESS", enter_game.get().strip(), "in progress")
                    with open(p, "w") as config_file:
                        config.write(config_file)
                    self.progress_list.delete(0, tk.END)
                    for game in sorted(config["IN PROGRESS"]):
                        self.progress_list.insert(tk.END, game.title())
                    messagebox.showinfo(title="Success", message="Added game to Games in Progress")
                    popup.destroy()
                else:
                    return
                
             elif self.add_location == "incomplete":
                if messagebox.askyesno(title="Confirm Submission", message=f"Would you like to add:\n'{enter_game.get()}'\nto Incomplete Games"):
                    config.set("INCOMPLETE", enter_game.get().strip(), "incomplete")
                    with open(p, "w") as config_file:
                        config.write(config_file)
                    self.incomplete_list.delete(0, tk.END)
                    for game in sorted(config["INCOMPLETE"]):
                        self.incomplete_list.insert(tk.END, game.title())
                    messagebox.showinfo(title="Success", message="Added game to Incomplete Games")
                    popup.destroy()
                else:
                    return

             elif self.add_location == "completed":
                if messagebox.askyesno(title="Confirm Submission", message=f"Would you like to add:\n'{enter_game.get()}'\nto Completed Games"):
                    config.set("COMPLETED", enter_game.get().strip(), "completed")
                    with open(p, "w") as config_file:
                        config.write(config_file)
                    self.completed_list.delete(0, tk.END)
                    for game in sorted(config["COMPLETED"]):
                        self.completed_list.insert(tk.END, game.title())
                    messagebox.showinfo(title="Success", message="Added game to Completed Games")
                    popup.destroy()
                else:
                    return
                if messagebox.askyesno(title="Review", message="Would you like to leave a review?"):
                    popup.destroy()
                    self.leave_review(game=item)
                else:
                    return
             else:
                 print("error")

        submit = tk.Button(popup,
                        text="Submit",
                        font=("Arial", 14),
                        fg=self.theme[2],
                        bg=self.theme[1],
                        relief=RAISED,
                        bd=8,
                        command=submit_game
                        )
        submit.pack()


    def leave_review(self, game="No Game"):
        review_popup = tk.Toplevel(self.root)
        review_popup.geometry("800x600")
        review_popup.minsize(300, 425)
        review_popup.config(bg=self.theme[0])

        header = tk.Label(review_popup,
                         text="Leave Review".upper(),
                         font=("Luckiest Guy", 22),
                         fg=self.theme[1],
                         bg=self.theme[2],
                         relief=SUNKEN,
                         bd=3)
        header.pack(ipadx=10, pady=5)

        game_name = tk.Label(review_popup,
                             text=game.title(),
                             font=("Arial", 18),
                             fg=self.theme[1],
                             bg=self.theme[0])
        game_name.pack()

        review_number = tk.DoubleVar()
        review_scale = tk.Scale(review_popup,
                                from_=1, to=11,
                                orient="horizontal",
                                length=400,
                                resolution=.1,
                                variable=review_number
                                )
        review_scale.pack(pady=20)

        review_text = tk.Text(review_popup, height=10, width=50, font=("Arial", 12))
        review_text.pack()

        def submit_review():
            full_review = f"{review_text.get("1.0", tk.END).strip().replace("\n", "")} | Rating: {review_number.get():.1f}"
            if messagebox.askyesno(title="Confirm", message="Would you like to submit this review?"):
                config.read(p)
                config.set("REVIEWS", game.lower(), full_review)
                with open(p, "w") as config_file:
                        config.write(config_file)
                messagebox.showinfo(title="Success", message="Added Game Review")
                review_popup.destroy()
            else:
                return

        submit_btn = tk.Button(review_popup,
                        text="Submit",
                        font=("Arial", 14),
                        fg=self.theme[2],
                        bg=self.theme[1],
                        relief=RAISED,
                        bd=8,
                        command=submit_review
                        )
        submit_btn.pack(pady=10)

    def change_status_function(self, current_page):
        if current_page == "In Progress":
            page_list = self.progress_list
        elif current_page == "Incomplete":
            page_list = self.incomplete_list
        elif current_page == "Completed":
            page_list = self.completed_list

        try:
            index = page_list.curselection()
            if not index:
                messagebox.showerror(title="Error", message="No Game Selected")
                return
            item = page_list.get(index)
        except Exception as ex:
            return

        status_popup = tk.Toplevel(self.root)
        status_popup.config(bg=self.theme[2])
        status_popup.geometry("800x600")
        status_popup.minsize(375, 410)

        header = tk.Label(status_popup,
                         text="Change Game Status".upper(),
                         font=("Luckiest Guy", 26),
                         fg=self.theme[1],
                         bg=self.theme[2],
                         relief=SUNKEN,
                         bd=3)
        header.pack(ipadx=10, pady=5)

        game_label = tk.Label(status_popup,
                              text=item,
                              font=("Verdana", 28, "bold"),
                              fg=self.theme[1],
                              bg=self.theme[2])
        game_label.pack(pady=20)


        selected_option = tk.StringVar(value=current_page)
        options = [("In Progress", "In Progress"),
                   ("Incomplete", "Incomplete"),
                   ("Completed", "Completed")]
        
        for text, value in options:
            radio = tk.Radiobutton(
                status_popup,
                text=text,
                value=value,
                font=("Impact", 18),
                fg=self.theme[1],
                bg=self.theme[2],
                variable=selected_option
            )
            radio.pack(pady="5")
        
        def submit_status():
            if messagebox.askyesno(title="Confirm", message="Are you sure you would like to update the games status?"):
                config.read(p)
                if item in config[current_page.upper()]:
                    config.remove_option(current_page.upper(), item)
                    config.set(selected_option.get().upper(), item, selected_option.get().lower())
                else:
                    messagebox.showerror(title="Error", message="Item not found in config file")
                    return

                with open(p, "w") as configfile:
                    config.write(configfile)

                if current_page.lower() == "in progress" or selected_option.get().lower() == "in progress":
                    self.progress_list.delete(0, tk.END)
                    for game in sorted(config["IN PROGRESS"]):
                        self.progress_list.insert(tk.END, game.title())
                if current_page.lower() == "incomplete" or selected_option.get().lower() == "incomplete":
                    self.incomplete_list.delete(0, tk.END)
                    for game in sorted(config["INCOMPLETE"]):
                        self.incomplete_list.insert(tk.END, game.title())
                if current_page.lower() == "completed" or selected_option.get().lower() == "completed":
                    self.completed_list.delete(0, tk.END)
                    for game in sorted(config["COMPLETED"]):
                        self.completed_list.insert(tk.END, game.title())
                
                


                messagebox.showinfo(title="Success", message="Status Updated")
                if selected_option.get().lower() == "completed":
                    if messagebox.askyesno(title="Leave Review", message=f"Would you like to leave a review for {item.title()}?"):
                        self.leave_review(game=item)
                status_popup.destroy()
            else:
                return
            

        submit_btn = tk.Button(status_popup,
                               text="Submit",
                               font=("Arial", 16),
                               fg=self.theme[2],
                               bg=self.theme[1],
                               relief=RAISED,
                               bd=8,
                               command=submit_status)
        submit_btn.pack(pady=20)

    def remove_game_function(self, current_page):
        if current_page == "In Progress":
            page_list = self.progress_list
        elif current_page == "Incomplete":
            page_list = self.incomplete_list
        elif current_page == "Completed":
            page_list = self.completed_list

        try:
            index = page_list.curselection()
            if not index:
                messagebox.showerror(title="Error", message="No Game Selected")
                return
            item = page_list.get(index)
        except Exception as ex:
            return
        
        
        if messagebox.askyesno(title="Confirm", message=f"Are you sure you would like to Remove {item.title()}?"):
            config.read(p)
            if item in config[current_page.upper()]:
                config.remove_option(current_page.upper(), item)
                if item in config["REVIEWS"]:
                    config.remove_option("REVIEWS", item) 
            else:
                messagebox.showerror(title="Error", message="Item not found in config file")
                return

            with open(p, "w") as configfile:
                config.write(configfile)

            if current_page.lower() == "in progress":
                self.progress_list.delete(0, tk.END)
                for game in sorted(config["IN PROGRESS"]):
                    self.progress_list.insert(tk.END, game.title())
            if current_page.lower() == "incomplete":
                self.incomplete_list.delete(0, tk.END)
                for game in sorted(config["INCOMPLETE"]):
                    self.incomplete_list.insert(tk.END, game.title())
            if current_page.lower() == "completed":
                self.completed_list.delete(0, tk.END)
                for game in sorted(config["COMPLETED"]):
                    self.completed_list.insert(tk.END, game.title())
    
            messagebox.showinfo(title="Success", message=f"{item.title()} Removed")
        else:
            return
            
    def view_review_function(self):

        def open_review(review):
            review_win = tk.Toplevel(self.root)
            review_win.geometry("1000x800")
            review_win.minsize(500, 650)
            review_win.config(bg=self.theme[2])
            
            header = tk.Label(review_win,
                         text=item.upper(),
                         font=("Luckiest Guy", 42),
                         fg=self.theme[1],
                         bg=self.theme[2],
                         relief=SUNKEN,
                         bd=3)
            header.pack(ipadx=10, pady=5)

            rating_match = re.search(r"\| Rating:\s*(\d+\.\d+)", review)
            if rating_match:
                rating = rating_match.group(1)
            else:
                rating = "N/A"

            score_label = tk.Label(review_win,
                              text=f"Rating: {rating}",
                              font=("Courier", 26, "bold"),
                              fg=self.theme[1],
                              bg=self.theme[2])
            score_label.pack(pady=10)

            review_text = tk.Text(review_win,
                                  font=("Arial", 20, "bold"),
                                  width=500,
                                  height=10)
            review_text.pack(pady=30)
            review_text.insert(tk.END, review)

            close_btn = tk.Button(review_win,
                               text="Close",
                               font=("Arial", 16),
                               fg=self.theme[2],
                               bg=self.theme[1],
                               relief=RAISED,
                               bd=8,
                               command=review_win.destroy)
            close_btn.pack(pady=20)


        try:
            index = self.completed_list.curselection()
            if not index:
                messagebox.showerror(title="Error", message="No Game Selected")
                return
            item = self.completed_list.get(index)
        except Exception as ex:
            return
        
        if item in config["REVIEWS"]:
            open_review(config["REVIEWS"][item])
        else:
            messagebox.showerror("Error", f"No Review Found for {item.title()}")
            if messagebox.askyesno(title="Create Review", message=f"Would you like to create a review for {item.title()}?"):
                self.leave_review(game=item)
            return
    
    def time_to_beat_function(self, current_page):
        if current_page == "In Progress":
            page_list = self.progress_list
        elif current_page == "Incomplete":
            page_list = self.incomplete_list
        else:
            messagebox.showerror(title="Error", message="Dev Error: Didnt pass in page")
            return
            
        try:
            index = page_list.curselection()
            if not index:
                messagebox.showerror(title="Error", message="No Game Selected")
                return
            item = page_list.get(index)
        except Exception as ex:
            return
        
        results = HowLongToBeat().search(item, similarity_case_sensitive=False)
        if results is not None and len(results) > 0:
            best_element = max(results, key=lambda element: element.similarity)
            messagebox.showinfo(
                title="Time To Beat",
                message=f"Game: {best_element.game_name}\n\n\nMain Story: {math.ceil(best_element.main_story * 2) / 2} Hours\n\nMain Story + Extras: {math.ceil(best_element.main_extra * 2) / 2} Hours\n\nCompletionist: {math.ceil(best_element.completionist * 2) / 2} Hours")
        else:
            messagebox.showerror(title="Invalid Name", message=f"{item} Not Found on HowLongToBeat. Re-add with precise title. Sorry!")






if __name__ == "__main__":
    journal = GUI()