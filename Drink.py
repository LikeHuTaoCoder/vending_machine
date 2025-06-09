class Drink:
    """
    음료수 클래스
    음료수의 이름, 가격, 갯수를 관리합니다.
    """
    def __init__(self, name, price, num):
        self.name = name      # 음료수 이름
        self.price = price    # 음료수 가격
        self.num = num        # 음료수 재고

    def __add__(self, other):
        if isinstance(other, int):
            return Drink(self.name, self.price, self.num + other)
        elif isinstance(other, Drink) and other.name == self.name:
            return Drink(self.name, self.price, self.num + other.num)
        else:
            return Drink(self.name, self.price, self.num)

    def is_available(self):
        return self.num > 0

    def purchase(self):
        if self.is_available():
            self.num -= 1
            return True
        return "재고가 부족합니다."

    def __str__(self):
        return f"{self.name} {self.num}개 남음)"


