"""Tests for JWT utility functions"""
import pytest
from datetime import datetime, timedelta
import jwt
from api.app.utils.jwt_utils import (
    create_access_token,
    decode_access_token,
    SECRET_KEY,
    ALGORITHM,
)


class TestJWTUtils:
    """Test suite for JWT utility functions"""

    def test_create_access_token_with_default_expiry(self):
        """Test creating an access token with default expiry"""
        data = {"sub": "test_user", "user_id": 1}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token can be decoded
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "test_user"
        assert decoded["user_id"] == 1
        assert "exp" in decoded

    def test_create_access_token_with_custom_expiry(self):
        """Test creating an access token with custom expiry"""
        data = {"sub": "test_user", "user_id": 1}
        expires_delta = timedelta(hours=2)
        token = create_access_token(data, expires_delta=expires_delta)
        
        assert isinstance(token, str)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "test_user"
        assert decoded["user_id"] == 1

    def test_create_access_token_with_empty_data(self):
        """Test creating an access token with empty data dict"""
        data = {}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "exp" in decoded

    def test_create_access_token_with_complex_data(self):
        """Test creating an access token with complex nested data"""
        data = {
            "sub": "test_user",
            "user_id": 1,
            "roles": ["admin", "user"],
            "metadata": {"email": "test@example.com"}
        }
        token = create_access_token(data)
        
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded["sub"] == "test_user"
        assert decoded["user_id"] == 1
        assert decoded["roles"] == ["admin", "user"]
        assert decoded["metadata"]["email"] == "test@example.com"

    def test_decode_access_token_valid(self):
        """Test decoding a valid access token"""
        data = {"sub": "test_user", "user_id": 1}
        token = create_access_token(data)
        
        decoded = decode_access_token(token)
        
        assert decoded is not None
        assert decoded["sub"] == "test_user"
        assert decoded["user_id"] == 1

    def test_decode_access_token_expired(self):
        """Test decoding an expired token"""
        data = {"sub": "test_user", "user_id": 1}
        # Create token that expires immediately
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta=expires_delta)
        
        decoded = decode_access_token(token)
        
        assert decoded is None

    def test_decode_access_token_invalid(self):
        """Test decoding an invalid token"""
        invalid_token = "invalid.token.string"
        decoded = decode_access_token(invalid_token)
        
        assert decoded is None

    def test_decode_access_token_tampered(self):
        """Test decoding a tampered token"""
        data = {"sub": "test_user", "user_id": 1}
        token = create_access_token(data)
        
        # Tamper with the token
        tampered_token = token[:-5] + "xxxxx"
        decoded = decode_access_token(tampered_token)
        
        assert decoded is None

    def test_decode_access_token_missing_exp(self):
        """Test decoding token without exp claim still works"""
        data = {"sub": "test_user", "user_id": 1}
        # Create a JWT directly without exp claim
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        
        # Should still decode successfully even without exp
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["sub"] == "test_user"

    def test_create_and_decode_roundtrip(self):
        """Test creating and decoding token roundtrip"""
        original_data = {
            "sub": "user123",
            "user_id": 42,
            "email": "user@example.com",
            "is_active": True
        }
        
        token = create_access_token(original_data)
        decoded = decode_access_token(token)
        
        assert decoded is not None
        assert decoded["sub"] == original_data["sub"]
        assert decoded["user_id"] == original_data["user_id"]
        assert decoded["email"] == original_data["email"]
        assert decoded["is_active"] == original_data["is_active"]

    def test_decode_with_wrong_secret_key(self):
        """Test that token decoded with wrong secret fails"""
        data = {"sub": "test_user", "user_id": 1}
        token = create_access_token(data)
        
        # Try to decode with wrong secret
        with pytest.raises(jwt.InvalidTokenError):
            jwt.decode(token, "wrong-secret-key", algorithms=[ALGORITHM])

    def test_decode_with_wrong_algorithm(self):
        """Test that token decoded with wrong algorithm fails"""
        data = {"sub": "test_user", "user_id": 1}
        token = create_access_token(data)
        
        # Try to decode with wrong algorithm
        with pytest.raises(jwt.InvalidTokenError):
            jwt.decode(token, SECRET_KEY, algorithms=["HS512"])

    def test_token_contains_all_required_claims(self):
        """Test that generated token contains all required claims"""
        data = {"sub": "test_user", "user_id": 1}
        token = create_access_token(data)
        
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Should have both original data and exp claim
        assert "sub" in decoded
        assert "user_id" in decoded
        assert "exp" in decoded
        assert decoded["sub"] == "test_user"
        assert decoded["user_id"] == 1
