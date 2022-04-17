# 조건
Python3.*
pipenv


# Local에서 서버 돌리는 법
Project Root dir에서
1. `pipenv sync`
2. `pipenv shell`
3. `uvicorn app.main:app --reload`
4. `http://localhost:8000/docs#/` 접속

Enum같은 경우는, Swagger에서 Request Body -> Schema 선택하시면 옵션 확인 가능합니다.


# 회원가입 순서
1. POST /verification/
2. POST /user/


# 비밀번호 변경 순서
1. POST /verification/
2. POST /user/password/


# 회원 로그인 후 조회 순서
1. POST /user/login/


# Dependency management

- To install new package to pipenv 

`pipenv install [package]`

- To install packages in pipfile to local (syncing with dependencies in pipfile)

`pipenv sync`

- To spawn a virtualenv in pipenv

`pipenv shell`

#### for the rest... just run `pipenv` on shell to find out.... 

---