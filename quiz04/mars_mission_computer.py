# 시간 관련 라이브러리만 사용 허용됨 (제약 조건 만족)
import time


# 문제 3 - DummySensor 클래스 정의
# 화성 기지의 환경 값을 생성하는 센서 시뮬레이터
# random 사용 금지로, 시간 기반의 변동 값 생성
class DummySensor:
    def __init__(self):
        # 환경 값 저장용 딕셔너리 (문제 요구: 내부/외부 온도, 습도, 광량, CO2, 산소)
        self.env_values = {
            "mars_base_internal_temperature": 0.0,
            "mars_base_external_temperature": 0.0,
            "mars_base_internal_humidity": 0.0,
            "mars_base_external_illuminance": 0.0,
            "mars_base_internal_co2": 0.0,
            "mars_base_internal_oxygen": 0.0
        }

    # 시간 기반의 변동값을 생성하여 env_values에 저장
    def set_env(self):
        t = time.time()  # 현재 시간 기준 값
        self.env_values["mars_base_internal_temperature"] = 20 + (t % 10) * 0.1
        self.env_values["mars_base_external_temperature"] = -60 + (t % 5) * 0.5
        self.env_values["mars_base_internal_humidity"] = 30 + (t % 3) * 0.3
        self.env_values["mars_base_external_illuminance"] = 20000 + (t % 7) * 100
        self.env_values["mars_base_internal_co2"] = 400 + (t % 2) * 10
        self.env_values["mars_base_internal_oxygen"] = 21 + (t % 4) * 0.1

    # 현재 환경 값 반환
    def get_env(self):
        return self.env_values


# 미션 컴퓨터 클래스 정의 (문제 요구: 클래스 이름은 MissionComputer)
class MissionComputer:
    def __init__(self, sensor):
        # env_values: 센서에서 받은 환경 데이터를 저장하는 딕셔너리 (문제 요구)
        self.env_values = {}

        # ds 인스턴스 (문제 3에서 제작한 DummySensor를 ds로 인스턴스화)
        self.sensor = sensor

        # 5분 평균 계산을 위한 이력 리스트
        self.history = []

        # 시스템 중단을 위한 플래그
        self.stop_flag = False

    # 문제 요구: get_sensor_data 메서드 정의
    def get_sensor_data(self):
        while not self.stop_flag:
            # 센서에서 환경값 수집 후 저장 (문제 요구 1단계)
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()

            # JSON 형태처럼 환경 값 출력 (문제 요구 2단계)
            print("Current Sensor Data:")
            self.print_env_values(self.env_values)

            # 보너스 과제 2 - 5분 평균 데이터 저장
            self.history.append(self.env_values.copy())
            if len(self.history) == 60:
                print("5-Minute Average Sensor Data:")
                self.print_avg_data()
                self.history = []

            # 5초마다 반복 (문제 요구 3단계)
            time.sleep(5)

    # JSON 포맷처럼 출력하는 함수 (외부 라이브러리 사용 금지 조건 만족)
    def print_env_values(self, data):
        print("{")
        for key in data:
            print("    \"{}\": {}".format(key, round(data[key], 2)))
        print("}")

    # 보너스 과제 2 - 5분 평균 출력 함수
    def print_avg_data(self):
        avg_values = {
            "mars_base_internal_temperature": 0.0,
            "mars_base_external_temperature": 0.0,
            "mars_base_internal_humidity": 0.0,
            "mars_base_external_illuminance": 0.0,
            "mars_base_internal_co2": 0.0,
            "mars_base_internal_oxygen": 0.0
        }

        # 모든 값을 누적 합산
        for entry in self.history:
            for key in avg_values:
                avg_values[key] += entry[key]

        # 평균 계산 후 출력
        for key in avg_values:
            avg_values[key] /= len(self.history)

        self.print_env_values(avg_values)

    # 보너스 과제 1 - 시스템 정지 처리
    def stop(self):
        self.stop_flag = True
        print("System stopped...")


# 메인 실행 영역
if __name__ == "__main__":
    # DummySensor 클래스 인스턴스 생성 (ds로 이름 지정 - 문제 조건)
    ds = DummySensor()

    # MissionComputer 클래스 인스턴스를 RunComputer로 생성 (문제 조건)
    RunComputer = MissionComputer(ds)

    # 센서 데이터 수집 및 출력 메서드 실행
    try:
        RunComputer.get_sensor_data()
    # 보너스 과제 1 - Ctrl+C 입력 시 시스템 정지 처리
    except KeyboardInterrupt:
        RunComputer.stop()
