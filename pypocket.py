# ==============================================================================
# โปรเจกต์: PyPocket (ระยะที่ 1 - ปรับปรุงระบบหมวดหมู่รายจ่าย)
# คำอธิบาย: ระบบบันทึกรายรับ-รายจ่าย มีระบบเลือกหมวดหมู่รายจ่ายตามรายการที่กำหนด
# ==============================================================================

import json
import os
from pathlib import Path

DATA_FILE = Path(__file__).with_name("transactions.json")

def load_transactions():
    """อ่านประวัติรายการจากไฟล์ JSON"""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            transactions = json.load(file)
        if isinstance(transactions, list):
            return transactions
        print("ข้อผิดพลาด: รูปแบบข้อมูลในไฟล์ไม่ถูกต้อง เริ่มต้นด้วยประวัติว่าง")
    except (OSError, json.JSONDecodeError):
        print("ข้อผิดพลาด: ไม่สามารถอ่านไฟล์ประวัติได้ เริ่มต้นด้วยประวัติว่าง")

    return []

def save_transactions(transactions):
    """บันทึกประวัติรายการลงไฟล์ JSON"""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(transactions, file, ensure_ascii=False, indent=4)
    except OSError:
        print("ข้อผิดพลาด: ไม่สามารถบันทึกไฟล์ประวัติได้")

def clear_terminal():
    """ล้างหน้าจอ Terminal ตามระบบปฏิบัติการ"""
    os.system("cls" if os.name == "nt" else "clear")

# 1. การเตรียมข้อมูลและหมวดหมู่รายจ่าย
transactions = load_transactions()

# รายการหมวดหมู่รายจ่ายที่กำหนดไว้ในโค้ด
EXPENSE_CATEGORIES = [
    "อาหาร",
    "เครื่องดื่ม",
    "เดินทาง",
    "ของใช้ส่วนตัว",
    "บันเทิง/ช้อปปิ้ง",
    "สังสรรค์",
    "ค่าหอ",
    "ออมเงิน",
    "อื่นๆ"
]

def display_menu():
    """ฟังก์ชันสำหรับแสดงหน้าต่างเมนูหลัก"""
    clear_terminal()
    print("\n" + "="*30)
    print("\tPyPocket Menu")
    print("="*30)
    print("1. บันทึกรายรับ")
    print("2. บันทึกรายจ่าย")
    print("3. ดูยอดเงินคงเหลือ")
    print("4. ดูประวัติรายการทั้งหมด")
    print("5. ล้างประวัติรายการทั้งหมด")
    print("0. ออกจากโปรแกรม")
    print("="*30)

# 2. การทำงานหลักของโปรแกรม (Main Loop)
while True:
    display_menu()
    user_choice = input("กรุณาเลือกเมนู (1-5 หรือกด 0 เพื่อออก): ").strip()

    # กรณีเลือกออกจากโปรแกรมที่เมนูหลัก
    if user_choice == "0":
        print("ขอบคุณที่ใช้งาน PyPocket")
        break

    # กรณีเลือกเมนู 1: บันทึกรายรับ
    elif user_choice == "1":
        try:
            amount = float(input("กรุณากรอกจำนวนเงิน [รายรับ]: "))
            if amount <= 0:
                print("ข้อผิดพลาด: จำนวนเงินต้องมากกว่า 0 บาท")
                continue
        except ValueError:
            print("ข้อผิดพลาด: กรุณากรอกตัวเลขที่ถูกต้อง (เช่น 100 หรือ 50.50)")
            continue

        # รายรับตัดการถามหมวดหมู่ออก และกำหนดให้เป็น "รายรับ" โดยอัตโนมัติ
        category = "รายรับ"
        note = input("กรุณากรอกรายละเอียดเพิ่มเติม (หรือกด Enter เพื่อข้าม): ").strip()

        # บันทึกข้อมูลลง Dictionary
        transaction = {
            "type": "รายรับ",
            "amount": amount,
            "category": category,
            "note": note if note else "-"
        }
        transactions.append(transaction)
        save_transactions(transactions)
        print(f"-> บันทึก รายรับ จำนวน {amount:.2f} บาท เรียบร้อยแล้ว")

    # กรณีเลือกเมนู 2: บันทึกรายจ่าย
    elif user_choice == "2":
        # แสดงเมนูเลือกหมวดหมู่รายจ่าย
        print("\n--- เลือกหมวดหมู่รายจ่าย ---")
        for idx, cat_name in enumerate(EXPENSE_CATEGORIES, start=1):
            print(f"{idx}. {cat_name}")

        # ลูปรับค่าหมวดหมู่รายจ่ายจนกว่าจะถูกต้อง
        category = ""
        while True:
            cat_choice = input("กรุณาเลือกหมายเลขหมวดหมู่ (1-9): ").strip()

            # ตรวจสอบว่ากรอกเป็นตัวเลข 1-8 หรือไม่
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= 8:
                category = EXPENSE_CATEGORIES[int(cat_choice) - 1]
                break
            # กรณีเลือก 9 (อื่นๆ) ให้ผู้ใช้พิมพ์หมวดหมู่เอง
            elif cat_choice == "9":
                custom_cat = input("กรุณากรอกหมวดหมู่ที่ต้องการ (กด enter สำหรับอื่นๆ): ").strip()
                category = custom_cat if custom_cat else "อื่นๆ"
                break
            else:
                print("ข้อผิดพลาด: กรุณาเลือกตัวเลขหมวดหมู่ระหว่าง 1 ถึง 9 เท่านั้น")

        try:
            amount = float(input("กรุณากรอกจำนวนเงิน [รายจ่าย]: "))
            if amount <= 0:
                print("ข้อผิดพลาด: จำนวนเงินต้องมากกว่า 0 บาท")
                continue
        except ValueError:
            print("ข้อผิดพลาด: กรุณากรอกตัวเลขที่ถูกต้อง (เช่น 100 หรือ 50.50)")
            continue

        note = input("กรุณากรอกรายละเอียดเพิ่มเติม (หรือกด Enter เพื่อข้าม): ").strip()

        # บันทึกข้อมูลลง Dictionary
        transaction = {
            "type": "รายจ่าย",
            "amount": amount,
            "category": category,
            "note": note if note else "-"
        }
        transactions.append(transaction)
        save_transactions(transactions)
        print(f"-> บันทึก รายจ่าย [{category}] จำนวน {amount:.2f} บาท เรียบร้อยแล้ว")

    # กรณีเลือกเมนู 3: คำนวณยอดเงินคงเหลือ
    elif user_choice == "3":
        total_income = sum(item["amount"] for item in transactions if item["type"] == "รายรับ")
        total_expense = sum(item["amount"] for item in transactions if item["type"] == "รายจ่าย")
        balance = total_income - total_expense

        print("\n--- สรุปยอดเงินคงเหลือ ---")
        print(f"รายรับรวม  : {total_income:.2f} บาท")
        print(f"รายจ่ายรวม : {total_expense:.2f} บาท")
        print(f"คงเหลือสุทธิ: {balance:.2f} บาท")

    # กรณีเลือกเมนู 4: แสดงประวัติรายการทั้งหมด
    elif user_choice == "4":
        print("\n--- ประวัติรายการทั้งหมด ---")
        if not transactions:
            print("ยังไม่มีข้อมูลรายการในระบบ")
        else:
            for index, item in enumerate(transactions, start=1):
                print(f"{index}. [{item['type']}] หมวดหมู่: {item['category']} | จำนวน: {item['amount']:.2f} บาท | โน้ต: {item['note']}")

    # กรณีเลือกเมนู 5: ล้างประวัติรายการทั้งหมด
    elif user_choice == "5":
        if not transactions:
            print("ยังไม่มีข้อมูลรายการให้ล้าง")
        else:
            while True:
                confirmation = input("ยืนยันการล้างประวัติทั้งหมด? (y/n): ").strip().lower()
                if confirmation in ("y", "yes"):
                    transactions.clear()
                    save_transactions(transactions)
                    print("-> ล้างประวัติรายการทั้งหมดเรียบร้อยแล้ว")
                    break
                elif confirmation in ("n", "no"):
                    print("ยกเลิกการล้างประวัติ")
                    break
                else:
                    print("\nกรุณายืนยัน (y/n)\n")

    # กรณีผู้ใช้พิมพ์ตัวเลือกอื่นนอกเหนือจาก 0-5
    else:
        print("ข้อผิดพลาด: กรุณาเลือกตัวเลขเมนูที่ถูกต้อง")
        continue

    # 3. ส่วนถามยืนยันหลังทำรายการเสร็จ
    while True:
            next_action = input("\nทำรายการต่อไปหรือออก (กด Enter เพื่อเลือกเมนู / กด 0 เพื่อออกจากโปรแกรม): ")
            if next_action == "0":
                print("ขอบคุณที่ใช้งาน PyPocket")
                exit()
            elif next_action == "":
                break
            else:
                print("\nกรุณากด enter หรือ 0")
                continue