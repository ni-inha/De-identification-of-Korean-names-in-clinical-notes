# De-identification of Korean names in clinical notes

EMR 임상노트 속 의료진의 한국어 이름을 규칙 기반으로 비식별화합니다. <br>
분석할 csv 파일의 컬럼(column) 데이터를 익명화하여 새로운 파일로 저장합니다.

## 사용 환경

- Python 3.X
- pandas

pandas가 설치되어 있지 않다면, 터미널에 아래 명령어를 입력하여 설치할 수 있습니다.

```bash
$ pip install pandas
```

## 사용 방법 (터미널)

```bash
$ python main.py
```

프로그램 실행 후, 분석할 csv 파일의 경로를 상대경로 혹은 절대경로로 입력해야 합니다. <br>
해당 파일에서 분석할 컬럼(column) 이름을 입력하면 비식별화가 된 새로운 파일이 저장됩니다.
