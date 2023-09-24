import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def load_model():
    with open('random_forest_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model
model = load_model()

@st.cache(suppress_st_warning=True)
def get_fvalue(val):
    feature_dict = {"No":1, "Yes":2}
    for key, value in feature_dict.items():
        if val==key:
            return value
        
def get_value(val,my_dict):
    for key, value in my_dict.items():
        if val==key:
            return value
        
app_mode = st.sidebar.selectbox("Select Page", ["Home", "Prediksi pinjaman"])
if app_mode=='Home':
    st.title('Prediksi pinjaman')
    st.write('Dibuat dengan hati oleh tim Elang merpati21 💖💖💖')
    st.write('1. Ketua = Asep Saepul Anwar')
    st.write('2. Anggota = Guruh Maulana')
    st.write('3. Anggota = Febi Marzeta')
    st.image('deal-loan.jpg')
    st.markdown('Dataset :')
    data = pd.read_csv('dataset3.csv')
    st.write(data.head())
    st.markdown('Perkirakan umur kamu dengan prediksi persetujuan pinjaman dari bank.')
    st.bar_chart(data[['Age','Status']].head(20))

elif app_mode == 'Prediksi pinjaman':
    st.title('Aplukasi Kredit pinjaman')
    st.image('credit-loan.jpg')
    st.subheader('Halo, tolong isi semua informasi yang dibutuhkan, agar mendapatkan balasan untuk permintaan pinjaman anda!')
    st.sidebar.header("Infomasi peminjam Melalui file:")
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
    else:
        def input_user():
            st.sidebar.header('Atau')
            st.sidebar.header('Masukan Data Manual:')
            Age = st.sidebar.number_input('Usia', min_value=20, max_value=100, step=1)
            income = st.sidebar.number_input('Pendapatan($)', min_value=4000, step=100)
            Emp_length = st.sidebar.number_input('Lama kerja(dalam tahun)', min_value=0, step=10)
            Amount = st.sidebar.number_input('Berapa anda ingin meminjam?($)', min_value=500, step=100)
            Rate = st.sidebar.number_input('Suku bunga pinjaman(%)', min_value=5.42)
            Cred_length = st.sidebar.number_input('Lama pinjaman(dalam tahun)', min_value=2, step=100)
            Home = st.sidebar.selectbox('Kepemilikan rumah anda', options=['Hipotek', 'Pribadi', 'Sewa', 'Lainnya'])
            intent = st.sidebar.selectbox('Untuk apa anda meminjam?', options=['Debtconsolidasi', 'Pendidikan', 'Perbaikan rumah','Medis', 'Kebutuhan pribadi','Model usaha'])
            riwayat = st.sidebar.selectbox('Pernah meminjam sebelumnya?', options=['Tidak pernah','Pernah'])

            # Tambahkan input untuk fitur lain sesuai kebutuhan
            HOME_MORTGAGE, HOME_OTHER, HOME_OWN, HOME_RENT = 0,0,0,0
            if Home == 'Hipotik':
                HOME_MORTGAGE = 1
            elif Home == 'Pribadi':
                HOME_OWN = 1
            elif Home == 'Sewa':
                HOME_RENT = 1
            else:
                HOME_OTHER = 1
            Intent_DEBTCONSOLIDATION, Intent_EDUCATION, Intent_HOMEIMPROVEMENT, Intent_MEDICAL, Intent_PERSONAL, Intent_VENTURE = 0,0,0,0,0,0
            if intent == 'Debtconsolidasi':
                Intent_DEBTCONSOLIDATION = 1
            elif intent == 'Pendidikan':
                Intent_EDUCATION = 1
            elif intent == 'Perbaikan rumah':
                Intent_HOMEIMPROVEMENT = 1
            elif intent == 'Medis':
                Intent_MEDICAL = 1
            elif intent == 'Kebutuhan pribadi':
                Intent_PERSONAL = 1
            else:
                Intent_VENTURE = 1

            Default_N, Default_Y = 0,0
            if riwayat == 'Tidak pernah':
                Default_N = 1
            else:
                Default_Y = 1 
                
            data = {
                'Usia':[Age],
                'Pendapatan':[income],
                'Lama bekerja':[Emp_length],
                'Pinjaman yang diajukan':[Amount],
                'Rate':[Rate],
                'Rumah_hipotik':[HOME_MORTGAGE],
                'Rumah pribadi':[HOME_OWN],
                'Rumah_sewa':[HOME_RENT],
                'Rumah_lainnya':[HOME_OTHER],
                'Tujuan_debtconsolidasi':[Intent_DEBTCONSOLIDATION],
                'Tujuan_pendidikan':[Intent_EDUCATION],
                'Tujuan_perbaikan_rumah':[Intent_HOMEIMPROVEMENT],
                'Tujuan_medis':[Intent_MEDICAL],
                'Tujuan_kebutuhan_pribadi':[Intent_PERSONAL],
                'Tujuan_modal_Usaha':[Intent_VENTURE],
                'Tidak pernah_meminjam':[Default_N],
                'Pernah_meminjam':[Default_Y]
            }
            features = pd.DataFrame(data)
            return features
        input_df = input_user()
        # Inisialisasi pipeline dengan normalisasi, Label Encoder, dan Random Forest
        pipeline = Pipeline([
            ('scaler', StandardScaler())  # Random Forest
        ])
        pipeline.fit(input_df)
        # Displays the user input features
        if st.sidebar.button('Prediksi'):
            st.subheader('Masukkan pengguna')
            st.write(input_df)
            st.text('')
            prediction = model.predict(input_df)
            if prediction[0] == 1:
                st.write("Hasil Prediksi: Layak untuk pinjaman")
            else:
                st.write("Hasil Prediksi: Tidak layak untuk pinjaman")