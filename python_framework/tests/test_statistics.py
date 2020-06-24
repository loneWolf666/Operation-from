from unittest import TestCase

import pandas as pd
import pendulum

from app.statistics import write_dataframe_to_db, \
    insert_current_month_statistics, engine


class StatisticsTest(TestCase):

    def setUp(self):
        self.engine = engine
        self.test_s_type = 122

    def tearDown(self):
        # delete models
        sql = """
                DELETE FROM `trade_statistics`
                    WHERE s_type = {}
                """.format(self.test_s_type)
        self.engine.execute(sql)

    def test_statistics_of_month(self):
        s_type = self.test_s_type
        last_month = pendulum.now().subtract(months=1).start_of('month')
        d_t = last_month.format('YYYYMMDD')

        data = {
            's_type': [s_type for i in range(4)],
            'd_t': [int(d_t) + i for i in range(4)],
            'p_id': [2 for i in range(4)],
            'g_id': [0 for i in range(4)],
            'r_id': [11, 11, 12, 12],
            'amount': [100, 200, 100, 150],
        }
        dataframe = pd.DataFrame(data)
        write_dataframe_to_db(dataframe, self.engine)

        insert_current_month_statistics(s_type)
        r_sql = """
        SELECT * FROM `trade_statistics`
            WHERE d_t = {}
        """.format(last_month.format('YYYYMM'))
        result = self.engine.execute(r_sql).fetchall()

        self.assertEqual(result[0][-1], 300)
        self.assertEqual(result[1][-1], 250)
