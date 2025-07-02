# Swerve Load Robot - ROS1 & CAD Design Integration

Bu proje, swerve mekanizmasına sahip bir mobil robotun CAD tasarımı, ROS1 üzerinde simülasyonları, arayüz kontrolü ve gerçek donanım entegrasyonlarını kapsamaktadır. Ayrıca proje kapsamında yapılan akademik çalışmalar da bu repoda paylaşılmıştır.

## 🔧 Proje Bileşenleri

### 1. CAD Tasarımı
- [📁 CAD Tasarım Dosyaları](https://github.com/MelikeBeyazli/Swerve-Load-Robot)
- SolidWorks ile modellenmiş, swerve tabanlı yük taşıma robotu.
- Tasarıma dair analizler ve açıklamalar ilgili dizinlerde mevcuttur.

### 2. ROS1 Simülasyonları (Gazebo)
#### ✅ Polaris_v1
- Temel kontrol mimarisi ve hareket testleri.

#### ✅ Polaris_v2
- Geliştirilmiş manevra kabiliyeti ve sensör simülasyonları.

#### ✅ Polaris_v3
- İz takip ve ileri seviye navigasyon mimarisi.

> Her versiyonda ROS1 eğitiminde öğrenilen kavramların pratiği yapılmıştır.

### 3. Arayüz Kontrolü (Interface)
- PyQt5 kullanılarak geliştirilen GUI sayesinde robot hareketleri manuel olarak kontrol edilmektedir.
- Arayüz, temel yön kontrolleri, hız ayarları ve anlık durum görselleştirmesini sağlar.

### 4. Velocity_Control
- Gerçek bir aracın motor hızlarını yazılımsal olarak kontrol etmeye yönelik geliştirilmiştir.
- PWM ve motor sürücü etkileşimleri üzerine denemeler içerir.

---

## 🎓 Akademik Kaynaklar

- Proje kapsamında hazırlanan makale ve bildiriler repoda paylaşılmıştır.
- İçeriğe ulaşmak için: [`/makaleler`](https://github.com/MelikeBeyazli/Swerve-Load-Robot/tree/main/makaleler)

---

## 🎥 Video Demoları

### 🔹 Manuel Kontrol Test Videosu

[![Manual Kontrol Videosu](https://img.youtube.com/vi/YOUTUBE_VIDEO_ID1/0.jpg)](https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID1)

> PyQt5 arayüzü ile yapılan ilk sürüş denemesi.

---

### 🔹 Çizgi Takip Test Videosu

[![Çizgi Takip Videosu](https://img.youtube.com/vi/YOUTUBE_VIDEO_ID2/0.jpg)](https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID2)

> Çizgi takip algoritmasının simülasyon üzerindeki ilk denemesi.

---

## 🚀 Gelecek Planlar

- **ROS2 (Jazzy) + Gazebo Harmonic** altyapısına geçilmiştir.
- Mevcut projede tespit edilen eksiklikler, ROS2 sürümünde giderilecektir.
- Yeni mimaride daha modüler, stabil ve gerçek zamanlı performans hedeflenmektedir.
- Geliştirmeler ayrı bir ROS2 reposu altında paylaşılacaktır.

---

## 💬 İletişim
Görüş ve önerileriniz için GitHub üzerinden issue açabilir veya doğrudan iletişime geçebilirsiniz.

---

> **Not**: Bu proje hâlen geliştirilmektedir. Eksiklikler bilinçli olarak bırakılmış ve ROS2 mimarisi ile tamamlanması planlanmaktadır.
