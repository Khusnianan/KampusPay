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
        program_studi = st.text_input("Program Studi")
        nim = st.text_input("NIM")
        nama = st.text_input("Nama")
        sks_kuliah = st.number_input("SKS Kuliah", min_value=0)
        tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
        semester = st.selectbox("Semester", ["Ganjil", "Genap"])
        biaya = st.number_input("Biaya Kuliah", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Simpan")

        if submit:
            query = '''INSERT INTO biaya_kuliah
                       (program_studi, nim, nama, sks_kuliah, tahun, semester, biaya_total)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            run_query(query, (program_studi, nim, nama, sks_kuliah, tahun, semester, biaya))
            st.success("Biaya kuliah berhasil disimpan.")

# Halaman: Bayar Angsuran
def bayar_angsuran():
    st.header("Bayar Angsuran Biaya Kuliah")
    with st.form("form_angsuran"):
        program_studi = st.text_input("Program Studi")
        nim = st.text_input("NIM")
        nama = st.text_input("Nama")
        angsuran_ke = st.number_input("Angsuran Ke-", min_value=1)
        tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
        semester = st.selectbox("Semester", ["Ganjil", "Genap"])
        tanggal = st.date_input("Tanggal", value=date.today())
        bayar = st.number_input("Jumlah Bayar", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Simpan")

        if submit:
            query = '''INSERT INTO angsuran_kuliah
                       (program_studi, nim, nama, angsuran_ke, tahun, semester, tanggal_pembayaran, jumlah_bayar)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            run_query(query, (program_studi, nim, nama, angsuran_ke, tahun, semester, tanggal, bayar))
            st.success("Pembayaran angsuran berhasil disimpan.")

# Halaman: Laporan Pembayaran Sudah Lunas
def laporan_lunas():
    st.header("Laporan Mahasiswa Lunas")
    program_studi = st.text_input("Program Studi")
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])

    if st.button("Cari"):
        query = '''
        SELECT b.nim, b.nama, b.biaya_total, SUM(a.jumlah_bayar) AS total_bayar
        FROM biaya_kuliah b
        JOIN angsuran_kuliah a ON a.nim = b.nim
        WHERE b.program_studi = %s AND b.tahun = %s AND b.semester = %s
        GROUP BY b.nim, b.nama, b.biaya_total
        HAVING SUM(a.jumlah_bayar) >= b.biaya_total
        '''
        results = run_query(query, (program_studi, tahun, semester), fetch=True)
        st.dataframe(results, use_container_width=True)

# Halaman: Laporan Belum Lunas
def laporan_belum_lunas():
    st.header("Laporan Mahasiswa Belum Lunas")
    program_studi = st.text_input("Program Studi")
    tahun = st.number_input("Tahun", min_value=2000, max_value=2100)
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])

    if st.button("Cari"):
        query = '''
        SELECT b.nim, b.nama, b.biaya_total, COALESCE(SUM(a.jumlah_bayar), 0) AS total_bayar
        FROM biaya_kuliah b
        LEFT JOIN angsuran_kuliah a ON a.nim = b.nim
        WHERE b.program_studi = %s AND b.tahun = %s AND b.semester = %s
        GROUP BY b.nim, b.nama, b.biaya_total
        HAVING COALESCE(SUM(a.jumlah_bayar), 0) < b.biaya_total
        '''
        results = run_query(query, (program_studi, tahun, semester), fetch=True)
        st.dataframe(results, use_container_width=True)

# Halaman: Pencarian Angsuran
def cari_angsuran():
    st.header("Pencarian Angsuran Biaya Kuliah")
    program_studi = st.text_input("Program Studi")
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

# Navigasi
menu = st.sidebar.selectbox("Menu", [
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
