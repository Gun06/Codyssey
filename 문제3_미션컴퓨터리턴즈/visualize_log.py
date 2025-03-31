import os
import matplotlib.pyplot as plt
import platform
from datetime import datetime

# 한글 폰트 설정 (한글 깨짐 방지)
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'      # 윈도우
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'         # macOS
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

# 로그 파일 경로
LOG_DIR = "문제3_미션컴퓨터리턴즈"
LOG_PATH = os.path.join(LOG_DIR, "mars_env_log.txt")

# 로그 파싱 함수
def parse_log():
    timestamps = []
    internal_temps = []
    external_temps = []
    humidities = []
    illuminances = []
    co2s = []
    oxygens = []

    with open(LOG_PATH, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for i in range(0, len(lines), 8):  # 8줄씩 끊어서 1세트
        try:
            timestamp = datetime.strptime(lines[i].strip()[1:-1], "%Y-%m-%d %H:%M:%S")
            internal_temp = float(lines[i+1].split(":")[1].replace("도", "").strip())
            external_temp = float(lines[i+2].split(":")[1].replace("도", "").strip())
            humidity = float(lines[i+3].split(":")[1].replace("%", "").strip())
            illuminance = float(lines[i+4].split(":")[1].replace("W/m2", "").strip())
            co2 = float(lines[i+5].split(":")[1].replace("%", "").strip())
            oxygen = float(lines[i+6].split(":")[1].replace("%", "").strip())

            timestamps.append(timestamp)
            internal_temps.append(internal_temp)
            external_temps.append(external_temp)
            humidities.append(humidity)
            illuminances.append(illuminance)
            co2s.append(co2)
            oxygens.append(oxygen)
        except Exception as e:
            print(f"로그 파싱 오류: {e}")
            continue

    return timestamps, internal_temps, external_temps, humidities, illuminances, co2s, oxygens

# 그래프 출력 함수
def plot_graph(x, y, title, ylabel):
    plt.figure(figsize=(10, 4))
    plt.plot(x, y, marker='o')

    # 각 데이터 포인트에 값 표시
    for i in range(len(x)):
        plt.text(x[i], y[i], f"{y[i]}", fontsize=8, ha='center', va='bottom')

    plt.title(title)
    plt.xlabel("시간")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()


# 메인 실행
if __name__ == "__main__":
    t, t_in, t_out, hum, light, co2, oxy = parse_log()

    plot_graph(t, t_in, "화성 기지 내부 온도 변화", "온도 (℃)")
    plot_graph(t, t_out, "화성 기지 외부 온도 변화", "온도 (℃)")
    plot_graph(t, hum, "화성 기지 내부 습도 변화", "습도 (%)")
    plot_graph(t, light, "화성 기지 외부 광량 변화", "광량 (W/m²)")
    plot_graph(t, co2, "화성 기지 내부 이산화탄소 농도 변화", "CO₂ (%)")
    plot_graph(t, oxy, "화성 기지 내부 산소 농도 변화", "산소 (%)")
