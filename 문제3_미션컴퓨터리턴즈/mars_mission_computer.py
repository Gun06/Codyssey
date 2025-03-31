import random
from datetime import datetime

class DummySensor:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }

    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = round(random.uniform(18, 30), 2)
        self.env_values["mars_base_external_temperature"] = round(random.uniform(0, 21), 2)
        self.env_values["mars_base_internal_humidity"] = round(random.uniform(50, 60), 2)
        self.env_values["mars_base_external_illuminance"] = round(random.uniform(500, 715), 2)
        self.env_values["mars_base_internal_co2"] = round(random.uniform(0.02, 0.1), 4)
        self.env_values["mars_base_internal_oxygen"] = round(random.uniform(4, 7), 2)

    def get_env(self):
        # 로그 작성
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_lines = [
            f"[{now}]",
            f"내부 온도: {self.env_values['mars_base_internal_temperature']}도",
            f"외부 온도: {self.env_values['mars_base_external_temperature']}도",
            f"내부 습도: {self.env_values['mars_base_internal_humidity']}%",
            f"외부 광량: {self.env_values['mars_base_external_illuminance']} W/m2",
            f"내부 CO2: {self.env_values['mars_base_internal_co2']}%",
            f"내부 산소: {self.env_values['mars_base_internal_oxygen']}%",
            ""  # 한 줄 공백으로 로그 간 구분
        ]

        with open("mars_env_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write("\n".join(log_lines))

        return self.env_values



# 인스턴스 생성 및 사용
if __name__ == "__main__":
    ds = DummySensor()
    ds.set_env()
    env_data = ds.get_env()
    
    # 출력 확인
    print("🌌 화성 기지 환경 센서 데이터:")
    for key, value in env_data.items():
        print(f"{key}: {value}")
