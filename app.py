import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Sistem Pembayaran Kuliah", layout="wide")

st.title("📚 Sistem Pembayaran Uang Kuliah Mahasiswa")

menu = st.sidebar.radio("Menu", [
    "Input Biaya Kuliah",
    "Bayar Angsuran",
    "Pencarian Pembayaran",
    "Laporan Lunas",
    "Laporan Belum Lunas"
])

if menu == "Input Biaya Kuliah":
    st.header("💰 Input Biaya Kuliah")
    col1, col2 = st.columns(2)
    with col1:
        program_studi = st.text_input("Program Studi")
        nim = st.text_input("NIM")
        nama = st.text_input("Nama")
        sks = st.number_input("Jumlah SKS", min_value=0)
    with col2:
        tahun = st.text_input("Tahun Ajaran")
        semester = st.selectbox("Semester", ["Ganjil", "Genap"])
        biaya_kuliah = st.number_input("Biaya Kuliah", min_value=0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Simpan"):
            st.success("Data biaya kuliah disimpan (dummy).")
    with col2:
        if st.button("Hapus"):
            st.warning("Data biaya kuliah dihapus (dummy).")
    with col3:
        if st.button("Cari"):
            st.info("Hasil pencarian (dummy).")
    with col4:
        if st.button("Cek Biaya"):
            st.info(f"Total biaya untuk {sks} SKS: Rp {sks * 150000} (contoh perhitungan dummy)")

elif menu == "Bayar Angsuran":
    st.header("💳 Bayar Angsuran Biaya Kuliah")
    col1, col2 = st.columns(2)
    with col1:
        program_studi = st.text_input("Program Studi")
        nim = st.text_input("NIM")
        nama = st.text_input("Nama")
        angsuran_ke = st.number_input("Angsuran Ke-", min_value=1)
    with col2:
        tahun = st.text_input("Tahun Ajaran")
        semester = st.selectbox("Semester", ["Ganjil", "Genap"])
        tanggal = st.date_input("Tanggal Bayar", datetime.today())
        bayar = st.number_input("Jumlah Bayar", min_value=0)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Simpan"):
            st.success("Pembayaran disimpan (dummy).")
    with col2:
        if st.button("Hapus"):
            st.warning("Pembayaran dihapus (dummy).")
    with col3:
        if st.button("Cari"):
            st.info("Hasil pencarian pembayaran (dummy).")

elif menu == "Pencarian Pembayaran":
    st.header("🔍 Pencarian Pembayaran Angsuran")
    col1, col2 = st.columns(2)
    with col1:
        program_studi = st.text_input("Program Studi")
        tahun = st.text_input("Tahun Ajaran")
        semester = st.selectbox("Semester", ["Ganjil", "Genap"])
    with col2:
        tanggal = st.date_input("Tanggal")
        bulan = st.selectbox("Bulan", [f"{i:02d}" for i in range(1, 13)])

    if st.button("Cari"):
        st.info("Menampilkan hasil pencarian pembayaran (dummy).")

elif menu == "Laporan Lunas":
    st.header("✅ Laporan Pembayaran Sudah Lunas")
    program_studi = st.text_input("Program Studi")
    tahun = st.text_input("Tahun Ajaran")
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])

    if st.button("Cari"):
        st.success("Menampilkan data yang sudah lunas (dummy).")

elif menu == "Laporan Belum Lunas":
    st.header("❌ Laporan Pembayaran Belum Lunas")
    program_studi = st.text_input("Program Studi")
    tahun = st.text_input("Tahun Ajaran")
    semester = st.selectbox("Semester", ["Ganjil", "Genap"])

    if st.button("Cari"):
        st.warning("Menampilkan data yang belum lunas (dummy).")
