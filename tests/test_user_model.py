import pytest

from weather_app.models.user_model import User


@pytest.fixture
def sample_usename():
    return "poopoo"
@pytest.fixture
def sample_password():
    return "passwordmane"

##########################################################
# User Creation
##########################################################

def test_create_user(sample_user, sample_password):
    """Test creating a new user with a unique username."""
    User.create_user(sample_user,sample_password)

def test_create_duplicate_user(sample_usename, sample_password):
    """Test attempting to create a user with a duplicate username."""
    User.create_user(sample_usename,sample_password)

##########################################################
# User Authentication
##########################################################

def test_check_password(sample_usename, sample_password):
    """Test attempting to create a user with a duplicate username."""
    return User.check_password(sample_usename,sample_password)
def test_get_id_by_username(sample_usename):
    return User.get_id_by_username(sample_usename)
def test_update_password(sample_usename,sample_password,samplenew):
    User.update_password(sample_usename,sample_password,samplenew)

#test_create_user("Hello","testing123")

test_check_password("Hello","testing123")

test_get_id_by_username("Hello")

test_update_password("Hello","testing123","Poopatron")


