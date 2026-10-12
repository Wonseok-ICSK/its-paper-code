# 시간에 따른 상류부(V_u), 하류부 통행속도(V_d), 구간 평균 통행 속도(V 파악 
# 이후, 시간대 별 교통 상태(Sectional state (State))를 4개로 분류: 원활(FF), 병목(BN), 정체(CT), 완화(BQ) 상태 
# FF: V_u>V_threshold, V_d>V_threshold (e.g. V_threshold=80km/h)
# BN: V_u<V_d, V_u≤V_threshold
# BQ: V_u>V_d, V_d≤V_threshold
# CT: V_u<V_threshold, V_d<V_threshold 
