# FAZ-9: Gönderi Detay Sayfası (Submission Detail)

**Tarih:** 2026-01-23  
**Durum:** ✅ Tamamlandı  
**Geliştirici:** Abdullah Doğan  
**Commit:** `f942a4a`

---

## Özet

Yazar gönderimini detaylı olarak görüntüleyebileceği tam kapsamlı bir detay sayfası oluşturuldu. Sayfa 4 sekmeli yapıda (Overview, Files, Authors, Details) tasarlandı. Sağ kenar çubuğunda duruma göre dinamik aksiyon butonları, gönderi bilgileri ve kronolojik durum geçmişi timeline'ı yer alıyor. Backend tarafında durum geçişleri artık otomatik olarak `SubmissionStatusHistory` tablosuna kaydediliyor.

---

## Yapılan Değişiklikler

### Backend

| Dosya | Değişiklik |
|---|---|
| `apps/submissions/serializers.py` | **Yeni** - `StatusHistorySerializer` (from/to status, display labels, changed_by_name) |
| `apps/submissions/serializers.py` | **Güncellendi** - `SubmissionDetailSerializer`'a `status_history` alanı eklendi, dosyalar sadece aktif olanları döndürüyor |
| `apps/submissions/views.py` | **Yeni** - `withdraw` endpoint'i (frontend'de vardı ama backend'de eksikti) |
| `apps/submissions/views.py` | **Güncellendi** - `submit` ve `withdraw` aksiyonlarında otomatik `SubmissionStatusHistory` kaydı |
| `apps/submissions/views.py` | **Güncellendi** - Queryset'e `status_history` prefetch eklendi |

### Frontend

| Dosya | Değişiklik |
|---|---|
| `views/submission/SubmissionDetail.vue` | **Yeniden yazıldı** - Placeholder'dan tam kapsamlı detay sayfasına dönüştürüldü |
| `components/submission/StatusTimeline.vue` | **Yeni** - Kronolojik durum geçmişi timeline bileşeni |
| `components/submission/SubmissionTable.vue` | **Güncellendi** - Başlıklar tıklanabilir (detay sayfasına), Edit wizard'a yönlendiriyor |
| `types/submission.ts` | **Güncellendi** - `StatusHistoryEntry` interface ve `Submission`'a `status_history` alanı eklendi |
| `REPORTS/PROJE_YOL_HARITASI.md` | **Yeni** - FAZ-9'dan FAZ-19'a kadar proje yol haritası |

---

## Mimari

```
Kullanıcı → /submissions/:id → SubmissionDetail.vue
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                 │
               Overview Tab     Files Tab        Authors Tab
               (Özet, keywords, (Dosya listesi,  (Yazar listesi,
                istatistikler)   indirme)         kurum, ORCID)
                                     │
                                Details Tab
                                (Kapak mektubu, etik,
                                 hakem önerileri, vb.)
                                     
                              Sağ Kenar Çubuğu:
                              ├── Aksiyonlar (Edit/Withdraw/Delete)
                              ├── Gönderi Bilgileri (tarihler, editör)
                              └── StatusTimeline (durum geçmişi)
```

### Durum Geçişi Kayıt Akışı

```
Yazar "Submit" tıklar → views.py submit()
  ├── old_status = submission.status
  ├── submission.submit() (FSM geçişi)
  ├── submission.save()
  └── SubmissionStatusHistory.objects.create(
        from_status=old_status,
        to_status=submission.status,
        changed_by=request.user
      )
```

---

## Detay Sayfası Özellikleri

### Sekmeler

| Sekme | İçerik |
|-------|--------|
| **Overview** | Özet, İngilizce özet (TR makaleler), anahtar kelimeler, istatistik kartları (yazar/dosya/revizyon sayısı, tarih) |
| **Files** | Dosya listesi, dosya tipi badge, boyut, tarih, presigned URL ile indirme butonu |
| **Authors** | Sıralı yazar listesi, sorumlu yazar işaretli, kurum/departman, e-posta, ORCID, katkı bilgisi |
| **Details** | Kapak mektubu, etik beyanı, çıkar çatışması, fonlama, hakem önerileri/itirazları, editöre yorum, revizyon notları |

### Dinamik Aksiyonlar

| Durum | Kullanılabilir Aksiyonlar |
|-------|--------------------------|
| `draft` | Edit, Delete |
| `submitted` | Withdraw |
| `under_review` | — (aksiyon yok) |
| `revision_required` | Edit, Withdraw |
| `accepted` / `rejected` / `withdrawn` | — (aksiyon yok) |

### Status Timeline

- Kronolojik sıralı (en eski → en yeni)
- Her geçiş için renkli nokta, durum etiketi, tarih/saat
- "Draft Created" her zaman ilk giriş olarak gösterilir
- Mevcut durum vurgulanır

---

## API Değişiklikleri

### Yeni Endpoint

| Method | URL | Açıklama |
|--------|-----|----------|
| `POST` | `/api/v1/submissions/{id}/withdraw/` | Gönderiyi geri çek |

### Güncellenen Endpoint

| Method | URL | Değişiklik |
|--------|-----|------------|
| `GET` | `/api/v1/submissions/{id}/` | Yanıta `status_history[]` eklendi, dosyalar sadece `is_active=True` olanları döndürüyor |

### StatusHistory Yanıt Örneği

```json
{
  "status_history": [
    {
      "id": "uuid",
      "from_status": "draft",
      "to_status": "submitted",
      "from_status_display": "Draft",
      "to_status_display": "Submitted",
      "changed_by": "user-uuid",
      "changed_by_name": "Abdullah Doğan",
      "notes": "Manuscript submitted by author",
      "created_at": "2026-01-23T14:30:00Z"
    }
  ]
}
```

---

## Test Kontrol Listesi

- [ ] Detay sayfası yükleniyor (`/submissions/:id`)
- [ ] Overview sekmesinde özet, anahtar kelimeler görünüyor
- [ ] Files sekmesinde dosyalar listeleniyor
- [ ] Dosya indirme (presigned URL) çalışıyor
- [ ] Authors sekmesinde yazarlar sıralı görünüyor
- [ ] Sorumlu yazar badge'i görünüyor
- [ ] Details sekmesinde ek bilgiler görünüyor
- [ ] Draft durumunda "Edit" ve "Delete" butonları var
- [ ] Submitted durumunda "Withdraw" butonu var
- [ ] Withdraw onay dialogu çalışıyor
- [ ] Status Timeline doğru sırada gösteriliyor
- [ ] Dashboard'dan "View Details" tıklanınca detay sayfasına gidiyor
- [ ] Submissions listesinden başlık tıklanınca detay sayfasına gidiyor
- [ ] "Edit" butonu wizard'a yönlendiriyor
- [ ] Hata durumunda error state görünüyor
- [ ] Loading state (skeleton) görünüyor
