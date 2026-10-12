# highD dataset 기반 화물차량이 연속류에 미치는 영향에 대한 경험적 분석

고려대학교 세종캠퍼스 「지능형교통체계」 프로젝트 → 한국교통학회지 투고용 분석 코드 (2023)

- 분석 기간: 2023-09 ~ 2023-12
- 보고서 최신본: `paper/보고서_20231212.docx`
- 투고본: `paper/한국교통학회지/최원석.hwp`

---

## 1. 연구 개요

고해상도 카메라를 장착한 드론으로 취득한 고속도로 Vehicle Trajectory 데이터(highD)를 사용해
**이동형 병목(Moving Bottleneck)** 현상을 실증적으로 관측한다.

핵심 가설: 주변 교통류보다 느리게 주행하는 차량(주로 화물차량)이 이동형 병목을 형성하여
후속 교통류에 **지체(delay)** 와 **용량 저하(capacity drop)** 를 유발한다.

기존 연구 대부분이 검지기 기반 거시 자료 또는 시뮬레이션에 의존한 반면,
본 연구는 미시적 실측 trajectory로 이를 정량화하는 것을 목표로 한다.

분석 결과 요약 (보고서 기준):

- 일반 차량 평균 통행속도 **110.4 km/h** vs 화물 차량 **85.6 km/h**
- 차로별 화물차 비율: 1차로(inner) **0.51%**, 2차로(middle) **8.6%**
- 트럭 중 저속차량으로 식별된 비율 **11.1%**, 저속차량 중 트럭인 비율 **55.6%**

---

## 2. 데이터

### highD dataset

독일 A4 / A46 / A61 고속도로, 드론 촬영, **25 fps**, 약 **420 m** 구간, 1개 recording = 약 15분.

`data/` 에 148개 파일 = **37개 recording × 4파일**

| 파일 | 내용 |
|---|---|
| `{track}_tracks.csv` | 프레임별 개별 차량 상태 (25컬럼, 약 80 MB) |
| `{track}_tracksMeta.csv` | 차량 단위 요약 (차종 `class`, 평균속도 `meanVel` 등) |
| `{track}_recordingMeta.csv` | recording 단위 메타 (locationId, duration, numVehicles 등) |
| `{track}_highway.png` | 해당 구간 항공 이미지 |

### track 번호 규칙

모든 스크립트 상단의

```python
tracks = [11,12,13,14,25,26,27,...,57]
```

는 **Site 1(데이터 제공량이 가장 많은 지역, 37개) 만 선별한 목록**이다.
Site 선정 근거는 `read recording meta.py`(track → locationId 출력)와 보고서 Table 1.

### 차로(laneId) 규칙

편도 3차선 × 2방향, 총 6차로.

| laneId | 방향 | xVelocity 부호 |
|---|---|---|
| 2, 3, 4 | Upstream | 음수 (-) |
| 5 | 중앙분리대 (항상 비어 있음) | - |
| 6, 7, 8 | Downstream | 양수 (+) |

코드에 반복적으로 나오는 `if N_LANE == 5: continue` 는 이 때문이다.
**방향 구분은 laneId가 아니라 `xVelocity` 의 부호로 처리**된 곳이 많다.

### `newData/` 가공본

`manipulate_csv.py` 로 생성한 축약·분리본. 25컬럼 → **7컬럼**(`frame,id,x,y,xVelocity,yVelocity,laneId`)으로 줄여 용량을 1/3 수준으로 축소.

| prefix | 내용 | track 11 행 수 |
|---|---|---|
| `M{track}_tracks.csv` | 전체 차량 | 658,772 |
| `C{track}_tracks.csv` | 승용차(Car)만 | 572,407 |
| `T{track}_tracks.csv` | 화물차(Truck)만 | 86,366 |

`sectorSpd.py` 가 다른 스크립트와 달리 `X_SPD=4, LANE=6` 인덱스를 쓰는 이유는 이 7컬럼 포맷을 읽기 때문이다(버그 아님).

---

## 3. 코드 구조

**`cv.py` 만 공용 라이브러리이고, 나머지 28개 파일은 전부 독립 실행 스크립트다.**
그리고 **스크립트 1개 ↔ 결과물 폴더 1개**가 거의 1:1로 대응하므로, 폴더 이름이 곧 코드의 색인 역할을 한다.

### 3.1 공용 라이브러리 — `cv.py` (550줄, Python 3.11)

| 분류 | 함수 |
|---|---|
| 지표 계산 | `spaceHeadway(s)`, `timeHeadway(s)`, `averageSpeed(s)`, `countVeh`, `countVehInTime`, `countVehs` |
| 가상 검지기 | `makeGraph`, `makeGraphs` → 50/200/350m 지점 누적 통행량(N-curve 원재료) |
| 지체 계산 | `measureDelay`(두 곡선 사이 면적, 음수는 0으로 clip), `averageDelay`(÷ 차량수) |
| 저속차량 식별 | `detectSlowVeh`, `detectSlowVehPandas`, `detectSlowVehs`, `detectSlowVehNew` |
| 차종 조회 | `getTruckIds` |
| 최종 표 생성 | `toCsv` ← 논문 본표 생성기 |

### 3.2 시공도 (Time-Space Diagram) — 보고서 Fig 3, 4

| 파일 | 역할 | 출력 |
|---|---|---|
| `dump_conti.py` | **완성형**. 전 차로 연속 컬러맵(`gist_rainbow`, 0~140 km/h clip) | `Trajectory/` |
| `truckPoint Trajectory.py` | 화물차만 검정색으로 오버레이 | `Trajectory/` |
| `drawTrajectory.py` | ID 리스트를 받아 특정 차량만 그림 (대화형 `input()`) | - |
| `NewSTD.py` | 속도 9단계 이산 색상 버전 | - |
| `colorbar.py` | hsv 컬러맵 실험 | - |
| `BACKUP.py` | 가장 초기 버전 (속도 6단계, track 03 하드코딩) | - |
| `old code/*.py` | 그 전신 (`colourmap.py`, `new cont colour.py`, `maint.py`) | - |

> 아래 → 위 순서로 발전했다. 실제로 논문 그림에 쓰인 것은 `dump_conti.py` 와 `truckPoint Trajectory.py`.

### 3.3 가상 검지기 · N-curve · 지체 ★분석의 척추

출발점으로부터 **50 m(r) / 200 m(g) / 350 m(b)** 에 가상 검지기를 설치하고(±3 m threshold),
각 지점 통과 차량을 누적해 N-curve를 그린 뒤 곡선 간 면적으로 지체를 구한다.

| 파일 | 역할 | 출력 |
|---|---|---|
| `ncurve.py` | 원본 N-curve (프레임 단위) | `N-curve/original_*` |
| `smoothing N.py` | 측정 인터벌을 1프레임 → 5초로 늘린 스무딩 N-curve | `sector/smoothingN_*` |
| `integral.py` | (C곡선 − A곡선), 음수 clip 후 `trapz` → **Total delay (veh·sec)** | `integral/Track*` |
| `accumulateTotalDelay.py` | 위를 `cumsum` 한 누적 지체 그래프 | `integral/accum_*` |
| `flow graph.py` | 검지기 통과 간격의 역수 = 지점 flow | `flow/` |
| `sectorSpd.py` | 3개 검지기 지점의 속도 시계열 (`newData/T*` 사용) | `speed/` |
| `SectionalState.py` | 교통상태 4분류(FF/BN/BQ/CT) — **주석만, 미구현** | - |

### 3.4 저속차량 식별

정의가 세 번 재정의되며 발전했다. 이것이 중복 코드가 많아 보이는 주된 이유다.

| 정의 | 기준 | 구현 |
|---|---|---|
| 정의 1 | 선행 차량 평균속도의 **90% 미만** | `comparewTruck.py` → `ToS_SoT.csv` |
| 정의 2 | 선행 차량 대비 **10% 이상** 느리고 + 좌·우 인접 차로 대비 **5% 이상** 느림 | `detectSlowVeh.py` ★실제 사용본 |
| 정의 3 | 트럭의 3 / 6 / 9초 후행 차량군 | **미착수** (교수님 코멘트) |

`detectSlowVeh.py` 는 식별과 동시에

- 진단용 CSV (`SideSpeed/side_output.csv` — id별 속도비 및 판정 플래그 `b_old`, `b_new`, `b_side`)
- 저속차량을 검정색으로 표시한 차로별 시공도 (`slowveh/`)
- 전체 대수 + 저속차량 대수 2선 그래프 (`cv.countVeh` → `countvehicle/i_track*_lane*`)

를 함께 생성한다. 정의 1 → 2 적용 시 약 4만대 중 저속차량 **2,300대 → 1,200대**로 감소(`231113 to do.txt` 기록).

### 3.5 차량 vs 화물차 특성 분석

| 파일 | 역할 | 출력 |
|---|---|---|
| `speedHisto.py` | 차종별 평균속도 히스토그램 (보고서 Fig 11, 12) | `hist/` |
| `spaceHeadway.py` | space headway (`dhw`, m) 차종별 분포 | `headway/b_track*` |
| `timeHeadway.py` | time headway (`dhw` ÷ 평균속도, sec) — 콘솔 출력만 | - |
| `truckRatiobyLane.py` | 차로별 화물차 비율 | `truckRatiobyLane.csv` |
| `countVehicle_inFrame.py` | 프레임별 관측 가능 차량 수 | `countvehicle/track*` |
| `averageVehicleNumPerLane.py` | 15분 환산 방향별 통행량 (보고서 Table 2) | `countVehPer15m/result_*.csv` |

### 3.6 최종 산출물 — Capacity drop 표

```
paperDataExtraction.py  →  cv.toCsv()  →  chart/*.csv
```

Leader vehicle(일반 차량 / 저속 차량)을 지정하고 **15초 Time Window**로
해당 차량 기준 50 / 200 / 350 m 지점의 교통 지표를 측정한다.

`chart/SLOW_total.csv` 컬럼:

```
Track, Lane, Direction, LeaderVehId, isTruck, Distance(m),
AverageTimeHeadway(sec), AverageSpaceHeadway(m), AverageSpeed(km/h), k(veh/hr/lane)
```

`chartmod.py` 는 결과 CSV의 짝수 행만 남기는 후처리 유틸.

### 3.7 유틸리티

| 파일 | 역할 |
|---|---|
| `data extract.py` | recordingMeta 집계 / 속도 min-max 점검 (보고서 Table 1) |
| `read recording meta.py` | track → locationId 출력 (Site 선정 근거) |
| `manipulate_csv.py` | `newData/M*` → 차종별 `C*` / `T*` 분리 |

---

## 4. 폴더 구조

```
src/
├── data/                  원본 highD (손대지 않음)
├── newData/               가공본 M*(전체) C*(승용) T*(화물), 7컬럼 축약
├── cv.py                  ★ 공용 라이브러리
├── paperDataExtraction.py ★ 최종 표 생성 엔트리포인트
├── detectSlowVeh.py       ★ 저속차량 식별 (정의 2) 엔트리포인트
│
├── Trajectory/            시공도 (223개)
├── slowveh/               저속차량 표시 시공도
├── SideSpeed/             저속차량 식별 진단 CSV + 시공도 + 시계열
├── N-curve/               N-curve (149개)
├── sector/                스무딩 N-curve (150개)
├── integral/              Total delay / 누적 delay 그래프
├── flow/                  지점 flow 그래프
├── speed/                 지점별 속도 시계열
├── hist/                  속도 히스토그램 (75개)
├── headway/               headway 분포
├── countvehicle/          프레임별 차량 수
├── countVehPer15m/        15분 환산 통행량 CSV
├── chart/                 ★ 논문 본표 원재료 CSV
├── n/, 기타/              임시 산출물
├── old code/              초기 실험 코드
└── paper/                 보고서 docx, 발표자료, 투고본(hwp), 그림 백업
```

### 작업 기록 문서

- `231113 to do.txt` — **가장 중요한 문서**. 항목별 완료 여부(`[o]/[a]/[-]/[]`)와 **결과물이 어느 폴더에 있는지**가 적혀 있다. 교수님 코멘트 원문 포함.
- `231203 to do.txt` — 후속 작업 목록
- `231210 to do.txt` — 빈 파일 (0 byte)

---

## 5. 재실행 시 주의사항

> 폴더 구조를 중간에 한 번 옮겼기 때문에 **지금 `src/` 에서 그냥 실행하면 상당수가 에러로 죽는다.**

1. **데이터 경로가 두 종류로 섞여 있다.**
   - `'../data/'` 사용: `ncurve.py`, `integral.py`, `accumulateTotalDelay.py`, `smoothing N.py`, `dump_conti.py`, `flow graph.py`, `NewSTD.py`, `colorbar.py`, `drawTrajectory.py`, `truckPoint Trajectory.py`, `averageVehicleNumPerLane.py`, `data extract.py`, `read recording meta.py`, `BACKUP.py`
   - `'data/'` 사용: `detectSlowVeh.py`, `paperDataExtraction.py`, `spaceHeadway.py`, `timeHeadway.py`, `speedHisto.py`, `truckRatiobyLane.py`, `countVehicle_inFrame.py`, `comparewTruck.py`, `manipulate_csv.py`, `cv.py`

   → 전자 그룹은 현재 위치에서 `FileNotFoundError` 가 난다.

2. **존재하지 않는 출력 폴더.** `NewSTD.py`, `colorbar.py`, `drawTrajectory.py`, `dump_conti.py`, `truckPoint Trajectory.py` 는 `newSTD/` 에 저장하려 하지만 그 폴더가 없다(결과물은 `Trajectory/` 로 이동됨). `plt.savefig` 에서 죽는다.

3. **컬럼 인덱스 하드코딩.** `csv` 모듈 기반 스크립트는 전부 `FRAME=0, ID=1, X_POS=2, X_SPD=6, LANE=24`.
   예외: `sectorSpd.py` 는 `X_SPD=4, LANE=6` (7컬럼 가공본용).

4. **방향 전환이 수동 토글이다.** `integral.py`(`xVelocity > 0`, posSpd)와 `accumulateTotalDelay.py`(`xVelocity < 0`, negSpd)는 사실상 같은 코드의 복붙 변종이다.
   코드 안의 `# <><><>` 주석이 "방향을 바꾸려면 이 3곳을 같이 수정하라"는 표시다.

5. **성능.** `detectSlowVeh*` 계열은 매 행마다 `data[data['id'] == p_id]` 전체 스캔을 돌려 **O(N²)** 이다. track 하나가 80 MB라 매우 느리다.
   → highD에 이미 **`precedingXVelocity` 컬럼이 존재**하므로 이 루프 전체를 한 줄로 대체할 수 있다. (`spaceHeadway.py` 의 `drop` 목록에 컬럼명이 보이는데 정작 활용하지 않고 있다.)

---

## 6. 남은 작업

`231113 to do.txt` 기준 미완료 항목:

- [ ] **(7번)** 각 Lane × 3지점(50/200/350 m)의 flow · time headway · 평균속도 · LC 종합표
  → `paperDataExtraction.py` 로 절반쯤 진행. 위 `isTruck` 버그로 비교군이 비어 있음.
- [ ] **(8번)** Leader vehicle(전방 차량 없는 차량) 기준 platoon 분석
  → 후보군 생성 후 "후속 N대 이상" 필터링 필요. 미착수.
- [ ] **(9번)** 저속차량 비율 ↔ delay 발생의 **상관관계 / p-value 검정**
  → 교수님 코멘트 3.3, 4번. 미착수.
- [ ] **저속차량 정의 3** (트럭의 3/6/9초 후행 차량군) 측정. 미착수.
- [ ] `SectionalState.py` 구현 (시간대별 교통상태 FF/BN/BQ/CT 분류)
- [ ] 저속차량 출현 시점·위치 분포 시각화 (`231203 to do.txt` 4번)

---

## 8. 실행 환경

- Python 3.11 (`__pycache__/cv.cpython-311.pyc`)
- 의존성: `pandas`, `numpy`, `matplotlib`, `scipy`, `tqdm`

```bash
pip install pandas numpy matplotlib scipy tqdm
```
