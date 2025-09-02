#!/usr/bin/env python
"""
简单的调试测试文件
用于验证调试配置是否正确
"""

def test_function():
    """测试函数"""
    x = 10
    y = 20
    result = x + y
    print(f"计算结果: {result}")
    return result

if __name__ == "__main__":
    print("开始调试测试...")
    test_function()
    print("调试测试完成！")

