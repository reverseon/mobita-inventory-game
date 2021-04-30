import os
import sys
import math
import time
import argparse
import datetime

# DEVELOPER NOTE
# FILE .CSV HARUS PUNYA 1 ROW KOSONG DI AKHIR FILE 
# .CSV DIASUMSIKAN MENGIKUTI SPESIFIKASI YANG ADA DI GOOGLE DOCS

# GLOBAL DB

udb = ""
gdb = ""
cdb = ""
gbhdb = ""
grhdb = ""
chdb = ""

# GLOBAL DB PROPERTIES

lrudb = 0 # LAST ROW UDB
lrgdb = 0
lrcdb = 0
lrgbhdb = 0
lrgrhdb = 0
lrchdb = 0

# USER CREDENTIALS 
credid = ""
creduname = ""
crednama = ""
credalamat = ""
credpw = ""
credrole = ""

# GLOBAL VAR

savefoldername = "savefolder" # WHERE VARIOUS SAVE FOLDER ARE STORED
savepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), savefoldername) # SAVE FOLDER THAT INCLUDES CSV ( WILL BE MODIFIED WHEN FIRST RUN IN LOAD() )
isExit = False # FOR EXIT
targetfolder = "" # Tempat Folder Save

# MISCELLANEOUS

def strike(text): # 23
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result[:-1]

# FUNDAMENTAL FUNCTION

def searchborrow(id, prop): #1
    index = 0
    for i in range(0, len(gbhdb[0])):
        if gbhdb[0][i] == id:
            index = i
    if prop == "id_peminjam":
        return gbhdb[1][index]
    elif prop == "id_gadget":
        return gbhdb[2][index]
    elif prop == "tanggal_peminjaman":
        return gbhdb[3][index]
    elif prop == "jumlah":
        return gbhdb[4][index]
    else:
        return gbhdb[5][index]

def searchgadget(id, prop): #2
    index = 0
    for i in range(0, len(gdb[0])):
        if gdb[0][i] == id:
            index = i
    if prop == "nama":
        return gdb[1][index]
    elif prop == "deskripsi":
        return gdb[2][index]
    elif prop == "jumlah":
        return gdb[3][index]
    elif prop == "rarity":
        return gdb[4][index]
    else:
        return gdb[5][index]

def searchidcred(id, prop): #3
    index = 0
    for i in range(0, len(udb[0])):
        if udb[0][i] == id:
            index = i
    if prop == "username":
        return udb[1][index]
    elif prop == "nama":
        return udb[2][index]
    elif prop == "alamat":
        return udb[3][index]
    elif prop == "password":
        return udb[4][index]
    else:
        return udb[5][index]

def searchcons(id, prop): #4
    index = 0
    for i in range(0, len(cdb[0])):
        if cdb[0][i] == id:
            index = i
    if prop == "nama":
        return cdb[1][index]
    elif prop == "deskripsi":
        return cdb[2][index]
    elif prop == "jumlah":
        return cdb[3][index]
    else:
        return cdb[4][index]

def chooser(choice): #5
    if choice == "exit":
        yns = input("Apakah anda ingin save session ini? (Y/N): ")
        if (yns != "Y" and yns != "N" and yns != "n" and yns != "y"):
            print("Pilihan Hanya Y/y atau N/n")
            return
        if (yns == "Y" or yns == "y"):
            save()
        exitpr()
    elif choice == "riwayatpinjam":
        riwayatpinjam()
    elif choice == "riwayatkembali":
        riwayatkembali()
    elif choice == "riwayatambil":
        riwayatambil()
    elif choice == "register":
        register()
    elif choice == "save":
        save()
    elif choice == "carirarity":
        carirarity()
    elif choice == "caritahun":
        caritahun()
    elif choice == "hapusitem":
        hapusitem()
    elif choice == "tambahitem":
        tambahitem()
    elif choice == "ubahjumlah":
        ubahjumlah()        
    elif choice == "pinjam":
        pinjam()           
    elif choice == "kembalikan":
        kembalikan()
    elif choice == "minta":
        minta()
    elif choice == "help":
        helpf()
    else:
        print("Fungsi tidak tersedia atau tidak ditemukan!")

def getindex(target, col, db): # 6
    for i in range(0, len(db[col])):
        if db[col][i] == target:
            return i
    return -1

def findcol(name): # FIND COLUMN OF CSV # 7
    with open(savepath + "\\" + targetfolder + "\\" + name + '.csv') as f:
        return f.readline().count(";") + 1

def frl(name): # FIRST ROW LENGTH # 8
    with open(savepath + "\\" + targetfolder + "\\" + name + '.csv') as f:
        return len(f.readline())

def file_len(name): # 9
    with open(savepath + "\\" + targetfolder + "\\" + name + '.csv') as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def getdb(name, mode): # 10
    return open(savepath + "\\" + targetfolder + "\\" + name + '.csv', mode)

def unload(name): # 11
    db = getdb(name, 'r+').read()
    row = file_len(name) - 1 # minus col name
    holder = [[""]*row for i in range(0, findcol(name))]
    rc = 0
    cc = 0
    for i in range(frl(name), len(db)):
        if (db[i] == ";"):
            cc += 1
        elif(db[i] == "\n"):
            rc += 1
            cc = 0
        else:
            holder[cc][rc] += db[i]
    return holder

def readargs(): # 12
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="nama folder load")
    args = parser.parse_args()
    return args.folder

def whatfirst(date1, date2): # is Date 1 duluan than Date 2 # 13
    d1 = int(date1[0:2])
    m1 = int(date1[3:5])
    y1 = int(date1[6:])
    d2 = int(date2[0:2])
    m2 = int(date2[3:5])
    y2 = int(date2[6:])
    if (y1 > y2):
        return False
    elif (y1 < y2):
        return True
    else:
        if (m1 > m2):
            return False
        elif (m1 < m2):
            return True
        else:
            if (d1 < d2):
                return True
            else:
                return False

def gbhsort(): # 14
    global gbhdb
    start = 0
    dblen = len(gbhdb[0])
    while (start != dblen-1):
        localmin = gbhdb[3][start]
        lmid = start
        for i in range(start+1, dblen):
            if whatfirst(localmin, gbhdb[3][i]):
                localmin = gbhdb[3][i]
                lmid = i
        for i in range(0, findcol("gadget_borrow_history")):
            temp = gbhdb[i][lmid]
            gbhdb[i][lmid] = gbhdb[i][start]
            gbhdb[i][start] = temp
        start += 1

def grhsort(): # 15
    global grhdb
    start = 0
    dblen = len(grhdb[0])
    while (start != dblen-1):
        localmin = grhdb[2][start]
        lmid = start
        for i in range(start+1, dblen):
            if whatfirst(localmin, grhdb[2][i]):
                localmin = grhdb[2][i]
                lmid = i
        for i in range(0, findcol("gadget_return_history")):
            temp = grhdb[i][lmid]
            grhdb[i][lmid] = grhdb[i][start]
            grhdb[i][start] = temp
        start += 1

def chsort(): # 16
    global chdb
    start = 0
    dblen = len(chdb[0])
    while (start != dblen-1):
        localmin = chdb[3][start]
        lmid = start
        for i in range(start+1, dblen):
            if whatfirst(localmin, chdb[3][i]):
                localmin = chdb[3][i]
                lmid = i
        for i in range(0, findcol("consumable_history")):
            temp = chdb[i][lmid]
            chdb[i][lmid] = chdb[i][start]
            chdb[i][start] = temp
        start += 1

def random(): # 17
    return (8121 * int(time.time()) + 28411) % 134456;

def isalphanumberlower(uname): # 18
    for i in uname:
        check = ord(i)
        if (((not (check >= 48 and check <= 57)) and (not (check >= 97 and check <= 122))) or check == 32): # 48 - 57 number, 97 - 122 lowercase, 32 space
            return False
    return True

def isnumber(target): # 19
    if len(target) == 0:
        return False
    for i in target:
        check = ord(i)
        if (not (check >= 48 and check <= 57)):
            return False
    return True

def checkdup(val, col, arrdb): # 20
    for i in arrdb[col]:
        if (val == i):
            return True
    return False

def checkdir(name): # 21
    listdir = [a for a in os.listdir(savepath) if os.path.isdir(os.path.join(savepath, a))]
    for h in listdir:
        if h == name:
            return True
    return False

def isformatvalid(date): # 22
    if len(date) == 10:
        dd = date[0:2]
        mm = date[3:5]
        yy = date[6::]
        if (not isnumber(dd) or not isnumber(mm) or not isnumber(yy)):
            return False
        else:
            try:
                datetime.datetime(year=int(yy), month=int(mm), day=int(dd))
                return True
            except:
                return False
    else:
        return False

# F01 - F17

def exitpr():
    global isExit
    isExit = not isExit
    print("Terima Kasih Telah Bermain bersama Kantong Ajaib! Wishing You A Great Adventure Ahead!")

def load():
    global savepath
    global udb
    global cdb
    global gdb
    global gbhdb
    global grhdb
    global chdb
    global targetfolder
    global lrudb 
    global lrgdb 
    global lrcdb 
    global lrgbhdb 
    global lrgrhdb 
    global lrchdb 
    targetfolder = readargs()
    if not (os.path.exists(os.path.join(savepath, targetfolder))):
        print("File Save Tidak Tersedia, Silahkan Ulangi Program dengan Argumen yang Benar")
        exit() # EOF 1
    udb = unload("user")
    gdb = unload("gadget")
    cdb = unload("consumable")
    gbhdb = unload("gadget_borrow_history")
    grhdb = unload("gadget_return_history")
    chdb = unload("consumable_history")
    lrudb = file_len("user")  
    lrgdb = file_len("gadget")
    lrcdb = file_len("consumable")
    lrgbhdb = file_len("gadget_borrow_history")
    lrgrhdb = file_len("gadget_return_history")
    lrchdb = file_len("consumable_history")
    print("Load Database Sukses...")
    print("Selamat Datang di Kantong Ajaib!")
    print(strike("Aku Ingin Terbang Bebas di Angkasaaaa..."))
    print(strike("Hey... Ada Maling Jambu!"))

def login():
    global credid
    global creduname
    global crednama
    global credalamat
    global credpw
    global credrole
    print("Masukkan username:", end=" ")
    uname = input()
    index = getindex(uname, 1, udb)
    while (index == -1):
        print("username tidak ditemukan\nsilahkan masukkan kembali username yang benar:", end=" ")
        uname = input()
        index = getindex(uname, 1, udb)
    print("Masukkan password:", end=" ")
    pw = input()
    while (pw != udb[4][index]):
        print("password yang anda masukkan salah\nsilahkan masukkan password kembali:", end=" ")
        pw = input()
    # UPDATE CREDENTIALS 
    credid = udb[0][index]
    creduname = udb[1][index]
    crednama = udb[2][index]
    credalamat = udb[3][index]
    credpw = udb[4][index]
    credrole = udb[5][index]
    print(f"\nUser {uname}! Selamat Datang di Kantong Ajaib")

def register():
    if (credrole == "user"):
        print("Maaf, fitur ini hanya bisa diakses oleh admin, terima kasih.")
        return
    global udb
    print("Selamat Datang di Bagian Registrasi, silahkan masukan nama, username, password dan alamat kamu.")
    print("Harap diperhatikan bahwa username yang dimasukkan harus memenuhi beberapa kriteria yaitu:")
    print("1. Hanya dapat terdiri dari karakter a-z dan angka 0-9")
    print("2. Tidak boleh mengandung spasi")
    print("3. Tidak boleh kosong dan tidak boleh lebih dari 16 karakter")
    print("4. Tidak boleh sama dengan user yang sudah terlebih dahulu mendaftar")
    idn = str(random())
    while (checkdup(idn, 0, udb)):
            idn = str(random())
    print("Masukan nama:", end=" ")
    nama = input()
    if nama == "":
        print("Nama tidak boleh kosong")
        return
    print("Masukan username:", end=" ")
    uname = input()
    while (not (isalphanumberlower(uname) and (not checkdup(uname, 1, udb) and (len(uname) <= 16 and len(uname) > 0)))):
            print("Username sudah digunakan atau tidak memenuhi kriteria\nsilahkan masukan username kembali:", end=" ")
            uname = input()
    print("Masukan password:", end=" ")
    pw = input()
    if pw == "":
        print("Password tidak boleh kosong")
        return
    print("Masukan alamat:", end=" ")
    alamat = input()
    if alamat == "":
        print("Alamat tidak boleh kosong")
    udb[0].append(idn)
    udb[1].append(uname)
    udb[2].append(nama)
    udb[3].append(alamat)
    udb[4].append(pw)
    udb[5].append("user")
    print(f"\nUser {uname} telah berhasil register ke dalam Kantong Ajaib")

def carirarity():
    print("Masukkan rarity:", end=" ")
    rarity = input()
    if (not (rarity == "C" or rarity == "B" or rarity == "A" or rarity == "S")):
        print("Rarity tidak valid. value yang valid hanya C, B, A, dan S")
        return
    print("\nHasil Pencarian :", end="\n\n")
    counter = 0
    for i in range(0, len(gdb[4])):
        if (gdb[4][i] == rarity):
            counter += 1
            print("Nama: " + gdb[1][i])
            print("Deskripsi: " + gdb[2][i])
            print("Jumlah: " + gdb[3][i] + " buah")
            print("Rarity: " + gdb[4][i])
            print("Tahun Ditemukan: " + gdb[5][i])
            print()
    if (counter == 0):
        print(f"Tidak ada Item dengan Rarity {rarity} ditemukan")

def caritahun():
    print("Masukkan tahun:", end=" ")
    tahun = input()
    if (len(tahun) != 4 or not isnumber(tahun)):
        print("Tahun tidak valid. silahkan masukkan TEPAT 4 digit ANGKA (0-9) tahun dengan nol di depan tetap ditulis, mis: 0211")
        return 
    print("Masukkan kategori:", end=" ")
    kategori = input()
    print("\nHasil Pencarian:", end="\n\n")
    if (kategori == "="):
        found = False
        for i in range(0, len(gdb[4])):
            if (int(gdb[5][i]) == int(tahun)):
                found = True
                print("Nama: " + gdb[1][i])
                print("Deskripsi: " + gdb[2][i])
                print("Jumlah: " + gdb[3][i] + " buah")
                print("Rarity: " + gdb[4][i])
                print("Tahun Ditemukan: " + gdb[5][i])
                print()
        if not found:
            print("Tidak ada Gadget yang memenuhi kriteria")
    elif (kategori == ">"):
        found = False
        for i in range(0, len(gdb[4])):
            if (int(gdb[5][i]) > int(tahun)):
                found = True
                print("Nama: " + gdb[1][i])
                print("Deskripsi: " + gdb[2][i])
                print("Jumlah: " + gdb[3][i] + " buah")
                print("Rarity: " + gdb[4][i])
                print("Tahun Ditemukan: " + gdb[5][i])
                print()
        if not found:
            print("Tidak ada Gadget yang memenuhi kriteria")
    elif (kategori == "<"):
        found = False
        for i in range(0, len(gdb[4])):
            if (int(gdb[5][i]) < int(tahun)):
                found = True
                print("Nama: " + gdb[1][i])
                print("Deskripsi: " + gdb[2][i])
                print("Jumlah: " + gdb[3][i] + " buah")
                print("Rarity: " + gdb[4][i])
                print("Tahun Ditemukan: " + gdb[5][i])
                print()
        if not found:
            print("Tidak ada Gadget yang memenuhi kriteria")
    elif (kategori == "<="):
        found = False
        for i in range(0, len(gdb[4])):
            if (int(gdb[5][i]) <= int(tahun)):
                found = True
                print("Nama: " + gdb[1][i])
                print("Deskripsi: " + gdb[2][i])
                print("Jumlah: " + gdb[3][i] + " buah")
                print("Rarity: " + gdb[4][i])
                print("Tahun Ditemukan: " + gdb[5][i])
                print()
        if not found:
            print("Tidak ada Gadget yang memenuhi kriteria")
    elif (kategori == ">="):
        found = False
        for i in range(0, len(gdb[4])):
            if (int(gdb[5][i]) >= int(tahun)):
                found = True
                print("Nama: " + gdb[1][i])
                print("Deskripsi: " + gdb[2][i])
                print("Jumlah: " + gdb[3][i] + " buah")
                print("Rarity: " + gdb[4][i])
                print("Tahun Ditemukan: " + gdb[5][i])
                print()
        if not found:
            print("Tidak ada Gadget yang memenuhi kriteria")
    else:
        print("kategori tidak ditemukan")

def tambahitem():
    if credrole == "admin":
        itemid = input("Masukkan ID: ")
        if len(itemid) < 2 or not (itemid[0] in ['G', 'C'] and len(itemid) == 1 and isnumber(itemid[1:]) and int(itemid[1:]) > 0):
            print("Format ID tidak Valid, id harus diawali G atau C diikuti dengan integer lebih dari nol")
            return
        elif itemid[0] == 'G':
            if checkdup(itemid, 0, gdb):
                print("Gagal menambahkan item karena ID sudah ada")
                return
            nama = input("Masukkan nama: ")
            if (nama == ""):
                print("Nama tidak valid, nama tidak boleh kosong.")
                return
            deskripsi = input("Masukkan deskripsi: ")
            if (deskripsi == ""):
                print("Deskripsi tidak valid, deskripsi tidak boleh kosong.")
                return
            jumlah = input("Masukkan jumlah: ")
            if (not isnumber(jumlah) or jumlah == ""):
                print("Jumlah tidak valid. jumlah tidak boleh kosong dan hanya masukkan angka integer")
                return
            rarity = input("Masukkan rarity: ")
            if (not (rarity == "C" or rarity == "B" or rarity == "A" or rarity == "S")):
                print("Rarity tidak valid. value yang valid hanya C, B, A, dan S")
                return
            tahun = input("Masukkan tahun ditemukan (yyyy): ")
            if (len(tahun) != 4 or not isnumber(tahun)):
                print("Tahun tidak valid. silahkan masukkan TEPAT 4 digit ANGKA (0-9) tahun dengan nol di depan tetap ditulis, mis: 0211")
                return 
            gdb[0].append(itemid)
            gdb[1].append(nama)
            gdb[2].append(deskripsi)
            gdb[3].append(jumlah)
            gdb[4].append(rarity)
            gdb[5].append(tahun)
            print("Item telah berhasil ditambahkan ke database")
        else:
            if checkdup(itemid, 0, cdb):
                print("Gagal menambahkan item karena ID sudah ada")
                return
            nama = input("Masukkan nama: ")
            if (nama == ""):
                print("Nama tidak valid, nama tidak boleh kosong.")
                return
            deskripsi = input("Masukkan deskripsi: ")
            if (deskripsi == ""):
                print("Deskripsi tidak valid, deskripsi tidak boleh kosong.")
                return
            jumlah = input("Masukkan jumlah: ")
            if (not isnumber(jumlah) or jumlah == ""):
                print("Jumlah tidak valid. jumlah tidak boleh kosong dan hanya masukkan angka integer")
                return
            rarity = input("Masukkan rarity: ")
            if (not (rarity == "C" or rarity == "B" or rarity == "A" or rarity == "S")):
                print("Rarity tidak valid. value yang valid hanya C, B, A, dan S")
                return
            cdb[0].append(itemid)
            cdb[1].append(nama)
            cdb[2].append(deskripsi)
            cdb[3].append(jumlah)
            cdb[4].append(rarity)
            print("Item telah berhasil ditambahkan ke database") 
    else:
        print("Maaf, Fitur Ini Hanya Bisa Diakses oleh Admin")

def hapusitem():
    if (credrole == "user"):
        print("Maaf, fitur ini hanya bisa diakses oleh admin, terima kasih.")
        return
    itemid = input("Masukkan Item ID: ")
    if len(itemid) < 2 or not (itemid[0] in ['G', 'C'] and isnumber(itemid[1:]) and int(itemid[1:]) > 0):
        print("Format ID tidak Valid, id harus diawali G atau C diikuti dengan integer lebih dari nol")
        return
    elif itemid[0] == "G":
        if not checkdup(itemid, 0, gdb):
             print("Tidak ada Item dengan ID tersebut")
        else:
            index = getindex(itemid, 0, gdb)
            print(f"Apakah anda yakin ingin menghapus {searchgadget(itemid, 'nama')} (Y/N)? ")
            choose = input()
            if (choose == 'Y' or choose == "y"):
                for i in range(0, len(gdb)):
                    gdb[i].pop(index)
                print("Item berhasil dihapus dari database")
            elif (choose == "N" or choose == "n"):
                print("Proses Dibatalkan")
            else:
                print("Pilihan tidak valid, hanya tersedia Y/y dan N/n")
    else:
        if not checkdup(itemid, 0, cdb):
             print("Tidak ada Item dengan ID tersebut")
        else:
            index = getindex(itemid, 0, cdb)
            print(f"Apakah anda yakin ingin menghapus {searchcons(itemid, 'nama')} (Y/N)? ")
            choose = input()
            if (choose == 'Y' or choose == "y"):
                for i in range(0, len(cdb)):
                    cdb[i].pop(index)
                print("Item berhasil dihapus dari database")
            elif (choose == "N" or choose == "n"):
                print("Proses Dibatalkan")
            else:
                print("Pilihan tidak valid, hanya tersedia Y/y dan N/n")

def ubahjumlah():
    if (credrole == "user"):
        print("Maaf, fitur ini hanya bisa diakses oleh admin, terima kasih.")
        return
    itemid = input("Masukkan Item ID: ")
    if len(itemid) < 2 or not (itemid[0] in ['G', 'C'] and isnumber(itemid[1:]) and int(itemid[1:]) > 0):
        print("Format ID tidak Valid, id harus diawali G atau C diikuti dengan integer lebih dari nol")
        return
    elif itemid[0] == "G":
        if not checkdup(itemid, 0, gdb):
             print("Tidak ada Item dengan ID tersebut")
        else:
            index = getindex(itemid, 0, gdb)
            jumlah = int(searchgadget(itemid, "jumlah"))
            alter = input("Masukkan Jumlah: ")
            if (not isnumber(alter[1::] if alter[0] == "-" else alter)):
                print("Jumlah alteration harus integer")
                return
            alter = int(alter)
            if (jumlah + alter >= 0):
                print(f"{alter} {searchgadget(itemid, 'nama')} berhasil {'dibuang' if jumlah < 0 else 'ditambahkan'}")
                gdb[3][index] = str(jumlah + alter)
                print(f"Stok sekarang: {gdb[3][index]}")
            else:
                print(f"{abs(alter)} {searchgadget(itemid, 'nama')} gagal dibuang karena stok kurang.")
                print(f"Stok sekarang: {gdb[3][index]}")
    else:
        if not checkdup(itemid, 0, cdb):
             print("Tidak ada Item dengan ID tersebut")
        else:
            index = getindex(itemid, 0, cdb)
            jumlah = int(searchcons(itemid, "jumlah"))
            alter = input("Masukkan Jumlah: ")
            if (not isnumber(alter[1::] if alter[0] == "-" else alter)):
                print("Jumlah alteration harus integer")
                return
            alter = int(alter)
            if (jumlah + alter >= 0):
                print(f"{alter} {searchcons(itemid, 'nama')} berhasil {'dibuang' if jumlah < 0 else 'ditambahkan'}")
                cdb[3][index] = str(jumlah + alter)
                print(f"Stok sekarang: {cdb[3][index]}")
            else:
                print(f"{abs(alter)} {searchcons(itemid, 'nama')} gagal dibuang karena stok kurang.")
                print(f"Stok sekarang: {cdb[3][index]}")

def pinjam():
    if (credrole == "admin"):
        print("Maaf, fitur ini hanya bisa diakses oleh user, terima kasih.")
        return
    itemid = input("Masukkan Item ID: ")
    if len(itemid) < 2 or not (itemid[0] in ['G'] and isnumber(itemid[1:]) and int(itemid[1:]) > 0):
        print("Format ID tidak Valid, id harus diawali G diikuti dengan integer lebih dari nol")
        return
    else:
        if not checkdup(itemid, 0, gdb):
             print("Tidak ada Item dengan ID tersebut")
        else:
            tanggal = input("Tanggal Peminjaman: ")
            if (not isformatvalid(tanggal)):
                print("Format Tanggal Tidak Valid, silahkan gunakan dd/mm/yyyy tepat 10 karakter")
                print("Benar:\n03/01/0020 (3 Januari 20)")
                print("Salah:\n3/1/20 (3 Januari 20)")
                return
            index = getindex(itemid, 0, gdb)
            jumlah = int(searchgadget(itemid, "jumlah"))
            alter = input("Masukkan Jumlah: ")
            if (not isnumber(alter)):
                print("Jumlah Peminjaman harus integer dan lebih dari atau sama dengan nol")
                return
            alter = int(alter)
            if (jumlah - alter >= 0):
                print(f"Item {searchgadget(itemid, 'nama')} (x{alter}) berhasil dipinjam!")
                gdb[3][index] = str(jumlah - alter)
                gbhdb[0].append(str(random()))
                gbhdb[1].append(str(credid))
                gbhdb[2].append(itemid)
                gbhdb[3].append(tanggal)
                gbhdb[4].append(str(alter))
                gbhdb[5].append("false")
            else:
                print(f"Item {searchgadget(itemid, 'nama')} (x{alter}) gagal dipinjam karena stok kurang.")

def kembalikan():
    if (credrole == "admin"):
        print("Maaf, fitur ini hanya bisa diakses oleh user, terima kasih.")
        return
    chid = []
    counter = 0
    for i in range(0, len(gbhdb[1])):
        if (gbhdb[1][i] == credid and gbhdb[5][i] == "false"):
            print(f"{counter+1}. {searchgadget(gbhdb[2][i], 'nama')}")
            counter += 1
            chid.append(gbhdb[0][i])
    if (counter == 0):
        print("Tidak ada barang yang bisa dikembalikan")
        return
    no = input("Masukkan nomor peminjaman: ")
    if (not isnumber(no)):
        print("Nomor tidak valid, pastikan hanya memasukkan opsi yang tersedia")
        return
    elif int(no) > counter:
        print("Nomor tidak valid, pastikan hanya memasukkan opsi yang tersedia")
        return
    no = int(no)
    idx = getindex(chid[no-1], 0, gbhdb)
    jumlah = input("Jumlah pengembalian: ")
    if (not isnumber(jumlah)):
        print("Jumlah tidak valid, jumlah hanya bisa integer positif dan nol")
        return
    jumlah = int(jumlah)
    if (jumlah <= int(gbhdb[4][idx])):
        afterstock = int(gbhdb[4][idx]) - jumlah
        tanggal = input("Tanggal Pengembalian: ")
        if (not isformatvalid(tanggal)):
            print("Format Tanggal Tidak Valid, silahkan gunakan dd/mm/yyyy tepat 10 karakter")
            print("Benar:\n03/01/0020 (3 Januari 20)")
            print("Salah:\n3/1/20 (3 Januari 20)")
            return
        print(f"Item {searchgadget(gbhdb[2][idx], 'nama')} (x{jumlah}) telah berhasil dikembalikan")
        if afterstock == 0:
            gbhdb[5][idx] = "true"
            print("Seluruh Gadget Sudah Dikembalikan")
        gbhdb[4][idx] = str(afterstock)
        grhdb[0].append(str(random()))
        grhdb[1].append(gbhdb[0][idx])
        grhdb[2].append(tanggal)
        # ALTER GADGET CSV
        gadgetidx = getindex(gbhdb[2][idx], 0, gdb)
        gdb[3][gadgetidx] = str(jumlah + int(gdb[3][gadgetidx]))
    else:
        print("Jumlah Pengembalian tidak bisa melebihi jumlah peminjaman")

def minta():
    if (credrole == "admin"):
        print("Maaf, fitur ini hanya bisa diakses oleh user, terima kasih.")
        return
    itemid = input("Masukkan Item ID: ")
    if len(itemid) < 2 or not (itemid[0] in ['C'] and isnumber(itemid[1:]) and int(itemid[1:]) > 0):
        print("Format ID tidak Valid, id harus diawali C diikuti dengan integer lebih dari nol")
        return
    else:
        if not checkdup(itemid, 0, cdb):
            print("Tidak ada Consumables dengan ID tersebut")
        else:
            considx = getindex(itemid, 0, cdb)
            stock = int(cdb[3][considx])  
            if stock <= 0:
                print("Consumables Kosong, Silahkan coba consumables lain")
                return
            jumlah = input("Masukkan Jumlah: ")
            if (not isnumber(jumlah)):
                print("Jumlah tidak valid, pastikan jumlah adalah angka integer positif atau nol")
                return
            jumlah = int(jumlah)
            if jumlah > stock:
                print(f"Stok yang tersedia hanya {stock} buah")
                print("Tidak bisa meminta lebih dari stok yang ada")
                return
            tanggal = input("Tanggal Permintaan: ")
            if (not isformatvalid(tanggal)):
                print("Format Tanggal Tidak Valid, silahkan gunakan dd/mm/yyyy tepat 10 karakter")
                print("Benar:\n03/01/0020 (3 Januari 20)")
                print("Salah:\n3/1/20 (3 Januari 20)")
                return
            cdb[3][considx] = str(stock - jumlah)
            # RECORD
            chdb[0].append(str(random()))
            chdb[1].append(credid)
            chdb[2].append(cdb[0][considx])
            chdb[3].append(tanggal)
            chdb[4].append(str(jumlah))
            print(f"Item {cdb[1][considx]} (x{jumlah}) telah berhasil diambil!") 

def riwayatpinjam(): # Gadget Borrow History (gbhdb)
    if credrole == "admin":
        if (gbhdb[0] == []):
            print("Tidak ada data yang dapat ditampilkan")
            return
        gbhsort()
        row = len(gbhdb[0])
        page = 0
        while True:
            for i in range(page*5, page*5+5 if page*5+5 < row else row):
                print()
                print("ID Peminjaman:", gbhdb[0][i])
                print("Nama Peminjam:", searchidcred(gbhdb[1][i], "nama"))
                print("Nama Gadget:", searchgadget(gbhdb[2][i], "nama"))
                print("Tanggal Pengambilan:", gbhdb[3][i])
                print("Jumlah:", gbhdb[4][i])
            print()
            print(f"b for back, n for next, any string for exit")
            print(">>>", end=" ")
            ch = input()
            if (ch == 'b'):
                page = page-1 if page > 0 else 0
            elif (ch == 'n'):
                page = page+1 if page < row//5 else (row//5)
            else:
                break
    else:
        print("Maaf, Fitur Ini Hanya Bisa Diakses oleh Admin")

def riwayatkembali(): # GADGET RETURN HISTORY (grhdb)
    if credrole == "admin":
        if (grhdb[0] == []):
            print("Tidak ada data yang dapat ditampilkan")
            return
        grhsort()
        row = len(grhdb[0])
        page = 0
        while True:
            for i in range(page*5, page*5+5 if page*5+5 < row else row):
                print()
                print("ID Peminjaman:", grhdb[0][i])
                print("Nama Peminjam:", searchidcred(searchborrow(grhdb[1][i], "id_peminjam"), "nama"))
                print("Nama Gadget:", searchgadget(searchborrow(grhdb[1][i], "id_gadget"), "nama"))
                print("Tanggal Pengembalian:", grhdb[2][i])
            print()
            print(f"b for back, n for next, any string for exit")
            print(">>>", end=" ")
            ch = input()
            if (ch == 'b'):
                page = page-1 if page > 0 else 0
            elif (ch == 'n'):
                page = page+1 if page < row//5 else (row//5)
            else:
                break
    else:
        print("Maaf, Fitur Ini Hanya Bisa Diakses oleh Admin")

def riwayatambil(): # CONSUMABLE HISTORY (chdb)
    if credrole == "admin":
        if (chdb[0] == []):
            print("Tidak ada data yang dapat ditampilkan")
            return
        chsort()
        row = len(chdb[0])
        page = 0
        while True:
            for i in range(page*5, page*5+5 if page*5+5 < row else row):
                print()
                print("ID Pengambilan:", chdb[0][i])
                print("Nama Pengambil:", searchidcred(chdb[1][i], "nama"))
                print("Nama Consumable:", searchcons(chdb[2][i], "nama"))
                print("Tanggal Peminjaman:", chdb[3][i])
                print("Jumlah:", chdb[4][i])
            print()
            print(f"b for back, n for next, any string for exit")
            print(">>>", end=" ")
            ch = input()
            if (ch == 'b'):
                page = page-1 if page > 0 else 0
            elif (ch == 'n'):
                page = page+1 if page < row//5 else (row//5)
            else:
                break
    else:
        print("Maaf, Fitur Ini Hanya Bisa Diakses oleh Admin")

def save():
    savetarget = input("Masukkan nama folder penyimpanan: ")
    if not checkdir(savetarget):
        os.mkdir(savepath + "\\" + savetarget)
    # USER CSV
    holderfile = open(savepath + "\\" + savetarget + "\\" + 'user.csv', 'w')
    holderfile.write("id;username;nama;alamat;password;role\n")
    for i in range(0, len(udb[0])):
        for j in range(0, 5):
            holderfile.write(udb[j][i] + ";")
        holderfile.write(udb[5][i])
        holderfile.write("\n")
    # GADGET CSV
    holderfile = open(savepath + "\\" + savetarget + "\\" + 'gadget.csv', 'w')
    holderfile.write("id;nama;deskripsi;jumlah;rarity;tahun_ditemukan\n")
    for i in range(0, len(gdb[0])):
        for j in range(0, 5):
            holderfile.write(gdb[j][i] + ";")
        holderfile.write(gdb[5][i])
        holderfile.write("\n")    
    # CONSUMABLE CSV
    holderfile = open(savepath + "\\" + savetarget + "\\" + 'consumable.csv', 'w')
    holderfile.write("id;nama;deskripsi;jumlah;rarity\n")
    for i in range(0, len(cdb[0])):
        for j in range(0, 4):
            holderfile.write(cdb[j][i] + ";")
        holderfile.write(cdb[4][i])
        holderfile.write("\n")
    # GADGET RETURN HISTORY
    holderfile = open(savepath + "\\" + savetarget + "\\" + 'gadget_return_history.csv', 'w')
    holderfile.write("id;id_peminjaman;tanggal_pengembalian\n")
    for i in range(0, len(grhdb[0])):
        for j in range(0, 2):
            holderfile.write(grhdb[j][i] + ";")
        holderfile.write(grhdb[2][i])
        holderfile.write("\n")
    # GADGET BORROW HISTORY
    holderfile = open(savepath + "\\" + savetarget + "\\" + 'gadget_borrow_history.csv', 'w')
    holderfile.write("id;id_peminjam;id_gadget;tanggal_peminjaman;jumlah;is_returned\n")
    for i in range(0, len(gbhdb[0])):
        for j in range(0, 5):
            holderfile.write(gbhdb[j][i] + ";")
        holderfile.write(gbhdb[5][i])
        holderfile.write("\n")
    # CONSUMABLE HISTORY CSV
    holderfile = open(savepath + "\\" + savetarget + "\\" + 'consumable_history.csv', 'w')
    holderfile.write("id;id_pengambil;id_consumable;tanggal_pengambilan;jumlah\n")
    for i in range(0, len(chdb[0])):
        for j in range(0, 4):
            holderfile.write(chdb[j][i] + ";")
        holderfile.write(chdb[4][i])
        holderfile.write("\n")
    print("Saving...")
    print(f"Data telah berhasil disimpan pada folder {savetarget}!")

def helpf():
    print("=============HELP============")
    if credrole == "admin":
        print("register -- menambahkan user ke dalam database")
        print("tambahitem -- menambahkan Gadget atau Consumables ke database")
        print("hapusitem -- menghapus Gadget atau Consumables dari database")
        print("ubahjumlah -- menambahkan jumlah gadget atau consumables di database")
        print("riwayatpinjam -- melihat riwayat peminjaman gadget")
        print("riwayatkembali -- melihat riwayat pengembalian gadget")
        print("riwayatambil -- melihat riwayat pengambilan gadget")
    elif credrole == "user":
        print("pinjam -- meminjam gadget")
        print("kembalikan -- mengembalikan gadget yang dipinjam")
        print("minta -- meminta consumables")
    else:
        print("Untuk mengakses seluruh fungsi, silahkan login terlebih dahulu\n")
        print("==========AKSES UMUM=========")
        print("login -- untuk masuk ke dalam sistem")
        print("=========AKSES ADMIN==========")
        print("register -- menambahkan user ke dalam database")
        print("tambahitem -- menambahkan Gadget atau Consumables ke database")
        print("hapusitem -- menghapus Gadget atau Consumables dari database")
        print("ubahjumlah -- menambahkan jumlah gadget atau consumables di database")
        print("riwayatpinjam -- melihat riwayat peminjaman gadget")
        print("riwayatkembali -- melihat riwayat pengembalian gadget")
        print("riwayatambil -- melihat riwayat pengambilan gadget")
        print("=========AKSES USER==========")
        print("pinjam -- meminjam gadget")
        print("kembalikan -- mengembalikan gadget yang dipinjam")
        print("minta -- meminta consumables")
        print("=====AKSES ADMIN & USER======")
    print("carirarity -- mencari gadget berdasarkan rarity")
    print("caritahun -- mencari gadget berdasarkan tahun ditemukan")
    print("save -- menyimpan database ke folder save")
    print("exit -- keluar dari program")

# MAIN DRIVER
if __name__ == "__main__":
    load()
    print("\nSelamat Datang di Kantong Ajaib")
    while credrole == "" and not isExit:
        print("\nSilahkan Masukkan Menu yang ingin dipilih, untuk list menu, ketik help\n")
        print(">>>", end=" ")
        choose = input()
        if choose == "help":
            helpf()
        elif choose == "login":
            login()
        elif choose == "exit":
            exitpr()
        else:
            print("Fungsi tidak tersedia, tidak ditemukan, atau tidak dapat diakses!")
    while not isExit:
        print("\nSilahkan Masukkan Menu yang ingin dipilih, untuk list menu, ketik help\n")
        print(">>>", end=" ")
        choose = input()
        chooser(choose)