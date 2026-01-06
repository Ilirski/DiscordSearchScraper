"""Tests for DiscordSearcher class."""

import json
import os
from unittest.mock import patch

import pytest

from scraper import DiscordSearcher


@pytest.fixture
def mock_token():
    """Fixture providing a mock Discord token."""
    return "mock_test_token_12345"


@pytest.fixture
def mock_guild_id():
    """Fixture providing a mock guild ID."""
    return "123456789012345678"


@pytest.fixture
def searcher(mock_token, mock_guild_id):
    """Fixture providing a DiscordSearcher instance."""
    with patch("scraper.logging.basicConfig"):
        return DiscordSearcher(
            guild_id=mock_guild_id,
            token=mock_token,
            query="test query",
        )


class TestDiscordSearcherInit:
    """Tests for DiscordSearcher initialization."""

    def test_init_with_token(self, mock_guild_id, mock_token):
        """Test initialization with token parameter."""
        with patch("scraper.logging.basicConfig"):
            searcher = DiscordSearcher(
                guild_id=mock_guild_id,
                token=mock_token,
            )
        assert searcher.token == mock_token
        assert searcher.guild_id == mock_guild_id

    def test_init_with_env_token(self, mock_guild_id):
        """Test initialization with token from environment variable."""
        with (
            patch.dict(os.environ, {"DISCORD_TOKEN": "env_token_123"}),
            patch("scraper.logging.basicConfig"),
        ):
            searcher = DiscordSearcher(
                guild_id=mock_guild_id,
            )
        assert searcher.token == "env_token_123"

    def test_init_without_token_raises_error(self, mock_guild_id):
        """Test that initialization fails without token."""
        with (
            patch.dict(os.environ, {}, clear=True),
            pytest.raises(ValueError, match="Token is required"),
        ):
            DiscordSearcher(guild_id=mock_guild_id)

    def test_init_without_guild_id_raises_error(self, mock_token):
        """Test that initialization fails without guild ID."""
        with pytest.raises(ValueError, match="Guild ID is required"):
            DiscordSearcher(guild_id="", token=mock_token)

    def test_init_with_invalid_after_snowflake(self, mock_guild_id, mock_token):
        """Test that initialization fails with invalid after snowflake."""
        with (
            patch("scraper.logging.basicConfig"),
            pytest.raises(ValueError, match="Invalid snowflake"),
        ):
            DiscordSearcher(
                guild_id=mock_guild_id,
                token=mock_token,
                after="invalid_snowflake",
            )

    def test_init_with_valid_after_snowflake(self, mock_guild_id, mock_token):
        """Test initialization with valid after snowflake."""
        with patch("scraper.logging.basicConfig"):
            searcher = DiscordSearcher(
                guild_id=mock_guild_id,
                token=mock_token,
                after="12345678901234567",
            )
        assert searcher.after == "12345678901234567"


class TestGenerateFilename:
    """Tests for generate_filename method."""

    def test_generate_filename_with_query(self, searcher):
        """Test filename generation with query."""
        filename = searcher.generate_filename()
        assert isinstance(filename, str)
        assert searcher.guild_id in filename
        # query is now a URL, so just check that filename is generated
        assert ".jsonl" in filename

    def test_generate_filename_without_query(self, mock_token, mock_guild_id):
        """Test filename generation without query."""
        with patch("scraper.logging.basicConfig"):
            searcher = DiscordSearcher(
                guild_id=mock_guild_id,
                token=mock_token,
            )
        filename = searcher.generate_filename()
        assert isinstance(filename, str)
        assert mock_guild_id in filename
        assert filename.endswith(".jsonl")


class TestSetOutput:
    """Tests for set_output method."""

    def test_set_output_with_none(self, searcher):
        """Test setting output with None generates filename."""
        searcher.set_output(None)
        assert searcher.output is not None
        assert searcher.output.endswith(".jsonl")

    def test_set_output_with_directory(self, searcher, tmp_path):
        """Test setting output with directory path."""
        output_dir = str(tmp_path / "output")
        searcher.set_output(output_dir)
        assert searcher.output is not None
        assert output_dir in searcher.output

    def test_set_output_creates_directory(self, searcher, tmp_path):
        """Test that set_output creates directory if it doesn't exist."""
        output_dir = str(tmp_path / "new_output") + "/"
        assert not os.path.exists(output_dir.rstrip("/"))
        searcher.set_output(output_dir)
        assert os.path.exists(output_dir.rstrip("/"))

    def test_set_output_with_file(self, searcher, tmp_path):
        """Test setting output with file path."""
        output_file = str(tmp_path / "output.jsonl")
        searcher.set_output(output_file)
        assert searcher.output == output_file


class TestFormSearchQuery:
    """Tests for form_search_query method."""

    def test_form_query_basic(self, mock_token, mock_guild_id):
        """Test basic query formation."""
        with patch("scraper.logging.basicConfig"):
            searcher = DiscordSearcher(
                guild_id=mock_guild_id,
                token=mock_token,
            )
        assert searcher.query is not None
        assert "discord.com/api/v9/guilds" in searcher.query
        assert mock_guild_id in searcher.query

    def test_form_query_with_content(self, mock_token, mock_guild_id):
        """Test query formation with content filter."""
        with patch("scraper.logging.basicConfig"):
            searcher = DiscordSearcher(
                guild_id=mock_guild_id,
                token=mock_token,
                query="test content",
            )
        assert "content" in searcher.query
        assert "test" in searcher.query or "content" in searcher.query

    def test_form_query_with_channel_id(self, mock_token, mock_guild_id):
        """Test query formation with channel ID."""
        channel_id = "987654321098765432"
        with patch("scraper.logging.basicConfig"):
            searcher = DiscordSearcher(
                guild_id=mock_guild_id,
                token=mock_token,
                channel_id=channel_id,
            )
        assert "channel_id" in searcher.query
        assert channel_id in searcher.query

    def test_form_query_with_after(self, mock_token, mock_guild_id):
        """Test query formation with after parameter."""
        after_id = "12345678901234567"
        with patch("scraper.logging.basicConfig"):
            searcher = DiscordSearcher(
                guild_id=mock_guild_id,
                token=mock_token,
                after=after_id,
            )
        assert "min_id" in searcher.query
        assert after_id in searcher.query

    def test_form_query_with_before(self, mock_token, mock_guild_id):
        """Test query formation with before parameter."""
        before_id = "12345678901234567"
        with patch("scraper.logging.basicConfig"):
            searcher = DiscordSearcher(
                guild_id=mock_guild_id,
                token=mock_token,
                before=before_id,
            )
        assert "max_id" in searcher.query
        assert before_id in searcher.query


class TestAppendMessage:
    """Tests for append_message method."""

    def test_append_message(self, searcher, tmp_path):
        """Test appending messages to file."""
        output_file = str(tmp_path / "test_output.jsonl")
        searcher.set_output(output_file)

        messages = {
            "messages": [
                {"id": "1", "content": "Test message 1"},
                {"id": "2", "content": "Test message 2"},
            ]
        }
        searcher.append_message(messages)

        assert os.path.exists(output_file)
        with open(output_file) as f:
            lines = f.readlines()
        assert len(lines) == 2
        assert json.loads(lines[0])["id"] == "1"
        assert json.loads(lines[1])["id"] == "2"

    def test_append_multiple_times(self, searcher, tmp_path):
        """Test appending messages multiple times."""
        output_file = str(tmp_path / "test_output.jsonl")
        searcher.set_output(output_file)

        messages1 = {"messages": [{"id": "1", "content": "Message 1"}]}
        messages2 = {"messages": [{"id": "2", "content": "Message 2"}]}

        searcher.append_message(messages1)
        searcher.append_message(messages2)

        with open(output_file) as f:
            lines = f.readlines()
        assert len(lines) == 2


class TestUpdateQueryParams:
    """Tests for _update_query_params method."""

    def test_update_query_params_no_min_id(self, searcher):
        """Test updating query params when no min_id exists."""
        searcher.query = "https://discord.com/api/v9/guilds/123/messages/search"
        searcher._update_query_params("99999999999999999")
        assert "min_id=99999999999999999" in searcher.query

    def test_update_query_params_with_min_id(self, searcher):
        """Test updating query params when min_id exists."""
        searcher.query = "https://discord.com/api/v9/guilds/123/messages/search?min_id=11111111111111111"
        searcher._update_query_params("99999999999999999")
        assert "min_id=99999999999999999" in searcher.query
        assert "11111111111111111" not in searcher.query

    def test_update_query_params_no_query_set(self, searcher):
        """Test that updating params fails without query."""
        searcher.query = None
        with pytest.raises(ValueError, match="No query set"):
            searcher._update_query_params("99999999999999999")
