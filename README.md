# 페어 프로그래밍

# 주요 기능

## 1. 회원가입 및 로그인

### App name: accounts

`signup`

- UserCreationForm을 사용하여 CustomUserCreationForm을 작성하도록 구현.
  - username, last_name, first_name, email, password

`login`

- AuthenticationForm을 사용.
- logout 기능 내포

`profile`

- 사용자 정보 표시
  - fullname, username, email, 가입일
  - Follow 및 Follower 수
  - 사용자가 작성한 게시글 및 댓글

`update`

- CustomUserChangeForm으로 수정할 수 있도록 구현.
- update_session_auth_hash을 사용하여 세션 유지 가능.

* 사용자 정보 수정
  - username, first name, last name, email
  - Password 수정

`user-list`

- 회원 목록 출력
- 회원 아이디 클릭 시 사용자 정보 페이지로 이동

`follow`

- ManyToManyField를 사용하여 사용자끼리 팔로우 및 팔로우 취소할 수 있도록 구현.
- 사용자의 팔로우 및 팔로잉 수를 profile 페이지에 표시.

`search`

- 사용자 username 및 full name 검색이 가능하도록 구현.

<br>

## 2. 게시글

### App name: articles

`reviews`

- 사용자가 작성한 글 목록을 구현.
  - 댓글 수 및 좋아요 수
  - username

`create`

- ArticleForm을 사용하여 게시글 생성 기능을 구현.

  - title, content, movie_name, grade, image, thumbnail

`update`

- ArticleForm을 통헤 기존 글을 불러와 수정할 수 있도록 구현.

`delete`

- 게시글 삭제 기능 구현.

`like`

- `like_users.filter`를 통해 해당 게시글의 좋아요 및 좋아요 취소 기능을 구현함

`comment`

- CommentForm을 통하여 해당 게시글의 댓글 및 댓글 삭제 기능을 구현

`search`

- 게시글의 title 및 content 검색이 가능하도록 구현.
