# 사용 Stack
- Python3.*

- pipenv

- FastAPI + Uvicorn



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

(type Enum에 두 종류 [sign_up, find_password])


# 회원 로그인 후 조회 순서
1. POST /user/login/

(type Enum에 세 종류 [ phone_number, email, nickname ])

(식별 가능한 정보: 전화번호, 이메일, 닉네임)

p.s. 이름은 중복이 가능하기에, 식별 불가능한 정보로 간주


# Dependency management

- To install new package to pipenv 

`pipenv install [package]`

- To install packages in pipfile to local (syncing with dependencies in pipfile)

`pipenv sync`

- To spawn a virtualenv in pipenv

`pipenv shell`

#### for the rest... just run `pipenv` on shell to find out.... 

---
