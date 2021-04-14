import argparse
import os

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

# USER CREDENTIALS 
credid = ""
creduname = ""
crednama = ""
credalamat = ""
credpw = ""
credrole = ""


# DB PROPERTIES NOTE
# USER        : COL = 6 FROWLEN = 38
# GADGET      : COL = 6 FROWLEN = 48
# CONSUMABLES : COL = 5 FROWLEN = 32
# G BORROW H  : COL = 5 FROWLEN = 51
# G RETURN H  : COL = 5 FROWLEN = 46
# CONS H      : COL = 4 FROWLEN = 38

# GLOBAL VAR

savefoldername = "savefolder" # WHERE VARIOUS SAVE FOLDER ARE STORED
savepath = os.path.dirname(os.path.realpath(__file__)) + "\\" + savefoldername # SAVE FOLDER THAT INCLUDES CSV ( WILL BE MODIFIED WHEN FIRST RUN IN LOAD() )
isExit = False # FOR EXIT

# MISCELLANEOUS

def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result[:-1]

# FUNDAMENTAL FUNCTION

def na():
    print("Not Available")

def searchgadget(id, prop):
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

def searchidcred(id, prop):
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

def searchcons(id, prop):
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

def chooser(choice):
    if choice == "exit":
        print("Terima Kasih Telah Bermain bersama Kantong Ajaib! Wishing You A Great Adventure Ahead!")
        exitpr()
    elif choice == "riwayatpinjam":
        riwayatpinjam()
    elif choice == "riwayatkembali":
        riwayatkembali()
    elif choice == "riwayatambil":
        riwayatambil()
    else:
        print("Fungsi tidak tersedia atau tidak ditemukan!")

def getindex(target, col, db):
    for i in range(0, len(db[col])):
        if db[col][i] == target:
            return i
    return -1

def findcol(name): # FIND COLUMN OF CSV
    with open(savepath + name + '.csv') as f:
        return f.readline().count(";") + 1

def frl(name): # FIRST ROW LENGTH
    with open(savepath + name + '.csv') as f:
        return len(f.readline())

def file_len(name):
    with open(savepath + name + '.csv') as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def getdb(name, mode):
    return open(savepath + name + '.csv', mode)

def unload(name):
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

def readargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="nama folder load")
    args = parser.parse_args()
    return args.folder

def whatfirst(date1, date2): # is Date 1 duluan than Date 2
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

def gbhsort():
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

def gbhsort():
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

def grhsort():
    global grhdb
    start = 0
    dblen = len(grhdb[0])
    while (start != dblen-1):
        localmin = grhdb[3][start]
        lmid = start
        for i in range(start+1, dblen):
            if whatfirst(localmin, grhdb[3][i]):
                localmin = grhdb[3][i]
                lmid = i
        for i in range(0, findcol("gadget_return_history")):
            temp = grhdb[i][lmid]
            grhdb[i][lmid] = grhdb[i][start]
            grhdb[i][start] = temp
        start += 1

def chsort():
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


# F01 - F17

def exitpr():
    global isExit
    isExit = not isExit

def load():
    global savepath
    global udb
    global cdb
    global gdb
    global gbhdb
    global grhdb
    global chdb
    savepath = savepath + "\\" + readargs() + "\\"
    if not (os.path.exists(savepath)):
        print("File Save Tidak Tersedia, Silahkan Ulangi Program dengan Argumen yang Benar")
        exit() # EOF 1
    udb = unload("user")
    gdb = unload("gadget")
    cdb = unload("consumable")
    gbhdb = unload("gadget_borrow_history")
    grhdb = unload("gadget_return_history")
    chdb = unload("consumable_history")
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

def riwayatpinjam(): # Gadget Borrow History (gbhdb)
    if credrole == "admin":
        gbhsort()
        row = len(gbhdb[0])
        page = 0
        while True:
            for i in range(page*5, page*5+5 if page*5+5 < row else row):
                print()
                print("ID Peminjaman:", gbhdb[0][i])
                print("Nama Peminjam:", searchidcred(gbhdb[1][i], "nama"))
                print("Nama Gadget:", searchgadget(gbhdb[2][i], "nama"))
                print("Tanggal Peminjaman:", gbhdb[3][i])
                print("Jumlah:", gbhdb[4][i])
                holder = i
            print()
            print(f"b for back, n for next, e for exit")
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
        grhsort()
        row = len(grhdb[0])
        page = 0
        while True:
            for i in range(page*5, page*5+5 if page*5+5 < row else row):
                print()
                print("ID Peminjaman:", grhdb[0][i])
                print("Nama Peminjam:", searchidcred(grhdb[1][i], "nama"))
                print("Nama Gadget:", searchgadget(grhdb[2][i], "nama"))
                print("Tanggal Peminjaman:", grhdb[3][i])
                holder = i
            print()
            print(f"b for back, n for next, e for exit")
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
                holder = i
            print()
            print(f"b for back, n for next, e for exit")
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

if __name__ == "__main__":
    load()
    print("\nUntuk Menggunakan Kantong Ajaib, Silahkan Login Terlebih Dahulu\n")
    login()
    while not isExit:
        print("Silahkan Masukkan Menu yang ingin dipilih, untuk list menu, ketik help\n")
        print(">>>", end=" ")
        choose = input()
        chooser(choose)