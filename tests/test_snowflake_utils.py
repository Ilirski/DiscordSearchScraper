"""Tests for Discord snowflake utility functions."""

import datetime

from scraper import DISCORD_EPOCH, is_snowflake, to_datetime, to_snowflake


class TestToDatetime:
    """Tests for to_datetime function."""

    def test_convert_snowflake_to_datetime(self):
        """Test converting a valid snowflake to datetime."""
        # Discord's first snowflake (2015-01-01T00:00:00.000Z)
        snowflake = str(DISCORD_EPOCH << 22)
        result = to_datetime(snowflake)
        assert isinstance(result, datetime.datetime)
        # Year should be 2015 (may vary by timezone)
        assert result.year >= 2015

    def test_convert_snowflake_with_custom_epoch(self):
        """Test converting snowflake with custom epoch."""
        custom_epoch = 1609459200000  # 2021-01-01
        snowflake = "0"
        result = to_datetime(snowflake, epoch=custom_epoch)
        assert isinstance(result, datetime.datetime)
        assert result.year == 2021

    def test_convert_large_snowflake(self):
        """Test converting a large snowflake (recent timestamp)."""
        # Use a recent snowflake
        snowflake = "1234567890123456789"
        result = to_datetime(snowflake)
        assert isinstance(result, datetime.datetime)
        assert result.year >= 2021


class TestToSnowflake:
    """Tests for to_snowflake function."""

    def test_convert_datetime_to_snowflake(self):
        """Test converting datetime to snowflake."""
        dt = datetime.datetime(2021, 1, 1, 0, 0, 0)
        result = to_snowflake(dt)
        assert isinstance(result, str)
        assert result.isdigit()
        assert len(result) >= 17

    def test_convert_discord_epoch_to_snowflake(self):
        """Test converting Discord epoch to snowflake."""
        dt = datetime.datetime(2015, 1, 1, 0, 0, 0)
        result = to_snowflake(dt)
        # Should be close to zero (offset by Discord epoch)
        snowflake_int = int(result)
        # Allow for timezone differences
        assert snowflake_int < 1000000


class TestIsSnowflake:
    """Tests for is_snowflake function."""

    def test_valid_snowflake(self):
        """Test checking valid snowflakes."""
        # Valid snowflakes (17-19 digits)
        assert is_snowflake("12345678901234567") is True
        assert is_snowflake("123456789012345678") is True
        assert is_snowflake("1234567890123456789") is True

    def test_invalid_snowflake_too_short(self):
        """Test snowflake that's too short."""
        assert is_snowflake("1234567890123456") is False

    def test_invalid_snowflake_too_long(self):
        """Test snowflake that's too long."""
        assert is_snowflake("12345678901234567890") is False

    def test_invalid_snowflake_with_letters(self):
        """Test snowflake with non-numeric characters."""
        assert is_snowflake("1234567890123456a") is False
        assert is_snowflake("abcd12345678901234") is False

    def test_invalid_snowflake_empty(self):
        """Test empty string."""
        assert is_snowflake("") is False

    def test_invalid_snowflake_with_special_chars(self):
        """Test snowflake with special characters."""
        assert is_snowflake("12345678901234567!") is False
        assert is_snowflake("123-45678901234567") is False
