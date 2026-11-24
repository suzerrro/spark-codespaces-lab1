# 내 GitHub 계정에서 시작하는 Spark Codespaces 실습

이 패키지는 학생이 자신의 GitHub 저장소를 만들고, 브라우저에서 Codespaces를 생성하여 Spark Master 1개, Worker 2개, Client 1개를 실행하는 실습입니다. PC에 Docker·Java·Spark를 설치할 필요는 없습니다. 인터넷과 GitHub 계정이 필요하며 Codespaces 사용 가능 여부는 계정 정책에 따릅니다.

## 1 내 저장소 만들기

1. 배포 ZIP을 PC에서 압축 해제합니다. ZIP 파일 자체를 GitHub에 올리지 않습니다.
2. https://github.com 에 자신의 계정으로 로그인합니다.
3. 오른쪽 위 + 메뉴의 New repository를 선택합니다.
4. Owner가 자신의 계정인지 확인하고 Repository name에 spark-codespaces-lab을 입력합니다.
5. 공개 범위는 수업 지침에 맞게 정합니다. Add a README file을 켜고 Create repository를 누릅니다. 빈 저장소에서는 Codespace 생성 버튼이 비활성화될 수 있습니다.
6. 저장소 주소가 https://github.com/내계정/spark-codespaces-lab 인지 확인합니다.

## 2 압축 해제한 파일 올리기

저장소의 Add file > Upload files를 선택합니다. 압축 해제한 spark-codespaces-lab 폴더의 '내용물'을 올립니다. 상위 spark-codespaces-lab 폴더를 한 겹 더 만들지 않습니다. 기존 README와 같은 이름은 교체될 수 있습니다. 업로드 후 Commit changes를 눌러 서버에 저장합니다.

저장소 최상위에서 반드시 아래 경로를 확인하세요.

- .devcontainer/devcontainer.json
- docker-compose.yml
- apps/01_hello_spark.py 등 4개 파일
- scripts/start.sh와 scripts/run.sh
- data/orders.csv와 data/wordcount.txt
- README.md

특히 .devcontainer가 없으면 Codespaces에 Docker 구성이 적용되지 않습니다. 파일 탐색기에서 숨김 파일 표시를 켜 확인하세요. 웹 업로드에서 이 폴더가 빠지면 GitHub의 Add file > Create new file을 선택하고 파일명에 .devcontainer/devcontainer.json을 입력합니다. 패키지의 같은 파일을 메모장으로 열어 내용을 그대로 붙여 넣고 Commit changes를 누릅니다. 이 한 파일을 복구한 뒤 Codespace를 만드세요.

GitHub 주소에 spark-codespaces-lab/spark-codespaces-lab/docker-compose.yml처럼 폴더가 중복되면 잘못 올린 것입니다. 루트 바로 아래 docker-compose.yml이 있어야 합니다.

## 3 자신의 저장소에서 Codespace 생성

1. 자신의 저장소에서 녹색 Code 버튼 > Codespaces 탭을 엽니다.
2. Create codespace on main을 누릅니다. 선택 화면에서는 우선 2 cores / 8 GB를 사용합니다. 생성 시간이 걸릴 수 있습니다.
3. 브라우저에 VS Code 편집기가 나타나면 Terminal > New Terminal을 선택합니다.
4. 아래 명령을 실행합니다.

~~~bash
pwd
ls -la
test -f .devcontainer/devcontainer.json && echo DEVCONTAINER_OK
bash scripts/doctor.sh
~~~

[OK]가 나오면 Docker Client, Server와 Compose 설정을 확인한 것입니다. 최초 준비 명령은 데이터와 출력 폴더만 준비하고, Spark 이미지 다운로드와 클러스터 시작은 다음 단계에서 직접 수행합니다.

복구 모드 안내가 보이거나 docker가 없으면 .devcontainer 파일 경로부터 확인합니다. Ctrl+Shift+P > Codespaces: Rebuild Container를 실행합니다. Docker Server 연결 실패는 잠시 기다린 뒤 doctor.sh를 다시 실행하고 계속 실패하면 재구성합니다.

## 4 Spark 클러스터 시작

~~~bash
bash scripts/start.sh
~~~

이 스크립트는 출력 폴더 준비, Docker 설정 검사, 이미지 다운로드, 네 서비스 실행, Worker 2개 등록 확인을 차례로 수행합니다. 네 서비스는 같은 apache/spark:4.0.5-python3 이미지를 서로 다른 명령으로 실행합니다.

완료 후 아래 명령으로 상태를 봅니다.

~~~bash
docker compose ps
bash scripts/check_cluster.sh 2
~~~

기대 결과는 Master·Client·Worker 2개가 실행되고 활성 Worker가 2개인 상태입니다. 이미지 다운로드가 중단되면 start.sh를 다시 실행할 수 있습니다. 오류가 반복되면 logs와 Docker 로그를 확인하세요. 종료 코드를 무시하고 다음 단계로 넘어가지 않습니다.

## 5 관리 화면과 포트

VS Code 하단 PORTS 탭에서 8080의 Open in Browser를 누릅니다. 보이지 않으면 Add Port로 8080을 추가합니다. 포트의 Visibility는 Private를 유지합니다.

| Codespaces 포트 | 용도 | 확인 항목 |
|---|---|---|
| 8080 | Master UI | 활성 Worker 2개, 총 2코어, 선언 메모리 2GiB |
| 8081 | Worker 1 UI | Executor와 작업 로그 |
| 8082 | Worker 2 UI | 컨테이너 내부 8081을 외부 8082로 연결 |
| 4040 | Driver UI | 작업 실행 중 Jobs, Stages, Executors |

7077은 Docker 네트워크 내부 Master 통신 포트입니다. 브라우저에 공개할 필요가 없습니다. Master UI 안의 spark-worker-1:8081 링크는 PC 브라우저에서 직접 열리지 않을 수 있습니다. PORTS 탭에서 각각 8081, 8082를 여세요. Driver UI는 프로그램이 종료되면 사라집니다.

## 6 첫 프로그램 실행

~~~bash
bash scripts/run.sh apps/01_hello_spark.py
~~~

Master는 spark://spark-master:7077, 파티션 수는 4, count는 100이 나와야 합니다. repartition(4)는 데이터의 논리적 조각 수를 정하며 Worker 4개를 만드는 명령이 아닙니다.

UI를 천천히 관찰하려면 아래처럼 90초 대기 옵션을 사용합니다. 명령이 끝나기 전에 PORTS 탭의 4040을 열어 Jobs, Stages, Executors를 확인합니다.

~~~bash
bash scripts/run.sh apps/01_hello_spark.py --hold-seconds 90
~~~

Driver는 spark-client에서 실행됩니다. Master가 Worker에 Executor 실행을 지시하면 Driver가 Executor에 Task를 배정합니다. Executor와 Driver는 Docker 네트워크에서 직접 통신합니다.

## 7 CSV와 SQL 분석

~~~bash
head -n 6 data/orders.csv
wc -l data/orders.csv
bash scripts/run.sh apps/02_orders_analysis.py
~~~

orders.csv는 헤더를 포함해 2401줄입니다. 데이터 2400건 중 PAID 2026건, CANCELLED 248건, REFUNDED 126건입니다. 금액은 quantity × unit_price이며 실제 결제 완료 거래액을 계산할 때는 PAID 필터를 적용합니다.

이 패키지는 재현 가능한 새 가상 데이터를 포함합니다. 기존 교재의 지역별 정답을 그대로 적용하지 마세요. 이번 데이터의 정답은 다음과 같습니다.

| 지역 | PAID 거래액 |
|---|---:|
| Busan | 28,075,000 |
| Daegu | 29,690,000 |
| Daejeon | 25,860,000 |
| Incheon | 29,155,000 |
| Seoul | 29,655,000 |

DataFrame과 SQL의 지역별 결과가 같아야 합니다. 프로그램은 data/expected.json과 비교한 후 [PASS]를 출력하고 output/orders_summary.json에 저장합니다. collect는 작은 집계 결과에만 사용합니다. 전체 원본을 Driver로 수집하는 예제가 아닙니다.

과제 A는 제공된 category 집계 예시를 참고하여 channel별 PAID 거래액을 추가로 계산하는 것입니다. 결과와 코드, PAID 조건이 필요한 이유를 제출합니다.

## 8 실제 Task를 처리한 Worker 확인

~~~bash
bash scripts/run.sh apps/03_partition_workers.py
~~~

정수 1~10000을 8개 파티션으로 나눕니다. 각 행에 파티션 번호, 실행 호스트, PID, 원소 수, 부분 합계가 나타납니다. 원소 수 총합은 10000, 전체 합계는 50005000입니다. 1~10000 합계는 10000 × 10001 ÷ 2로도 검산할 수 있습니다.

실행 호스트에서 spark-worker-1과 spark-worker-2를 찾습니다. 파티션 배정은 매번 달라질 수 있습니다. 한 호스트만 보이면 Master UI의 활성 Worker 수와 점유 자원을 확인하고 다시 실행합니다. 8개 파티션을 2개 코어로 처리하므로 모든 Task를 동시에 실행하지는 않습니다. 두 컨테이너 모두 하나의 Codespace VM에서 실행됩니다.

## 9 RDD WordCount

~~~bash
cat data/wordcount.txt
bash scripts/run.sh apps/04_wordcount.py
~~~

기본 입력 정답은 spark 4, data 3, hadoop 2, python 2, sql 2, engineering 1입니다. 텍스트 줄에서 flatMap으로 단어를 추출하고, map으로 (단어, 1)을 만들고, reduceByKey로 합칩니다.

과제 B는 data/wordcount.txt 맨 뒤에 spark spark spark 한 줄을 추가하고 다시 실행하는 것입니다. spark 개수가 4에서 7로 증가해야 합니다. 이 프로그램은 현재 파일을 기준으로 정답을 재계산하므로 수정 실습 후에도 검증할 수 있습니다. 출력은 output/wordcount.json과 실행별 wordcount-* 폴더에 남습니다.

## 10 로컬 모드와 비교

~~~bash
bash scripts/run_local.sh apps/03_partition_workers.py
~~~

| 구분 | run.sh | run_local.sh |
|---|---|---|
| Master | spark://spark-master:7077 | local[2] |
| Task 실행 호스트 | Worker 컨테이너 | spark-client |
| 파티션 수 | 8 | 8 |
| 실행 병렬성 | Worker별 1코어 | 한 호스트의 두 스레드 |
| 전체 합계 | 50005000 | 50005000 |

로컬 모드에서도 파티션을 만들 수 있습니다. 파티션은 물리 서버 수와 다릅니다. 두 모드 모두 실제로는 동일한 Codespace VM 안에서 실행됩니다.

## 11 Worker 수 변경

실행 중인 프로그램이 모두 끝난 뒤 아래 명령을 수행합니다.

~~~bash
bash scripts/worker_one.sh
~~~

Worker 2를 정지하고 활성 Worker가 1개가 될 때까지 기다린 뒤 같은 파티션 실습을 실행합니다. Master의 상태 갱신에 약 1분이 걸릴 수 있습니다. 사용 호스트가 spark-worker-1만 남고 전체 합계는 50005000인지 확인합니다.

다음 명령으로 Worker 2를 복구합니다.

~~~bash
bash scripts/worker_restore.sh
~~~

이 실험은 다음 작업에 배정 가능한 자원을 줄이는 실험입니다. 실행 도중 장애를 일으켜 복구 성능을 측정하는 실험은 아닙니다.

## 12 전체 실행과 결과 검증

클러스터가 두 Worker 상태일 때 다음 명령으로 전체 실습을 순서대로 실행할 수 있습니다.

~~~bash
bash scripts/run_all.sh
~~~

스크립트는 각 실습의 실제 종료 코드를 확인합니다. 오류가 발생하면 중단하며 logs/에 실행 로그가 남습니다. 이후 출력 파일 검사는 다음 명령으로 다시 수행할 수 있습니다.

~~~bash
python3 scripts/verify_results.py
~~~

검증은 실제 output JSON을 입력 데이터의 정답과 비교합니다. 아직 실습을 실행하지 않았다면 결과 파일이 없어 실패하는 것이 정상입니다.

## 13 저장하고 실습 종료

Codespaces 편집기에서 파일을 저장한 것과 GitHub 저장소에 반영한 것은 다릅니다. Ctrl+S 후 왼쪽 Source Control에서 변경 파일을 확인하고 Stage Changes, Commit, Sync Changes 또는 Push를 수행합니다. 결과 폴더는 기본적으로 Git에서 제외합니다. 제출할 로그·화면은 별도로 다운로드하거나 reports/ 같은 폴더에 필요한 것만 저장하세요.

터미널에서 저장할 때는 내용 확인 후 다음처럼 특정 파일만 추가할 수 있습니다.

~~~bash
git status
git add apps/02_orders_analysis.py data/wordcount.txt
git commit -m "Complete Spark exercises"
git push
bash scripts/stop.sh
~~~

그다음 https://github.com/codespaces 에서 해당 Codespace의 ... 메뉴 > Stop codespace를 누릅니다. docker compose down이나 브라우저 탭 닫기만으로 Codespace 사용량이 멈췄다고 판단하지 않습니다. 중지 후에도 보관 저장 공간의 사용량은 남을 수 있습니다. 필요 없는 Codespace는 변경 내용이 GitHub에 반영되었는지 확인한 뒤 Delete합니다. 저장소 삭제와 Codespace 삭제는 다른 작업입니다. 무료 포함량·과금 여부는 자신의 Billing 화면에서 확인하세요.

## 14 오류 해결

| 증상 | 먼저 할 일 |
|---|---|
| Code 또는 Codespaces 생성 버튼 비활성 | 로그인, 저장소 권한, 최소 1개 커밋, 계정 사용량 확인 |
| docker가 없음 또는 복구 모드 | 루트 .devcontainer/devcontainer.json 확인 후 Rebuild Container |
| Docker Server 연결 실패 | 잠시 후 doctor.sh 재시도, 계속 실패하면 Rebuild Container |
| no configuration file provided | pwd와 ls -la 확인, docker-compose.yml이 있는 저장소 루트로 이동 |
| Worker 0개 | docker compose ps 및 Master·Worker 로그 확인 |
| Driver Connection refused | run.sh 설정을 유지하고 동시 작업을 종료한 뒤 재시도 |
| 입력 파일 없음 | data 경로와 모든 서비스의 동일한 /lab/data 마운트 확인 |
| 메모리 부족 | 다른 작업 중단, 필요시 4코어/16GB 머신으로 변경 |
| UI가 열리지 않음 | 컨테이너 상태, PORTS 탭, 4040은 실행 중인지 확인 |
| CRLF 또는 bash 오류 | .gitattributes 확인 후 GitHub 원본에서 다시 가져오기 |

~~~bash
docker compose ps
docker compose logs --tail=80 spark-master spark-worker-1 spark-worker-2
docker stats --no-stream
~~~

동시에 두 프로그램을 제출하지 마세요. 이 실습은 Driver 포트와 작은 실행 자원을 고정합니다. 입력은 /lab/data에 읽기 전용으로, 결과는 /lab/output에 쓰기 가능으로 연결됩니다. PC 파일은 Codespace에 자동 공유되지 않습니다. data 파일은 Codespaces 편집기에서 수정하세요.

## 15 제출 항목

1. 자기 계정의 GitHub 저장소 주소와 루트 구성 화면
2. Master UI의 활성 Worker 2개 화면
3. 파티션별 호스트와 합계가 보이는 결과
4. 과제 A 코드·결과 및 PAID 필터 설명
5. 과제 B의 spark 4 → 7 변화
6. 로컬·클러스터, Worker 1개·2개 차이 설명
7. Codespace를 중지한 화면

배점 예시: 개인 저장소·클러스터 실행 20점, DataFrame·SQL 20점, Worker·파티션 관찰 25점, 로컬 비교 15점, 과제 해석 20점.

## 공식 참고 문서

- GitHub Codespace 생성: https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository
- Dev Container 설정: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers
- 포트 전달: https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace
- 사용량 관리: https://docs.github.com/en/codespaces/troubleshooting/troubleshooting-included-usage
- Spark Standalone: https://spark.apache.org/docs/4.0.5/spark-standalone.html
- Apache 공식 이미지 태그: https://github.com/apache/spark-docker/blob/master/versions.json
- Docker-in-Docker: https://github.com/devcontainers/features/tree/main/src/docker-in-docker

패키지 검증 범위는 VALIDATION.md를 참고하세요.
