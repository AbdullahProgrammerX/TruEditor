# FAZ-8: S3 Dosya Yönetimi (Cloudflare R2)

**Tarih:** 2026-01-23  
**Durum:** ✅ Tamamlandı (kod tarafı)  
**Geliştirici:** Abdullah Doğan

---

## Özet

Dosya yükleme sistemi Cloudflare R2 (S3-uyumlu) entegrasyonu ile tamamlandı. `StepFileUpload.vue` artık gerçek API'ye bağlı, sürükle-bırak ile dosya yükleme, ilerleme takibi, indirme ve silme destekliyor.

---

## Yapılan Değişiklikler

### Backend

| Dosya | Değişiklik |
|---|---|
| `apps/files/services.py` | **Yeni** - FileService sınıfı (validate, checksum, presigned URL, delete, reorder) |
| `core/settings/base.py` | Zaten hazırdı - USE_S3, AWS_S3_ENDPOINT_URL, django-storages config |
| `requirements/base.txt` | Zaten hazırdı - boto3, django-storages[s3] |

### Frontend

| Dosya | Değişiklik |
|---|---|
| `composables/useFileUpload.ts` | **Yeni** - File upload composable (progress tracking, validate, CRUD) |
| `components/submission/wizard/StepFileUpload.vue` | **Güncellendi** - Simülasyondan gerçek API'ye geçiş |
| `views/submission/NewSubmission.vue` | **Güncellendi** - submissionId prop + auto-draft creation |
| `types/submission.ts` | **Güncellendi** - ManuscriptFile'a download_url eklendi |

---

## Mimari

```
User → StepFileUpload.vue → useFileUpload.ts → API (axios multipart)
                                                    ↓
                                              ManuscriptFileViewSet
                                                    ↓
                                              django-storages (S3Boto3Storage)
                                                    ↓
                                              Cloudflare R2 Bucket
```

### Upload Akışı
1. Kullanıcı dosya seçer veya sürükle-bırak yapar
2. `useFileUpload.ts` dosyayı validate eder (boyut, uzantı)
3. `FormData` ile multipart POST isteği gönderilir
4. `onUploadProgress` ile gerçek zamanlı ilerleme çubuğu
5. Backend dosyayı R2'ye yükler, `ManuscriptFile` kaydı oluşturur
6. Frontend dosya listesini günceller

### Presigned URL İndirme
1. Kullanıcı "Download" butonuna tıklar
2. Frontend `/files/{id}/presigned_url/` endpoint'ine GET atar
3. Backend 15 dakika geçerli presigned URL oluşturur
4. Tarayıcı URL'e yönlendirilir, dosya indirilir

---

## Cloudflare R2 Yapılandırması

**Render Environment Variables:**

```
USE_S3=true
AWS_ACCESS_KEY_ID=<Cloudflare R2 Access Key>
AWS_SECRET_ACCESS_KEY=<Cloudflare R2 Secret Key>
AWS_STORAGE_BUCKET_NAME=trueditor-files
AWS_S3_ENDPOINT_URL=<Cloudflare R2 Endpoint URL>
AWS_S3_REGION_NAME=auto
```

---

## Dosya Kısıtlamaları

- **Maksimum boyut:** 50MB
- **İzin verilen formatlar:** DOC, DOCX, PDF, JPG, JPEG, PNG, TIFF, TIF, XLS, XLSX
- **Soft delete:** Dosyalar silindiğinde `is_active=False` yapılır
- **Presigned URL süresi:** 15 dakika

---

## Test Kontrol Listesi

- [ ] Render'a env variables eklendi
- [ ] Dosya yükleme çalışıyor (drag-and-drop)
- [ ] Dosya yükleme çalışıyor (browse butonu)
- [ ] Progress bar görünüyor
- [ ] Dosya silme çalışıyor
- [ ] Presigned URL ile indirme çalışıyor
- [ ] 50MB üstü dosya reddediliyor
- [ ] İzin verilmeyen uzantılar reddediliyor
