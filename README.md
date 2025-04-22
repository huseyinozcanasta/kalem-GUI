# kalem-GUI
Çok Fonksiyonlu pc ekranüstü çizim uygulaması

Bu uygulama, ekran üzerinde çizim yapmanızı, lazer kalem ile etkileşimde bulunmanızı ve çizimlerinizi kaydetmenizi sağlayan bir araçtır. PyQt5 kullanılarak geliştirilmiştir ve özellikle sunumlar, eğitim materyalleri veya hızlı notlar almak için ideal bir uygulamadır.

## Özellikler

- **Çizim Modu**: Ekran üzerinde serbest çizim yapmanıza olanak tanır.
- **Lazer Kalem**: Sunum sırasında belirli noktaları vurgulamak için lazer kalem özelliği.
- **Renk Seçimi**: Çizim rengi değiştirme imkanı.
- **Fırça Boyutu Ayarı**: Çizim fırçasının genişliğini ayarlayabilirsiniz.
- **Ekran Görüntüsü Alarak Çizim**: Çizime başlamadan önce ekran görüntüsü alır ve üzerine çizim yapmanıza olanak tanır.
- **Çizim Kaydetme**: Çizimlerinizi PNG formatında kaydedebilirsiniz.
- **Fare Tekerleği Kontrolü**: Fare tekerleği kullanıldığında çizim modu otomatik olarak kapanır ve durduğunda yeniden açılır.
- **Klavye Kısayolları**:
  - `CTRL + A`: Çizim modunu aç/kapat.
  - `CTRL + L`: Lazer kalem modunu aç/kapat.
- **Kullanıcı Dostu Arayüz**: Kolay erişilebilir araç çubuğu ve dinamik ekran boyutlandırması.
- **Şeffaf Arayüz**: Uygulama, ekran üzerinde şeffaf bir şekilde çalışır ve ekranın tamamını kaplamaz.

## Gereksinimler

Bu uygulamayı çalıştırmak için aşağıdaki yazılımların ve kütüphanelerin kurulu olması gerekir:

- **Python 3.7 veya üstü**
- **PyQt5**

PyQt5 kütüphanesini yüklemek için aşağıdaki komutu kullanabilirsiniz:

```bash
pip install PyQt5
```

## Kullanım

1. Uygulamayı çalıştırmak için aşağıdaki komutu terminalde çalıştırın:

   ```bash
   python app.py
   ```

2. Uygulama açıldıktan sonra:
   - **Renk Seç**: Renk değiştirmek için bu butona tıklayın.
   - **Çizim Modu**: Çizim modunu açmak için bu butonu kullanın ve ekran üzerinde çizim yapmaya başlayın.
   - **Lazer Kalem**: Lazer kalemi etkinleştirmek için bu butona tıklayın. Lazer kalem ile ekran üzerinde vurgular yapabilirsiniz.
   - **Kaydet**: Çizimlerinizi kaydetmek için bu butona tıklayın.
   - **Kapat**: Uygulamayı kapatmak için sağ üst köşedeki kırmızı "X" butonuna tıklayın.

3. Çiziminizi kaydetmek için "Kaydet" butonuna tıklayın ve dosya adını belirleyerek PNG formatında kayıt yapın.

## Ekran Görüntüsü

Ekran görüntüsü çekerken ve çizim yaparken uygulama şeffaf bir arka plan sağlar, böylece ekranınızın üzerine kolayca çizim yapabilirsiniz.

## Özelleştirme

- **Fırça Boyutu**: Araç çubuğundaki slider ile fırça boyutunu ayarlayabilirsiniz.
- **Renk Seçimi**: Araç çubuğundaki "Renk Seç" butonuna tıklayarak çizim rengini değiştirebilirsiniz.

## Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz, lütfen bir `Pull Request` gönderin veya bir `Issue` açarak önerilerinizi paylaşın.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasını inceleyin.

## İletişim

Herhangi bir sorunuz varsa, lütfen benimle iletişime geçin: [huseyinozcanasta](https://github.com/huseyinozcanasta)
