from Drink import Drink
from Changes import Changes

class VendingMachine:
    """
    자판기 클래스
    음료수 목록, 잔돈 카트리지, 관리자 모드 관리
    """
    password = "0414"

    def __init__(self):
        self.drinks = []               # Drink 인스턴스 리스트
        self.changes = Changes()       # Changes 인스턴스
        self.adminMode = False

    def activate_admin_mode(self, pwd=None):
        if pwd is None:
            pwd = input("관리자 비밀번호를 입력하세요: ")
        if pwd == self.password:
            self.adminMode = True
            print(" 관리자 모드에 진입했습니다.")
        else:
            print(" 잘못된 비밀번호입니다.")

    def deactivate_admin_mode(self):
        self.adminMode = False
        print(" 관리자 모드 해제됨.")

    def append_drink(self, drink: Drink):
        if not self.adminMode:
            print("관리자 권한이 필요합니다.")
            return
        self.drinks.append(drink)
        print(f"음료 '{drink.name}' 추가 완료.")

    def add_drink(self, drink_index, num):
        if not self.adminMode:
            print("관리자 권한이 필요합니다.")
            return
        if 0 <= drink_index < len(self.drinks):
            self.drinks[drink_index] += num
            print(f"{self.drinks[drink_index].name} 재고 {num}개 추가 완료.")
        else:
            print("유효하지 않은 음료 인덱스입니다.")

    def add_coin(self, coin_name, num):
        if not self.adminMode:
            print("관리자 권한이 필요합니다.")
            return
        if coin_name not in self.changes.coins:
            self.changes.coins[coin_name] = 0
        self.changes.coins[coin_name] += num
        print(f"{coin_name}원 {num}개 보충 완료.")

    def get_all_storage(self):
        if not self.adminMode:
            print("관리자 권한이 필요합니다.")
            return
        storage = self.changes.empty_storage()
        return storage

    def refill_coin_cartridge(self):
        if not self.adminMode:
            print("관리자 권한이 필요합니다.")
            return
        for coin in self.changes.coins:
            self.changes.coins[coin] = 50
        print(" 잔돈 카트리지 보충 완료.")

    def buy_drink(self, drink_index):
        if drink_index < 0 or drink_index >= len(self.drinks):
            return "존재하지 않는 음료입니다."

        drink = self.drinks[drink_index]
        if drink.num <= 0:
            return f"{drink.name}은(는) 품절입니다."
        if self.changes.count < drink.price:
            return "돈이 부족합니다."

        self.changes.use(drink.price)
        drink.num -= 1
        return f"{drink.name}을(를) 구매하셨습니다. 잔액: {self.changes.count}원"

    def insert_money(self, amount):
        try:
            self.changes.add(amount)
            print(f" {amount}원 투입 완료. 현재 잔액: {self.changes.count}원")
        except Exception as e:
            print(f"투입 실패: {e}")


