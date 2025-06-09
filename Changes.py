class Changes:
    """
    잔돈의 갯수를 세는 클래스
    자판기내 잔돈과 자판기의 투입된 화폐를 관리합니다.
    """
    def __init__(self):
        # 화폐 단위별 보관 개수 (지폐+동전)
        self.storage = {
            "1000": 0,  # 1000원 지폐
            "500": 0,   # 500원 동전
            "100": 0,   # 100원 동전
            "50": 0,    # 50원 동전
        }
        
        self.coins = {
            "500": 30,
            "100": 30,
            "50": 30
        } # 잔돈용 동전 보관 개수

        self.count = 0 # 투입된 돈 총량량
        self.bill_inserted = False  # 지폐 투입 여부
    def add(self, money):
        self.storage[str(money)] += 1
        self.count += int(money)
        if money == 1000:
            self.bill_inserted = True
    def use(self, num):
        if self.count >= num:
            self.count -= num
            return True
        return False
    def return_change(self):
        change = {}
        if self.bill_inserted and self.count >= 1000: #지폐가 투입되었고, 잔액이 1000원 이상일 때
            change["1000"] = 1
            self.storage["1000"] -= 1
            self.bill_inserted = False
            self.count -= 1000
        for i in [500, 100, 50]:
            num_coins = min(self.count // i, self.coins[str(i)])
            change[str(i)] = num_coins
            self.count -= num_coins * i
            self.coins[str(i)] -= num_coins
        if self.count > 0:
            print("잔돈이 부족합니다. 관리자에게 문의하세요. 잔액:", self.count)
            return change
        return change
    def empty_storage(self):
        """
        보관함(storage)을 비움
        """
        profit = self.storage.copy()
        self.storage = {
            "1000": 0,
            "500": 0,
            "100": 0,
            "50": 0
        }
        return profit
