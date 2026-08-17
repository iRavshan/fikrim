# Fikrim — loyiha haqida to'liq ma'lumot

> Bu hujjat taqdimot generatsiya qilish uchun manba matn sifatida tayyorlangan.
> Oxirida 8 slaydlik tayyor tuzilma berilgan (shablon slaydlari soniga mos).
>
> **Diqqat:** «TEKSHIRILSIN» belgisi qo'yilgan raqamlar tasdiqlanmagan.
> Ularni rasmiy manbadan olib qo'ying yoki taqdimotdan olib tashlang —
> aks holda savol-javobda himoya qilib bo'lmaydi.

---

## 1. Bir jumlada

**Fikrim** — bemorlar shifoxona xizmati sifati haqida QR kod orqali
**mutlaqo anonim** fikr qoldiradigan, kelib tushgan fikrlarni esa sun'iy
intellekt avtomatik toifalab, rahbarga tayyor tahlil ko'rinishida
ko'rsatadigan veb-platforma.

**Shior varianti:** «Har bir fikr — eshitiladi. Hech bir bemor — tanilmaydi.»

---

## 2. Muammo

Bemor shifoxona xizmatidan norozi bo'lsa, amalda uch yo'l bor va uchalasi ham ishlamaydi:

| Mavjud yo'l | Nega ishlamaydi |
|---|---|
| Shikoyat daftari / qutisi | Bemor yozayotganini xodimlar ko'radi. Norozilik bildirgan bemor davolanishda o'ziga munosabat o'zgarishidan qo'rqadi. |
| Rasmiy murojaat, ariza | Ism-sharif, imzo talab qilinadi — anonimlik yo'q. Uzoq va rasmiy jarayon. |
| Ijtimoiy tarmoqlarda yozish | Shifoxonaga qadar yetib bormaydi, obro'ga zarar yetkazadi, muammo esa tuzatilmaydi. |

**Natijada:**

- Bemor jim qoladi. Muammo takrorlanaveradi.
- Rahbar o'z muassasasida nima bo'layotganini bilmaydi — unga faqat xodimlar aytgan ma'lumot yetib boradi.
- Muammo faqat u katta janjalga yoki ommaviy shikoyatga aylangandan keyin ma'lum bo'ladi, ya'ni eng qimmat bosqichda.

**Asosiy sabab — qo'rquv.** Bemor davolanish jarayonida shifoxonaga qaram
holatda bo'ladi. Anonimlik kafolatlanmasa, u rost gapirmaydi.

---

## 3. Yechim

Har bir bemor xonasiga QR kod o'rnatiladi. Bemor uni telefonida skanerlaydi
va ochilgan sahifada fikrini yozadi.

**Bemor uchun:**

- Ro'yxatdan o'tish **yo'q**, login **yo'q**, telefon raqami **yo'q**
- Ilova o'rnatish shart emas — oddiy veb-sahifa
- Xohlasa rasm biriktiradi (masalan, buzuq jihoz yoki iflos xona surati)
- 30 soniyada tugaydi

**Rahbar uchun:**

- Shaxsiy kabinetda barcha fikrlar bir joyda
- Sun'iy intellekt fikrlarni 5 toifaga avtomatik ajratadi
- Diagrammalar: qaysi yo'nalishda muammo ko'p ekani darhol ko'rinadi
- Toifa bo'yicha filtr

**Fikrlarni faqat tashkilot rahbari ko'radi.** Xodimlar ham, boshqa
tashkilotlar ham, tashqi foydalanuvchilar ham ko'ra olmaydi.

---

## 4. Qanday ishlaydi

**Bemor yo'li:**

1. Xonadagi QR kodni telefon kamerasi bilan skanerlaydi
2. Fikr yozish sahifasi ochiladi
3. Fikrini yozadi, xohlasa rasm biriktiradi (kameradan yoki galereyadan)
4. «Yuborish» tugmasini bosadi
5. Rahmat sahifasi chiqadi — jarayon tugadi

**Tizim yo'li (bemor kutmaydi):**

6. Fikr bazaga darhol saqlanadi
7. Fon rejimida Gemini AI ga yuboriladi
8. AI toifani aniqlaydi va yozuvga qo'shadi
9. Rahbar kabinetida diagramma yangilanadi

**Muhim texnik yechim:** AI javobi 16–18 soniya oladi. Agar bemor shuncha
kutsa, sahifa qotib qolgandek ko'rinadi va u yuborishni tashlab ketadi.
Shuning uchun fikr avval saqlanadi, toifalash keyin fonda bajariladi.

---

## 5. Anonimlik — bu va'da emas, texnik kafolat

Bu loyihaning eng muhim qismi. Anonimlik shunchaki aytilmaydi, kodda
ta'minlanadi:

| Xavf | Qanday yopilgan |
|---|---|
| Bemorni akkaunti orqali aniqlash | Akkaunt umuman yo'q — ro'yxatdan o'tish talab qilinmaydi |
| IP manzil orqali aniqlash | Xom IP bazaga **yozilmaydi**. Faqat `sha256(tuz + xona + IP)` hashi saqlanadi. Hashdan IP ni qayta tiklab bo'lmaydi. |
| Rasm ichidagi GPS koordinatalari | Har bir rasm saqlashdan oldin butunlay qayta yoziladi. Yangi faylga faqat piksellar ko'chiriladi, EXIF (GPS, telefon modeli, aniq sana) ko'chirilmaydi. |
| Fayl nomi orqali sizib chiqish | Original nom (`IMG_Alisher_uy.jpg` kabi) tashlanadi, tasodifiy nom beriladi |
| Xodimlarning fikrni ko'rishi | Fikrlarni faqat tashkilot egasi ko'radi |

Hashning maqsadi — bir bemor bir necha marta fikr yubormasligini
tekshirish, uni tanish emas.

---

## 6. Sun'iy intellekt tahlili

**Model:** Google Gemini 3.5 Flash

Har bir fikr avtomatik ravishda beshta toifadan biriga ajratiladi:

| Toifa | Nimalarni o'z ichiga oladi |
|---|---|
| **Xodimlar va xizmat ko'rsatish** | Shifokor, hamshira, qabul xodimi, muomala madaniyati |
| **Texnik ta'minot va sharoitlar** | Bino holati, tozalik, jihozlar, isitish/sovitish, navbat |
| **Tibbiy xizmat va dori-darmon** | Davolash sifati, tashxis, dorilar, laboratoriya, operatsiya |
| **Moliyaviy masalalar va narxlar** | Narxlar, to'lov, sug'urta, ortiqcha pul undirish |
| **Boshqa masalalar** | Yuqoridagilarga kirmagan fikrlar |

**Nega bu kerak?** 20 xonali shifoxonada oyiga yuzlab fikr to'planadi.
Ularni qo'lda o'qib chiqish va guruhlash — alohida odamning ishi. AI buni
bir necha soniyada bajaradi va rahbarga «qaysi yo'nalishda muammo eng ko'p»
degan savolga tayyor javob beradi.

**Ishonchlilik:** tizim AI chaqiruvi yiqilganda fikrni yo'qotmaydi. Har bir
fikrda «toifalangan vaqt» belgisi bor; toifalanmagan fikrlar navbatda
qoladi va aloqa tiklangach avtomatik qayta ishlanadi.

---

## 7. Texnologiyalar

| Qatlam | Yechim |
|---|---|
| Backend | Python 3.14, Django 6.1 |
| Ma'lumotlar bazasi | PostgreSQL |
| Server | Gunicorn, Railway bulut platformasi |
| Rasmlar ombori | Cloudflare R2 |
| Sun'iy intellekt | Google Gemini 3.5 Flash |
| QR kod | `qrcode` kutubxonasi, har so'rovda generatsiya qilinadi |
| Rasm qayta ishlash | Pillow |
| Diagrammalar | Chart.js |
| Statik fayllar | WhiteNoise |

**Diqqatga sazovor yechimlar:**

- **QR kod diskda saqlanmaydi** — har safar so'rov kelganda yangidan
  chiziladi. Shuning uchun domen o'zgarsa ham QR kodlar buzilmaydi va
  serverdagi fayllar yo'qolib qolishi muammo tug'dirmaydi.
- **Rasmlar Cloudflare R2 da** — Railway fayl tizimi har yangilanishda
  tozalanadi, ya'ni u yerda saqlansa bemor yuborgan rasmlar yo'qolardi.
- **Yorug' va qorong'i rejim** — tizim sozlamasiga qarab avtomatik.

---

## 8. Hozirgi holat

**Tayyor va ishlayapti:**

- ✅ Tashkilot qo'shish, tahrirlash, o'chirish
- ✅ Tashkilot uchun QR kod generatsiyasi va yuklab olish
- ✅ Anonim fikr yuborish (ro'yxatdan o'tishsiz)
- ✅ Rasm biriktirish: bir nechta rasm, jami 50 MB gacha, kameradan yoki galereyadan, oldindan ko'rish
- ✅ EXIF va GPS ma'lumotlarini tozalash
- ✅ AI orqali avtomatik toifalash
- ✅ Rahbar kabineti: doiraviy va ustunli diagrammalar, toifa bo'yicha filtr
- ✅ Logotip va yagona rang palitrasi, yorug'/qorong'i rejim
- ✅ Loyiha Railway'da onlayn ishlab turibdi

**Rejada (hali bajarilmagan):**

- ⏳ **Har bir xona uchun alohida QR kod** — ma'lumotlar bazasida xona
  tuzilmasi tayyor, boshqaruv oynasi qolgan
- ⏳ **Bir bemor — bir fikr cheklovi** — hash maydoni tayyor, tekshiruv
  mantiqini ulash qolgan
- ⏳ Menejer rollari (rahbardan tashqari bo'lim boshliqlari)
- ⏳ Yangi fikr kelganda bildirishnoma
- ⏳ `fikrim.uz` domenini ulash

---

## 9. Biznes modellari

O'zbekiston bozori uchun eng real variantlar, ustuvorlik tartibida:

**1. Obuna (SaaS) — asosiy model**

Shifoxona oylik yoki yillik to'lov qiladi. Narx xona yoki koyka soniga
bog'lanadi — kichik klinika kam, yirik shifoxona ko'p to'laydi.

- Kuchli tomoni: barqaror, oldindan bashorat qilinadigan daromad
- Zaif tomoni: davlat muassasalarida byudjet jarayoni sekin

**2. Freemium**

Asosiy funksiya (QR + fikr yig'ish) bepul. AI tahlili, diagrammalar,
tarixiy hisobotlar, bir nechta filial boshqaruvi — pullik.

- Kuchli tomoni: kirish to'sig'i nol, tez tarqaladi
- Zaif tomoni: bepul foydalanuvchilarni pullikka o'tkazish qiyin

**3. Xususiy klinikalar — birinchi maqsadli mijoz**

Xususiy klinikalar bemor uchun bir-biri bilan raqobatlashadi va obro'ga
pul sarflashga tayyor. Qaror bir kishi — egasi — tomonidan tez qabul
qilinadi. Davlat muassasasidan farqli, tender kutilmaydi.

**4. B2G — Sog'liqni saqlash vazirligi yo'nalishi**

Viloyat sog'liqni saqlash boshqarmasi bilan shartnoma: bir nechta
shifoxona bitta shartnoma ostida. Bitta shartnoma — o'nlab muassasa.

- Kuchli tomoni: bir shartnomada katta qamrov
- Zaif tomoni: uzoq muzokara, rasmiy jarayonlar

**5. Oq yorliq (white-label)**

Klinikalar tarmog'i tizimni o'z brendi ostida ishlatadi.

**Tavsiya:** 3-variant bilan boshlash (xususiy klinikalar, obuna asosida),
mahsulot pishgach 4-variantga chiqish.

---

## 10. Bozor

- O'zbekistonda sog'liqni saqlash tizimi raqamlashtirilmoqda — davlat
  darajasidagi ustuvor yo'nalish
- Xususiy tibbiyot sektori jadal o'smoqda, klinikalar obro' uchun
  raqobatlashmoqda
- Smartfon va QR kod odati aholida allaqachon shakllangan (to'lov
  tizimlari orqali)

> **TEKSHIRILSIN:** shifoxonalar soni, xususiy klinikalar soni, sektor
> hajmi — bu raqamlarni Statistika agentligi yoki Sog'liqni saqlash
> vazirligi ma'lumotlaridan oling.

---

## 11. Raqobat ustunligi

| Ustunlik | Izoh |
|---|---|
| **Haqiqiy anonimlik** | Raqobatchilar «anonim» deydi, lekin akkaunt yoki telefon raqami so'raydi. Bizda texnik jihatdan bemorni aniqlash imkoni yo'q. |
| **Bemor uchun to'siq nol** | Ilova yo'q, ro'yxatdan o'tish yo'q. QR — yozish — tugadi. |
| **AI tahlili** | Raqobatchilarda odatda faqat fikrlar ro'yxati bo'ladi. Bizda tayyor tahlil. |
| **O'zbek tilida** | Interfeys ham, AI toifalash ham o'zbek tilidagi matn uchun sozlangan. |
| **Tibbiyotga ixtisoslashgan** | Toifalar umumiy emas, aynan tibbiy muassasa muammolariga moslangan. |

---

## 12. Rivojlanish rejasi

**1-bosqich — hozir**
Xususiy klinikalarda sinov. Har bir xona uchun QR va bir marta fikr
bildirish cheklovini yakunlash.

**2-bosqich**
Menejer rollari, bildirishnomalar, hisobotni PDF ga chiqarish, `fikrim.uz`
domeni.

**3-bosqich**
Bir nechta filialni bitta kabinetdan boshqarish, davr solishtiruvi
(«o'tgan oyga nisbatan»), muammo takrorlanayotganini avtomatik ogohlantirish.

**4-bosqich**
Tibbiyotdan tashqariga chiqish: bank filiallari, mehmonxonalar, ta'lim
muassasalari — model bir xil, faqat toifalar almashadi.

---

# 8 slaydlik taqdimot tuzilmasi

Shablonda 8 ta slayd bor. Quyidagi taqsimot shunga moslangan.

**Slayd 1 — Sarlavha**
Fikrim. «Har bir fikr — eshitiladi. Hech bir bemor — tanilmaydi.»
Anonim fikr-mulohaza platformasi tibbiy muassasalar uchun.

**Slayd 2 — Muammo**
Bemor norozi, lekin gapira olmaydi. Sabab — qo'rquv. Uchta mavjud yo'l va
ularning kamchiliklari. Rahbar haqiqatni bilmaydi.

**Slayd 3 — Yechim**
QR kod → anonim fikr → AI tahlili → rahbar kabineti. Bemor uchun 30
soniya, ro'yxatdan o'tishsiz.

**Slayd 4 — Qanday ishlaydi**
5 qadamli sxema: skaner → yozish → yuborish → AI toifalash → diagramma.

**Slayd 5 — Anonimlik kafolati**
Akkaunt yo'q. IP hash ko'rinishida. Rasm metama'lumotlari tozalanadi.
Fikrni faqat rahbar ko'radi.

**Slayd 6 — AI tahlili**
Gemini 3.5 Flash. Beshta toifa. Diagramma tasviri. «Qaysi yo'nalishda
muammo ko'p» — tayyor javob.

**Slayd 7 — Biznes model va bozor**
Obuna modeli. Birinchi mijoz — xususiy klinikalar. Keyin vazirlik
yo'nalishi.

**Slayd 8 — Holat va reja**
Nima tayyor (ishlab turgan mahsulot), keyingi bosqichlar, murojaat uchun
ma'lumot.

---

## Taqdimot uchun kalit jumlalar

- «Bemor davolanish jarayonida shifoxonaga qaram. Anonimlik bo'lmasa, u rost gapirmaydi.»
- «Biz anonimlikni va'da qilmaymiz — uni texnik jihatdan ta'minlaymiz.»
- «Ro'yxatdan o'tish yo'q, ilova yo'q. QR, yozish, tamom.»
- «Rahbar muammoni janjalga aylanishidan oldin ko'radi.»
- «Yuzlab fikrni o'qib chiqish — odamning ishi. Sun'iy intellekt buni soniyalarda bajaradi.»
