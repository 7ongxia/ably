import email
from fastapi import FastAPI, HTTPException
from models import UserBase, UserLogin, UserLoginType, UserIn, UserOut, UserInDB, Verification, VerificationInDB, VerificationType
from random import randint
from typing import List
import bcrypt

app = FastAPI()

db: List[UserBase] = []
sms_db: List[Verification] = []


def generate_verification_code(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


@app.post("/verification/", response_model=VerificationInDB)
async def verify_phone(verification: Verification):
    for sms in sms_db:
        if sms.phone_number == verification.phone_number:
            sms_db.remove(sms)

    sms = VerificationInDB(**verification.dict(), verification_code=generate_verification_code(6))
    sms_db.append(sms)
    return sms


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn, verification_code: int):
    if not sms_db:
        raise HTTPException(
            status_code=422,
            detail=f"Please enter a valid Verification code",
        )
    for sms in sms_db:
        if sms.type == VerificationType.sign_up and sms.phone_number == user_in.phone_number and sms.verification_code == verification_code:
            sms_db.remove(sms)
        else:
            raise HTTPException(
                status_code=422,
                detail=f"Please enter a valid Verification code",
            )
    
    for user in db:
        if user.phone_number == user_in.phone_number:
            raise HTTPException(
                status_code=422,
                detail=f"User with {user.phone_number} exists",
            )
        elif user.email == user_in.email:
            raise HTTPException(
                status_code=422,
                detail=f"User with {user.email} exists",
            )
        elif user.nickname == user_in.nickname:
            raise HTTPException(
                status_code=422,
                detail=f"User with {user.nickname} exists",
            )

    hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), bcrypt.gensalt())
    user_saved = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    db.append(user_saved)
    return user_saved


@app.post("/user/password/", response_model=UserOut)
async def change_user_password(phone_number: str, verification_code: int, new_password: str):
    if not sms_db:
        raise HTTPException(
            status_code=422,
            detail=f"Please enter a valid Verification code",
        )
    for sms in sms_db:
        if sms.type == VerificationType.find_password and sms.phone_number == phone_number and sms.verification_code == verification_code:
            sms_db.remove(sms)
        else:
            raise HTTPException(
                status_code=422,
                detail=f"Please enter a valid Verification code",
            )
    
    user_out = None
    for user in db:
        if user.phone_number == phone_number:
            user.hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user_out = user
    
    return user_out


@app.post("/user/login", response_model=UserOut)
async def get_user(user_in: UserLogin):
    for user in db:
        if user.password == user_in.password:
            if user_in.type == UserLoginType.phone_number:
                if user.phone_number == user_in.identification_info:
                    return user
            elif user_in.type == UserLoginType.email:
                if user.email == user_in.identification_info:
                    return user
            elif user_in.type == UserLoginType.nickname:
                if user.nickname == user_in.identification_info:
                    return user
        else:
            raise HTTPException(
                status_code=422,
                detail=f"Password is wrong",
            )