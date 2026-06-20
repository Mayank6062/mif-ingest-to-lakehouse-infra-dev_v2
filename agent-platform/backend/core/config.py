"""
Application configuration module.

Frozen Architecture Reference: STEP-4, STEP-11.2, STEP-11.3
Implements environment-based settings with Pydantic v2.
"""
from enum import Enum
from typing import Optional

from pydantic import ConfigDict, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Allowed environments per STEP-4."""
    LOCAL = "local"
    DEV = "dev"
    QA = "qa"
    UAT = "uat"
    PROD = "prod"


class Settings(BaseSettings):
    """
    Application configuration.
    
    Loads from environment variables with validation.
    Per STEP-4: Configuration must support all environments.
    Per STEP-11.2: Secrets must be abstracted.
    Per STEP-11.3: Security settings must be enforced.
    """
    
    # ============================================
    # ENVIRONMENT & BASE
    # ============================================
    ENVIRONMENT: Environment = Field(
        default=Environment.LOCAL,
        description="Execution environment"
    )
    DEBUG: bool = Field(
        default=False,
        description="Enable debug mode (only local/dev)"
    )
    
    # ============================================
    # APPLICATION IDENTITY
    # ============================================
    APP_NAME: str = Field(
        default="agent-platform",
        description="Application name"
    )
    APP_VERSION: str = Field(
        default="0.1.0",
        description="Application version"
    )
    SECRET_KEY: SecretStr = Field(
        min_length=32,
        description="Secret key for session signing (≥32 chars per STEP-11.2)"
    )
    
    # ============================================
    # DATABASE (Per STEP-10)
    # ============================================
    DATABASE_URL: str = Field(
        default="postgresql://localhost:5432/agent_db",
        description="PostgreSQL connection URL"
    )
    DATABASE_POOL_SIZE: int = Field(
        default=20,
        description="Connection pool size"
    )
    DATABASE_MAX_OVERFLOW: int = Field(
        default=10,
        description="Max overflow connections"
    )
    DATABASE_POOL_TIMEOUT: int = Field(
        default=30,
        description="Pool timeout in seconds"
    )
    
    # ============================================
    # REDIS (Per STEP-11.2)
    # ============================================
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    REDIS_SENTINEL_ENABLED: bool = Field(
        default=False,
        description="Enable Sentinel HA mode (STEP-11.2)"
    )
    REDIS_SENTINEL_MASTER_NAME: Optional[str] = Field(
        default=None,
        description="Sentinel master name if HA enabled"
    )
    
    # ============================================
    # GITHUB OAUTH (Per STEP-2)
    # ============================================
    GITHUB_CLIENT_ID: str = Field(
        description="GitHub OAuth app client ID"
    )
    GITHUB_CLIENT_SECRET: SecretStr = Field(
        description="GitHub OAuth app client secret"
    )
    GITHUB_REDIRECT_URI: str = Field(
        description="GitHub OAuth redirect URI"
    )
    GITHUB_API_URL: str = Field(
        default="https://api.github.com",
        description="GitHub API base URL"
    )
    GITHUB_OAUTH_AUTHORIZE_URL: str = Field(
        default="https://github.com/login/oauth/authorize",
        description="GitHub OAuth authorize URL"
    )
    GITHUB_OAUTH_TOKEN_URL: str = Field(
        default="https://github.com/login/oauth/access_token",
        description="GitHub OAuth token URL"
    )
    
    # ============================================
    # SESSION (Per STEP-3, STEP-5.1)
    # ============================================
    SESSION_TIMEOUT_SECONDS: int = Field(
        default=3600,
        description="Session timeout in seconds (1 hour default)"
    )
    SESSION_REFRESH_THRESHOLD_SECONDS: int = Field(
        default=300,
        description="Refresh session if <5 mins remaining"
    )
    
    # ============================================
    # SECURITY & TOKENS (Per STEP-11.2, STEP-11.3)
    # ============================================
    CORS_ORIGINS: list = Field(
        default=["http://localhost:5173"],
        description="CORS allowed origins"
    )
    CORS_CREDENTIALS: bool = Field(
        default=True,
        description="Allow credentials in CORS"
    )
    CORS_METHODS: list = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Allowed CORS methods"
    )
    CORS_HEADERS: list = Field(
        default=["*"],
        description="Allowed CORS headers"
    )
    
    # Token settings per STEP-11.2
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
        description="Access token lifetime in minutes"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token lifetime in days"
    )
    
    # ============================================
    # SECRETS MANAGER (Per STEP-11.2)
    # ============================================
    SECRETS_MANAGER: str = Field(
        default="env",
        description="Secrets manager backend: env|vault|azure|aws"
    )
    VAULT_ADDR: Optional[str] = Field(
        default=None,
        description="Vault server address (if SECRETS_MANAGER=vault)"
    )
    VAULT_TOKEN: Optional[SecretStr] = Field(
        default=None,
        description="Vault authentication token"
    )
    AWS_REGION: Optional[str] = Field(
        default=None,
        description="AWS region for Secrets Manager (if SECRETS_MANAGER=aws)"
    )
    AZURE_KEYVAULT_URL: Optional[str] = Field(
        default=None,
        description="Azure Key Vault URL (if SECRETS_MANAGER=azure)"
    )
    
    # ============================================
    # LOGGING (Per STEP-11.2)
    # ============================================
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level"
    )
    LOG_FORMAT: str = Field(
        default="json",
        description="Log format: json|text"
    )
    LOG_FILE: Optional[str] = Field(
        default=None,
        description="Log file path (optional)"
    )
    
    # ============================================
    # OBSERVABILITY (Per STEP-11.2)
    # ============================================
    OTEL_ENABLED: bool = Field(
        default=False,
        description="Enable OpenTelemetry"
    )
    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[str] = Field(
        default=None,
        description="OTEL collector endpoint"
    )
    
    # ============================================
    # AUDIT & RBAC (Per STEP-11.3)
    # ============================================
    AUDIT_ENABLED: bool = Field(
        default=True,
        description="Enable audit trail logging"
    )
    AUDIT_RETENTION_DAYS_HOT: int = Field(
        default=365,
        description="Hot retention in days (per STEP-11.3)"
    )
    AUDIT_RETENTION_DAYS_COLD: int = Field(
        default=2555,
        description="Cold retention in days (7 years per STEP-11.3)"
    )
    RBAC_ENABLED: bool = Field(
        default=True,
        description="Enable RBAC enforcement"
    )
    
    # ============================================
    # API & PERFORMANCE
    # ============================================
    API_V1_PREFIX: str = Field(
        default="/api/v1",
        description="API v1 prefix"
    )
    REQUEST_TIMEOUT_SECONDS: int = Field(
        default=30,
        description="Request timeout in seconds"
    )
    MAX_BODY_SIZE_MB: int = Field(
        default=10,
        description="Max request body size in MB"
    )
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @field_validator("ENVIRONMENT", mode="before")
    @classmethod
    def validate_environment(cls, v):
        """Validate environment value."""
        if isinstance(v, str):
            v = v.lower()
        return v
    
    @field_validator("DEBUG", mode="before")
    @classmethod
    def validate_debug(cls, v):
        """Convert string boolean to actual boolean."""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return v
    
    @field_validator("DEBUG")
    @classmethod
    def debug_only_for_non_prod(cls, v, info):
        """Enforce DEBUG only for local/dev environments."""
        if v and info.data.get("ENVIRONMENT") in (Environment.PROD, Environment.UAT):
            raise ValueError("DEBUG must be False for PROD/UAT environments")
        return v
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def validate_cors_origins(cls, v, info):
        """Validate CORS origins based on environment."""
        env = info.data.get("ENVIRONMENT", Environment.LOCAL)
        if env == Environment.PROD and "*" in v:
            raise ValueError("CORS_ORIGINS cannot contain '*' in PROD")
        return v


def get_settings() -> Settings:
    """
    Get application settings.
    
    Returns:
        Settings instance with validated configuration.
    
    Raises:
        ValidationError: If required settings are missing or invalid.
    
    Per STEP-4: Configuration must validate on startup.
    """
    return Settings()


# Frozen singleton for convenience
settings: Optional[Settings] = None


def load_settings() -> Settings:
    """Load and cache settings (frozen per STEP-4)."""
    global settings
    if settings is None:
        settings = get_settings()
    return settings
