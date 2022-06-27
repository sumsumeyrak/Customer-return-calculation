#gerekli kütüphaneleri oluşturalım
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv('../input/projectgamepersona/persona.csv')
df.head(10)

# Kaç unique Source vardır? Frekansları nedir? 
df.SOURCE.nunique()
2
#Kaç uniquePRICE vardır?
df.PRICE.unique()
array([39, 49, 29, 19, 59,  9])
#Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

#Hangi ülkeden kaçar tane satış olmuş
df["COUNTRY"].value_counts()

#Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE": "sum"}).head()

#SOURCE türlerine göre satış sayıları nedir?
df["SOURCE"].value_counts()

#Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE": "mean"}).head()

#SOURCE'laragöre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE": "mean"}).head()

#COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(['SOURCE','COUNTRY'])[['PRICE']].agg('mean')

#COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY","SOURCE","SEX", "AGE"]).agg({"PRICE": "mean"}).head()

# Çıktıyı PRICE’a göre sıralayalım.
agg_df = df.groupby(["COUNTRY","SOURCE","SEX", "AGE"]).agg({"PRICE": "mean"}).head()

#sort_values metodunu azalan olacak şekilde PRICE’a göre ayarlamak.
agg_df.sort_values(by = ['PRICE'],ascending = False,
                          inplace = True)
agg_df.head()

agg_df.reset_index(inplace = True)
agg_df.head()


# Aralıkları ikna edici şekilde oluşturalım:
# • ‘0_18', ‘19_23', '24_30', '31_40', '41_70' gibi:

agg_df['AGE_CATGR'] = pd.cut(x = agg_df['AGE'], bins = [0,16,20,23,41,70], 
                        labels=['0_18', '19_23', '24_30', '31_40', '41_70'])
agg_df.head()

#Yeni seviye tabanlı müşterileri (persona) tanımlayalım
  File "/tmp/ipykernel_19/2807467643.py", line 1
#Yeni seviye tabanlı müşterileri (persona) tanımlayalım

#Yeni seviye tabanlı müşterileri (persona) tanımlayınız ve 
#age ve price dışındaki verileri yanyana yazdıracağımdan 
#bu sütunları drop yapıp yeni bir liste yaptım
agg_df['customers_level_based'] = ['_'.join(i).upper() for i in agg_df.drop(['AGE', 'PRICE'], axis=1).values]
                                   
agg_df
#Yeni müşterileri (personaları) segmentlere ayırınız

#Yeni müşterileri PRICE’a göre 4 segmente ayırınız. 
#(Örnek: USA_ANDROID_MALE_0_18) 
agg_df=agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df.head(30)
#Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D","C","B","A"])
agg_df
#33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir 
#ve ortalama ne kadar gelir kazandırması beklenir?
new_user = 'TUR_ANDROID_FEMALE_TUR_31_40'
#Segmentleri betimleyiniz:
#(Segmentlere göre group by yapıp price mean,max,sum’larını alınız)
agg_df.groupby("SEGMENT").agg({"PRICE":["mean","max","sum"]}).head()
#Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz
