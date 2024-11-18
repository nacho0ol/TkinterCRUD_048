import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nilai_siswa')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fungsi untuk menyimpan data ke dalam database
def save_to_database(nama_siswa, biologi, fisika, inggris, prediksi_fakultas):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama_siswa, biologi, fisika, inggris, prediksi_fakultas))
    conn.commit()
    conn.close()
      
# Fungsi untuk memperbarui data di database
def update_database(id, nama_siswa, biologi, fisika, inggris, prediksi_prodi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_prodi = ?
        WHERE id = ?
    ''', (nama_siswa, biologi, fisika, inggris, prediksi_prodi, id))
    conn.commit()
    conn.close()
    
# Fungsi untuk menghapus data di database
def delete_database(id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
# Fungsi untuk menghitung prediksi fakultas
def calc_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return 'Kedokteran'
    elif fisika > biologi and fisika > inggris:
        return 'Teknik'
    elif inggris > biologi and inggris > fisika:
        return 'Bahasa'
    else:
        return 'Tidak Diketahui'
    
# Fungsi untuk menangani tombol submit
def submit():
    
    try:
        nama_siswa = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())
        
        if not nama_siswa:
            raise Exception("Nama siswa harus diisi")
        
        prediksi = calc_prediction(biologi, fisika, inggris)
        
        save_to_database(nama_siswa, biologi, fisika, inggris, prediksi)
        
        messagebox.showinfo("Sukses", "Data berhasil disimpan! \nPrediksi Fakultas: " + prediksi)
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")
        
# Fungsi untuk menangani tombol update
def update():
    try:
        if not selected_id.get():
            raise Exception("Pilih data yang akan diupdate")
        
        id = int(selected_id.get())
        nama_siswa = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())
        
        if not nama_siswa:
            raise ValueError("Nama siswa harus diisi")
        
        prediksi = calc_prediction(biologi, fisika, inggris)
        
        update_database(selected_id.get(), nama_siswa, biologi, fisika, inggris, prediksi)
        
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!\nPrediksi Fakultas: " + prediksi)
        clear_inputs()
        populate_table()
    except Exception as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")
        
# Fungsi untuk menangani tombol delete
def delete():
    try:
        if not selected_id.get():
            raise Exception("Pilih data yang akan dihapus")
        
        id = int(selected_id.get())
        delete_database(id)

        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")
        
# Fungsi untuk mengosongkan input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_id.set("")
    
# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():
        tree.delete(row)
        
    for row in fetch_data():
        tree.insert("", "end", values=row)
        
# Fungsi untuk mengisi input dengan data dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_data = tree.item(selected_item)['values']
        
        selected_id.set(selected_data[0])
        nama_var.set(selected_data[1])
        biologi_var.set(selected_data[2])
        fisika_var.set(selected_data[3])
        inggris_var.set(selected_data[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yg valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")
root.configure(bg="#D2E0FB")


# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_id = StringVar()

# Element GUI
Label(root, text="Nama Siswa", bg="#FEF9D9").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Bahasa Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Membuat tombol Add, Update, dan Delete
Button(root, text="Add", command=submit, bg="#FEF9D9").grid(row=4, column=0, padx=10, pady=5)
Button(root, text="Update", command=update, bg="#FEF9D9").grid(row=4, column=1, padx=10, pady=5)
Button(root, text="Delete", command=delete, bg="#FEF9D9").grid(row=4, column=2, padx=10, pady=5)

# Tabel untuk menampilkan data
columns = ("ID", "Nama Siswa", "Biologi", "Fisika", "Bahasa Inggris", "Prediksi")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama Siswa", text="Nama Siswa")
tree.heading("Biologi", text="Biologi")
tree.heading("Fisika", text="Fisika")
tree.heading("Bahasa Inggris", text="Bahasa Inggris")
tree.heading("Prediksi", text="Prediksi")
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Menyatakan posisi teks di setipa kolom ke tengah
# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor="center")

tree.bind("<ButtonRelease-1>", fill_inputs_from_table)

root.mainloop()