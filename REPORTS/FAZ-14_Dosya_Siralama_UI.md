# FAZ-14: Dosya Sıralama UI (Sürükle-Bırak)

**Tamamlanma Tarihi:** 2026-03-02  
**Geliştirici:** Abdullah Doğan  

---

## Özet

Dosya yükleme adımına native HTML5 Drag & Drop ile sürükle-bırak dosya sıralama özelliği eklendi. Kullanıcılar dosyalarını istedikleri sıraya sürükleyerek düzenleyebilir.

---

## Frontend Değişiklikleri

### StepFileUpload.vue
- **Drag handle:** Altı nokta ikonu ile sürükleme başlatma
- **Sıra numarası:** Her dosyanın yanında 1, 2, 3... gösterimi
- **Görsel geri bildirim:**
  - Sürüklenen dosya: yarı saydam + kesikli çizgi (`dragging`)
  - Hedef konum: vurgulanmış kenarlık (`drag-over`)
- **Reorder çağrısı:** Bırakma sonrası backend `reorderFiles` API çağrısı
- **İpucu metni:** 2+ dosya olduğunda "Drag to reorder" gösterimi
- **Toast bildirimi:** "File order updated"

### useFileUpload Composable
- Mevcut `reorderFiles` fonksiyonu StepFileUpload'a bağlandı

---

## Backend

- Mevcut `POST /api/v1/files/{id}/reorder/` endpoint kullanıldı (yeni ekleme yok)

---

## Değişen Dosyalar

| Dosya | Tür |
|-------|-----|
| `frontend/src/components/submission/wizard/StepFileUpload.vue` | Güncelleme |
| `REPORTS/PROJE_YOL_HARITASI.md` | Güncelleme |
