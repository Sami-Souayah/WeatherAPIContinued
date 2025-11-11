import pytest

from weather_app.models.user_model import User
from db.db_connection import get_database
import os
import hashlib



@pytest.fixture
def user():
    return User()

@pytest.fixture
def sample_username():
    return "poopoo"
@pytest.fixture
def sample_password():
    return "passwordmane"

@pytest.fixture
def dbms():
    dbname = get_database()
    dbname = dbname["Users"]
    return dbname

@pytest.fixture
def samplenew():
    return "newpass"




##########################################################
# User Creation
##########################################################

def test_create_user(sample_username, sample_password, user, dbms):
    """Test creating a new user with a unique username."""
    try:
        user.create_user(sample_username,sample_password)
        assert dbms.find_one({"Username": sample_username})["Username"]==sample_username
    finally:
        user.delete_user(sample_username)

def test_create_duplicate_user(sample_username, sample_password, user, dbms):
    """Test attempting to create a user with a duplicate username."""
    try:
        user.create_user(sample_username,sample_password)
        with pytest.raises(ValueError, match="already exists"):
            user.create_user(sample_username, sample_password)        
    finally:
        user.delete_user(sample_username)
    


##########################################################
# User Authentication
##########################################################

def test_check_password(sample_username, sample_password, user):
    """Test attempting to create a user with a duplicate username."""
    try:
        user.create_user(sample_username, sample_password)
        assert user.check_password(sample_username, sample_password)==True
    finally:
        user.delete_user(sample_username)

def test_get_id_by_username(sample_username, sample_password, dbms, user):
    try:
        user.create_user(sample_username, sample_password)
        assert user.get_id_by_username(sample_username)==dbms.find_one({"Username": sample_username})["_id"]
    finally:
        user.delete_user(sample_username)
    

def test_update_password(sample_username,sample_password,user, samplenew):
    try:
        user.create_user(sample_username,sample_password)
        user.update_password(sample_username,samplenew)
        assert user.check_password(sample_username, samplenew)==True
    finally:
        user.delete_user(sample_username)





