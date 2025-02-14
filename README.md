# Apriori Algoritması Kullanan Film Öneri Sistemi (Özet)

## Proje Hakkında
Bu proje, **MovieLens 20M** veri setinden yararlanarak **Apriori algoritması** ile film önerileri sunmayı amaçlar. Kullanıcıların izleme geçmişlerini inceleyerek sık tekrar eden film kümeleri ve birliktelik kuralları elde edilir. Böylece hem **kişiselleştirilmiş** hem de **popüler** filmler önerilir.

## Özellikler
- **Apriori Algoritması** ile sıkça birlikte izlenen film kümelerinin belirlenmesi  
- **Birliktelik Kuralları** (destek, güven, lift) analiziyle daha anlamlı öneriler  
- **Kişiselleştirilmiş Öneriler**: Kullanıcının beğenilerine göre özel liste sunma  
- **Popüler Öneriler**: Genel izleyici eğilimlerine dayalı film önerileri  
- **Film Türü** ve **Film Adı** bazlı esnek öneri seçenekleri  
- **Pytest** ile test edilerek doğrulanmış işlevsellik

## Kullanılan Veri Seti
[**MovieLens 20M**](https://grouplens.org/datasets/movielens/20m/) veri seti, 1995-2015 aralığında kullanıcıların filmlere verdiği puanlar ve etiketlerden oluşur. Başlıca dosyalar:
- **ratings.csv**: Kullanıcıların film puanları  
- **movies.csv**: Filmlerin başlık ve tür bilgileri  
- **tags.csv**: Kullanıcıların filmlerle ilgili etiket girişleri  
- **genome_scores.csv** ve **genome_tags.csv**: Filmlerin etiketlerle ilişkisini ve ilgililik düzeylerini içerir  
- **links.csv**: Filmlerin IMDb/TMDb kimlikleri

Ön işleme aşamasında, düşük puanlı veya az etkileşimli kayıtlar elendi. Daha sonra tür ve etiket bazında filtrelemeler yapıldı.

## Öneri Yaklaşımları
1. **Film Türüne Göre Öneri**: Kullanıcının sevdiği türde filmlere puan veren diğer kullanıcılarla ortak ilgi alanları bulunur ve onlardan film önerileri elde edilir.  
2. **Film Adına Göre Öneri**: Belirli bir film üzerinden, benzer etiketlere ve yüksek relevans puanına sahip diğer filmler sıralanarak tavsiye listesi oluşturulur.  

## Arayüz ve Kullanıcı Seçimleri
 **GUI** (grafik arayüz) üzerinde kullanıcı seçimlerine göre farklı öneri fonksiyonlarını çağırarak film önerileri sunar. Kodun temel mantığı şöyledir:

1. **Seçenekler (selected_option)**  
   - **Popüler Film Önerileri**: Kullanıcıya genel popülerlik esas alınarak film önerileri getirilir.  
   - **Kişiselleştirilmiş Film Önerileri**: Belirli bir kullanıcı kimliği (ID) üzerinden, kişinin izleme geçmişi veya beğenileri dikkate alınarak film önerileri sunulur.

2. **Koşullar (selected_condition)**  
   - **Film Türüne Göre Öneriler**: Kullanıcı arayüzündeki “Tür Listesi”nden (`genre_listbox`) seçilen türe göre film önerisi yapılır.  
   - **Film İsmine Göre Öneriler**: Kullanıcı arayüzündeki “Film İsmi Listesi”nden (`name_listbox`) seçilen film adı referans alınarak benzer filmler önerilir.

3. **Fonksiyonlar ve Modüller**  
   - `populer_tur_oner(selected_genre)` (turpop.py):  
     Seçilen film türüne göre, veritabanında **popülerliği yüksek** filmleri bulur ve bu filmlerin listesini döndürür.
   - `populer_film_oner(selected_name)` (isimpop.py):  
     Seçilen film adına benzer veya o filmle ortak özelliklere sahip popüler filmleri bularak öneriler oluşturur.  
   - `film_oner(person_id, selected_genre)` (turkisi.py):  
     Hem kullanıcı ID’sini (kişiye özgü) hem de film türünü dikkate alır. Kullanıcının daha önceki beğenilerine uyumlu olan, aynı türdeki filmleri filtreleyip önerir.  
   - `kisi_film_oner(person_id, selected_name)` (isimkisi.py):  
     Kullanıcının izlediği spesifik bir film (film adı) üzerinden, benzer özelliklere sahip diğer filmleri listeler. Bu esnada kullanıcının geçmiş izleme tercihlerini dikkate alarak **kişiselleştirilmiş** bir sonuç sağlar.

4. **Akış (Kodun İçi Mantık)**  
   - Kullanıcı, arayüzdeki listbox veya seçeneklerle (radiobutton, dropdown vb.) bir **öneri türü** ve bir **koşul** belirler.  
   - Kod, `if-elif` yapısıyla hangi işlevin çağrılacağına karar verir.  
   - Seçime göre `genre_listbox` veya `name_listbox` içerisinden **aktif** (seçilmiş) öğe alınır ve gerektiğinde `person_listbox` içerisinden bir **kullanıcı ID** çekilir.  
   - Uygun fonksiyon (örneğin `populer_tur_oner` veya `film_oner`) çağrılarak **öneri listesi** (`recommended_films`) oluşturulur.  
   - Bu öneri listesi, GUI üzerinden ekrana yansıtılabilir ya da farklı bir şekilde kullanıcıya sunulabilir.

Bu yapı sayesinde, kod okunması ve genişletilmesi kolay bir şekilde organize edilmiştir. “Popüler” ve “Kişiselleştirilmiş” öneri ayrımıyla, kullanıcıların dilediği türde veya film adı üzerinde filtreleyerek hem genel ilgi çeken filmlere hem de kişisel zevklere uygun filmlere hızlıca ulaşması sağlanır.

  
## Testler
Projede, çeşitli senaryolar ve işlevler **Pytest** kullanılarak test edilmiştir. Testler arasında:
- Geçerli film/tür adıyla önerilerin döndürülmesi  
- Geçersiz sorgulamalarda boş veya hata yanıtı dönmesi  
- Belirli bir zaman sınırı içinde performans kontrolü gibi kriterler yer almaktadır.

## Sonuçlar
- **Apriori** ile elde edilen sık öğe kümeleri sayesinde kullanıcıların beğenilerine uygun, isabetli öneriler üretildi.  
- **Birliktelik Kuralları** (destek, güven ve lift) ile filmlerin ilişkileri ölçülerek önerilerin anlamlılığı artırıldı.  
- Hem genel popülerlik temelli hem de kullanıcının geçmişine göre özelleştirilmiş listeler sunuldu.  
- Test sonuçları, modelin doğruluk ve performans beklentilerini karşıladığını gösterdi.

## Kaynakça
1. [MovieLens 20M Dataset](https://grouplens.org/datasets/movielens/20m/)  
2. [GeeksforGeeks: Implementing Apriori Algorithm in Python](https://www.geeksforgeeks.org/implementing-apriori-algorithm-in-python/)  
3. [VeriBilimiOkulu: Python ile Birliktelik Kuralları Analizi](https://www.veribilimiokulu.com/python-ile-birliktelik-kurallari-analizi-association-rules-analysis-with-python/)  

Bu proje, veri madenciliği ve öneri sistemleri alanında Apriori algoritması uygulamasını gösteren örnek bir çalışmadır. Geliştirmeye ve iyileştirmeye devam edilebilir.
