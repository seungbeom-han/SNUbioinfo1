# 생물정보학실습1 term project: LIN28A binding과 base pairing
## 1. Base pairing에 따른 LIN28A binding strength
Entropy를 기반으로 GRCm39 유전체에서 LIN28A가 결합할 것으로 예상되는 위치를 고른 다음 그 주변 -10부터 +10까지 구간을 고르고, GC ratio, reverse complement sequence와 이루는 local alignment 점수 등을 구하여 Watson-Crick base pairing이 얼마나 잘 나타날 지 계산한다. 이렇게 구한 base pairing의 stability가 hexamer motif의 서열, CLIP-seq signal의 크기 등과 어떤 관련성이 있는지 조사한다. 이렇게 base pairing과 LIN28A binding strength 사이 관련성을 알면 sequence motif를 찾는 모델을 만드는 데 도움이 될 것이다.

## 2. 서로 가까운 LIN28A binding site의 간섭 효과
Watson-Crick base pairing이 뚜렷하게 나타난 binding site 중 서로 가까운 위치(6bp 이내)에 있는 LIN28A binding site를 포함하는 유전자를 골라 문헌 조사, LIN28A binding site가 서로 멀리 떨어진 gene과 비교 등을 수행하여 binding site가 서로 간섭할 가능성이 있는지 알아본다. 