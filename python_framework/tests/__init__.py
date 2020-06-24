import unittest

case_path = '.'


# 获取所有测试用例
def get_all_case():
    discover = unittest.defaultTestLoader.discover(
        case_path, pattern="test*.py")
    suite = unittest.TestSuite()
    suite.addTest(discover)
    return suite


if __name__ == '__main__':
    # 运行测试用例
    runner = unittest.TextTestRunner()
    runner.run(get_all_case())
