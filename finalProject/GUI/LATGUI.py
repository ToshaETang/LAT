#python LATGUI.py
from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
font = {'family': 'MicroSoft YaHei'}
plt.rc('font',**font)


root0 = Tk()
root0.minsize(1000, 500)
root0.title('主頁面')
#===================================
def search():
    
    text.delete("1.0","end")
    school=comboSchool.get()
    #subject=comboSubject.get()
    if(school!="選擇查詢學校"):        
        dfSchool = pd.read_csv(r"data\{}.csv".format(school), encoding="utf-8")
        text.insert('1.0', dfSchool)
        data = dfSchool

        def calculate_ratios(data):
            國count = (data['採計科目(含一階篩選方式、倍率、超篩)'].str.contains('國')).sum()
            國countratio = 國count / len(data)

            英count = (data['採計科目(含一階篩選方式、倍率、超篩)'].str.contains('英')).sum()
            英countratio = 英count / len(data)

            數Bcount = (data['採計科目(含一階篩選方式、倍率、超篩)'].str.contains('B')).sum()
            數Bcountratio = 數Bcount / len(data)

            數Acount = (data['採計科目(含一階篩選方式、倍率、超篩)'].str.contains('A')).sum()
            數Acountratio = 數Acount / len(data)

            社count = (data['採計科目(含一階篩選方式、倍率、超篩)'].str.contains('社')).sum()
            社countratio = 社count / len(data)

            自count = (data['採計科目(含一階篩選方式、倍率、超篩)'].str.contains('自')).sum()
            自countratio = 自count / len(data)

            英聽count = (data['採計科目(含一階篩選方式、倍率、超篩)'].str.contains('聽')).sum()
            英聽countratio = 英聽count / len(data)

            return [國countratio, 英countratio, 數Acountratio, 數Bcountratio, 社countratio, 自countratio, 英聽countratio]


        ratios_df1 = calculate_ratios(data)

        科目比例 = [ratios_df1]

        大學名稱 = [school] 
        plt.figure(figsize=(8, 10))
        # 繪製熱力圖
        sns.heatmap(科目比例, cmap='coolwarm', annot=True, fmt=".2f")
        plt.xticks(rotation=45)  # 旋轉橫軸刻度標籤
        plt.yticks(rotation=45)  # 旋轉縱軸刻度標籤
        # 設置刻度標籤和軸標籤
        plt.xticks(range(len(科目比例[0])), ['國文', '英文', '數A', '數B', '社會', '自然', '英聽'])
        plt.yticks(range(len(大學名稱)), 大學名稱)
        # 設置圖表標題和軸標籤等
        plt.title("各科目比例熱力圖")
        plt.xlabel("科目")
        plt.ylabel("大學名稱")
        # 顯示圖表
        plt.show()


    if(subject!="選擇查詢科目"):
        dfSubject = pd.read_csv(r"data\total.csv", encoding="utf-8")
        #dfSubject = pd.DataFrame(dfSubject)
        print(dfSubject[1])
        for i in dfSubject:
            print(i)
            if subject in i['sub']:
                pass
                #print(i['sub'])
                
        


    
    

    



#-------------
subjectList=["選擇查詢科目","國","英","數A","數B","自","社","英聽","體育百分等級","音樂術科","美術術科"]
schoolList=["選擇查詢學校","國立臺灣大學","國立臺灣師範大學","國立中興大學","國立成功大學",
        "東吳大學","國立政治大學","高雄醫學大學","中原大學","東海大學",
        "國立清華大學","中國醫藥大學","國立陽明交通大學","淡江大學",
        "逢甲大學","國立中央大學","中國文化大學","靜宜大學","大同大學",
        "輔仁大學","國立臺灣海洋大學","國立高雄師範大學","國立彰化師範大學",
        "中山醫學大學","國立中山大學","國立臺北藝術大學","長庚大學",
        "國立臺中教育大學","國立臺北教育大學","國立臺南大學","國立東華大學",
        "臺北市立大學","國立屏東大學","國立臺東大學","國立體育大學","元智大學",
        "國立中正大學","大葉大學","中華大學","華梵大學","義守大學","銘傳大學",
        "世新大學","實踐大學","長榮大學","國立臺灣藝術大學","國立暨南國際大學",
        "南華大學","國立臺灣體育運動大學","國立臺南藝術大學","玄奘大學","真理大學",
        "國立臺北大學","國立嘉義大學","國立高雄大學","慈濟大學","臺北醫學大學",
        "開南大學","康寧大學","中信金融管理學院","佛光大學","明道大學","亞洲大學",
        "國立宜蘭大學","國立聯合大學","馬偕醫學院","國立金門大學","臺北基督學院"]

#------------------------------------
comboSchool = ttk.Combobox(root0,values=schoolList)
comboSchool.current(0)
comboSchool.place(x=30, y=40, width=200)
#comboSubject = ttk.Combobox(root0,values=subjectList)
#comboSubject.current(0)
#comboSubject.place(x=300, y=40, width=150)

text = tk.Text(root0)
text.tag_configure("left", justify='left')
text.place(x=30, y=130, width=800, height=300)

searchBotton = tk.Button(root0, text='搜尋', state=tk.NORMAL, command=search)
searchBotton.place(x=500, y=40)
#===================================
root0.mainloop()