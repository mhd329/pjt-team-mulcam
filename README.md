# 페어 프로젝트 저장소 협업 방법

<br>

- 1번 사람
  1. 깃허브 저장소와 장고 프로젝트를 생성
  2. 깃허브 콜라보레이터로 코딩동료 초대
  3. `.gitignore` 에 가상환경 추가
  4. `pip freeze > requirements.txt` 로 패키지 목록 생성
  5. 생성한 저장소에 장고 프로젝트를 `push`
- 2번 사람
  1. 저장소를 클론
  2. 가상환경 생성과 `pip install -r requirements.txt` 로 패키지 설치
  3. 앱을 생성
  4. 저장소에 앱을 `push`
  5. 1번사람이 `pull`
- 드라이버와 네비게이터 항상 같은 코드를 유지해야 한다.
- 드라이버인 사람이 add commit push
- 네비게이터 pull