# 화재 탐지 Segmentation

<a href="https://www.youtube.com/embed/d2gssF8AygE"><p align = "center"><img src = "./result/youtube.PNG"></a>

[영상 출처](https://m.facebook.com/%ED%95%B4%EB%82%A8%EC%86%8C%EB%B0%A9%EC%84%9C-245731289699385/videos/%EC%9E%84%EC%95%BC%ED%99%94%EC%9E%AC-%EC%9E%AC%ED%98%84-%EC%8B%A4%ED%97%982020317/504090356931158/)

Depth : 5, Initial Feature : 32 에서의 실험 영상

|Depth|Initial Feature|mIoU|FPS|
|------|---|---|---|
|5|32|64.2%|7.63|
|4|32|62.1%|8.23|
|5|16|63.3%|9.12|
|4|16|60.1%|10.09|
|4|8|57.4%|12.32|
|3|16|53.9%|13.78|

## 결과

검은색 빨간색 파란색 회색 흰색 은 각각
배경,불,검은 연기,회색 연기,흰색 연기를 의미합니다.

### Test
좌:Input 중:Mask 우:Mix(Input+Mask)
<p align = "center"><img src="./result/test/1.jpg"></p>
<p align = "center"><img src="./result/test/2.jpg"></p>
<p align = "center"><img src="./result/test/3.jpg"></p>
<p align = "center"><img src="./result/test/4.jpg"></p>
### Train
<p align = "center"><img src="./result/train/1.jpg"></p>
<p align = "center"><img src="./result/train/2.jpg"></p>
<p align = "center"><img src="./result/train/3.jpg"></p>
