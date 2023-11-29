#####################################################
# Veri Seti Hikayesi
#####################################################
# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç


import pandas as pd
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel("ab_testing.xlsx",sheet_name="Control Group")
df_test = pd.read_excel("ab_testing.xlsx",sheet_name="Test Group")
def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control) # Eksik değer yok, verilerin dağılımı normal
check_df(df_test) # Eksik değer yok, verilerin dağılımı normal

# Daha rahat çalışabilmek için veri setlerini birleştirebiliriz. Ayırt edebilmek için control ve test olarak etiketliyorum.
df_control["group"] = "control"
df_test["group"] = "test"
df = pd.concat([df_control,df_test], axis=0,ignore_index=False)

# H0 : M1 = M2 (Control grubu satın alma ortalaması ile test grubu satın alma ortalaması arasında istatistiksel olarak anlamlı bir fark yoktur)
# H1 : M1 != M2 (Anlamlı bir farklılık vardır)

df.groupby("group").agg({"Purchase": "mean"})
# Test sınıfının ortalama satın olması daha yüksek gözüküyor  control 550.89406   test    582.10610

# Varsayım kontrollerini yapmamız gerek.

shapiro(df.loc[df["group"] == "control" , "Purchase"]) # pvalue=0.5891125202178955 yani control grubu normal dağılıyor
shapiro(df.loc[df["group"] == "test" , "Purchase"]) # pvalue=0.15413342416286469 yani test grubu normal dağılıyor

levene(df.loc[df["group"] == "control" , "Purchase"],df.loc[df["group"] == "test" , "Purchase"]) # pvalue=0.10828588271874791 yani iki grubun varyansları benzer
# sonuç olarak iki varsayım testini de geçiyor. Bundan dolayı iki örneklem t testi uygulanması gerek.
ttest_ind(df.loc[df["group"] == "control", "Purchase"], df.loc[df["group"] == "test", "Purchase"],equal_var=True)
# pvalue=0.34932579202108416 0.05'ten büyük olduğu için H0 hipotezini reddedemeyiz yani iki grup arasında anlamlı farklılık yoktur.
