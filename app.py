# app.pyDd
# CI/CD 실습을 위한 간단한 파이썬 애플리케이션 코드dd

def add(a, b):
    """두 숫자를 더하는 함수"""
    return a + b

def subtract(a, b):
    """두 숫자를 빼는 함수"""
    return a - b

if __name__ == "__main__":
    print(f"Adding 5 and 3: {add(5, 3)}")
    print(f"Subtracting 10 from 7: {subtract(7, 10)}")