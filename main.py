import base64
from tkinter import *
from tkinter import messagebox

def encode(key,clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key,enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def save_enc_notes():
    title = entry_title.get()
    message = text_secret.get("1.0", END)
    master_key = entry_masterKey.get()

    if not title or not message or not master_key:
        messagebox.showwarning("Error","Please enter all info")
    else:
        #encryption
        enc_message = encode(master_key, message)
        try:
            with open("mysecret.txt","a") as data_file:
                data_file.write(f"\n{title}\n{enc_message}")
        except FileNotFoundError:
            with open("mysecret.txt","w") as data_file:
                data_file.write(f"\n{title}\n{enc_message}")
        finally:
            entry_title.delete(0,END)
            entry_masterKey.delete(0,END)
            text_secret.delete("1.0", END)

def dec_notes():
    enc_message = text_secret.get("1.0", END)
    masterKey= entry_masterKey.get()

    if not enc_message or not masterKey:
        messagebox.showerror("Error", message="Please enter your encrypted text to secreet. And please enter your master key!")
    else:
        try:
            dec_message = decode(masterKey, enc_message)
            text_secret.delete("1.0", END)
            text_secret.insert("1.0", dec_message)
        except:
            messagebox.showerror("Error", "Please enter encrypted text")

#UI
FONT = ("Verdana",20,"normal")
window = Tk()
window.title("Secret Notes")
window.config(padx=30,pady=30)

img_logo = PhotoImage(file="secret.png")
img_label = Label(image= img_logo)
img_label.pack()

lbl_title = Label(text="Enter your title", font=FONT)
lbl_title.pack()

entry_title = Entry(width=30)
entry_title.pack()

lbl_secret = Label(text="Enter your secret", font=FONT)
lbl_secret.pack()

text_secret = Text(width=50,height=30)
text_secret.pack()

lbl_masterKey = Label(text="Enter master key", font=FONT)
lbl_masterKey.pack()

entry_masterKey = Entry(width=30, show="*")
entry_masterKey.pack()

btn_save_enc = Button(text="Save & Encrypt", command=save_enc_notes)
btn_save_enc.pack()

btn_decrypt = Button(text="Decrypt", command=dec_notes)
btn_decrypt.pack()

window.mainloop()