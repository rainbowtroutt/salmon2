import streamlit as st
import pandas as pd
import plotly.express as px

# 파일 경로
FILE_TOTAL = "202504_202504_\u110c\u1165\u11bc\u3139\u1167\u11bd\u1107\u1167\u11af\u110b\u1175\u11bd\u110b\u116e\u1112\u1167\u11bc_\u110b\u116f\u11af\u3131\u1161\u11ab_\u1102\u1161\u11b7\u1102\u1167\u1112\u1161\u11b9\u3131\u1166.csv"
FILE_GENDER = "202504_202504_\u110c\u1165\u11bc\u3139\u1167\u11bd\u1107\u1167\u11af\u110b\u1175\u11bd\u110b\u116e\u1112\u1167\u11bc_\u110b\u116f\u11af\u3131\u1161\u11ab_\u1102\u1161\u11b7\u1102\u1167\u1111\u116e\u11ab\u3139\u1165.csv"

# 데이터 불러오기 @st.cache_data로 캐싱
@st.cache_data
def load_data():
    df_total = pd.read_csv(FILE_TOTAL, encoding='cp949')
    df_gender = pd.read_csv(FILE_GENDER, encoding='cp949')
    return df_total, df_gender

df_total, df_gender = load_data()

st.title("서울특별시 연령별 인구 현황 시각화")

# 행정구역 선택
regions = df_total['행정구역'].unique()
selected_region = st.selectbox("행정구역 선택", regions)

# 선택한 지역에 해당하는 데이터 필터링
data_total = df_total[df_total['행정구역'] == selected_region]
data_gender = df_gender[df_gender['행정구역'] == selected_region]

# 연령별 열만 추출 (합계 기준)
age_cols = [col for col in data_total.columns if '계_' in col and '_' in col.split('_')[-1]]
ages = [col.split('_')[-1] for col in age_cols]
counts_total = data_total[age_cols].iloc[0].str.replace(",", "").astype(int)

# 성별 분리
age_cols_male = [col for col in data_gender.columns if '남_' in col and '_' in col.split('_')[-1]]
age_cols_female = [col for col in data_gender.columns if '여_' in col and '_' in col.split('_')[-1]]

counts_male = data_gender[age_cols_male].iloc[0].str.replace(",", "").astype(int)
counts_female = data_gender[age_cols_female].iloc[0].str.replace(",", "").astype(int)

# Plotly 시각화
fig_total = px.bar(x=ages, y=counts_total, labels={'x': '연령', 'y': '인구수'},
                   title=f"{selected_region} 연령별 인구 (남녀 합계)")

fig_gender = px.bar(x=ages + ages, 
                    y=list(counts_male) + list(counts_female), 
                    color=["남"] * len(ages) + ["여"] * len(ages),
                    barmode='group',
                    labels={'x': '연령', 'y': '인구수', 'color': '성별'},
                    title=f"{selected_region} 연령별 남녀 인구")

# 출력
st.plotly_chart(fig_total)
st.plotly_chart(fig_gender)

st.markdown("데이터 출처: 서울열린데이터광장")
