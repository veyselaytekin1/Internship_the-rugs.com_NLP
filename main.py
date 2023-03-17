import pandas as pd                                                             # textleri tablo halinde göstermek ve CSV dosyalarini kullanmak icin
from textblob import TextBlob                                                   # https://textblob.readthedocs.io/en/dev/index.html
import streamlit as st
import cleantext
from wordcloud import WordCloud
import matplotlib.pyplot as plt 







st.image('the-rugs-logo2.png', use_column_width=True)
st.header(':blue[_The-Rugs Sentiment Analysis_]')



with st.expander('Analyze Text'):
    text = st.text_input('Text here please')                                     # buda bir alt satir olusturuyor ve icine yapmasi gerekenleri söylüyorsun
    if text:                                                                     # burda yani o expander icinde bir metin varsa, yani bos degilse, anlamina geliyor,biseler olunca demek
        blob = TextBlob(text)                                                    # girilen metni bu hazir library degerlendiriyor
        st.write('Polarity: ', round(blob.sentiment.polarity, 2))                # polarity library icinde hazir hesaplanan degeri alacagiz.pretrained edilmis bir kütüphane
        st.write('Subjectivity: ', round(blob.sentiment.subjectivity, 2))
        def output_sentiment():
            if (round(blob.sentiment.polarity, 2)) > 0.5:
                output_positive = ':blue[Positive]'
                return output_positive
            elif (round(blob.sentiment.polarity, 2)) < 0:
                output_negative = ':red[Negative]'
                return output_negative

            else:
                output_nötr = 'Nötr'
                return output_nötr

        st.write('Sentiment : ', output_sentiment())                             # bu fonksiyon olarak koydum, ve ona sira geldiginde hemen calismasi icin

    pre = st.text_input('Clean Text : ')                                         # bu da orda bir satir acti, su an biz expander Analyze Text altindayiz
    if pre:
        st.write(cleantext.clean(pre, clean_all=False, extra_spaces=True, stopwords= True, lowercase=True,
                                 numbers=True, punct=True))                      # numaralari ve punctuation silmek icin, burda stopwordleri silerken not olanlari silmiyor,denedim







# ------------------------------------------------------------------------------------------------------
# ANALYZE THE ENTIRE FILE PART

with st.expander('Analyze The Entire File'):
    uploaded_file = st.file_uploader('Upload a Excel File')   # bunun ile dosyayi yüklemek icin pencere aciliyor, ve dosyayi secme islemi yapiliyor


    #Read excel or csv file



    def score(x):
        blob1 = TextBlob(x)
        return blob1.sentiment.polarity



    def analyze(x):
        if x >= 0.5:
            output_analyze = 'Positive'
            return output_analyze
        elif x<= 0:
            output_analyze = 'Negative'
            return output_analyze
        else:
            return 'Neutral'




    if uploaded_file:
        df = pd.read_excel(uploaded_file)                       # bununla tüm dosyayi aliyoruz.icinde bir sürü features var. asagida bana lazim olanlari sececegim.
        df.dropna(inplace=True)
        #del df['Unnamed: 0']
        df['score'] = df['COMMENTS'].apply(score)               # bu sütunu ben kendim yeni olusturuyorum, icindeki score ise yukarida tanimladigim bir function
        df['analyze'] = df['score'].apply(analyze)              # bunuda ben yeni olusturuyorum, score functionu ile  buldugum degerleri positive veya negative diye cikti verecek, buda yukarida yazilan bir function

        wordcloud_text = df['COMMENTS'].str.cat(sep=' ')        # #bu ile tüm metinlari birlestirip tek bir text haline getirdim,

        #st.write(wordcloud_text)                               # eger yorumlarin birlestirilmesiyle olusturulan texti toplu halde görmek istersek bunu kullanabiliriz.



        st.set_option('deprecation.showPyplotGlobalUse',False)

        st.subheader('Wordcloud of the Data')
        if wordcloud_text:                                      # bu yukarida olusturdugum text eger varsa, calisiyor.
            wordcloud_result = WordCloud().generate(wordcloud_text)  # generate bu metinden bir bulut olusturacagimizi söylüyoruz.
            plt.imshow(wordcloud_result)
            st.pyplot()












        st.write(df)                                            #tüm yorumlari görmek istedigim icin df.head(10) gibi bir sinirlama yapmadim













#--------------------------------------------------------------------------------
# for the Downland the CSV file

        @st.cache_data                                              # bu sekilde eger bu dosyayi bir daha okutmak istersen, öncekileri hafizasinda turuyor, ve yenileri aliyor
                                                                    # bu sekilde daha az maliyetli bir calisma olur
        def convert_df(df):

            return df.to_csv().encode('utf-8')                      # bu sekilde ise, datayi excelden ceviriyor ve csv olarak kaydetmemiz icin

        csv = convert_df(df)                                        # burda csv olarak datamizi yakaliyoruz, asagidaki satirlarda data=csv yazacagiz


        st.download_button(
            label='Download data as CSV',
            data = csv,
            file_name='Sentmiment.csv',  #buraya excelwriter ile bisey gelmesi gerekiyor
            mime='text/csv')


#---------------------------------------------------------------------------












