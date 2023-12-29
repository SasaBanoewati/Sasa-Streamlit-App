import streamlit as st
import pandas as pd
import plotly_express as px
#import mysql.connector


st.set_page_config(layout="wide")
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


df = pd.read_csv('retail_2.csv')
#mydb = mysql.connector.connect(
    #host="localhost",
    #user="root",
    #password="",
    #database="retail_2"
#)

#mycursor = mydb.cursor()

#sql = "SELECT \
#transactions_sales_ok_3.transaction_id, \
#transactions_sales_ok_3.cust_id, \
#transactions_sales_ok_3.tran_date, \
#prod_subcat_info_ok_2.prod_subcat as sub_category, \
#prod_cat_info_ok_3.prod_cat as category, \
#transactions_sales_ok_3.Qty, \
#transactions_sales_ok_3.Rate, \
#transactions_sales_ok_3.Tax, \
#transactions_sales_ok_3.total_amt, \
#transactions_sales_ok_3.Store_type \
#FROM transactions_sales_ok_3 \
#LEFT JOIN prod_cat_info_ok_3 ON transactions_sales_ok_3.prod_cat_code =  prod_cat_info_ok_3.prod_cat_code \
#LEFT JOIN prod_subcat_info_ok_2 ON transactions_sales_ok_3.prod_cat_code = prod_subcat_info_ok_2.prod_cat_code"

#mycursor.execute(sql)

#myresult = mycursor.fetchall()

#df =pd.DataFrame([[ij for ij in i] for i in df])
#df.rename(columns={0: 'transaction_id', 1: 'cust_id', 2: 'tran_date', 3: 'sub_category', 4: 'category',
                   #5: 'Qty', 6: 'Rate', 7: 'Tax', 8: 'total_amt', 9: 'Store_type'}, inplace=True)
#df[["Qty", "Rate", "Tax", "total_amt"]] = df[["Qty", "Rate", "Tax", "total_amt"]].apply(pd.to_numeric)


df['tran_date_2'] = df['tran_date']
df['tran_date'] = pd.to_datetime(df['tran_date'], infer_datetime_format=True, errors='coerce')
df.set_index('tran_date', inplace=True)
df['tran_date_2'] = df['tran_date_2'].astype('datetime64[ns]')


df['month'] = pd.to_datetime(df['tran_date_2']).dt.month.astype(str)
df['year'] = pd.to_datetime(df['tran_date_2']).dt.year.astype(str)
df['week'] = pd.to_datetime(df['tran_date_2']).dt.weekday.astype(str)
df['month_full'] = df['tran_date_2'].dt.month_name()

ordered_months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]

df['to_sort']=df['month_full'].apply(lambda x: ordered_months.index(x))
df = df.sort_values('to_sort')
tran_date_2 = df['tran_date_2']


#st.write(df)


#---SIDE BAR FILTER---
col1, col2, col3, col4 = st.columns(4)
#col1.header("Please Filter Here:")
min_date = tran_date_2.min()
max_date = tran_date_2.max()
selected_date_range = col1.date_input(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
)
category = col2.multiselect(
    "Select the Category:",
    options=df["category"].unique(),
    default=df["category"].unique()
)
sub_category = col3.multiselect(
    "Select the Sub Category:",
    options=df["sub_category"].unique(),
    default=df["sub_category"].unique()
)
store_type = col4.multiselect(
    "Select the Store Type:",
    options=df["Store_type"].unique(),
    default=df["Store_type"].unique()
)
start_date, end_date = selected_date_range
df_selection = df.query(
    "category == @category & sub_category == @sub_category & tran_date_2 >= @start_date & tran_date_2 <= @end_date & Store_type == @store_type"
)
#st.dataframe(df_selection)



#---BOX CARD---
total_sales = int(df_selection["total_amt"].sum())
average_sales = round(df_selection["total_amt"].mean(),2)
formatted_total_sales = '{:,.0f}'.format(total_sales)
formatted_average_sales = '{:,.2f}'.format(average_sales)
left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(formatted_total_sales)
with right_column :
    st.subheader("Average Sales Per Transaction:")
    st.subheader(formatted_average_sales)
st.markdown("---")

#---BAR CHART COUNT ACHIEVEMENT FROM TOTAL AMOUNT---

total_sales_2 = df_selection.groupby('Store_type')['total_amt'].sum().sort_values(ascending=False)
df4 = pd.DataFrame(total_sales_2)
df4.loc[(df4['total_amt'] > 0) & (df4['total_amt'] < 5500000), 'Achievement'] = 'not achieved'
df4.loc[(df4['total_amt'] > 5500001) & (df4['total_amt'] < 10000000), 'Achievement'] = 'achieved'
df4.loc[df4['total_amt'] > 10000001, 'Achievement'] = 'More Than achieved'
category_sales=df4.groupby('Achievement')['Achievement'].count()
fig_grandtotal_category_sales = px.bar(
    data_frame=category_sales,
    barmode='group',
    text_auto=True,
    orientation="h",
    title="<b>Achievement by Store Type</b>",
    color_discrete_sequence=["#0083b8"] * len(category_sales),
    template="plotly_white",
)
fig_grandtotal_category_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#st.write(fig_grandtotal_category_sales)

#---BAR CHART RETURN CUSTOMER---
customer = df_selection.groupby('cust_id')['cust_id'].count().sort_values(ascending=False)
df3 = pd.DataFrame(customer)
df3.loc[(df3['cust_id'] > 0) & (df3['cust_id'] < 6), 'Customer Return'] = '1 - 5 Times'
df3.loc[(df3['cust_id'] > 5) & (df3['cust_id'] < 10), 'Customer Return'] = '6 - 9 Times'
df3.loc[df3['cust_id'] > 10, 'Customer Return'] = 'More Than 10'
return_customer = df3.groupby('Customer Return')['Customer Return'].count()
fig_grandtotal_return_customer = px.bar(data_frame=return_customer,
                  barmode='group', text_auto=True,
                  width=800, height=400
                  )
fig_grandtotal_return_customer.update_traces(marker_color='#f5d018', textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig_grandtotal_return_customer.update_layout(
        title={
            'text': "Return Customer",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis={'categoryorder':'total ascending'})
#st.write(fig_grandtotal_return_customer)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_grandtotal_category_sales, use_container_width=True)
right_column.plotly_chart(fig_grandtotal_return_customer, use_container_width=True)

fig_grandtotal_monthly = px.bar(data_frame=df_selection.groupby(['month_full']).sum().reset_index(), x='month_full', y='total_amt',
                 text_auto='.2s',
                 width=800, height=400)
fig_grandtotal_monthly.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_color='green')
fig_grandtotal_monthly.update_xaxes(categoryorder='array',
                     categoryarray=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                    'September', 'October', 'November', 'December'])
fig_grandtotal_monthly.update_layout(
        title={
            'text': "Total Amount - Month",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

#st.write(fig_grandtotal_monthly)

fig_grandtotal_category_ok = px.pie(data_frame=df_selection.groupby(['category']).sum().reset_index(), names='category', values='total_amt',
                  width=800, height=400)
fig_grandtotal_category_ok.update_traces(textposition='inside', textinfo='value+label')
fig_grandtotal_category_ok.update_layout(
        title={
            'text': "Total Amount - Category",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

left_column_2, right_column_2 = st.columns(2)
left_column_2.plotly_chart(fig_grandtotal_monthly, use_container_width=True)
right_column_2.plotly_chart(fig_grandtotal_category_ok, use_container_width=True)

fig_grandtotal_storetype = px.pie(data_frame=df_selection.groupby(['Store_type']).sum().reset_index(), names='Store_type', values='total_amt',
                  width=800, height=400, hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
fig_grandtotal_storetype.update_traces(textposition='inside', textinfo='value+label')
fig_grandtotal_storetype.update_layout(
        title={
            'text': "Total Amount - Store Type",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

fig_grandtotal_subcategory = px.bar(data_frame=df_selection.groupby(['sub_category']).sum().reset_index(), x='total_amt', y='sub_category',
                  text_auto='.2s',
                  width=800, height=400,orientation='h'
                  )
fig_grandtotal_subcategory.update_traces(marker_color='#eb0788',
                       textfont_size=12, textangle=0, textposition="outside", cliponaxis=False,)
fig_grandtotal_subcategory.update_layout(
        title={
            'text': "Total Amount - Sub Category",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis={'categoryorder':'total ascending'})

left_column_3, right_column_3 = st.columns(2)
left_column_3.plotly_chart(fig_grandtotal_storetype, use_container_width=True)
right_column_3.plotly_chart(fig_grandtotal_subcategory, use_container_width=True)
st.dataframe(df_selection)
