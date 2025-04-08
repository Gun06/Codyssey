# 파일 경로
csv_path = "/Users/kogun/Downloads/Mars Base Inventory List.csv"
danger_csv_path = "/Users/kogun/Downloads/Mars_Base_Inventory_danger.csv"  # 저장할 경로

# 리스트 객체 초기화
inventory_list = []

try:
    with open(csv_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        header = lines[0].strip().split(",")  # 첫 줄은 헤더 (열 이름)

        for line in lines[1:]:  # 헤더 제외
            parts = line.strip().split(",")
            if len(parts) == len(header):
                item = {
                    "Substance": parts[0],
                    "Weight": parts[1],
                    "Specific Gravity": parts[2],
                    "Strength": parts[3],
                    "Flammability": parts[4]
                }
                inventory_list.append(item)
except FileNotFoundError:
    print("❌ 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"❌ 오류 발생: {e}")

# 원본 출력
print("\n📄 원본 리스트 (상위 5개):")
for item in inventory_list[:5]:
    print(item)

# 인화성 변환 및 정렬
sorted_inventory = []
for item in inventory_list:
    try:
        item["Flammability"] = float(item["Flammability"])
        sorted_inventory.append(item)
    except ValueError:
        continue

sorted_inventory = sorted(sorted_inventory, key=lambda x: x["Flammability"], reverse=True)

print("\n🔥 인화성이 높은 순으로 정렬된 리스트 (상위 5개):")
for item in sorted_inventory[:5]:
    print(item)

# 인화성 ≥ 0.7 항목 필터링
dangerous_items = [item for item in sorted_inventory if item["Flammability"] >= 0.7]

print("\n🚨 인화성 지수 0.7 이상 화물 목록:")
for item in dangerous_items:
    print(item)

# ✅ 위험 목록을 CSV로 저장
try:
    with open(danger_csv_path, "w", encoding="utf-8") as f:
        f.write("Substance,Weight,Specific Gravity,Strength,Flammability\n")
        for item in dangerous_items:
            f.write(f"{item['Substance']},{item['Weight']},{item['Specific Gravity']},{item['Strength']},{item['Flammability']}\n")
    print(f"\n📁 CSV 파일 저장 완료: {danger_csv_path}")
except Exception as e:
    print(f"❌ CSV 저장 중 오류 발생: {e}")


# ✅ 이진 파일로 저장 (인화성 순 정렬된 전체 목록)
binary_file_path = "/Users/kogun/Downloads/Mars_Base_Inventory_List.bin"

try:
    with open(binary_file_path, "wb") as bin_file:
        for item in sorted_inventory:
            line = f"{item['Substance']},{item['Weight']},{item['Specific Gravity']},{item['Strength']},{item['Flammability']}\n"
            bin_file.write(line.encode("utf-8"))  # 문자열을 바이트로 인코딩해서 저장
    print(f"\n💾 이진 파일 저장 완료: {binary_file_path}")
except Exception as e:
    print(f"❌ 이진 파일 저장 중 오류 발생: {e}")


# ✅ 저장된 이진 파일을 다시 읽어서 출력
try:
    with open(binary_file_path, "rb") as bin_file:
        print("\n📤 이진 파일 내용 출력:")
        lines = bin_file.readlines()
        for line in lines:
            decoded_line = line.decode("utf-8").strip()  # 바이트 → 문자열
            print(decoded_line)
except FileNotFoundError:
    print("❌ 이진 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"❌ 이진 파일 읽기 중 오류 발생: {e}")

