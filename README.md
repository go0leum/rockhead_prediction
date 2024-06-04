# rockhead_prediction

### Introduction

지반 정보의 경우, 시추조사와 물리탐사를 병행 수행해 지반의 1차원 또는 2차원 주상 특성을 확인되는 방법이 활용되고 있다.
다만 시추조사의 경우, 한 점의 지반 정보만을 획득 가능하고, 조사에 걸리는 기간이 1달에 달 한다는 문제점이 존재한다. 

## Data

국토지반정보 통합DB센터의 데이터 중 건국대학교 부지 내외 시추공 데이터 91개를 선택하였다.
시추공의 개수가 매우 한정적이므로 공간 보간 기법 중 크리깅을 활용해 데이터 수를 증강하였다.

![input data](https://github.com/go0leum/rockhead_prediction/assets/111696539/e9fdff6f-2072-41ee-938a-406ce915b198)

![input data-kriging](https://github.com/go0leum/rockhead_prediction/assets/111696539/67493edf-11df-4985-830b-3c38e067a0a0)

## Machine Learning

최근 지반 분야에서 액상화 발생 가능성 예측, 지반 특성 예측 등과 같이 지반 분야에 딥러닝 및 머신러닝 기법을 접목하여 결측된 지반 정보를 예측하려는 시도들이 많아졌다. 

---

- 다층 퍼셉트론(MLP)을 기반으로 한 연구, [1] 에서 시추주상도 정보를 학습 데이터로 하여 단위격자별 MLP기반 예측모델적용을 통한 층상구조를 결정하고 이를 가시화하였다. 

- [2]에서 국내 13개터널을 대상으로 11개의 학습 인자(심도, 암종, RQD, 전기비저항, 일축압축강도, 탄성파 P파속도 및 S파 속도, 영률, 단위중량, 포아송비, RMR) 데이터셋을 6개의 머신러닝 알고리즘(Decision Tree , SVM, ANN, PCA & ANN, Random Forest, XGBoost)에 적용하여 각 학습된 모델의 예측 성능을 비교하였다. 
    - SVM모델이 가장 우수한 예측 성능을 보였으며 PCA & ANN, ANN, XGBoost, Random Forest, Decision Tree은 전반적으로 비슷한 성능을 보였다. 

---

위 연구들을 토대로 본 연구에서는 광진구 건국대 주변 시추주상도 정보를 학습데이터로 하여 **Decision Tree**, **XGBoost**, **Random Forest**, **SVM**, **MLP**를 사용하며 각 알고리즘을 앙상블 학습 기법 중 하나인 **Votting** 기법을 이용하여 결과를 종합할 것이다. 

## Result

### accuracy, precision, recall, f1 result

#### 기존 데이터만 학습한 모델
|evaluation metrics|value|
|---|---|
|accuracy|0.9519|
|precision|0.9302|
|recall|0.9524|
|f1 score|0.9412|


#### 크리깅 데이터를 추가하여 학습한 모델
|evaluation metrics|value|
|---|---|
|accuracy|0.9808|
|precision|0.9762|
|recall|0.9762|
|f1 score|0.9762|

### confusion matrix
#### 기존 데이터만 학습한 모델
![eval_1](https://github.com/go0leum/rockhead_prediction/assets/111696539/9eadc94b-ac49-46da-8870-95596227f05b)

#### 크리깅 데이터를 추가하여 학습한 모델
![eval_2](https://github.com/go0leum/rockhead_prediction/assets/111696539/d0819586-9d6b-432e-9cd9-9a0a3af4fedf)

### prediction result
#### 기존 데이터만 학습한 모델
![output](https://github.com/go0leum/rockhead_prediction/assets/111696539/2c338011-0120-4a6e-8dcc-c0bc325a264d)

### 크리깅 데이터를 추가하여 학습한 모델
![output_kriging](https://github.com/go0leum/rockhead_prediction/assets/111696539/de6bb8a3-7b61-4bbd-a13a-cd88d0345d3c)

## references
[1] 지윤수, 김한샘, 이문교, 조형익 and 선창국. (2021). MLP 기반의 서울시 3차원 지반공간모델링 연구. 한국지반공학회논문집, 37(5), 47-63.
[2] 이제겸, 최원혁, 김양균 and 이승원. (2021). 머신러닝 기법을 활용한 터널 설계 시 시추공 내 암반분류에 관한 연구. 한국터널지하공간학회 논문집, 23(6), 469-484.
