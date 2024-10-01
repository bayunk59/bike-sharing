import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set seaborn style
sns.set(style='dark')

def jumlah_penyewa(df):
    jumlah_penyewa = df.groupby(["dteday"])[["cnt"]].sum().reset_index()
    return jumlah_penyewa

def jumlah_penyewa_hari_libur(df, jenis_hari):
    jumlah_penyewa = df[df['holiday'] == jenis_hari]['cnt'].sum()
    return jumlah_penyewa  

def jam_rame_non_holiday(df):
    non_holiday_df = df[df["holiday"] == "Non-holiday"]
    non_holiday_grouped = non_holiday_df.groupby(by="hr").agg({"cnt": "sum"})
    return non_holiday_grouped

# Membaca data penyewa 
newHours_df = pd.read_csv("newHours.csv")

# Judul dashboard
st.header("Collection Dashboard : Bike Sharing")
st.subheader("Bayun Kurniawan")

# Mengubah kolom dteday ke datetime
newHours_df["dteday"] = pd.to_datetime(newHours_df["dteday"])

# Membuat filter dengan widget date
min_date = newHours_df["dteday"].min()
max_date = newHours_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://play-lh.googleusercontent.com/P_PSOKvARCq6SUcl1oddA2W5a4xYRGwkf8r8fuBvZW_s5IUQ_qEprYBjeYo9fyGBCQ")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal
main_df = newHours_df[(newHours_df["dteday"] >= str(start_date)) & 
                    (newHours_df["dteday"] <= str(end_date))]

# Menghitung jumlah penyewa yang ada di main_df
penyewa = jumlah_penyewa(main_df)

# Visualisasi jumlah penyewa per hari
st.subheader("Jumlah Penyewa Sepeda")

col1, col2 = st.columns(2)
with col1:
    total_penyewa = penyewa.cnt.sum()
    st.metric("Total penyewa", value=total_penyewa)
with col2:
    rata_penyewa = penyewa.cnt.mean()
    st.metric("Rata-rata penyewa", value=rata_penyewa)    
    
plt.figure(figsize=(12, 6))
sns.lineplot(data=penyewa, x="dteday", y="cnt", marker='o')
plt.title("Jumlah Penyewa Sepeda")
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Penyewa")
st.pyplot(plt)

# Visualisasi jumlah penyewa berdasarkan hari libur
st.subheader("Jumlah Penyewa Sepeda Berdasarkan Hari Libur dan Tidak Libur")

# Membuat dua kolom untuk total penyewa dan rata-rata penyewa
col1, col2 = st.columns(2)

# Menghitung total penyewa untuk hari libur (holiday == 1) dan hari tidak libur (Non-holiday == 0)
total_holiday = main_df[main_df['holiday'] == "Holiday"]['cnt'].sum()
total_non_holiday = main_df[main_df['holiday'] == "Non-holiday"]['cnt'].sum()
# Menghitung rata-rata penyewa
rata_penyewa_holiday = main_df[main_df['holiday'] == "Holiday"]['cnt'].mean()
rata_penyewa_non_holiday = main_df[main_df['holiday'] == "Non-holiday"]['cnt'].mean()

# Menampilkan total dan rata-rata penyewa untuk hari libur dan tidak libur
with col1:
    st.metric("Total Penyewa pada Hari Libur", value=total_holiday)
    st.metric("Rata-rata Penyewa pada Hari Libur", value=rata_penyewa_holiday)
with col2:
    st.metric("Total Penyewa pada Hari Tidak Libur", value=total_non_holiday)
    st.metric("Rata-rata Penyewa pada Hari Tidak Libur", value=rata_penyewa_non_holiday)

# Visualisasi jumlah penyewa berdasarkan hari libur dan tidak libur
plt.figure(figsize=(12, 6))
sns.barplot(x=["Holiday", "Non-holiday"], y=[total_holiday, total_non_holiday])
plt.title("Jumlah Penyewa Sepeda pada Hari Libur vs Tidak Libur")
plt.xlabel("Kategori Hari")
plt.ylabel("Jumlah Penyewa")
st.pyplot(plt)

# Visualisasi jumlah penyewa berdasarkan jam
st.subheader("Jumlah Penyewa Sepeda Berdasarkan Jam")

# Mengelompokkan data berdasarkan jam untuk hari libur dan tidak libur
penyewa_per_jam_holiday = main_df[main_df['holiday'] == "Holiday"].groupby('hr')['cnt'].sum().reset_index()
penyewa_per_jam_non_holiday = main_df[main_df['holiday'] == "Non-holiday"].groupby('hr')['cnt'].sum().reset_index()

#Menentukan jam paling rame
# Menentukan jam paling ramai pada hari libur
jam_rame_holiday = main_df[main_df['holiday'] == "Holiday"].groupby('hr')['cnt'].sum().reset_index()
jam_teramai_holiday = jam_rame_holiday[jam_rame_holiday['cnt'] == jam_rame_holiday['cnt'].max()]

# Menentukan jam paling ramai pada hari tidak libur
jam_rame_non_holiday = main_df[main_df['holiday'] == "Non-holiday"].groupby('hr')['cnt'].sum().reset_index()
jam_teramai_non_holiday = jam_rame_non_holiday[jam_rame_non_holiday['cnt'] == jam_rame_non_holiday['cnt'].max()]

# Menampilkan hasil di dashboard
st.subheader("Jam Paling Ramai Penyewa Sepeda")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Jam Paling Ramai (Hari Libur)", value=f"{int(jam_teramai_holiday['hr'].values[0])}:00")
    st.write(f"Jumlah Penyewa: {int(jam_teramai_holiday['cnt'].values[0])}")

with col2:
    st.metric(label="Jam Paling Ramai (Hari Tidak Libur)", value=f"{int(jam_teramai_non_holiday['hr'].values[0])}:00")
    st.write(f"Jumlah Penyewa: {int(jam_teramai_non_holiday['cnt'].values[0])}")

# Membuat dua kolom untuk menampilkan grafik secara berdampingan
col1, col2 = st.columns(2)

# Membuat dua kolom untuk menampilkan grafik secara berdampingan
col1, col2 = st.columns(2)

# Visualisasi jumlah penyewa per jam pada hari libur
with col1:
    st.write("Jumlah Penyewa Sepeda pada Hari Libur")
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=penyewa_per_jam_holiday, x='hr', y='cnt', marker='o', color="blue")
    plt.title("Jumlah Penyewa Sepeda per Jam (Hari Libur)")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Penyewa")
    st.pyplot(plt)

# Visualisasi jumlah penyewa per jam pada hari tidak libur
with col2:
    st.write("Jumlah Penyewa Sepeda pada Hari Tidak Libur")
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=penyewa_per_jam_non_holiday, x='hr', y='cnt', marker='o', color="green")
    plt.title("Jumlah Penyewa Sepeda per Jam (Hari Tidak Libur)")
    plt.xlabel("Jam")
    plt.ylabel("Jumlah Penyewa")
    st.pyplot(plt)