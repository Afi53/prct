# from Tkin import *
import tkinter as tk
from tkinter import ttk

from fonbet import *
from match import get_data_LS,get_data_BS
from xl import *
from fs import *

def callbackFunc(event):
#    combo=event.widget.get()
    if combo.get()=='Фонбет-селен':
        l_matches,fp,sh=get_selen_F()
        get_png()
    #     load_matches(l_matches,fp,sh)
    # elif combo.get()=='Фонбет-ставки':
#        l_matches,fp,sh=get_data_F(turn())
        load_matches(l_matches,fp,sh)
    elif combo.get()=='Флаш-селен':
        sh_name_1='Ставки'
        sh_name_2='Врем'
        l_matches = upload_matches(sh_name_1)
        get_selen(l_matches)
        l_mfs = get_pages(l_matches)
        l_matches_rez,d_nov_kom=join_list(l_matches, l_mfs)
        n_rez=False
        load_xl(l_matches_rez,d_nov_kom,sh_name_1,sh_name_2,n_rez)
    elif combo.get() == 'Флаш-рез':
        sh_name_1='Ставки'
        sh_name_2='Врем'
        l_matches = upload_matches(sh_name_1)
        l_mfs = get_pages(l_matches)
        l_matches_rez,d_nov_kom=join_list(l_matches, l_mfs)
        n_rez=True
        load_xl(l_matches_rez,d_nov_kom,sh_name_1,sh_name_2,n_rez)
    elif combo.get() == 'ЛС-селен':
        l_turn=get_url_ls()
        get_selen_LS(l_turn)
        match, fp, sh = get_data_LS()
        load_matches(match, fp, sh)
    elif combo.get()=='ЛС-ставки':
#        match, fp, sh = get_data_BS()
        match,fp,sh= get_data_LS()
        load_matches(match, fp, sh)
    elif combo.get() == 'ЛС-рез':
        sh_name_1 = 'ЛС_рез'
        sh_name_2 = 'ЛС_врем'
        l_matches = upload_matches(sh_name_1)
        l_mfs = get_pages(l_matches)
        l_matches_rez,d_nov_kom=join_list(l_matches, l_mfs)
        n_rez=True
        load_xl(l_matches_rez,d_nov_kom,sh_name_1,sh_name_2,n_rez)
    elif combo.get()=="Статистика":
        stat()
    print("OK")

window=tk.Tk()
window.title('Bookmaker')
window.geometry('500x250')
text_font = ('Courier New', '12')
combo = ttk.Combobox(window,font=text_font)
window.option_add('*TCombobox*Listbox.font', text_font)
combo['values'] = ('Фонбет-селен', 'Флаш-селен', 'Флаш-рез', 'ЛС-селен','ЛС-ставки',
                   "ЛС-рез","Статистика")
combo.grid(column=0,row=0)
combo.bind("<<ComboboxSelected>>",callbackFunc)
# btn=Button(window,text='кнопка',command=clicked)
# btn.grid(column=1,row=0)

window.mainloop()

def main():
    pass


if __name__ == '__main__':
    main()
