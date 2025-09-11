# 1. 'Hello Mars' 출력
print("Hello Mars")

# 2. 로그 파일 열기 (예외 처리 포함)
log_file_path = '/Users/kogun/Desktop/Codyssey/quiz01/mission_computer_main.log'

# 로그 파일을 열고 예외를 처리
def read_log_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        exit(1)
    except IOError:
        print(f"Error: An error occurred while reading the file '{file_path}'.")
        exit(1)

log_data = read_log_file(log_file_path)

# 3. 로그 파일 출력
print("=== Log Data ===")
for line in log_data:
    print(line.strip())

# 4. 로그 데이터에서 시간 역순으로 정렬하기 위한 타임스탬프 추출 함수
def extract_timestamp(log_line):
    try:
        parts = log_line.split(',')
        if len(parts) < 3:  # 헤더를 제외하기 위한 조건
            return None
        timestamp_str = parts[0].strip()
        date_str, time_str = timestamp_str.split(' ')
        year, month, day = map(int, date_str.split('-'))
        hour, minute, second = map(int, time_str.split(':'))
        # 시간 정보를 튜플 형식으로 반환
        return (year, month, day, hour, minute, second)
    except Exception as e:
        print(f"Error extracting timestamp from log line: {log_line}")
        return None

# 5. 헤더 제외 및 로그 데이터 시간 역순으로 정렬
log_data = [line for line in log_data if "timestamp,event,message" not in line]  # 헤더 제외
sorted_log_data = sorted(
    [(extract_timestamp(line), line) for line in log_data if extract_timestamp(line) is not None],
    key=lambda x: x[0], reverse=True
)

# 6. 문제되는 로그만 필터링 (ERROR, CRITICAL, WARNING)
def filter_problematic_logs(sorted_log_data):
    return [line for _, line in sorted_log_data if "ERROR" in line or "CRITICAL" in line or "WARNING" in line]

problematic_lines = filter_problematic_logs(sorted_log_data)

# 7. Markdown 형태로 보고서 작성
def generate_markdown_report(problematic_lines):
    md_content = "# Log Analysis Report\n\n"
    md_content += "## 1. Log Overview\n"
    md_content += "This is a log analysis report for the `mission_computer_main.log` file. The following logs have been reviewed and analyzed to identify potential issues and causes of the accident.\n\n"
    md_content += "The logs are sorted in reverse chronological order:\n\n"

    # 로그 데이터를 표 형식으로 작성
    md_content += "| Timestamp           | Event  | Message                                                             |\n"
    md_content += "|---------------------|--------|---------------------------------------------------------------------|\n"
    
    for line in sorted_log_data:
        timestamp, log_line = line
        parts = log_line.split(',')
        md_content += f"| {parts[0]} | {parts[1]} | {parts[2]} |\n"

    md_content += "\n## 2. Accident Cause Analysis\n"
    md_content += "The following log entries contain errors, warnings, or critical messages that could indicate the cause of the accident:\n\n"
    
    # 문제 로그 분석 및 사고 원인 작성
    for log in problematic_lines:
        parts = log.split(',')
        timestamp = parts[0].strip()
        event = parts[1].strip()
        message = parts[2].strip()
        
        if "Oxygen tank" in message:
            md_content += f"- **Oxygen Tank Issues**: \n"
            md_content += f"  - **Timestamp**: {timestamp}\n"
            md_content += f"  - **Event**: {event}\n"
            md_content += f"  - **Message**: {message}\n\n"
        else:
            md_content += f"- **Mission Success**: \n"
            md_content += f"  - **Timestamp**: {timestamp}\n"
            md_content += f"  - **Event**: {event}\n"
            md_content += f"  - **Message**: {message}\n\n"

    md_content += "\n## 3. Conclusion\n"
    md_content += "Based on the log entries above, it appears that the accident was caused by the following issues:\n\n"
    md_content += "- **Oxygen Tank Instability**: The oxygen tank was unstable and eventually exploded, leading to the failure of mission-critical systems.\n"
    md_content += "- **Further Investigation**: A detailed investigation into the oxygen tank and related systems should be conducted to prevent similar accidents in the future.\n\n"
    md_content += "We recommend reviewing the safety mechanisms for the oxygen tank and ensuring that proper safeguards are in place for future missions."

    return md_content

# 8. Markdown 보고서 파일로 저장
def save_markdown_report(md_content, filename='/Users/kogun/Desktop/Codyssey/quiz01/log_analysis.md'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(md_content)

# 생성된 마크다운 보고서 저장
report = generate_markdown_report(problematic_lines)
save_markdown_report(report)

# 9. 결과 출력
print("Logs sorted in reverse order:")
for _, line in sorted_log_data:
    print(line.strip())
