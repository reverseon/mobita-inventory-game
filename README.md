# DOKUMENTASI
PENTING DIBACA! SUPAYA FLOWCHART KITA PUNYA FUNDAMENTAL YANG SAMA!

**PENTING (2) Developer Note:**
Tolong, Fungsi yang dibuat F01-F17 (bukan fungsi pemroses) ditaruh dibawah komen #F01 - F17

Fungsi pemroses silahkan ditaruh di bawah # Fundamental Function

Proses Input User pake fungsi chooser() [dokumentasi liat dibawah]

Load DB pake unload()

## FOLDER SAVE
Seluruh Folder Save tersedia di folder **savefolder**
Untuk Melakukan Saving Harap tidak di folder lain.

## GLOBAL VARIABLE

### DATABASE
**-> PENTING BUAT YANG BIKIN FUNGSI WRITE DB (F05 - F10) <-**
SETIAP CSV TOLONG DIKASIH **1 NEWLINE KOSONG** BIAR PARSERNYA JALAN
SELURUH ARRAY STORING CSV MENGIKUTI FORMAT INI

**CSV:**
kolom1;kolom2;kolom3
1;2;3
4;5;6

**ARRAY:**
[[1,4], [2,5], [3,6]]

1. UDB

-> Ini adalah tempat storing user.csv TANPA nama kolom dengan kolom di array 1 dan baris di array 2

2. GDB

-> Ini adalah tempat storing gadget.csv TANPA nama kolom dengan kolom di array 1 dan baris di array 2

3. CDB

-> Ini adalah tempat storing consumable.csv TANPA nama kolom dengan kolom di array 1 dan baris di array 2

4. GRHDB

-> Ini adalah tempat storing gadget_return_history.csv TANPA nama kolom dengan kolom di array 1 dan baris di array 2

5. GBHDB

-> Ini adalah tempat storing gadget_borrow_history.csv TANPA nama kolom dengan kolom di array 1 dan baris di array 2

6. CHDB

-> Ini adalah tempat storing consumable_history.csv TANPA nama kolom dengan kolom di array 1 dan baris di array 2

### USER CREDENTIALS 
Variabel ini sengaja ditaro di global biar gampang aksesnya, variabel ini meliputi 
**credid** -> ID user yang sedang login saat ini
**creduname** -> Username user yang sedang login saat ini  
**crednama** -> Nama user yang sedang login saat ini
**credalamat** -> Alamat user yang sedang login saat ini  
**credpw** -> Password user yang sedang login saat ini
**credrole** -> Role user yang sedang login saat ini

### SAVE FOLDER PATH

**savefoldername** : isinya nama folder save, saat ini isinya "savefolder"
**savepath** : PATH keseluruhan folder yang ada csvnya (.../savefolder/...)

### MISCELLANEOUS

**isExit** : buat toggle exit

## FUNDAMENTAL FUNCTION EXPLAINED

Ini Memuat Penjelasan Fungsi, Prerequisities, dan Dia Ngelakuin Apa

NOTE:
Ada beberapa fungsi yang gak gua jelasin secara detail banget karena

1. mungkin kalian ga akan pake juga
2. gua males :D

Tapi kalo mau detailnya bisa pc di line aja ya
### na() -> string
ngeprint "Not Available"

### searchgadget(id : string, prop : string) -> string
DB : gadget.csv
Buat nyari gadget berdasarkan ID

 * Argumen : id (string) -> id gadget
 * Argumen : prop (string) -> nama kolom (properties) 
Contoh: searchgadget(123, "nama") -> "Gadget Contoh"

### searchidcred(id : string, prop : string) -> string
DB : user.csv
Buat nyari user properties / credentials berdasarkan ID

 * Argumen : id (string) -> id gadget
 * Argumen : prop (string) -> nama kolom (properties) 

Contoh: searchidcred(555, "username") -> "thirafinajwan"

### searchcons(id : string, prop : string) -> string
DB: consumable.csv
Buat nyari consumable berdasarkan ID

 * Argumen : id (string) -> id gadget
 * Argumen : prop (string) -> nama kolom (properties) 

Contoh: searchcons(12312, "rarity") -> "S"

### chooser(choice : string) -> void

Buat memproses input fungsi user dengan memanggil fungsi yang dimau user

contoh: chooser("help") -> manggil help()

### getindex(target : string, col : integer, db : array) -> integer

Mencari di Index berapa target berada di array db kolom col

* Argumen : target -> target yang mau dicari
* Argumen : col -> di db kolom (mulai dari nol) berapa target tersebut berada
* Argumen : db -> di db mana target tersebut berada

Akan return indeks target bila ditemukan, -1 bila tidak

Contoh : getindex("thirafinajwan", 1, udb) -> 2

### findcol(name : string) -> integer
Buat nyari berapa banyak kolom di database csvnya

### frl(name : string) -> integer
Buat nyari length first row di db csv

### file_len(name : string) -> integer
Buat nyari panjang karakter csv

### getdb(name : string, mode : string) -> args
Shorthand open

### unload(name : string) -> array

Load Database ke Array 2 Dimensi Tanpa nama Kolom

* Argumen : name -> nama database tanpa .csv


Contoh Argumen yang tersedia:
* unload("user") - output array 2D dari user.csv tanpa nama kolom
* unload("gadget") - output array 2D dari gadget.csv tanpa nama kolom
* unload("consumable") - output array 2D dari consumable.csv tanpa nama kolom
* unload("gadget_borrow_history") - output array 2D dari gadget_borrow_history.csv tanpa nama kolom
* unload("gadget_return_history") - output array 2D dari gadget_return_history.csv tanpa nama kolom
* unload("consumable_history") - output array 2D dari consumable_history.csv tanpa nama kolom

### readargs() -> void

Buat argumen parser

### whatfirst(date1 : string, date2 : string) -> Boolean
NOTE: SELURUH TANGGAL DIASUMSIKAN VALID DAN SESUAI FORMAT

Apakah date1 duluan dari date2, True bila iya, False bila tidak
* Argumen : date1 -> TANGGAL YANG **HARUS MENGIKUTI FORMAT**
* Argumen : date2 -> TANGGAL YANG **HARUS MENGIKUTI FORMAT**

FORMAT TANGGAL:
"dd/mm/yyyy"
Benar : **03**/12/2003 Salah : **3**/12/2003
Benar : 10/**01**/2001 Salah : 10/**1**/2001
Benar : 21/10/**0200** Salah : 21/10/**200**

### gbhsort() -> void
sorting gbhdb berdasarkan tanggal descending

### grhsort() -> void
sorting grhdb berdasarkan tanggal descending

### chsort() -> void
sorting chdb berdasarkan tanggal descending

## F01 - F17

Self Explanatory

## FAQ

reserved for later.

## Further Questions
Line aja ya id  : thirafikurniatama23
atau email juga boleh si : reverseon@outlook.com

## FOOTNOTE

This documentation is not final and may be changed continuously without prior notice.

Regards, ReverseON.