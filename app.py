import streamlit as st
import psycopg2
from datetime import date

# Koneksi ke database PostgreSQL
def get_connection():
    return psycopg2.connect(
        host="gondola.proxy.rlwy.net",
        port=57367,
        dbname="railway",
        user="postgres",
        password="tAwxGzaYZTkTejKfaZCsZoMHrnSOCNVk"
    )

def run_query(query, params=None, fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    data = None
    if fetch:
        data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return data

# Halaman: Home
def home():
    st.title("🎓 Sistem Pembayaran Uang Kuliah Mahasiswa")
    st.image("https://images.unsplash.com/photo-1571260899304-425eee4c7efc", use_column_width=True)
    st.markdown("""
        Selamat datang di sistem manajemen pembayaran kuliah. Anda dapat:

        - Menginput dan mengecek biaya kuliah
        - Mengelola pembayaran angsuran
        - Melihat laporan pembayaran lunas dan belum lunas
    """)

# Halaman: Input Biaya Kuliah
def input_biaya_kuliah():
    st.header("Input Biaya Kuliah")
    with st.form("form_biaya"):
        program_studi = st.selectbox("Program Studi", [
            "Teknik Informatika", 
            "Teknik Mesin", 
            "Teknik Industri", 
            "Teknik Tekstil", 
            "Teknik BOM"
        ])
        nim = st.text_input("NIM")
        nama = st.text_input("Nama")
        sks_kuliah = st.number_input("SKS Kuliah", min_value=0)
        tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
        semester = st.selectbox("Semester", ["Ganjil", "Genap"])
        biaya = st.number_input("Biaya Kuliah", min_value=0.0, format="%.2f")
        
        # Tombol submit
        submit = st.form_submit_button("Simpan")
        
        # Tombol-tombol lainnya
        tombol_cari = st.form_submit_button("Cari")
        tombol_hapus = st.form_submit_button("Hapus")
        tombol_cek_biaya = st.form_submit_button("Cek Biaya")
        
        if submit:
            # Simpan data
            query = '''INSERT INTO biaya_kuliah
                       (program_studi, nim, nama, sks_kuliah, tahun, semester, biaya_total)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            run_query(query, (program_studi, nim, nama, sks_kuliah, tahun, semester, biaya))
            st.success("Biaya kuliah berhasil disimpan.")
        
        if tombol_cari:
            # Cari data berdasarkan NIM
            query = '''SELECT * FROM biaya_kuliah WHERE nim = %s'''
            results = run_query(query, (nim,), fetch=True)
            if results:
                st.dataframe(results)
            else:
                st.warning("Data tidak ditemukan.")
        
        if tombol_hapus:
            # Hapus data berdasarkan NIM
            query = '''DELETE FROM biaya_kuliah WHERE nim = %s'''
            run_query(query, (nim,))
            st.success("Data biaya kuliah berhasil dihapus.")
        
        if tombol_cek_biaya:
            # Cek total biaya kuliah berdasarkan NIM
            query = '''SELECT biaya_total FROM biaya_kuliah WHERE nim = %s'''
            result = run_query(query, (nim,), fetch=True)
            if result:
                st.write(f"Total Biaya Kuliah: Rp {result[0][0]:,.2f}")
            else:
                st.warning("Data biaya kuliah tidak ditemukan.")

# Halaman: Bayar Angsuran Biaya Kuliah
def bayar_angsuran():
    st.header("Bayar Angsuran Biaya Kuliah")
    with st.form("form_angsuran"):
        program_studi = st.selectbox("Program Studi", [
            "Teknik Informatika", 
            "Teknik Mesin", 
            "Teknik Industri", 
            "Teknik Tekstil", 
            "Teknik BOM"
        ])
        nim = st.text_input("NIM")
        nama = st.text_input("Nama")
        angsuran_ke = st.number_input("Angsuran Ke-", min_value=1)
        tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
        semester = st.selectbox("Semester", ["Ganjil", "Genap"])
        tanggal = st.date_input("Tanggal", value=date.today())
        bayar = st.number_input("Jumlah Bayar", min_value=0.0, format="%.2f")
        
        # Tombol submit
        submit = st.form_submit_button("Simpan")
        
        # Tombol lainnya
        tombol_cari = st.form_submit_button("Cari")
        tombol_hapus = st.form_submit_button("Hapus")
        
        if submit:
            # Simpan data angsuran
            query = '''INSERT INTO angsuran_kuliah
                       (program_studi, nim, nama, angsuran_ke, tahun, semester, tanggal_pembayaran, jumlah_bayar)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            run_query(query, (program_studi, nim, nama, angsuran_ke, tahun, semester, tanggal, bayar))
            st.success("Pembayaran angsuran berhasil disimpan.")
        
        if tombol_cari:
            # Cari data berdasarkan NIM dan angsuran ke-
            query = '''SELECT * FROM angsuran_kuliah WHERE nim = %s AND angsuran_ke = %s'''
            results = run_query(query, (nim, angsuran_ke), fetch=True)
            if results:
                st.dataframe(results)
            else:
                st.warning("Data angsuran tidak ditemukan.")
        
        if tombol_hapus:
            # Hapus data angsuran berdasarkan NIM dan angsuran ke-
            query = '''DELETE FROM angsuran_kuliah WHERE nim = %s AND angsuran_ke = %s'''
            run_query(query, (nim, angsuran_ke))
            st.success("Data angsuran berhasil dihapus.")

# Halaman: Pencarian Angsuran
def cari_angsuran():
    st.header("Pencarian Angsuran Biaya Kuliah")
    program_studi = st.selectbox("Program Studi", [
        "Teknik Informatika", 
        "Teknik Mesin", 
        "Teknik Industri", 
        "Teknik Tekstil", 
        "Teknik BOM"
    ])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    tanggal = st.date_input("Tanggal")

    if st.button("Cari"):
        query = '''
        SELECT nim, nama, angsuran_ke, tanggal_pembayaran, jumlah_bayar
        FROM angsuran_kuliah
        WHERE program_studi = %s AND tahun = %s AND semester = %s AND tanggal_pembayaran = %s
        '''
        results = run_query(query, (program_studi, tahun, semester, tanggal), fetch=True)
        st.dataframe(results, use_container_width=True)

def laporan_lunas():
    st.header("Laporan Angsuran Lunas")
    
    program_studi = st.radio("Program Studi", [
        "Teknik Informatika", 
        "Teknik Mesin", 
        "Teknik Industri", 
        "Teknik Tekstil", 
        "Teknik BOM"
    ])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    
    if st.button("Cari Lunas"):
        # Query untuk mendapatkan angsuran yang sudah lunas
        query = '''
            SELECT nim, nama, angsuran_ke, jumlah_bayar, tanggal_pembayaran
            FROM angsuran_kuliah
            WHERE program_studi = %s AND tahun = %s AND semester = %s
            GROUP BY nim, nama, angsuran_ke, jumlah_bayar, tanggal_pembayaran
            HAVING SUM(jumlah_bayar) >= (SELECT biaya_total FROM biaya_kuliah WHERE nim = angsuran_kuliah.nim)
        '''
        
        try:
            results = run_query(query, (program_studi, tahun, semester), fetch=True)
            if results:
                st.dataframe(results)
            else:
                st.warning("Tidak ada data angsuran yang lunas untuk kriteria tersebut.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mengambil data: {str(e)}")

def laporan_belum_lunas():
    st.header("Laporan Angsuran Belum Lunas")
    
    program_studi = st.radio("Program Studi", [
        "Teknik Informatika", 
        "Teknik Mesin", 
        "Teknik Industri", 
        "Teknik Tekstil", 
        "Teknik BOM"
    ])
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    
    if st.button("Cari Belum Lunas"):
        # Query untuk mendapatkan angsuran yang belum lunas
        query = '''
            SELECT nim, nama, angsuran_ke, jumlah_bayar, tanggal_pembayaran
            FROM angsuran_kuliah
            WHERE program_studi = %s AND tahun = %s AND semester = %s
            GROUP BY nim, nama, angsuran_ke, jumlah_bayar, tanggal_pembayaran
            HAVING SUM(jumlah_bayar) < (SELECT biaya_total FROM biaya_kuliah WHERE nim = angsuran_kuliah.nim)
        '''
        
        try:
            results = run_query(query, (program_studi, tahun, semester), fetch=True)
            if results:
                st.dataframe(results)
            else:
                st.warning("Tidak ada data angsuran yang belum lunas untuk kriteria tersebut.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mengambil data: {str(e)}")


# Navigasi
menu = st.sidebar.radio("Menu", [
    "Home", 
    "Input Biaya Kuliah", 
    "Bayar Angsuran", 
    "Pencarian Angsuran", 
    "Laporan Sudah Lunas", 
    "Laporan Belum Lunas"])

if menu == "Home":
    home()
elif menu == "Input Biaya Kuliah":
    input_biaya_kuliah()
elif menu == "Bayar Angsuran":
    bayar_angsuran()
elif menu == "Pencarian Angsuran":
    cari_angsuran()
elif menu == "Laporan Sudah Lunas":
    laporan_lunas()
elif menu == "Laporan Belum Lunas":
    laporan_belum_lunas()
