import logging

import pandas
import pendulum
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from env.server import mysql_options
from libs.server import get_mysql_url

logger = logging.getLogger(__name__)
db_url = get_mysql_url(mysql_options, database='ht_silo_statistics')
engine = create_engine(db_url)


def get_month_sql(time_str, s_type):
    """获取月数据"""
    time = pendulum.parse(time_str)
    start_of_month = time.start_of('month').format('YYYYMMDD')
    end_of_month = time.end_of('month').format('YYYYMMDD')
    sql = """
        SELECT * FROM `trade_statistics`
            WHERE `s_type` = {s_type} AND `d_t` >= {start} AND `d_t` <= {end};
        """.format(s_type=s_type,
                   start=start_of_month,
                   end=end_of_month)

    return sql


def sql_to_dataframe(sql, engine):
    """sql 语句转化为 DataFrame"""
    return pandas.read_sql(sql=sql, con=engine)


def calculate_dataframe(dataframe, d_t, s_type):
    """计算金额"""
    dataframe = dataframe.groupby(
        by=['p_id', 'g_id', 'r_id'],
        as_index=False,
    ).agg({
        'amount': 'sum',
        'd_t': lambda x: d_t,
        's_type': lambda x: s_type,
    })

    return dataframe


def write_dataframe_to_db(dataframe, engine):
    """写入数据到数据库"""
    dataframe.to_sql(name='trade_statistics',
                     con=engine,
                     if_exists='append',
                     index=False)


def insert_current_month_statistics(s_type):
    """插入当前月的统计数据到数据库"""
    last_month = pendulum.now().subtract(months=1)

    sql = get_month_sql(last_month.to_date_string(), s_type)
    data = sql_to_dataframe(sql, engine)
    data = calculate_dataframe(data,
                               last_month.format('YYYYMM'),
                               s_type)
    try:
        write_dataframe_to_db(data, engine)
    except IntegrityError:
        pass
