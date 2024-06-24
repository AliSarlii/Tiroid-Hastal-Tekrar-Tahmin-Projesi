import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Arayüzü yapmak için ChatGPT'den yardım aldık

def submit_form():
    #inputlardan çektiğimiz verileri testveri adlı dizide topluyoruz
    testveri = []
    testveri.append(int(age_entry.get()))
    testveri.append(gender.get())
    testveri.append(smoking_now.get())
    testveri.append(smoking_past.get())
    testveri.append(radiotherapy.get())
    testveri.append(troid_type.get())
    testveri.append(troid_location.get())
    if(adenopathy.get()=="hayır"):
        testveri.append("No")
    if(adenopathy.get()=="sağ"):
        testveri.append("Right")
    if(adenopathy.get()=="sol"):
        testveri.append("Left")
    if(adenopathy.get()=="yaygın"):
        testveri.append("Extensive")
    if(adenopathy.get()=="iki-tarafta"):
        testveri.append("Bilateral")
    if(adenopathy.get()=="arka-tarafında"):
        testveri.append("Posterior")
    testveri.append(tissue_result.get())
    if(tumor_location.get()=="Tekli-Noktada"):
        testveri.append("Uni-Focal")
    if(tumor_location.get()=="çoklu-noktalarda"):
        testveri.append("Multi-Focal")
    if(risk.get()=="düşük"):
        testveri.append("Low")
    if(risk.get()=="Orta"):
        testveri.append("Intermediate")
    if(risk.get()=="yüksek"):
        testveri.append("High")
    testveri.append(t_value.get())
    testveri.append(n_value.get())
    testveri.append(m_value.get())
    if(stage.get()=="1"):
        testveri.append("I")
    if(stage.get()=="2"):
        testveri.append("II")
    if(stage.get()=="3"):
        testveri.append("III")
    if(stage.get()=="4a"):
        testveri.append("IVA")
    if(stage.get()=="4b"):
        testveri.append("IVB")
    if(response.get()=="olumlu"):
        testveri.append("Excellent")
    elif(response.get()=="belirsiz"):
        testveri.append("Indeterminate")
    else:
        testveri.append(response.get())
    testVeri = []
    testVeri.append(testveri)
    print(testVeri)

    #burdan sonraki sonucu ekrana yazdırıncaya kadarki işlemler ana modelle aynı
    data = pd.read_csv("Thyroid_Diff.csv")

    y=data.pop("Recurred")

    sutun=data.columns
    testVeri=pd.DataFrame(testVeri,columns=sutun)
    merged_data = pd.concat([data, testVeri], axis=0, ignore_index=True)
    data = merged_data

    le=LabelEncoder()
    y=le.fit_transform(y)

    columns_to_encode = ['Gender', 'Smoking', 'Hx Smoking', 'Hx Radiothreapy',
        'Thyroid Function', 'Physical Examination', 'Adenopathy', 'Pathology',
        'Focality', 'Risk', 'T', 'N', 'M', 'Stage', 'Response']
    ct = ColumnTransformer([('onehot', OneHotEncoder(), columns_to_encode)], remainder='passthrough')
    data_encoded = ct.fit_transform(data).toarray()
    x = data_encoded

    x = pd.DataFrame(x)
    testveridonusum = pd.DataFrame(x.iloc[-1]).transpose()
    x.drop([len(x)-1], axis=0, inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    print(y_test)

    svm_model = SVC(kernel='linear', random_state=42)
    svm_model.fit(X_train, y_train)

    y_pred = svm_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Model Accuracy:", accuracy)

    testVeriPred=svm_model.predict(testveridonusum)
    print("Test verisinin sonucu : ",testVeriPred)

    result_window = tk.Toplevel(root)
    result_window.title("Sonuçlar")

    #kullanıcının girdiği verileri ekrana yazdırma
    data_frame = tk.LabelFrame(result_window, text="Verileriniz")
    data_frame.pack(padx=5, pady=5, fill="x", expand="false", anchor="nw")

    tk.Label(data_frame, text="Yaşınız: " + age_entry.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="Cinsiyetiniz: " + gender.get(), anchor="w", justify="left").pack(fill="both")
    if(smoking_now.get()=="Yes"):
        tk.Label(data_frame, text="Şu an sigara içiyor musunuz: " + "Evet", anchor="w", justify="left").pack(fill="both")
    if(smoking_now.get()=="No"):
        tk.Label(data_frame, text="Şu an sigara içiyor musunuz: " + "Hayır", anchor="w", justify="left").pack(fill="both")
    if(smoking_past.get()=="Yes"):
        tk.Label(data_frame, text="Geçmişte sigara içtiniz mi: " + "Evet", anchor="w", justify="left").pack(fill="both")
    if(smoking_past.get()=="No"):
        tk.Label(data_frame, text="Geçmişte sigara içtiniz mi: " + "Hayır", anchor="w", justify="left").pack(fill="both")
    if(radiotherapy.get()=="Yes"):
        tk.Label(data_frame, text="Hiç radyoterapi tedavisi aldınız mı: " + "Evet", anchor="w", justify="left").pack(fill="both")
    if(radiotherapy.get()=="No"):
        tk.Label(data_frame, text="Hiç radyoterapi tedavisi aldınız mı: " + "Hayır", anchor="w", justify="left").pack(fill="both")
    
    
    tk.Label(data_frame, text="Hangi tür troidiniz vardı: " + troid_type.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="Fiziksel Muayenede hangi taraflarda troidiniz vardı: " + troid_location.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="Lenf bezlerinizde anormal bir büyüme var mıydı: " + adenopathy.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="Doku örneği sonucunuz neydi: " + tissue_result.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="Tümör tek noktada mı çoklu noktalarda mıydı: " + tumor_location.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="Risk durumunuz neydi: " + risk.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="T değeri (Tümör boyutu ve yayılma derecesi) neydi: " + t_value.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="N değeri (Kanserin lenf nodlarında yayılma durumu) neydi: " + n_value.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="M değeri (Kanserin metastaz yapıyor mu) yayıldı mı: " + m_value.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="Kaçıncı aşamadaydı: " + stage.get(), anchor="w", justify="left").pack(fill="both")
    tk.Label(data_frame, text="Tedaviye verilen yanıt neydi: " + response.get(), anchor="w", justify="left").pack(fill="both")


    result_frame = tk.LabelFrame(result_window, text="Sonuç")
    result_frame.pack(padx=5, pady=5, fill="x", expand="false")

    # Sonuca göre kullanıcıya çıktı veriyoruz
    result_label = tk.Label(result_frame, text="")
    if testVeriPred[0] == 1:
        result_label.config(text="Dikkatli olunuz. Tekrardan troid hastalığını geçirebilirsiniz.",fg="red" )
    elif testVeriPred[0] == 0:
        result_label.config(text="Geçmiş olsun. Tekrardan troid hastalığını geçirme riskiniz çok düşük." , fg="green")
    result_label.pack(pady=5, padx=5, anchor="nw")

    #modelimizdeki gerçek sonuçlar ile modelin tahmin ettiği sonuçları grafikte gösteriyoruz 
    grafik_frame = tk.LabelFrame(result_window, text="Model Analizi", width=500, height=800)
    grafik_frame.pack(padx=5, pady=5, fill="x", expand="false", anchor="nw")
    grafik_label = tk.Label(grafik_frame, text="")
    grafik_label.pack(pady=5, padx=5)
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.plot(range(len(y_pred)), y_pred, label='Tahminler', marker='o')
    ax.plot(range(len(y_test)), y_test, label='Gerçek Değerler', marker='x')
    ax.set_title('Tahminler ve Gerçek Değerler')
    ax.set_xlabel('Örnek Numarası')
    ax.set_ylabel('Sınıf')
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=grafik_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    modelbilgi1 = tk.Label(grafik_label, text="Kullanılan Model : Support Vector Machine")
    modelbilgi1.pack(pady=5, padx=5)

    #modelin doğruluğunu yazdırıyoruz
    modelbilgi2 = tk.Label(grafik_label, text="Modelin Doğruluğu : "+ str(accuracy))
    modelbilgi2.pack(pady=5, padx=5)
    root.mainloop()

# Form ekranını oluşturma
root = tk.Tk()
root.title("Hasta Bilgi Formu")

# Yaş
age_label = ttk.Label(root, text="Yaşınız:")
age_label.grid(row=0, column=0, padx=10, pady=5)
age_entry = ttk.Entry(root)
age_entry.insert(0, "0")
age_entry.grid(row=0, column=1, padx=10, pady=5)

# Cinsiyet
gender_label = ttk.Label(root, text="Cinsiyetiniz:")
gender_label.grid(row=1, column=0, padx=10, pady=5)
gender = tk.StringVar(value="F")
male_check = ttk.Checkbutton(root, text="Erkek", variable=gender, onvalue="M", offvalue="")
male_check.grid(row=1, column=1, padx=10, pady=5)
female_check = ttk.Checkbutton(root, text="Kadın", variable=gender, onvalue="F", offvalue="")
female_check.grid(row=1, column=2, padx=10, pady=5)

# Şu an sigara içiyor musunuz?
smoking_now_label = ttk.Label(root, text="Şu an sigara içiyor musunuz?")
smoking_now_label.grid(row=2, column=0, padx=10, pady=5)
smoking_now = tk.StringVar(value="No")
smoking_now_check = ttk.Checkbutton(root, text="Evet", variable=smoking_now, onvalue="Yes", offvalue="")
smoking_now_check.grid(row=2, column=1, padx=10, pady=5)
smoking_now_check = ttk.Checkbutton(root, text="Hayır", variable=smoking_now, onvalue="No", offvalue="")
smoking_now_check.grid(row=2, column=2, padx=10, pady=5)

# Geçmişte sigara içtiniz mi?
smoking_past_label = ttk.Label(root, text="Geçmişte sigara içtiniz mi?")
smoking_past_label.grid(row=3, column=0, padx=10, pady=5)
smoking_past = tk.StringVar(value="No")
smoking_past_check = ttk.Checkbutton(root, text="Evet", variable=smoking_past, onvalue="Yes", offvalue="")
smoking_past_check.grid(row=3, column=1, padx=10, pady=5)
smoking_past_check = ttk.Checkbutton(root, text="Hayır", variable=smoking_past, onvalue="No", offvalue="")
smoking_past_check.grid(row=3, column=2, padx=10, pady=5)

# Hiç radyoterapi tedavisi aldı mı?
radiotherapy_label = ttk.Label(root, text="Hiç radyoterapi tedavisi aldınız mı?")
radiotherapy_label.grid(row=4, column=0, padx=10, pady=5)
radiotherapy = tk.StringVar(value="No")
radiotherapy_check = ttk.Checkbutton(root, text="Evet", variable=radiotherapy, onvalue="Yes", offvalue="")
radiotherapy_check.grid(row=4, column=1, padx=10, pady=5)
radiotherapy_check = ttk.Checkbutton(root, text="Hayır", variable=radiotherapy, onvalue="No", offvalue="")
radiotherapy_check.grid(row=4, column=2, padx=10, pady=5)

# Hangi tür troidiniz vardı?
troid_type_label = ttk.Label(root, text="Hangi tür troidiniz vardı?")
troid_type_label.grid(row=5, column=0, padx=10, pady=5)
troid_type = ttk.Combobox(root, values=["Euthyroid", "Clinical Hyperthyroidism", "Subclinical Hyperthyroidism"])
troid_type.set("Euthyroid")
troid_type.grid(row=5, column=1, padx=10, pady=5)

# Fiziksel Muayenede hangi taraflarda troidiniz vardı?
troid_location_label = ttk.Label(root, text="Fiziksel Muayenede hangi taraflarda troidiniz vardı?")
troid_location_label.grid(row=6, column=0, padx=10, pady=5)
troid_location = ttk.Combobox(root, values=["Single nodular goiter-left", "Single nodular goiter-right" , "Multinodular goiter", "Normal", "Diffuse goiter"])
troid_location.set("Single nodular goiter-left")
troid_location.grid(row=6, column=1, padx=10, pady=5)

# Lenf bezlerinizde anormal bir büyüme var mıydı?
adenopathy_label = ttk.Label(root, text="Lenf bezlerinizde anormal bir büyüme var mıydı?")
adenopathy_label.grid(row=7, column=0, padx=10, pady=5)
adenopathy = ttk.Combobox(root, values=["hayır", "sağ", "sol", "yaygın", "iki-tarafta", "arka-tarafında"])
adenopathy.set("hayır")
adenopathy.grid(row=7, column=1, padx=10, pady=5)

# Doku örneği sonucunuz neydi?
tissue_result_label = ttk.Label(root, text="Doku örneği sonucunuz neydi?")
tissue_result_label.grid(row=8, column=0, padx=10, pady=5)
tissue_result = ttk.Combobox(root, values=["Micropapillary", "Papillary", "Follicular", "Hurthel cell"])
tissue_result.set("Micropapillary")
tissue_result.grid(row=8, column=1, padx=10, pady=5)

# Tümör tek noktada mı çoklu noktalarda mıydı?
tumor_location_label = ttk.Label(root, text="Tümör tek noktada mı çoklu noktalarda mıydı?")
tumor_location_label.grid(row=9, column=0, padx=10, pady=5)
tumor_location = ttk.Combobox(root, values=["Tekli-Noktada", "çoklu-noktalarda"])
tumor_location.set("Tekli-Noktada")
tumor_location.grid(row=9, column=1, padx=10, pady=5)

# Risk durumunuz neydi?
risk_label = ttk.Label(root, text="Risk durumunuz neydi?")
risk_label.grid(row=10, column=0, padx=10, pady=5)
risk = ttk.Combobox(root, values=["düşük", "Orta", "yüksek"])
risk.set("düşük")
risk.grid(row=10, column=1, padx=10, pady=5)

# T değeri (Tümör boyutu ve yayılma derecesi) neydi?
t_value_label = ttk.Label(root, text="T değeri (Tümör boyutu ve yayılma derecesi) neydi?")
t_value_label.grid(row=11, column=0, padx=10, pady=5)
t_value = ttk.Combobox(root, values=["T1a", "T1b", "T2", "T3a", "T3b", "T4a", "T4b"])
t_value.set("T1a")
t_value.grid(row=11, column=1, padx=10, pady=5)

# N değeri (Kanserin lenf nodlarında yayılma durumu) neydi?
n_value_label = ttk.Label(root, text="N değeri (Kanserin lenf nodlarında yayılma durumu) neydi?")
n_value_label.grid(row=12, column=0, padx=10, pady=5)
n_value = ttk.Combobox(root, values=["N0", "N1b", "N1a"])
n_value.set("N0")
n_value.grid(row=12, column=1, padx=10, pady=5)

# M değeri (Kanserin metastaz yapıyor mu) yayıldı mı?
m_value_label = ttk.Label(root, text="M değeri (Kanserin metastaz yapıyor mu) yayıldı mı?")
m_value_label.grid(row=13, column=0, padx=10, pady=5)
m_value = ttk.Combobox(root, values=["M0", "M1"])
m_value.set("M0")
m_value.grid(row=13, column=1, padx=10, pady=5)

# Kaçıncı aşamadaydı?
stage_label = ttk.Label(root, text="Kaçıncı aşamadaydı?")
stage_label.grid(row=14, column=0, padx=10, pady=5)
stage = ttk.Combobox(root, values=["1", "2", "3", "4a", "4b"])
stage.set("1")
stage.grid(row=14, column=1, padx=10, pady=5)

# Tedaviye verilen yanıt neydi?
response_label = ttk.Label(root, text="Tedaviye verilen yanıt neydi?")
response_label.grid(row=15, column=0, padx=10, pady=5)
response = ttk.Combobox(root, values=["belirsiz", "olumlu", "Structural Incomplete", "Biochemical Incomplete"])
response.set("belirsiz")
response.grid(row=15, column=1, padx=10, pady=5)

# Formu gönderme butonu
submit_button = ttk.Button(root, text="Formu Gönder", command=submit_form)
submit_button.grid(row=16, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

