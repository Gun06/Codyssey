import csv
import os
from datetime import datetime
import getpass
import mysql.connector
import matplotlib.pyplot as plt

# === 설정 ===
# 필요한 패키지 설치:
# pip install mysql-connector-python matplotlib
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'mars_weathers_data.csv')  # CSV 데이터 파일 경로
OUTPUT_IMAGE = os.path.join(BASE_DIR, 'mars_weather_summary.png')  # 요약 그래프 이미지 저장 경로

class MySQLHelper:
    """
    MySQL 연결 및 쿼리 실행을 도와주는 헬퍼 클래스
    """
    def __init__(self, host='localhost', user='root', password='', database='mars_db'):
        # 접속 정보 초기화
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None  # 나중에 연결 객체가 저장될 변수

    def connect(self):
        """
        MySQL 서버에 연결을 생성합니다.
        """
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def close(self):
        """
        MySQL 연결을 닫습니다.
        """
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None):
        """
        INSERT, UPDATE, DELETE 등 데이터 변형 쿼리를 실행합니다.
        :param query: 실행할 SQL 문자열
        :param params: 쿼리 파라미터 튜플
        """
        cur = self.conn.cursor()
        cur.execute(query, params or ())
        self.conn.commit()  # 변경 사항 커밋
        cur.close()

    def fetchall(self, query, params=None):
        """
        SELECT 쿼리를 실행하고 결과를 모두 가져옵니다.
        :return: 결과 리스트
        """
        cur = self.conn.cursor()
        cur.execute(query, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows

    def create_table(self):
        """
        mars_weather 테이블을 생성합니다.
        IF NOT EXISTS를 사용하여 이미 존재하면 생성하지 않습니다.
        """
        sql = '''
        CREATE TABLE IF NOT EXISTS mars_weather (
            weather_id INT AUTO_INCREMENT PRIMARY KEY,
            mars_date DATETIME NOT NULL,
            temp FLOAT,
            storm INT
        )'''
        self.execute(sql)

    def insert_csv(self, csv_path):
        """
        CSV 파일을 읽어 데이터를 삽입합니다.
        동일한 mars_date가 이미 존재하면 건너뜁니다.
        :param csv_path: CSV 파일 경로
        """
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 문자열을 datetime 객체로 변환
                date = datetime.strptime(row['mars_date'], '%Y-%m-%d')
                temp = float(row['temp'])
                # 컬럼명이 'storm' 또는 'stom'인 경우 모두 처리
                storm = int(row.get('storm', row.get('stom', 0)))

                # 중복 체크: 같은 mars_date가 있는지 조회
                check_sql = 'SELECT weather_id FROM mars_weather WHERE mars_date = %s'
                if self.fetchall(check_sql, (date,)):
                    # 이미 데이터가 있으면 다음 행으로 넘어감
                    continue

                # 데이터 삽입
                insert_sql = (
                    'INSERT INTO mars_weather (mars_date, temp, storm) VALUES (%s, %s, %s)'
                )
                self.execute(insert_sql, (date, temp, storm))


def generate_summary(helper: MySQLHelper, image_path: str):
    """
    DB에서 mars_date와 temp를 조회해 꺾은선 그래프를 그리고
    지정된 경로에 PNG 파일로 저장합니다.
    :param helper: DB 헬퍼 인스턴스
    :param image_path: 저장할 이미지 파일 경로
    """
    # mars_date 순으로 정렬하여 데이터 조회
    rows = helper.fetchall(
        'SELECT mars_date, temp FROM mars_weather ORDER BY mars_date'
    )
    dates = [r[0] for r in rows]
    temps = [r[1] for r in rows]

    # Matplotlib 꺾은선 그래프 생성
    plt.figure()
    plt.plot(dates, temps)
    plt.title('Mars Surface Temperature Over Time')
    plt.xlabel('Mars Date')
    plt.ylabel('Temperature (°C)')
    plt.tight_layout()
    plt.savefig(image_path)  # 이미지 파일로 저장
    print(f'Summary image saved to {image_path}')


def main():
    # 사용자 입력을 통해 MySQL 접속 정보와 DB 이름을 설정
    host = input('MySQL host [localhost]: ') or 'localhost'
    user = input('MySQL user [root]: ') or 'root'
    pw = getpass.getpass('MySQL password: ')
    db = input('Database name [mars_db]: ') or 'mars_db'

    # 헬퍼 객체 초기화 및 연결
    helper = MySQLHelper(host, user, pw, db)
    helper.connect()
    helper.create_table()
    print('Table `mars_weather` is ready.')

    # CSV 데이터 삽입
    helper.insert_csv(CSV_FILE)
    print('CSV data inserted.')

    # 요약 그래프 생성
    generate_summary(helper, OUTPUT_IMAGE)
    helper.close()


if __name__ == '__main__':
    main()