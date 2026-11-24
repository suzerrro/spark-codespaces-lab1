# 검증 범위

제작 환경에는 Docker 데몬이 실행되지 않아 실제 Spark 컨테이너 기동 및 Codespaces 전체 실행을 완료하지 못했습니다. 실행 성공을 보장하는 보고서가 아닙니다.

검사 대상은 Compose 설정 파싱, Dev Container JSON, Bash 문법, Python 문법, 입력 데이터 2400행과 정답 재계산, 문서와 파일 경로의 일치입니다. 학생 환경에서는 scripts/start.sh, scripts/run_all.sh로 실제 기동과 계산 결과를 확인합니다.

교수자는 GitHub 저장소의 Actions에서 Spark cluster smoke test를 수동 실행할 수도 있습니다. 이는 Linux Docker 클러스터 검증이며 Codespaces Dev Container 생성 자체의 검증은 별도입니다. Actions 사용량도 계정 정책을 확인하세요.

코드 기준: Apache Spark 4.0.5 Python3 공식 이미지. 입력 데이터는 이 패키지용으로 재생성한 가상 데이터로, 기존 교재와 지역별 합계가 다릅니다. data/expected.json이 이 패키지의 정답입니다.
