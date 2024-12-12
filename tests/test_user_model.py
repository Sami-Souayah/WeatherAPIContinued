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

test_create_user("Hello","testing123")

test_create_duplicate_user("Hello","testing123")