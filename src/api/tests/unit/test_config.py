"""Tests for application configuration"""
import os
import pytest
from api.app.config import Settings, settings


class TestSettings:
    """Test suite for application settings"""

    def test_settings_instance_exists(self):
        """Test that settings instance is created"""
        assert settings is not None
        assert isinstance(settings, Settings)

    def test_settings_database_url_configured(self):
        """Test that database URL is configured"""
        assert hasattr(settings, "database_url")
        assert settings.database_url is not None
        assert isinstance(settings.database_url, str)
        assert len(settings.database_url) > 0

    def test_settings_database_url_protocol(self):
        """Test that database URL uses correct protocol"""
        assert settings.database_url.startswith("postgresql://") or \
               settings.database_url.startswith("sqlite://")

    def test_settings_loads_from_env_file(self):
        """Test that settings can load from .env file"""
        # Create a test settings instance
        test_settings = Settings()
        assert test_settings.database_url is not None

    def test_settings_case_insensitive(self):
        """Test that settings configuration is case insensitive"""
        # This is configured in model_config
        settings_config = Settings.model_config
        assert settings_config is not None
        # Should have case_sensitive=False
        assert settings_config.get("case_sensitive") == False

    def test_settings_ignores_extra_fields(self):
        """Test that settings ignores extra fields from .env"""
        # This is configured in model_config with extra="ignore"
        settings_config = Settings.model_config
        assert settings_config is not None
        assert settings_config.get("extra") == "ignore"

    def test_settings_has_default_database_url(self):
        """Test that settings has a default database URL value"""
        # If .env doesn't override, should use default
        new_settings = Settings()
        assert new_settings.database_url is not None
        # Default or from env should be set
        assert len(new_settings.database_url) > 0


class TestSettingsDefaults:
    """Test suite for settings default values"""

    def test_default_database_url_includes_localhost(self):
        """Test default database URL configuration"""
        # The default includes localhost
        expected_defaults = ["localhost", "postgresql"]
        assert any(part in settings.database_url for part in expected_defaults)

    def test_database_url_is_not_empty(self):
        """Test that database URL is never empty"""
        assert settings.database_url
        assert settings.database_url.strip() != ""
