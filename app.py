# ==============================================================================
# โปรเจกต์: PyPocket (ระยะที่ 1 - ปรับปรุงระบบหมวดหมู่รายจ่าย)
# คำอธิบาย: ระบบบันทึกรายรับ-รายจ่าย มีระบบเลือกหมวดหมู่รายจ่ายตามรายการที่กำหนด
# ==============================================================================

# 1. การเตรียมข้อมูลและหมวดหมู่รายจ่าย
transactions = []

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
    print("\n" + "="*30)
    print("        PyPocket Menu        ")
    print("="*30)
    print("1. บันทึกรายรับ")
    print("2. บันทึกรายจ่าย")
    print("3. ดูยอดเงินคงเหลือ")
    print("4. ดูประวัติรายการทั้งหมด")
    print("0. ออกจากโปรแกรม")
    print("="*30)

# 2. การทำงานหลักของโปรแกรม (Main Loop)
while True:
    display_menu()
    user_choice = input("กรุณาเลือกเมนู (1-4 หรือกด 0 เพื่อออก): ").strip()

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
        print(f"-> บันทึก รายรับ จำนวน {amount:.2f} บาท เรียบร้อยแล้ว")

    # กรณีเลือกเมนู 2: บันทึกรายจ่าย
    elif user_choice == "2":
        try:
            amount = float(input("กรุณากรอกจำนวนเงิน [รายจ่าย]: "))
            if amount <= 0:
                print("ข้อผิดพลาด: จำนวนเงินต้องมากกว่า 0 บาท")
                continue
        except ValueError:
            print("ข้อผิดพลาด: กรุณากรอกตัวเลขที่ถูกต้อง (เช่น 100 หรือ 50.50)")
            continue

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
                custom_cat = input("กรุณากรอกหมวดหมู่ที่ต้องการ: ").strip()
                category = custom_cat if custom_cat else "อื่นๆ"
                break
            else:
                print("ข้อผิดพลาด: กรุณาเลือกตัวเลขหมวดหมู่ระหว่าง 1 ถึง 9 เท่านั้น")

        note = input("กรุณากรอกรายละเอียดเพิ่มเติม (หรือกด Enter เพื่อข้าม): ").strip()

        # บันทึกข้อมูลลง Dictionary
        transaction = {
            "type": "รายจ่าย",
            "amount": amount,
            "category": category,
            "note": note if note else "-"
        }
        transactions.append(transaction)
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

    # กรณีผู้ใช้พิมพ์ตัวเลือกอื่นนอกเหนือจาก 0-4
    else:
        print("ข้อผิดพลาด: กรุณาเลือกตัวเลขเมนูที่ถูกต้อง")
        continue

    # 3. ส่วนถามยืนยันหลังทำรายการเสร็จ
    next_action = input("\nทำรายการต่อไปหรือออก (กด Enter เพื่อเลือกเมนู / กด 0 เพื่อออกจากโปรแกรม): ").strip()
    if next_action == "0":
        print("ขอบคุณที่ใช้งาน PyPocket")
        break