import pandas as pd 
from sklearn.compose import ColumnTransformer 
from sklearn.metrics import confusion_matrix 
from sklearn.preprocessing import LabelEncoder,OneHotEncoder  
from sklearn.model_selection import train_test_split 
from sklearn.svm import SVC 
from sklearn.metrics import accuracy_score 

# Projemiz Tiroid hastalığını geçiren isnsanların tekrar tiroid hastalığı geçirme durumunu tahmin eder
# Verileri https://archive.ics.uci.edu/dataset/915/differentiated+thyroid+cancer+recurrence adresinden aldık
# Verilerimizde eksik veri veya aşırı veriler olmadığı için sadece encode ettik
# Anamodel.py dosyasında arayüz olmadan sadece model oluşturup çıktısını aldığımız kod var
# Proje1.py dosyasında AnaModel.py dosyasındaki uygulamanın arayüzlü hali var 
# Proje2.py dosyasında Proje1.py dosyasındaki kodların aynısı yer alıyor farklı olarak Hx Radioterapy ve M verileri 
#sonuç üzerine fazla etkisi olmadığı için o verilerin çıkarılmış ve yaş verisinin StandartScaler kullanarak scale edilmiş hali var

# Yapan : Ali ŞARLI 

#csv dosyasından verileri okuma
data = pd.read_csv("Thyroid_Diff.csv")

#target verisini çıkarma
y=data.pop("Recurred")


#kolon isimlerini alma 
sutun=data.columns

#test verisini oluşturma
testVeri=[[17,"F","No","Yes","No","Euthyroid","Single nodular goiter-right","No","Papillary","Uni-Focal","Low","T1b","N0","M0","I","Excellent"]]

#test verisini sütunlara göre dataframe'e çevirme
testVeri=pd.DataFrame(testVeri,columns=sutun)

#datamız ile test verisini birleştirme (test verisini modelde deneyebilmemiz için dataya uygun bir şekilde encode etmek lazımdı 
#onun için data verisi ile birleştirip data verisi ile encode edip data verisi ile test verisini ayırıyoruz)
merged_data = pd.concat([data, testVeri], axis=0, ignore_index=True)
data = merged_data

#target verisini encode ediyoruz
le=LabelEncoder()
y=le.fit_transform(y)

#test verisi ile birleştirilmiş datamızı OneHotEncoder kullanarak encode ediyoruz 
columns_to_encode = ['Gender', 'Smoking', 'Hx Smoking', 'Hx Radiothreapy',
       'Thyroid Function', 'Physical Examination', 'Adenopathy', 'Pathology',
       'Focality', 'Risk', 'T', 'N', 'M', 'Stage', 'Response']
ct = ColumnTransformer([('onehot', OneHotEncoder(), columns_to_encode)], remainder='passthrough')
data_encoded = ct.fit_transform(data).toarray()
x = data_encoded

#dönüştürülmüş verimizden test verisini ayrı bir değişkene atayıp siliyoruz
x = pd.DataFrame(x)
testveridonusum = pd.DataFrame(x.iloc[-1]).transpose()
x.drop([len(x)-1], axis=0, inplace=True)

#kolerasyon matrisi hesaplaması yapıyoruz (Korelasyon matrisi değişkenler arasındaki ilişkiyi ölçmek için kullanılır)
kolerasyon = pd.DataFrame(x)
correlation_matrix = kolerasyon.corr()
print("-------------------------------Kolerasyon Matrisi-------------------------------")
print(correlation_matrix)

#verilerimizi train_test_split methodunu kullanarak train vve test olmak üzere ayırıyoruz %70 train , %30 test
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

#eğitim verilerimizle modelimizi eğitiyoruz
svm_model = SVC(kernel='linear', random_state=42)
svm_model.fit(X_train, y_train)

#ayırdığımız test verileri ile de modelimizin doğruluğunu ölçüyoruz
y_pred = svm_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Doğruluğu:", accuracy)

#dönüştürdüğümüz test verisini modelde deniyoruz
testVeriPred=svm_model.predict(testveridonusum)
print("Test verisinin sonucu : ",testVeriPred)

#karmaşıklık matrisi hesaplaması yapıyoruz (Karmaşıklık matrisi modelin performansını değerlendirmek için kullanılır)
cm = confusion_matrix(y_test, y_pred)
print("----------------------Karmaşıklık Matrisi-------------------")
print(cm)





