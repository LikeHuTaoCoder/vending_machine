#실행 파일
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
from VendingMachine import VendingMachine
from Drink import Drink

vm = VendingMachine()

# 기본 음료 등록 (이름 가격 재고 순)   
vm.activate_admin_mode("0414")
vm.append_drink(Drink("아이시스", 800, 5))
vm.append_drink(Drink("아쿠아 제로", 2000, 5))
vm.append_drink(Drink("레몬워터", 1800, 5))
vm.append_drink(Drink("옥수수 수염차", 1600, 5))
vm.append_drink(Drink("황금 보리", 1600, 5))
vm.append_drink(Drink("트레비", 1300, 5))
vm.append_drink(Drink("펩시제로", 1100, 5))
vm.append_drink(Drink("펩시", 1100, 5))
vm.append_drink(Drink("칠성사이다제로", 1300, 5))
vm.append_drink(Drink("칠성사이다", 1300, 5))
vm.append_drink(Drink("망고", 1200, 5))
vm.append_drink(Drink("립톤", 1200, 5))
vm.append_drink(Drink("애플 에이드", 1100, 5))
vm.append_drink(Drink("포도 에이드", 1300, 5))
vm.append_drink(Drink("레쓰비", 900, 5))
vm.append_drink(Drink("가나초코", 900, 5))
vm.append_drink(Drink("핫식스제로", 1300, 5))
vm.append_drink(Drink("밀키스", 1100, 5))
vm.append_drink(Drink("핫식스", 1300, 5))
vm.append_drink(Drink("레쓰비 카페타임 라떼", 1200, 5))
vm.append_drink(Drink("게토레이", 1000, 5))
vm.append_drink(Drink("코코포도", 1000, 5))
vm.append_drink(Drink("잔칫집 식혜", 1000, 5))
vm.deactivate_admin_mode()

# 메인 윈도우
window = tk.Tk()
window.title("자판기")
window.geometry("800x800")
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# ---------- 우측 display ----------
display = tk.Text(window, height=8, width=2, font=("맑은 고딕", 12), wrap="word")
display.insert("1.0", "돈을 넣고 버튼을 눌러 음료를 선택하세요.")
display.config(state="disabled", bg="lightyellow", relief="sunken")
display.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)

def update_display(msg):
    display.config(state="normal")
    display.delete("1.0", "end")
    display.insert("1.0", msg)
    display.config(state="disabled")

# ---------- 잔액 표시 ----------
balance_var = tk.StringVar()
balance_var.set("잔액: 0원")
balance_label = tk.Label(window, textvariable=balance_var, font=("맑은 고딕", 11))
balance_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

def update_balance_display():
    balance_var.set(f"잔액: {vm.changes.count}원")

# ---------- 음료 버튼 ----------
drink_frame = tk.LabelFrame(window, text="음료", padx=10, pady=10)
drink_frame.grid(row=0, column=0, columnspan=2,sticky="nsew", padx=10, pady=10)

def buy_drink_handler(idx):
    result = vm.buy_drink(idx)
    update_display(result)
    update_balance_display()
    render_drinks()

def render_drinks():
    for widget in drink_frame.winfo_children():
        widget.destroy()
    for i, drink in enumerate(vm.drinks):
        if drink.num <= 0:
            label = f"{drink.name}\n{drink.price}원 (매진)"
        else:
            label = f"{drink.name}\n{drink.price}원"
        tk.Button(drink_frame, text=label, width=18, height=3,
                  command=lambda idx=i: buy_drink_handler(idx)).grid(row=i//5, column=i%5, padx=5, pady=5)

render_drinks()

# ---------- 돈 투입 ----------
money_frame = tk.LabelFrame(window, text="돈 투입")
money_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)

def insert_money(amount):
    vm.insert_money(amount)
    update_display(f"{amount}원 투입했습니다.")
    update_balance_display()

for i, money in enumerate([50, 100, 500, 1000]):
    tk.Button(money_frame, text=f"{money}원", width=10,
              command=lambda m=money: insert_money(m)).grid(row=0, column=i, padx=5,pady=5)

# ---------- 잔돈 반환 ----------
def return_change():
    try:
        result = vm.changes.return_change()
        msg = " 거스름돈 반환:\n" + "\n".join([f"{k}원: {v}개" for k, v in result.items()])
        update_display(msg)
        update_balance_display()
    except ValueError as e:
        update_display(str(e))

tk.Button(window, text="잔돈 반환", command=return_change, width=15).grid(row=3, column=0, padx=10, pady=10, sticky="w")

# ---------- 관리자 모드 ----------
def admin_mode():
    pwd = simpledialog.askstring("관리자 인증", "비밀번호를 입력하세요:", show="*")
    if pwd is None:
        return
    vm.activate_admin_mode(pwd)
    if not vm.adminMode:
        update_display(" 잘못된 비밀번호입니다.")
        return

    # 팝업 창 생성
    admin_win = tk.Toplevel(window)
    admin_win.title("관리자 모드")
    admin_win.geometry("300x300")
    admin_win.resizable(False, False)

    tk.Label(admin_win, text="관리자 작업 선택", font=("맑은 고딕", 12)).pack(pady=10)

    def close_admin_popup():
        vm.deactivate_admin_mode()
        admin_win.destroy()
    admin_win.protocol("WM_DELETE_WINDOW", close_admin_popup)

    def add_drink_popup():
        name = simpledialog.askstring("음료 이름", "이름:")
        if name is None:
            return
        try:
            price = int(simpledialog.askstring("가격", "가격:"))
            count = int(simpledialog.askstring("재고", "수량:"))
            vm.append_drink(Drink(name, price, count))
            render_drinks()
            update_display(f" {name} 음료 추가 완료")
        except Exception as e:
            update_display(f" 오류: {e}")

    def remove_drink_popup():
        remove_win = tk.Toplevel(admin_win)
        remove_win.title("음료 제거")
        remove_win.geometry("300x400")

        tk.Label(remove_win, text="제거할 음료 선택", font=("맑은 고딕", 11)).pack(pady=10)

        def confirm_remove(idx):
            name = vm.drinks[idx].name
            confirm = messagebox.askyesno("삭제 확인", f"'{name}' 음료를 정말 제거하시겠습니까?")
            if confirm:
                del vm.drinks[idx]
                render_drinks()
                update_display(f"'{name}' 음료가 제거되었습니다.")
            remove_win.destroy()

        for i, drink in enumerate(vm.drinks):
            label = f"{drink.name} ({drink.num}개)"
            tk.Button(remove_win, text=label, width=25, command=lambda idx=i: confirm_remove(idx)).pack(pady=2)

    def add_stock_popup():
        stock_win = tk.Toplevel(window)
        stock_win.title("재고 보충")
        stock_win.geometry("300x150")

        tk.Label(stock_win, text="음료 선택", font=("맑은 고딕", 11)).pack(pady=5)

        # 드롭다운 (Combobox)
        drink_names = [f"{d.name} ({d.num}개)" for d in vm.drinks]
        combo = ttk.Combobox(stock_win, values=drink_names, state="readonly")
        combo.pack(pady=5)

        def apply_stock():
            selected_index = combo.current()
            if selected_index == -1:
                return
            drink = vm.drinks[selected_index]
            amount = simpledialog.askinteger("수량 입력", f"{drink.name}에 추가할 수량:")
            if amount is not None:
                vm.add_drink(selected_index, amount)
                render_drinks()
                update_display(f"{drink.name} 재고 {amount}개 추가 완료")
            stock_win.destroy()

        tk.Button(stock_win, text="보충", command=apply_stock).pack(pady=10)


    def refill_coins():
        vm.refill_coin_cartridge()
        update_display("잔돈 카트리지를 보충했습니다.")

    def empty_coin_hopper():
        result=vm.get_all_storage()
        msg = "동전 수거:\n" + "\n".join([f"{k}원: {v}개" for k, v in result.items()])
        msg += "\n총 수익: " + str(sum(int(k) * v for k, v in result.items())) + "원"
        update_display(msg)
    
    # 버튼 4개 생성
    tk.Button(admin_win, text="음료 추가", width=20, command=add_drink_popup).pack(pady=5)
    tk.Button(admin_win, text="음료 제거", width=20, command=remove_drink_popup).pack(pady=5)
    tk.Button(admin_win, text="재고 보충", width=20, command=add_stock_popup).pack(pady=5)
    tk.Button(admin_win, text="잔돈 보충", width=20, command=refill_coins).pack(pady=5)
    tk.Button(admin_win, text="동전 수거", width=20, command=empty_coin_hopper).pack(pady=5)
    tk.Button(admin_win, text="닫기", width=20, command=close_admin_popup).pack(pady=5)


tk.Button(window, text="관리자 모드", command=admin_mode, width=15).grid(row=3, column=1, padx=10, pady=10, sticky="e")

# ---------- 메인 루프 ----------
window.mainloop()
