import tkinter as tk
import pandas as pd
from tkinter import ttk, messagebox
from isimpop import populer_film_oner
from turkisi import film_oner  
from isimkisi import kisi_film_oner 
from turpop import populer_tur_oner

movies_df = pd.read_csv('yeni_movies.csv', sep=",")

ratings_df = pd.read_csv('yeni_ratings.csv', sep=",")

tages_df = pd.read_csv('filtered_tagg.csv', sep=",")

movies_dataf = pd.read_csv('movie.csv')

filmisim_kisisel_user = tages_df['userId'].unique().tolist()
    
filmtur_kisisel_user = ratings_df['userId'].unique().tolist()

filmisim_kisisel_title = tages_df.merge(movies_df[['movieId', 'title']], on='movieId', how='left')['title'].dropna().unique().tolist()

names = movies_df['title'].tolist()

class FilmOneriSistemi:
    def __init__(self, root):
        self.root = root
        self.root.title("Film Öneri Sistemi")

        
        self.output_label = ttk.Label(root, text="Önerilen Filmler:", font=("Helvetica", 36, "bold"), foreground="white", background="#046623")
        self.output_label.pack(pady=8)
        

        self.selection_frame = tk.Frame(root, bg="#F5F5F5")
        self.selection_frame.pack(pady=8)

        self.secenekler = ["Popüler Film Önerileri", "Kişiselleştirilmiş Film Önerileri"]
        self.first_selection = ttk.Combobox(self.selection_frame, values=self.secenekler, font=("Arial", 20), foreground="#81C784", state="readonly", width=30)  # Genişliği artırdık
        self.first_selection.set("Lütfen alacağınız öneri türünü seçiniz")  
        self.first_selection.bind("<<ComboboxSelected>>", self.update_second_selection)
        self.first_selection.grid(row=0, column=0, padx=(0, 60))  
 
        self.shartlar = []
        self.second_selection = ttk.Combobox(self.selection_frame, values=self.shartlar, font=("Arial", 20), foreground="#81C784", width=30)  # Genişliği artırdık
        self.second_selection.bind("<<ComboboxSelected>>", self.update_option_list)
        self.second_selection.grid(row=0, column=1) 

        
        self.genre_frame = tk.Frame(root, bg="#F5F5F5")  
        self.genre_frame.pack(pady=8, padx=20) 

        self.genre_label = tk.Label(self.genre_frame, text="Film Türü", font=("Arial", 16), bg="#F5F5F5", fg="#333333")
        self.genre_label.pack(pady=(0, 3)) 

        self.genre_listbox = tk.Listbox(self.genre_frame, height=3, width=40, font=("Arial", 14), bg="#FFFFFF", fg="#333333", selectbackground="#8BC34A", selectforeground="#FFFFFF", bd=2, relief="groove")
        self.genre_listbox.pack(side=tk.LEFT, padx=(0, 8))  

        self.genre_scrollbar = tk.Scrollbar(self.genre_frame)
        self.genre_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.genre_listbox.config(yscrollcommand=self.genre_scrollbar.set)
        self.genre_scrollbar.config(command=self.genre_listbox.yview)

        self.genre_scrollbar.config(bg="#8BC34A", troughcolor="#E0E0E0")


        self.name_frame = tk.Frame(root, bg="#F5F5F5")  
        self.name_frame.pack(pady=10, padx=20)  

        self.name_label = tk.Label(self.name_frame, text="Film İsimleri", font=("Arial", 16), bg="#F5F5F5", fg="#333333")
        self.name_label.pack(pady=(0, 3)) 

        self.name_listbox = tk.Listbox(self.name_frame, height=3, width=40, font=("Arial", 14), bg="#FFFFFF", fg="#333333", selectbackground="#8BC34A", selectforeground="#FFFFFF", bd=2, relief="groove")
        self.name_listbox.pack(side=tk.LEFT, padx=(0, 8)) 

        self.name_scrollbar = tk.Scrollbar(self.name_frame)
        self.name_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.name_listbox.config(yscrollcommand=self.name_scrollbar.set)
        self.name_scrollbar.config(command=self.name_listbox.yview)

        self.name_scrollbar.config(bg="#8BC34A", troughcolor="#E0E0E0")

        self.person_frame = tk.Frame(root, bg="#F5F5F5") 
        self.person_frame.pack(pady=10, padx=20)  

        self.person_label = tk.Label(self.person_frame, text="Kişiler", font=("Arial", 16), bg="#F5F5F5", fg="#333333")
        self.person_label.pack(pady=(0, 3)) 

        self.person_listbox = tk.Listbox(self.person_frame, height=3, width=40, font=("Arial", 14), bg="#FFFFFF", fg="#333333", selectbackground="#8BC34A", selectforeground="#FFFFFF", bd=2, relief="groove")
        self.person_listbox.pack(side=tk.LEFT, padx=(0, 8)) 

        self.person_scrollbar = tk.Scrollbar(self.person_frame)
        self.person_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.person_listbox.config(yscrollcommand=self.person_scrollbar.set)
        self.person_scrollbar.config(command=self.person_listbox.yview)

        self.person_scrollbar.config(bg="#8BC34A", troughcolor="#E0E0E0")

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 16), foreground="#81C784", background="#4CAF50", padding=10)
        style.map("TButton", background=[("active", "#388E3C")])  
        self.button = ttk.Button(root, text="Öneri Al", command=self.show_recommendations, style="TButton", width=20)
        self.button.pack(pady=8)    

            
    
        
        self.output_text = tk.Text(root, height=10, width=50,font=("Arial", 16), fg="black", wrap=tk.WORD)
        self.output_text.pack(pady=10)

        self.genre_listbox.bind('<<ListboxSelect>>', lambda event: self.on_select(event, self.genre_listbox))
        self.name_listbox.bind('<<ListboxSelect>>', lambda event: self.on_select(event, self.name_listbox))
        self.person_listbox.bind('<<ListboxSelect>>', lambda event: self.on_select(event, self.person_listbox))

    def on_select(self, event, listbox):
        selected_index = listbox.curselection()
        if not selected_index:
            return

        listbox.selection_clear(0, tk.END)
        listbox.selection_set(selected_index)
        listbox.activate(selected_index)

        for i in range(listbox.size()):
            if i == selected_index[0]:
                listbox.itemconfig(i, {'bg': '#8BC34A'})
            else:
                listbox.itemconfig(i, {'bg': 'grey'})

    def update_second_selection(self, event):
        if self.first_selection.get() == "Popüler Film Önerileri":
            self.shartlar = ["Film Türüne Göre Öneriler", "Film İsmine Göre Öneriler"]
        elif self.first_selection.get() == "Kişiselleştirilmiş Film Önerileri":
            self.shartlar = ["Film Türüne Göre Öneriler", "Film İsmine Göre Öneriler"]

        self.second_selection['values'] = self.shartlar
        self.second_selection.current(0)

    def update_option_list(self, event):
        self.genre_listbox.delete(0, tk.END)
        self.name_listbox.delete(0, tk.END)
        self.person_listbox.delete(0, tk.END)

        if self.first_selection.get() == "Popüler Film Önerileri":
            if self.second_selection.get() == "Film Türüne Göre Öneriler":
                genres = ["Drama", "Comedy", "Thriller", "Romance","Action", "Crime", "Horror", "Documentary","Adventure", "Sci-Fi"]
                for genre in genres:
                    self.genre_listbox.insert(tk.END, genre)
                self.genre_listbox.pack(pady=10)
                
            elif self.second_selection.get() == "Film İsmine Göre Öneriler":
                for name in names:
                    self.name_listbox.insert(tk.END, name)
                self.name_listbox.pack(pady=10)
                


        elif self.first_selection.get() == "Kişiselleştirilmiş Film Önerileri":
            if self.second_selection.get() == "Film Türüne Göre Öneriler":
                genres = ["Drama", "Comedy", "Thriller", "Romance","Action", "Crime", "Horror", "Documentary","Adventure", "Sci-Fi"]

                for genre in genres:
                    self.genre_listbox.insert(tk.END, genre)
                for person in filmtur_kisisel_user:
                    self.person_listbox.insert(tk.END, person)

                self.genre_listbox.pack(pady=10)
                self.person_listbox.pack(pady=10)
            elif self.second_selection.get() == "Film İsmine Göre Öneriler":
                for person in filmisim_kisisel_user:
                    self.person_listbox.insert(tk.END, person)
                self.person_listbox.bind("<<ListboxSelect>>", self.update_name_listbox_based_on_user)
                self.person_listbox.pack(pady=10)
                self.name_listbox.pack(pady=10)

    def update_name_listbox_based_on_user(self, event):
        self.name_listbox.delete(0, tk.END)
        selected_user_id = int(self.person_listbox.get(tk.ACTIVE))  
        user_watched_titles = tages_df[tages_df['userId'] == selected_user_id]['movieId']
        user_titles = movies_dataf[movies_dataf['movieId'].isin(user_watched_titles)]['title'].unique()

        for title in user_titles:
            self.name_listbox.insert(tk.END, title)
  
    def show_recommendations(self):
        selected_option = self.first_selection.get()
        selected_condition = self.second_selection.get()

        self.output_text.delete(1.0, tk.END)

        try:
            recommended_films = []  

            if selected_option == "Popüler Film Önerileri":
                if selected_condition == "Film Türüne Göre Öneriler":
                    selected_genre = self.genre_listbox.get(tk.ACTIVE)  
                    recommended_films = populer_tur_oner(selected_genre)
                    

                elif selected_condition == "Film İsmine Göre Öneriler":
                    selected_name = self.name_listbox.get(tk.ACTIVE)
                    recommended_films = populer_film_oner(selected_name)


            elif selected_option == "Kişiselleştirilmiş Film Önerileri":
                if selected_condition == "Film Türüne Göre Öneriler":
                    selected_genre = self.genre_listbox.get(tk.ACTIVE)
                    
                    selected_person = int(self.person_listbox.get(tk.ACTIVE))

                    recommended_films = film_oner(int(selected_person), selected_genre)
                
                elif selected_condition == "Film İsmine Göre Öneriler":
                    selected_name = self.name_listbox.get(tk.ACTIVE)

                    selected_person = self.person_listbox.get(tk.ACTIVE) 
                    recommended_films = kisi_film_oner(int(selected_person), selected_name)

            for i, film in enumerate(recommended_films):
                if i >= 50:
                    break
                self.output_text.insert(tk.END, film + "\n")

        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")


root = tk.Tk()
film_sistemi = FilmOneriSistemi(root)
root.geometry("800x800")
root.config(bg="#046623")  

root.mainloop()
