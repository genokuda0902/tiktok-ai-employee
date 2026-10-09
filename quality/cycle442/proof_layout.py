"""Original fictional proof visuals for review videos; never claim real UI."""
from PIL import ImageDraw, ImageFont

SAMPLE = [
    ('A-101', 120000), ('B-102', 150000), ('C-103', 90000),
    ('B-102', 150000), ('D-104', 180000),
]

def claims(rows=SAMPLE):
    seen=set(); total=0; corrected=0; duplicates=[]
    for key,amount in rows:
        if not isinstance(amount,int) or amount<0:
            raise ValueError('Invalid amount')
        total+=amount
        if key in seen: duplicates.append(key)
        else:
            corrected+=amount;seen.add(key)
    return dict(raw=total,unique=corrected,delta=total-corrected,duplicates=duplicates)

def draw_sheet(d,x,y,w,font_path,rows=SAMPLE,highlight=True):
    font=lambda n:ImageFont.truetype(font_path,n)
    d.rounded_rectangle((x,y,x+w,y+805),radius=25,fill='#edf5fb')
    d.rounded_rectangle((x+10,y+10,x+w-10,y+88),radius=15,fill='#194b68')
    d.text((x+30,y+24),'受注一覧  /  架空データ',font=font(33),fill='#ffffff')
    d.rounded_rectangle((x+20,y+105,x+w-20,y+176),radius=12,fill='#cce4ef')
    d.text((x+38,y+115),'列A   受注ID',font=font(31),fill='#144260')
    d.text((x+w-300,y+115),'列B   金額',font=font(31),fill='#144260')
    rowh=91
    for i,(key,amount) in enumerate(rows):
        yy=y+185+i*rowh
        d.rectangle((x+20,yy,x+w-20,yy+rowh-4),fill='#ffffff' if i%2==0 else '#e2edf5')
        d.text((x+35,yy+19),f'{i+2:02d}',font=font(29),fill='#7293a7')
        d.text((x+133,yy+16),key,font=font(36),fill='#173c56')
        d.text((x+w-322,yy+16),f'¥{amount:,}',font=font(35),fill='#174d62')
        if highlight and key=='B-102':
            d.rounded_rectangle((x+105,yy+5,x+w-27,yy+rowh-12),radius=10,outline='#ed6173',width=5)
    result=claims(rows)
    d.rounded_rectangle((x+25,y+664,x+w-25,y+773),radius=17,fill='#184c66')
    d.text((x+52,y+690),f"5行の合計  ¥{result['raw']:,}",font=font(39),fill='#ffffff')
    return result

def draw_bar_comparison(d,x,y,w,font_path,raw=690000,corrected=540000):
    expected=claims()
    if (raw,corrected)!=(expected['raw'],expected['unique']):
        raise ValueError('Bars must agree with source data')
    font=lambda n:ImageFont.truetype(font_path,n)
    d.rounded_rectangle((x,y,x+w,y+770),radius=28,fill='#e8f4fd')
    d.text((x+45,y+45),'重複除外の効果',font=font(48),fill='#164866')
    chart_bottom=y+615
    for idx,(name,val,col) in enumerate([('集計前',raw,'#e96780'),('集計後',corrected,'#23b99f')]):
        xx=x+155+idx*395
        hh=int(385*val/750000)
        d.rounded_rectangle((xx,chart_bottom-hh,xx+250,chart_bottom),radius=17,fill=col)
        d.text((xx+125,chart_bottom-hh-70),f'{val//10000}万円',font=font(44),anchor='mt',fill='#173c56')
        d.text((xx+125,chart_bottom+35),name,font=font(37),anchor='mt',fill='#174d64')
    d.text((x+w//2,y+712),'差額15万円  /  架空データ',font=font(35),anchor='mm',fill='#27647a')
    return expected
