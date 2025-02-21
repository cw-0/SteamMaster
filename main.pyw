import threading
from howlongtobeatpy import HowLongToBeat
import math
import time
import json
from dotenv import load_dotenv
import csv
import os
from io import BytesIO
import pygame
import webbrowser
import tkinter as tk
from tkinter import SUNKEN, GROOVE, FLAT, RIDGE, simpledialog, messagebox, ttk
from configparser import ConfigParser
from pathlib import Path
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup

# --- INITS ---
pygame.mixer.init()
config = ConfigParser()
load_dotenv()





config_file = Path.cwd() / "Assets" / "Configs" / "config.ini"

CLICK_MP3 = Path.cwd() / "Assets" / "Sounds" / "buttonclick.mp3"
LOGO_PATH = Path.cwd() / "Assets" / "Images" / "logo.jpg"
PFP_PATH = Path.cwd() / "Assets" / "Images" / "profile.jpg"
GUEST_PATH = Path.cwd() / "Assets" / "Images" / "guest.jpg"
JOURNAL_APP = Path.cwd() / "Assets" / "Programs" / "GameJournal" / "journalGUI.pyw"
GAME_CONFIG = Path.cwd() / "Assets" / "Configs" / "game_config.csv"

STEAM_URL = "https://steamcommunity.com/id/"

logo_image = Image.open(LOGO_PATH)

pfp_size = 50, 50
header_font = ("Comic Sans MS", 28, "bold")
subheader_font = ("Tahoma", 18)

class GUI:
    def __init__(self):
        self.STEAM_API_KEY = os.getenv("STEAM_KEY")

        if self.STEAM_API_KEY:
            self.flag_gotENV = True
        else:
            self.flag_gotENV = False

        if not config_file.exists():
            config["USER"] = {"Name": "None", "ID": "None"}
            with open(config_file, "w") as file:
                config.write(file)


        self.check = False
        self.user = None
        self.id = None

        self.root = tk.Tk()
        self.root.title("Steam Master")
        self.root.geometry("1400x800")
        self.root.minsize(800, 625)

        logo_tk = ImageTk.PhotoImage(logo_image.resize((100, 100)))
        header_logo_tk = ImageTk.PhotoImage(logo_image.resize((150, 150)))


        self.logo_tk = logo_tk
        self.header_logo_tk = header_logo_tk

        try:
            profile_image = Image.open(PFP_PATH)
            profile_tk_original = ImageTk.PhotoImage(profile_image)
            self.profile_tk_original = profile_tk_original

            profile_tk = ImageTk.PhotoImage(profile_image.resize((pfp_size)))
            self.profile_tk = profile_tk
        except FileNotFoundError:
            self.profile_tk_original = None
            self.profile_tk = None

        guest_image = Image.open(GUEST_PATH)

        guest_tk_original = ImageTk.PhotoImage(guest_image)
        self.guest_tk__original = guest_tk_original

        guest_tk = ImageTk.PhotoImage(guest_image.resize((pfp_size)))
        self.guest_tk = guest_tk



        try:
            config.read(config_file)
            self.user = config["USER"]["Name"]
            self.id = config["USER"]["ID"]
            if not self.user or self.user.lower() == "none" or not self.id:
                self.setup_win()
            else:
                self.home()

        except KeyError:
            self.setup_win()



    def start(self):
        self.root.mainloop()


    def playsound(self, sound):
        pygame.mixer.Sound(sound).play()


    def setup_win(self):
        self.check = True
        self.root.config(bg="#333333")


        header = tk.Label(self.root,
                            text="Steam Master",
                            font=header_font,
                            relief=SUNKEN,
                            bd=8
                            )
        header.pack(pady=5, ipady=5, ipadx=5)

        branding = tk.Label(
            self.root,
            text="Caden Warren",
            font=subheader_font,
            relief=RIDGE,
            bd=4,
        )
        branding.bind("<Button-1>", lambda x: self.open_link("https://github.com/cw-0"))
        branding.pack(pady=3, ipadx=10)

        empty = tk.Label(self.root, bg="#333333")
        empty.pack(pady=5)

        logo = tk.Label(self.root, image=self.header_logo_tk, bg="#333333")
        logo.pack(pady=15)

        empty = tk.Label(self.root, bg="#333333")
        empty.pack(pady=5)

        setup_btn = tk.Button(
            self.root,
            text="START",
            font=("Arial", 16),
            command=self.ask_user
            )
        setup_btn.bind("<Button-1>", lambda x: self.playsound(CLICK_MP3))
        setup_btn.pack(pady=15)

        help_btn = tk.Button(
            self.root,
            text="HELP", 
            font=("Arial", 16),
            command=self.help
            )
        help_btn.pack(pady=5)
        help_btn.bind("<Button-1>", lambda x: self.playsound(CLICK_MP3))
        help_btn.pack(pady=5, ipadx=5)


    def open_link(self, link):
        webbrowser.open(link)
        self.playsound(CLICK_MP3)

    def ask_user(self):
        if not self.flag_gotENV:
            env_API = simpledialog.askstring("Steam API", "Enter your Steam API")
            if not env_API:
                return
            else:
                env_API = env_API.strip()
                self.STEAM_API_KEY = env_API
                with open(".env", "w") as env_file:
                    env_file.write(f"STEAM_KEY={env_API}")

        user = simpledialog.askstring("Steam User", "Enter your Steam URL")
        if not user:
            return

        user = user.strip()
        
        if user.endswith("/"):
            self.user = user.split("/")[-2]
        elif "/" in user:
            self.user = user.split("/")[-1]
        else:
            self.user = user
        
        try:
            response = requests.get(f"https://steamid.io/lookup/{self.user}")
        except Exception as e:
            print(e)
            messagebox.showerror(title="Connection Failed", message="Failed to connect to steamid.io")
            return

        if response.status_code != 200:
            messagebox.showerror(title="Connection Failed", message="Failed to connect to steamid.io")
            print("Failed to Connect to steamid.io")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        search = soup.find("dt", string="steamID64").find_next("dd")
        if search:
            user_id = search.text.strip()
            self.id = user_id
            print(user_id)
        else:
            messagebox.showerror(title="Error", message="Failed to Retrieve Steam ID")
            print("Failed to retrieve steam id")

        

        config.read(config_file)
        config.set("USER", "Name", self.user)
        config.set("USER", "ID", self.id)
        with open(config_file, "w") as file:
                config.write(file)
        
        # Get PFP
        if not PFP_PATH.exists():
            self.get_pfp()

        # Get Library
        if not GAME_CONFIG.exists():
            self.get_library()

        
        self.home()
        
    def home(self):
        self.side_menu()
    
        self.root.grid_rowconfigure(0, weight=5, uniform="equal")
        self.root.grid_rowconfigure(1, weight=1, uniform="equal")
        self.root.grid_columnconfigure(1, weight=1, uniform="equal")
        self.root.config(bg="#136b9d")

        home_notebook = ttk.Notebook(self.root)
        home_notebook.grid(row=0, column=1, sticky="nsew")

        tab1 = ttk.Frame(home_notebook)
        tab2 = ttk.Frame(home_notebook)

        home_notebook.add(tab1, text="Profile")
        home_notebook.add(tab2, text="Settings")

        self.show_profile = tk.Label(
            tab1,
            image=(self.profile_tk_original if self.profile_tk_original else self.guest_tk__original),
            font=subheader_font,
            relief=FLAT,
            bg="#333333",
            fg="#C4C4C4"
        )
        self.show_profile.pack(pady=50)
        
        show_user = tk.Label(tab1,
                             text=f"Steam Name: {self.user}",
                             font=("Helvetica", 16))
        show_user.pack()

        show_id = tk.Label(tab1,
                           text=f"Steam ID: {self.id}",
                           font=("Helvetica", 16))
        show_id.pack()



    def side_menu(self):
        if self.check:
            for widget in self.root.winfo_children():
                widget.destroy()
        self.check = False
        self.root.config(bg="white")

        sidebar = tk.Frame(self.root)
        sidebar.grid(row=0, column=0, sticky="nsew")

        sidebar.columnconfigure(0, weight=1)
        sidebar.config(bg="#333333")

        logo = tk.Label(sidebar, image=self.logo_tk, bg="#333333")
        logo.grid(row=0, sticky=tk.N)

        empty = tk.Label(sidebar)
        empty.grid(row=2, pady=30)
        empty.config(bg="#333333")


        branding = tk.Label(
            sidebar,
            text="Steam Master",
            font=("Cooper Black", 20, "bold"),
            relief=RIDGE,
            bd=4,
            fg="white",
            bg="#1371a4"
        )
        branding.bind("<Button-1>", lambda x: self.open_link("https://github.com/cw-0"))
        branding.bind("<Enter>", self.branding_hover_enter)
        branding.bind("<Leave>", self.branding_hover_leave)
        branding.grid(pady=3, ipadx=10, row=1)


        home_btn = tk.Button(
            sidebar,
            text="Home",
            font=subheader_font,
            relief=FLAT,
            bg="#333333",
            fg="#C4C4C4",
            command=self.home
        )
        home_btn.bind("<Enter>", self.sidebar_hover_enter)
        home_btn.bind("<Leave>", self.sidebar_hover_leave)
        home_btn.bind("<Button-1>", lambda x: self.playsound(CLICK_MP3))
        home_btn.grid(row=3, sticky=tk.W+tk.E)
        
        
        library_btn = tk.Button(
            sidebar,
            text="Library",
            font=subheader_font,
            relief=FLAT,
            bg="#333333",
            fg="#C4C4C4",
            command=self.library_page
        )
        library_btn.bind("<Enter>", self.sidebar_hover_enter)
        library_btn.bind("<Leave>", self.sidebar_hover_leave)
        library_btn.bind("<Button-1>", lambda x: self.playsound(CLICK_MP3))
        library_btn.grid(row=4, sticky=tk.W+tk.E)

        wishlist_btn = tk.Button(
            sidebar,
            text="Wishlist",
            font=subheader_font,
            relief=FLAT,
            bg="#333333",
            fg="#C4C4C4",
            command=self.wishlist_page
        )
        wishlist_btn.bind("<Enter>", self.sidebar_hover_enter)
        wishlist_btn.bind("<Leave>", self.sidebar_hover_leave)
        wishlist_btn.bind("<Button-1>", lambda x: self.playsound(CLICK_MP3))
        wishlist_btn.grid(row=5, sticky=tk.W+tk.E)

        game_journal_btn = tk.Button(
            sidebar,
            text="Journal",
            font=subheader_font,
            relief=FLAT,
            bg="#333333",
            fg="#C4C4C4",
            command=lambda: os.startfile(JOURNAL_APP)
        )
        game_journal_btn.bind("<Enter>", self.sidebar_hover_enter)
        game_journal_btn.bind("<Leave>", self.sidebar_hover_leave)
        game_journal_btn.bind("<Button-1>", lambda x: self.playsound(CLICK_MP3))
        game_journal_btn.grid(row=6, sticky=tk.W+tk.E)

        update_btn = tk.Button(
            sidebar,
            text="Update / Verify Files",
            font=subheader_font,
            relief=FLAT,
            bg="#333333",
            fg="#C4C4C4",
            command=self.update_page
        )
        update_btn.bind("<Enter>", self.sidebar_hover_enter)
        update_btn.bind("<Leave>", self.sidebar_hover_leave)
        update_btn.bind("<Button-1>", lambda x: self.playsound(CLICK_MP3))
        update_btn.grid(row=7, sticky=tk.W+tk.E)


        account_frame = tk.Frame(self.root)
        account_frame.grid(row=1, column=0, sticky="nsew")

        account_frame.columnconfigure(0, weight=1)
        account_frame.columnconfigure(1, weight=2)
        account_frame.config(bg="#333333")

        empty = tk.Label(account_frame)
        empty.grid(row=0, column=0, pady=30)
        empty.config(bg="#333333")

        account_name = tk.Button(
            account_frame,
            text=self.user,
            font=subheader_font,
            relief=FLAT,
            bg="#333333",
            fg="#C4C4C4",
            command=lambda: webbrowser.open(f"{STEAM_URL}{self.user}")
        )
        account_name.bind("<Enter>", self.sidebar_hover_enter)
        account_name.bind("<Leave>", self.sidebar_hover_leave)
        account_name.bind("<Button-1>", lambda x: self.playsound(CLICK_MP3))
        account_name.grid(row=1, column=1, sticky="nsew")

        
        self.account_img = tk.Button(
            account_frame,
            image=(self.profile_tk if self.profile_tk else self.guest_tk),
            font=subheader_font,
            relief=FLAT,
            bg="#333333",
            fg="#C4C4C4",
            command=self.change_pfp
        )
        self.account_img.bind("<Enter>", self.sidebar_hover_enter)
        self.account_img.bind("<Leave>", self.sidebar_hover_leave)
        self.account_img.bind("<Button-1>", lambda x: self.playsound(CLICK_MP3))
        self.account_img.grid(row=1, column=0, sticky="nsew")





    def help(self):
        win = tk.Toplevel()
        win.attributes("-topmost", True)
        win.title("Help")
        win.geometry("600x500")

    def sidebar_hover_enter(self, event):
        event.widget.config(bg="#1A1A1A")

    def sidebar_hover_leave(self, event):
        event.widget.config(bg="#333333")

    def get_pfp(self):

        self.start_animation()
        threading.Thread(target=self.fetch_profile_pic, daemon=True).start()

    def fetch_profile_pic(self):
        try:
            messagebox.showinfo(
                title="Profile Picture",
                message="Getting Profile Picture"
                )
            
            response = requests.get(f"{STEAM_URL}{self.user}")

            if response.status_code != 200:
                self.stop_animation()
                messagebox.showerror(title="Error", message="Failed to connect to steam")

            else:
                soup = BeautifulSoup(response.text, "html.parser")
                pfp_url = soup.find("div", class_="playerAvatarAutoSizeInner").find_all("img")[-1]
                
                pfp_img = pfp_url["src"]
                print(pfp_img)
                r = requests.get(pfp_img)
                if r.status_code != 200:
                    self.stop_animation()
                    messagebox.showerror(title="Error", message="Failed to connect to steam")
                else:
                    try:
                        img_data = BytesIO(r.content)
                        img = Image.open(img_data)
                        
                        if img.format == "GIF":
                            img = img.convert("RGB")
                        elif img.mode != "RGB":
                            img = img.convert("RGB")

                        img.save(PFP_PATH, format="JPEG")
                        
                        
                        profile_image = Image.open(PFP_PATH)
                        profile_tk_original = ImageTk.PhotoImage(profile_image)
                        self.profile_tk_original = profile_tk_original

                        profile_tk = ImageTk.PhotoImage(profile_image.resize((pfp_size)))
                        self.profile_tk = profile_tk
                        
                        try:
                            self.account_img.config(image=self.profile_tk)
                            self.show_profile.config(image=self.profile_tk_original)
                            self.root.update()
                        except Exception as e:
                            self.stop_animation()
                            print(e)

                        self.stop_animation()
                        messagebox.showinfo("Completed", "Profile Picture Downloaded Successfully")

                    except Exception as e:
                        self.stop_animation()
                        messagebox.showerror(title="Account Image", message=e)
                        print(e)
        except Exception as e:
            self.stop_animation()
            messagebox.showerror(title="Error", message=e)

    def get_library(self):
        messagebox.showinfo(title="Pulling Library", message="Fetching your Games. This may take a moment. Will notify when done!")
       
        self.start_animation()

        threading.Thread(target=self.fetch_library_data, daemon=True).start()

    def fetch_library_data(self):
        try:
            url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={self.STEAM_API_KEY}&steamid={self.id}&format=json"
            response = requests.get(url)
            print(url)
            print(response.status_code)
            if response.status_code != 200:
                self.stop_animation()
                messagebox.showerror(title="Connection Failed", message="Failed to connect to Steam")
                print("Failed to connect to Steam")
                return
            
            data = response.json()
            dump_file = Path.cwd() / "logs" / "index.json"
            with open(dump_file, "w") as f:
                json.dump(data, f, indent=4)

            game_details = []

            if "response" in data and "games" in data["response"]:
                for game in data['response']['games']:
                    result = ""

                    game_name = self.convert_appid(game['appid'])

                    for char in game_name:
                        if not char.isalpha() and not char.isdigit() and char not in [" ", "-", "_", ":"]:
                            continue
                        result += char
                    game_name = result

                    game_main_story, game_completionist, game_score, game_release = self.calc_timetobeat(name=str(game_name))

                    game_info = {
                        'game_name': game_name,
                        'appid': game['appid'],
                        'playtime_forever': game['playtime_forever'],
                        'playtime_windows_forever': game['playtime_windows_forever'],
                        'playtime_mac_forever': game['playtime_mac_forever'],
                        'playtime_linux_forever': game['playtime_linux_forever'],
                        'playtime_deck_forever': game['playtime_deck_forever'],
                        'rtime_last_played': game['rtime_last_played'],
                        'playtime_disconnected': game['playtime_disconnected'],
                        'main_story': game_main_story,
                        'completionist': game_completionist,
                        'crit_score': game_score,
                        'release_year': game_release
                        }
                    game_details.append(game_info)
            else:
                print("No games found or error in response")

            
            for game in game_details:
                print(game)
    
            
            with open(GAME_CONFIG, "w", newline="", encoding="utf-8") as file:
                fieldnames = ["game_name",
                              "appid",
                              "playtime_forever",
                              "playtime_windows_forever",
                              "playtime_mac_forever",
                              "playtime_linux_forever",
                              "playtime_deck_forever",
                              "rtime_last_played",
                              "playtime_disconnected",
                              "main_story",
                              "completionist",
                              "crit_score",
                              "release_year"]
                
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                
                rows = game_details

                for row in rows:
                    writer.writerow(row)

            self.stop_animation()
            messagebox.showinfo(title="Done", message="Your Library has been updated")
        except Exception as e:
            self.stop_animation()
            messagebox.showerror(title="Error", message=f"Error: {e}")
            print(e)
        
    

    def convert_appid(self, appid):
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        retries = 3
        for attempt in range(retries):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data.get(str(appid), {}).get("success"):
                        return data[str(appid)]["data"]["name"]
                    else:
                        print(f"AppID {appid} not found in the store.")
                        return "Unknown Game"
                else:
                    print(f"Failed to fetch details for AppID {appid}, status code: {response.status_code}")
                    break
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}, retrying... ({attempt + 1}/{retries})")
                time.sleep(2)
        return "Unknown Game"


    def change_pfp(self):
        # Change this later to be a function under refresh not on pfp click
        if not messagebox.askyesno(title="Update PFP", message="Would you like to update your Profile Picture?"):
            return
        
        self.get_pfp()


    def calc_timetobeat(self, name=None):
        name = name.strip()
        if not name:
            print("calc_timetobeat requires name=name")
            return

        print(name)

        if "Edition" in name:
            name = name.replace("Edition", "")

        try:
            results = HowLongToBeat(0.2).search(name, similarity_case_sensitive=False)
            if results is not None and len(results) > 0:
                best_element = max(results, key=lambda element: element.similarity)

                def round_time(value):
                    return f"{math.ceil(value * 2) / 2} Hours" if value is not None else "N/A"

                main_story = round_time(best_element.main_story)
                if not main_story:
                    main_story = "N/A"

                completionist = round_time(best_element.completionist)
                if not completionist:
                    completionist = "N/A"

                score = best_element.review_score,
                if not score:
                    score = "N/A"

                release = best_element.release_world
                if not release:
                    release = "N/A"

                return main_story, completionist, score, release
            
            else:
                print("Game Not Found in HowLongToBeatDatabase")
                return "N/A", "N/A", "N/A", "N/A"
        except Exception as e:
            print(e)

    def library_page(self):
        self.side_menu()

        self.root.grid_rowconfigure(0, weight=5, uniform="equal")
        self.root.grid_rowconfigure(1, weight=1, uniform="equal")
        self.root.grid_columnconfigure(1, weight=1, uniform="equal")
        self.root.config(bg="#136b9d")

        library_notebook = ttk.Notebook(self.root)
        library_notebook.grid(row=0, column=1, sticky="nsew")

        self.games_tab = ttk.Frame(library_notebook)
        tab2 = ttk.Frame(library_notebook)

        library_notebook.add(self.games_tab, text="Games")
        library_notebook.add(tab2, text="Settings")

        self.load_game_data()
        self.sorting_func()
    
        

    def sorting_func(self):
        def get_rows_with_zero_minutes(treeview, column_name="playtime_forever"):
            zero_rows = []
            for item in treeview.get_children():
                value = treeview.item(item, "values")[treeview["columns"].index(column_name)]
                
                if value == "0 Minutes" or value == 0:
                    zero_rows.append(item)
            
            return zero_rows
        
        def get_playtime_total(treeview, column_name="playtime_forever"):
            hours = 0
            minutes = 0

            for item in treeview.get_children():
                value = treeview.item(item, "values")[treeview["columns"].index(column_name)]
                try:
                    if "Hours &" in value:
                        hours_str, minutes_str = value.split(" Hours & ")
                        hours += int(hours_str)
                        minutes += int(minutes_str.replace(" Minutes", ""))

                    elif "Hours" in value:
                        hours_str = value.split(" Hours")[0]
                        hours += int(hours_str)
                    elif "Minutes" in value:
                        minutes_str = value.split(" Minutes")[0]
                        minutes += int(minutes_str)
                    elif "Minute" in value:
                        minutes_str = value.split(" Minute")[0]
                        minutes += int(minutes_str)
                    else:
                        continue
                except IndexError:
                    print(f"Error with value: {value}")
            
            additional_hours = minutes // 60
            remaining_minutes = minutes % 60

            hours += additional_hours

            return f"{hours} Hours & {remaining_minutes} Minutes"
        
        def get_timetobeat_total(treeview, column_name="main_story"):
            hours = 0
            minutes = 0

            for item in treeview.get_children():
                value = treeview.item(item, "values")[treeview["columns"].index(column_name)]
                try:
                    if "Hours" in value:
                        hours_str = value.split(" Hours")[0]
                        hours += float(hours_str)
                    else:
                        continue
                except IndexError:
                    print(f"Error with value: {value}")

            return f"{hours} Hours"
        

        zero_rows = get_rows_with_zero_minutes(self.treeview)
        total_time_played_calc = get_playtime_total(self.treeview)
        total_time_to_beat_calc = get_timetobeat_total(self.treeview)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.config(bg="#136b9d")
        bottom_frame.grid(row=1, column=1)

        sort_btn = tk.Button(
            bottom_frame,
            text="Sort By",
            font=("Arial", 16),
            width=10,
            command=self.sort_window)
        sort_btn.grid(row=0, column=3, pady=20)

        totals_frame = tk.Frame(bottom_frame)
        totals_frame.grid(row=1, column=3)

        total_games = tk.Label(
            totals_frame,
            text=f"| Games: {len(self.treeview.get_children())} | ",
            font=("Arial", 16),
            bg="#136b9d",
            fg="white"
        )
        total_games.grid(row=0, column=0)

        total_unplayed = tk.Label(
            totals_frame,
            text=f" | Games Unplayed: {len(zero_rows)} |",
            font=("Arial", 16),
            bg="#136b9d",
            fg="white"
        )
        total_unplayed.grid(row=0, column=1)

        total_time_played = tk.Label(
            totals_frame,
            text=f"| Time Played: {total_time_played_calc} | ",
            font=("Arial", 16),
            bg="#136b9d",
            fg="white"
        )
        total_time_played.grid(row=0, column=2)

        total_time_to_beat = tk.Label(
            totals_frame,
            text=f"| Time To Beat Library: {total_time_to_beat_calc} | ",
            font=("Arial", 16),
            bg="#136b9d",
            fg="white"
        )
        total_time_to_beat.grid(row=0, column=3)
        

    def sort_window(self):
        sorting_popup = tk.Toplevel(self.root)
        sorting_popup.config(bg="#333333")
        sorting_popup.geometry("800x600")
        sorting_popup.minsize(375, 410)

        header = tk.Label(sorting_popup,
                        text="Sort By",
                        font=("Luckiest Guy", 26),
                        fg="white",
                        bg="#333333",
                        relief=SUNKEN,
                        bd=3)
        header.pack(ipadx=10, pady=15)

        self.selected_option = tk.StringVar(value="Name")
        options = [("Name", "Name"),
                ("Time Played", "Time Played"),
                ("Time to Beat", "Time to Beat"),
                ("Crit Score", "Crit Score"),
                ("Release Year", "Release Year")]
        
        for text, value in options:
            radio = tk.Radiobutton(
                sorting_popup,
                text=text,
                value=value,
                font=("Impact", 18),
                fg="white",
                bg="#333333",
                variable=self.selected_option,
                selectcolor="black"
            )
            radio.pack(pady="5")

        submit_btn = tk.Button(
            sorting_popup,
            text="Submit",
            font=("Arial", 16),
            width=10,
            command=lambda: self.do_sort(sorting_popup))
        submit_btn.pack(pady=20)


    def do_sort(self, window):
        key = self.get_key()

        if hasattr(self, "treeview") and self.treeview.winfo_exists():
            self.treeview.destroy()

        self.load_game_data(key=key)

        window.destroy()

    def get_key(self):
        selection = self.selected_option.get()
        
        if selection == "Name":
            return lambda x: x["game_name"]
        elif selection == "Time Played":
            return lambda x: self.extract_numeric_value(x["playtime_forever"])
        elif selection == "Time to Beat":
            return lambda x: self.extract_numeric_value(x["main_story"])
        elif selection == "Crit Score":
            return lambda x: self.extract_numeric_value(x["crit_score"].translate(str.maketrans("", "", "(),")))
        elif selection == "Release Year":
            return lambda x: self.extract_numeric_value(x["release_year"])
        else:
            return lambda x: x["game_name"]

    
    def load_game_data(self, key=lambda x: x["game_name"]):
        do_reverse = False

        if hasattr(self, 'treeview') and self.treeview.winfo_exists():
            self.treeview.config(yscrollcommand=None, xscrollcommand=None)
            self.treeview.destroy()

        self.treeview = ttk.Treeview(self.games_tab,
                                     columns=(
                                         "game_name",
                                         "appid",
                                         "playtime_forever",
                                         "main_story",
                                         "completionist",
                                         "crit_score",
                                         "release_year"), show="headings")
        
        self.treeview.heading("game_name", text="Game Name")
        self.treeview.heading("appid", text="App ID")
        self.treeview.heading("playtime_forever", text="Time Played")
        self.treeview.heading("main_story", text="Time To Beat")
        self.treeview.heading("completionist", text="Time To 100%")
        self.treeview.heading("crit_score", text="Crit Score")
        self.treeview.heading("release_year", text="Release Year")

        self.treeview.column("game_name", width=200)
        self.treeview.column("appid", width=100)
        self.treeview.column("playtime_forever", width=120)
        self.treeview.column("main_story", width=100)
        self.treeview.column("completionist", width=100)
        self.treeview.column("crit_score", width=100)
        self.treeview.column("release_year", width=80)

        if not hasattr(self, 'v_scroll') or not self.v_scroll.winfo_exists():
            self.v_scroll = tk.Scrollbar(self.games_tab, orient="vertical", command=self.treeview.yview)
            self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        if not hasattr(self, 'h_scroll') or not self.h_scroll.winfo_exists():
            self.h_scroll = tk.Scrollbar(self.games_tab, orient="horizontal", command=self.treeview.xview)
            self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)


        self.v_scroll.config(command=self.treeview.yview)
        self.h_scroll.config(command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.treeview.pack(fill=tk.BOTH, expand=True)

        if "game_name" in str(key):
            do_reverse = False
        elif "playtime_forever" in str(key):
            do_reverse = False
        elif "main_story" in str(key):
            do_reverse = True
        elif "crit_score" in str(key):
            do_reverse = True
        elif "release_year" in str(key):
            do_reverse = True

        if GAME_CONFIG:
            try:
                with open(GAME_CONFIG, newline="") as file:
                    reader = csv.DictReader(file)
                    for row in sorted(reader, key=key, reverse=do_reverse):
                        self.treeview.insert("", "end", values=(row['game_name'], row['appid'], self.format_time(int(row['playtime_forever'])),
                                                           row['main_story'], row['completionist'], row['crit_score'].translate(str.maketrans("", "", "(),")),
                                                           row['release_year']))
            except Exception as e:
                print(e)

    def format_time(self, minutes):
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if hours:
            return f"{hours} Hours & {remaining_minutes} Minutes"
        elif not hours and minutes:
            if minutes == 1:
                return f"{remaining_minutes} Minute"
            else:
                return f"{remaining_minutes} Minutes"
        elif not hours and not minutes:
            return f"0 Minutes"

    def extract_numeric_value(self, value):
        try:
            return float(value.split(" ")[0])
        except (ValueError, IndexError):
            return float('inf')

    def wishlist_page(self):
        messagebox.showinfo(title="Not Available", message="Coming Soon!")

    def update_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.side_menu()

        self.root.grid_rowconfigure(0, weight=5, uniform="equal")
        self.root.grid_rowconfigure(1, weight=1, uniform="equal")
        self.root.grid_columnconfigure(1, weight=1, uniform="equal")
        self.root.config(bg="#136b9d")

        button_frame = tk.Frame(self.root)
        button_frame.config(bg="#136b9d")
        button_frame.grid(row=0, column=1)

        game_list_btn = tk.Button(
            button_frame,
            text="Update Games",
            font=("Arial", 16),
            width=15,
            command=self.get_library)
        game_list_btn.grid(row=0, column=3, pady=20)


    def start_animation(self):
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("Loading...")
        self.loading_window.geometry("400x300")
        self.loading_window.configure(bg="black")

        self.loading_window.attributes("-topmost", True)

        canvas = tk.Canvas(self.loading_window, width=400, height=300, bg="black", highlightthickness=0)
        canvas.pack()

        center_x, center_y = 200, 150
        radius = 80
        dot_radius = 8
        num_dots = 10

        self.dots = []
        for i in range(num_dots):
            angle = (2 * math.pi / num_dots) * i
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            dot = canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill="gray")
            self.dots.append(dot)

        self.current_dot = 0
        self.animation_running = True

        def animate_loading():
            if not self.animation_running:
                return

            for dot in self.dots:
                canvas.itemconfig(dot, fill="gray")

            canvas.itemconfig(self.dots[self.current_dot], fill="cyan")
            self.current_dot = (self.current_dot + 1) % num_dots
            canvas.after(100, animate_loading)

        animate_loading()

    def stop_animation(self):
        self.animation_running = False
        if self.loading_window:
            self.loading_window.destroy()
            self.loading_window = None

    def branding_hover_enter(self, event):
        event.widget.config(bg="#144377")

    def branding_hover_leave(self, event):
        event.widget.config(bg="#1371a4")


if __name__ == "__main__":
    app = GUI()
    app.start()