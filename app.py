from flask import Flask, render_template
import folium

app = Flask(__name__)

@app.route('/')
def index():
    #!/usr/bin/env python
    # coding: utf-8

    import pandas as pd
    import numpy as np

    sk_df = pd.read_excel('sk_meta.xlsx')

    poly = list(map(list, np.flip(np.array([x.strip().replace('(','').replace(')','').split(',') for x in sk_df['상권좌표'].iloc[2].split('|')], dtype='float'))))

    import folium
    center = [37.279693, 127.047023]
    m = folium.Map(location=center, zoom_start=100)
    for i in range(len(sk_df)):
        poly = list(map(list, np.flip(np.array([x.strip().replace('(','').replace(')','').split(',') for x in sk_df['상권좌표'].iloc[i].split('|')], dtype='float'))))
        folium.Polygon(locations=poly, fill=True, tooltip='Polygon').add_to(m)

    schools= pd.read_csv('schools.csv', encoding='cp949')

    stu = pd.read_csv('학생수현황.csv', encoding='cp949')

    stu = stu[stu['기준년도']==2020]
    stu = stu[['학교명','합계사항(명)']]

    stu.drop_duplicates('학교명',inplace=True)

    condition = schools['교육지원청명'].isin(['경기도수원교육지원청','경기도용인교육지원청'])
    element = schools[condition][['학교명','학교급구분','교육지원청명','위도','경도']]

    element = element[element['학교급구분']=='초등학교']

    element.drop_duplicates('학교명',inplace=True)

    element = pd.merge(element, stu, left_on='학교명', right_on='학교명')

    for i in range(len(element)):
        gps = element[['위도','경도']].values.tolist()
        folium.Marker(gps[i], popup=element['학교명'].iloc[i], tooltip=element['합계사항(명)'].iloc[i]).add_to(m)

    kinder = pd.read_csv('유치원현황.csv', encoding='cp949')

    condition_1 = kinder['시군명'].isin(['용인시','수원시'])
    kinder = kinder[condition_1][['시설명','WGS84위도','WGS84경도']]

    for i in range(len(kinder)):
        gps = kinder[['WGS84위도','WGS84경도']].values.tolist()
        folium.Marker(gps[i], popup=kinder['시설명'].iloc[i], icon=folium.Icon('red', icon='star')).add_to(m)

    hk = pd.read_csv('체육도장업체현황.csv', encoding='cp949')


    condition_2 = hk['시군명'].isin(['용인시','수원시'])
    hk = hk[condition_2][['사업장명','영업상태명','WGS84위도','WGS84경도']]

    hk=hk[hk['영업상태명']=='영업중']


    hk = hk[hk['사업장명'].str.contains('태권도')]


    hk.dropna(inplace=True)

    for i in range(len(hk)):
        gps = hk[['WGS84위도','WGS84경도']].values.tolist()
        folium.Marker(gps[i], popup=hk['사업장명'].iloc[i], icon=folium.Icon('green', icon='star')).add_to(m)

    m.save('templates/map.html')

    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('7_map.html')

if __name__ == '__main__':
    app.run(debug=True)
