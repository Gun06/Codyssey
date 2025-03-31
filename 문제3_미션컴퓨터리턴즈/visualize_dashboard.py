import os
import matplotlib.pyplot as plt
import platform
from datetime import datetime

# 한글 폰트 설정 (운영체제별)
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

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

    for i in range(0, len(lines), 8):
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

# 서브플롯으로 6개 그래프를 하나의 창에 출력
def plot_dashboard(t, t_in, t_out, hum, light, co2, oxy):
    fig, axs = plt.subplots(2, 3, figsize=(18, 8))
    fig.suptitle("🌌 화성 기지 환경 센서 데이터 요약 대시보드", fontsize=16)

    data = [
        (t_in, "내부 온도", "℃"),
        (t_out, "외부 온도", "℃"),
        (hum, "내부 습도", "%"),
        (light, "외부 광량", "W/m²"),
        (co2, "내부 CO₂", "%"),
        (oxy, "내부 산소", "%")
    ]

    for i, (y, title, unit) in enumerate(data):
        row, col = divmod(i, 3)
        ax = axs[row][col]
        ax.plot(t, y, marker='o')
        ax.set_title(title)
        ax.set_xlabel("시간")
        ax.set_ylabel(f"{title} ({unit})")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)

        # 각 데이터 포인트에 값 표시
        for j in range(len(t)):
            ax.text(t[j], y[j], f"{y[j]}", fontsize=8, ha='center', va='bottom')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# 메인 실행
if __name__ == "__main__":
    t, t_in, t_out, hum, light, co2, oxy = parse_log()
    plot_dashboard(t, t_in, t_out, hum, light, co2, oxy)
