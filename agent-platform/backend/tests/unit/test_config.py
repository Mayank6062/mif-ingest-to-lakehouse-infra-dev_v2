"""
Unit tests for configuration module.

Frozen Architecture Reference: STEP-4, STEP-11.2, STEP-11.3
Tests configuration validation and environment-based settings.
"""
import os
import pytest
from pydantic import ValidationError

from backend.core.config import Environment, Settings, get_settings, load_settings


class TestEnvironmentEnum:
    """Test Environment enum values."""
    
    def test_valid_environments(self):
        """Verify all valid environments are defined."""
        assert Environment.LOCAL.value == "local"
        assert Environment.DEV.value == "dev"
        assert Environment.QA.value == "qa"
        assert Environment.UAT.value == "uat"
        assert Environment.PROD.value == "prod"


class TestSettingsValidation:
    """Test Settings validation per STEP-4."""
    
    def test_settings_load_with_valid_env(self, monkeypatch):
        """Test settings load with valid environment variables."""
        # Set required environment variables
        monkeypatch.setenv("ENVIRONMENT", "local")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-client-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-client-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings = get_settings()
        assert settings.ENVIRONMENT == Environment.LOCAL
        assert settings.APP_NAME == "agent-platform"
        assert settings.SECRET_KEY.get_secret_value() == "test-secret-key-minimum-32-characters-long-1234"
    
    def test_settings_missing_required_field(self, monkeypatch):
        """Test that settings validation fails without required fields."""
        monkeypatch.setenv("ENVIRONMENT", "local")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        # Intentionally don't set GITHUB_CLIENT_ID
        
        with pytest.raises(ValidationError) as exc_info:
            get_settings()
        
        # Verify error mentions the missing field
        assert "GITHUB_CLIENT_ID" in str(exc_info.value)
    
    def test_secret_key_minimum_length(self, monkeypatch):
        """Test SECRET_KEY must be at least 32 characters per STEP-11.2."""
        monkeypatch.setenv("ENVIRONMENT", "local")
        monkeypatch.setenv("SECRET_KEY", "short-key")  # < 32 chars
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        with pytest.raises(ValidationError) as exc_info:
            get_settings()
        
        assert "32" in str(exc_info.value)


class TestDebugEnforcement:
    """Test DEBUG flag enforcement per STEP-11.3."""
    
    def test_debug_allowed_in_local(self, monkeypatch):
        """Test DEBUG can be True in LOCAL environment."""
        monkeypatch.setenv("ENVIRONMENT", "local")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings = get_settings()
        assert settings.DEBUG is True
    
    def test_debug_allowed_in_dev(self, monkeypatch):
        """Test DEBUG can be True in DEV environment."""
        monkeypatch.setenv("ENVIRONMENT", "dev")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings = get_settings()
        assert settings.DEBUG is True
    
    def test_debug_forbidden_in_prod(self, monkeypatch):
        """Test DEBUG must be False in PROD per STEP-11.3."""
        monkeypatch.setenv("ENVIRONMENT", "prod")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        with pytest.raises(ValidationError) as exc_info:
            get_settings()
        
        assert "DEBUG" in str(exc_info.value)
    
    def test_debug_forbidden_in_uat(self, monkeypatch):
        """Test DEBUG must be False in UAT per STEP-11.3."""
        monkeypatch.setenv("ENVIRONMENT", "uat")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        with pytest.raises(ValidationError) as exc_info:
            get_settings()
        
        assert "DEBUG" in str(exc_info.value)


class TestCORSValidation:
    """Test CORS configuration per STEP-11.3."""
    
    def test_cors_wildcard_allowed_in_dev(self, monkeypatch):
        """Test CORS wildcard '*' allowed in DEV."""
        monkeypatch.setenv("ENVIRONMENT", "dev")
        monkeypatch.setenv("CORS_ORIGINS", '["*"]')
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings = get_settings()
        assert "*" in settings.CORS_ORIGINS
    
    def test_cors_wildcard_forbidden_in_prod(self, monkeypatch):
        """Test CORS wildcard '*' forbidden in PROD per STEP-11.3."""
        monkeypatch.setenv("ENVIRONMENT", "prod")
        monkeypatch.setenv("CORS_ORIGINS", '["*"]')
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        with pytest.raises(ValidationError) as exc_info:
            get_settings()
        
        assert "CORS" in str(exc_info.value)


class TestDatabaseConfiguration:
    """Test database configuration per STEP-10."""
    
    def test_database_url_default(self, monkeypatch):
        """Test DATABASE_URL has sensible default."""
        monkeypatch.setenv("ENVIRONMENT", "local")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings = get_settings()
        assert settings.DATABASE_URL == "postgresql://localhost:5432/agent_db"
        assert settings.DATABASE_POOL_SIZE == 20


class TestRedisConfiguration:
    """Test Redis configuration per STEP-11.2."""
    
    def test_redis_url_default(self, monkeypatch):
        """Test REDIS_URL has sensible default."""
        monkeypatch.setenv("ENVIRONMENT", "local")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings = get_settings()
        assert settings.REDIS_URL == "redis://localhost:6379/0"
    
    def test_redis_sentinel_configuration(self, monkeypatch):
        """Test Redis Sentinel HA configuration per STEP-11.2."""
        monkeypatch.setenv("ENVIRONMENT", "prod")
        monkeypatch.setenv("DEBUG", "false")
        monkeypatch.setenv("REDIS_SENTINEL_ENABLED", "true")
        monkeypatch.setenv("REDIS_SENTINEL_MASTER_NAME", "mymaster")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings = get_settings()
        assert settings.REDIS_SENTINEL_ENABLED is True
        assert settings.REDIS_SENTINEL_MASTER_NAME == "mymaster"


class TestGitHubOAuthConfiguration:
    """Test GitHub OAuth configuration per STEP-2."""
    
    def test_github_oauth_credentials_required(self, monkeypatch):
        """Test GitHub OAuth credentials are required."""
        monkeypatch.setenv("ENVIRONMENT", "local")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        # GitHub credentials intentionally missing
        
        with pytest.raises(ValidationError) as exc_info:
            get_settings()
        
        error_str = str(exc_info.value)
        assert "GITHUB_CLIENT_ID" in error_str or "GITHUB_CLIENT_SECRET" in error_str
    
    def test_github_oauth_urls_have_defaults(self, monkeypatch):
        """Test GitHub OAuth URLs have defaults per STEP-2."""
        monkeypatch.setenv("ENVIRONMENT", "local")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings = get_settings()
        assert settings.GITHUB_API_URL == "https://api.github.com"
        assert settings.GITHUB_OAUTH_AUTHORIZE_URL == "https://github.com/login/oauth/authorize"
        assert settings.GITHUB_OAUTH_TOKEN_URL == "https://github.com/login/oauth/access_token"


class TestSessionConfiguration:
    """Test session configuration per STEP-3, STEP-5.1."""
    
    def test_session_timeout_default(self, monkeypatch):
        """Test SESSION_TIMEOUT_SECONDS has default (1 hour)."""
        monkeypatch.setenv("ENVIRONMENT", "local")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings = get_settings()
        assert settings.SESSION_TIMEOUT_SECONDS == 3600  # 1 hour


class TestAuditConfiguration:
    """Test audit configuration per STEP-11.3."""
    
    def test_audit_retention_policy(self, monkeypatch):
        """Test audit retention policy per STEP-11.3."""
        monkeypatch.setenv("ENVIRONMENT", "prod")
        monkeypatch.setenv("DEBUG", "false")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings = get_settings()
        assert settings.AUDIT_RETENTION_DAYS_HOT == 365  # 1 year hot
        assert settings.AUDIT_RETENTION_DAYS_COLD == 2555  # 7 years cold


class TestSettingsSingleton:
    """Test settings singleton loading per STEP-4."""
    
    def test_load_settings_returns_singleton(self, monkeypatch):
        """Test load_settings returns cached instance."""
        monkeypatch.setenv("ENVIRONMENT", "local")
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-minimum-32-characters-long-1234")
        monkeypatch.setenv("GITHUB_CLIENT_ID", "test-id")
        monkeypatch.setenv("GITHUB_CLIENT_SECRET", "test-secret")
        monkeypatch.setenv("GITHUB_REDIRECT_URI", "http://localhost:5173/callback")
        
        settings1 = load_settings()
        settings2 = load_settings()
        
        # Should return same instance
        assert settings1 is settings2
