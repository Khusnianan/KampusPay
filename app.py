import streamlit as st
import psycopg2
from datetime import date
import io
from PIL import Image


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

def home():
    # ===== STYLE CUSTOMIZATION =====
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .main-title {
            color: #2b5876;
            font-size: 2.8rem !important;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .sub-title {
            color: #4e4376;
            font-size: 1.2rem !important;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .welcome-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        }
        
        .action-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.75rem 2rem !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }
        
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== HEADER SECTION =====
    st.markdown('<p class="main-title">🎓 Sistem Pembayaran Kuliah</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Universitas Bina Nusantara</p>', unsafe_allow_html=True)
    
    # ===== HERO SECTION =====
    with st.container():
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown("""
            <div class="welcome-card">
                <h2 style="color: #2b5876;">Selamat Datang!</h2>
                <p style="font-size: 1.1rem;">
                    Sistem terpadu untuk mengelola pembayaran kuliah mahasiswa 
                    dengan mudah dan efisien. Mulai kelola pembayaran sekarang 
                    dengan mengklik tombol di bawah.
                </p>
                <div style="text-align: center; margin-top: 2rem;">
                    <button class="action-btn">Masuk ke Dashboard</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Placeholder untuk ilustrasi (bisa diganti dengan gambar asli)
            st.image("https://cdn-icons-png.flaticon.com/512/3132/3132693.png", 
                    width=300, caption="Ilustrasi Pembayaran Digital")

    # ===== QUICK STATS SECTION =====
    st.markdown("---")
    st.subheader("📊 Statistik Singkat")
    
    stats_cols = st.columns(4)
    with stats_cols[0]:
        st.metric("Total Mahasiswa", "1,245", "+15 baru")
    with stats_cols[1]:
        st.metric("Pembayaran Lunas", "876", "70%")
    with stats_cols[2]:
        st.metric("Sedang Angsuran", "315", "25%")
    with stats_cols[3]:
        st.metric("Tunggakan", "54", "5%")

    # ===== FOOTER =====
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin: 2rem 0;">
        <p>© 2023 Bagian Keuangan Universitas Bina Nusantara</p>
        <p style="font-size: 0.8rem;">Versi 2.1.0 | Terakhir diperbarui: 15 November 2023</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    home()
    
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
    
    program_studi = st.selectbox("Program Studi", [
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
    
    program_studi = st.selectbox("Program Studi", [
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
