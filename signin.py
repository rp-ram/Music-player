import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import pygame
import os
import authentication

class SignInPage():
    def __init__(self, root):
        self.root = root
        self.root.title("Sign In")
        self.username = ""
        self.password = ""
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self.root, text="UserID:")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        self.username_entry.focus_set()

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.sign_in_button = tk.Button(self.root, text="Sign In", command=self.sign_in)
        self.sign_in_button.pack(pady=10)
        
        self.sign_up_button = tk.Button(self.root, text="Sign Up", command=self.show_sign_up_page)
        self.sign_up_button.pack(pady=5)

    def sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user = authentication.verify_user(username, password)
        if user:
            messagebox.showinfo("Success", "Sign-in successful.")
            self.show_songs_page()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
            
    
    def show_sign_up_page(self):
        self.root.withdraw()
        root2 = tk.Toplevel()
        sign_up_page = SignUpPage(root2)
        root2.mainloop()

    def show_songs_page(self):
        self.root.withdraw()
        root2 = tk.Toplevel()
        songs_page = SongsPage(root2)
        root2.mainloop()

class SignUpPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up")
        self.new_username = ""
        self.new_userid = ""
        self.new_password = ""
        self.new_email = ""
        self.new_mobilenumber = ""
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self.root, text="New Username:")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        self.username_entry.focus_set()

        self.userid_label = tk.Label(self.root, text="New User ID:")
        self.userid_label.pack(pady=10)
        self.userid_entry = tk.Entry(self.root)
        self.userid_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="New Password:")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.email_label = tk.Label(self.root, text="Email ID:")
        self.email_label.pack(pady=10)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        self.mobilenumber_label = tk.Label(self.root, text="Mobile Number:")
        self.mobilenumber_label.pack(pady=10)
        self.mobilenumber_entry = tk.Entry(self.root)
        self.mobilenumber_entry.pack(pady=5)

        self.sign_up_button = tk.Button(self.root, text="Sign Up", command=self.sign_up)
        self.sign_up_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Back to Sign In", command=self.show_sign_in_page)
        self.back_button.pack(pady=5)

    def sign_up(self):
        self.new_username = self.username_entry.get()
        self.new_userid = self.userid_entry.get()
        self.new_password = self.password_entry.get()
        self.new_email = self.email_entry.get()
        self.new_mobilenumber = self.mobilenumber_entry.get()

        if self.new_username and self.new_userid and self.new_password and self.new_email and self.new_mobilenumber:
            authentication.register_user(self.new_username, self.new_userid, self.new_password, self.new_email, self.new_mobilenumber)
            messagebox.showinfo("Sign Up Successful", "Account created successfully.")
            self.show_sign_in_page()
        else:
            messagebox.showerror("Error", "Please fill in all the fields.")

    def show_sign_in_page(self):
        self.root.withdraw()
        root2 = tk.Tk()
        sign_in_page = SignInPage(root2)
        root2.mainloop()

class SongsPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        self.music_path = None
        self.playing = False

        self.create_widgets()

    def create_widgets(self):
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.play_button = tk.Button(self.top_frame, text="Play", command=self.play_pause)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.top_frame, text="Delete Song", command=self.delete_song)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.top_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.top_frame, text="Search", command=self.search_song)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.close_button = tk.Button(self.top_frame, text="Close", command=self.close_app)
        self.close_button.pack(side=tk.LEFT, padx=5)

        self.select_button = tk.Button(self.top_frame, text="Select Song to Play", command=self.select_song_to_play)
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.list_button = tk.Button(self.top_frame, text="List All Songs", command=self.list_all_songs)
        self.list_button.pack(side=tk.LEFT, padx=5)

        pygame.mixer.init()
    
    def select_song_to_play(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            self.music_path = file_path
            self.stop_music()
            self.play_music()
    
    def play_music(self):
        if self.music_path and not self.playing:
            self.playing = True
            self.play_button.config(text="Pause")
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.play_button.config(text="Play")

    def play_pause(self):
        if self.playing:
            self.stop_music()
        else:
            self.search_song()
                
    def delete_song(self):
        search_text = self.search_var.get()
        if search_text == '':
            messagebox.showerror("Error","Entry is empty.")
        else:
            search_result = self.find_song_in_directory(search_text, "C:/")

            if search_result:
                self.music_path = search_result
                os.remove(self.music_path)
                self.music_path = None
                self.stop_music()
                messagebox.showinfo("Success","Song is deleted")
            else:
                messagebox.showinfo("Song Not Found", "No song matching the search criteria was found.")

    def search_song(self):
        search_text = self.search_var.get()
        if search_text == '':
            messagebox.showerror("Error","Entry is empty.")
        else:
            search_result = self.find_song_in_directory(search_text, "C:/")

            if search_result:
                self.music_path = search_result
                self.stop_music()
                self.play_music()
            else:
                messagebox.showinfo("Song Not Found", "No song matching the search criteria was found.")

    def find_song_in_directory(self, song_name, directory):
        for root, dirs, files in os.walk(directory):
            for f in files:
                filename = os.path.join(root, f)
                if filename.endswith('%s.mp3'%song_name):
                    return filename
        return None
    
    def list_all_songs(self):
        song_list = self.find_all_songs_in_directory("C:/") # Replace with your music directory path
        if song_list:
            self.show_song_list_window(song_list)
        else:
            messagebox.showinfo("No Songs Found", "No songs were found in the specified directory.")

    def find_all_songs_in_directory(self, directory):
        song_list = []
        for root, dirs, files in os.walk(directory):
            for f in files:
                filename = os.path.join(root, f)
                if filename.endswith('.mp3'):
                    song_list.append(f)
        return song_list

    def show_song_list_window(self, song_list):
        list_window = tk.Toplevel(self.root)
        list_window.title("List of Songs")
        listbox = Listbox(list_window, selectmode=tk.SINGLE)
        listbox.pack(fill=tk.BOTH, expand=True)
        for song in song_list:
            listbox.insert(tk.END, song)
    
    def close_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    sign_in_page = SignInPage(root)
    root.mainloop()
