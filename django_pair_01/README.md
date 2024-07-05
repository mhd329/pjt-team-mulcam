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

<br>

---

###### 저장소 복사 하는방법

- 그냥 `clone`
  - 그냥 클론 한 다음에 기존 `init` 지우고 자신의 `init` 으로 바꾸기
  - 대신 커밋 내역이 없어진다.
- `mirror`
  - `git clone --mirror [받아올 원본 repo 주소]`
  - 클론하고 그 폴더로 들어가기
  - `git remote set-url --push origin [내가 새로 만든 저장소 주소]`
  - `git push --mirror`

---

<br>