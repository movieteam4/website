from django.templatetags.static import static
import pandas as pd
def html_show(final_data):
    # 初始化HTML表格
    movie_list = final_data.groupby('中文片名').count().index
    res = '<table style="vertical-align: top;">'
    opt_btn=['<h4>Free Storage</h4>','<h4>User More</h4>','<h4>Reply Ready</h4>','<h4>Easy Layout</h4>']
    # 遍歷每部電影
    for n, movie in enumerate(movie_list[:4]):
        final_data_movie = final_data[final_data['中文片名'] == movie]
        ch_name = final_data_movie["中文片名"].iloc[0]
        eng_name = final_data_movie["英文片名"].iloc[0]
        genre=final_data_movie["類型"].iloc[0]

        # 初始化圖片顯示標誌
        img_displayed = False

        # 遍歷電影中的每一筆資料
        cinema_list = final_data_movie.groupby('電影院名稱').count().index
        img_url = final_data_movie['宣傳照'].iloc[0]  # 取得宣傳照的URL
        if pd.isna(img_url):
            img_url =static('dog.jpg')
            show_more=static('show_more.png')

        res += f'''<div class="col-lg-3 col-md-6">
            <div class="item">
              <div class="thumb">
                <a href="product-details.html"><img src="{img_url}" alt="" width='260px' height='170px'></a>
                <span class="price"><em>$28</em>$20</span>
              </div>
              <div class="down-content">
                <span class="category">{genre}</span>
                <h4>{ch_name}</h4>
                <a href="product-details.html">
                    <img src={show_more} alt="Product Image">
                </a>
              </div>
            </div>
          </div>'''

        # 顯示電影院名稱
    #     res += '<div style="text-align: left;">'
    #     for cinema in cinema_list:
    #         res += cinema
    #         date_list=final_data_movie[final_data_movie['電影院名稱']==cinema].groupby('日期').count().index
    #         for date in date_list:
    #             res+=f'<br><span style="font-size: 12px;">{date}</span><br>'
    #             time_list=final_data_movie[(final_data_movie['電影院名稱']==cinema) & (final_data_movie['日期']==date)].groupby('時刻表').count().index
    #             for time in time_list:
    #                 res+=f'<span style="border: 2px solid #333; padding: 5px 10px; margin: 3px; display: inline-block; font-size: 10px;">{time}</span>'
    #             res+='<br>'
    #     # 關閉<td>和<tr>標籤
    #     res += '</div></td></tr></table>'

    # # 結束表格
    # res += '</table>'

    return res  # 返回生成的HTML

