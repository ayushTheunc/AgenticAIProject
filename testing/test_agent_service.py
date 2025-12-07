"""
Unit tests for agent_service.py
Tests all functions in the AgentService class
"""

import pytest
import os
import sys
import tempfile
import shutil
import zipfile
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.agent_service import AgentService, agent_service_function


@pytest.fixture
def agent_service():
    """Create an AgentService instance for testing."""
    with patch.dict(os.environ, {
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'test-deployment'
    }):
        return AgentService()


@pytest.fixture
def temp_repo_dir():
    """Create a temporary directory with sample Python files."""
    temp_dir = tempfile.mkdtemp()
    
    # Create sample Python file
    with open(os.path.join(temp_dir, "test.py"), "w") as f:
        f.write("def hello():\n    print('Hello, World!')")
    
    yield temp_dir
    
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def sample_zip_data():
    """Create sample zip file data."""
    import io
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('test.py', 'def test():\n    pass')
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


class TestAgentServiceInit:
    """Tests for AgentService initialization."""
    
    def test_init_with_valid_env(self, agent_service):
        """Test that AgentService initializes with valid environment variables."""
        assert agent_service.prompt_template is not None
        assert 'code' in agent_service.prompt_template.input_variables
        assert 'rubric' in agent_service.prompt_template.input_variables
    
    def test_init_without_env_variables(self):
        """Test that initialization fails without required environment variables."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(Exception, match="Missing required environment variables"):
                AgentService()


class TestValidateEnvironment:
    """Tests for _validate_environment method."""
    
    def test_validate_environment(self):
        """Test environment validation with missing API key."""
        with patch.dict(os.environ, {'AZURE_OPENAI_ENDPOINT': 'test', 'AZURE_OPENAI_DEPLOYMENT_NAME': 'test', 'AZURE_OPENAI_API_KEY': 'test'}, clear=True):
            AgentService()
    
    def test_validate_environment_missing_key(self):
        """Test environment validation with missing API key."""
        with patch.dict(os.environ, {'AZURE_OPENAI_ENDPOINT': 'test', 'AZURE_OPENAI_DEPLOYMENT_NAME': 'test'}, clear=True):
            with pytest.raises(Exception, match="AZURE_OPENAI_API_KEY"):
                AgentService()


class TestExtractRepoFromGithub:
    """Tests for extract_repo_from_github method."""
    
    def test_extract_repo_invalid_url_type(self, agent_service):
        """Test with non-string URL."""
        with pytest.raises(ValueError, match="github_url must be a non-empty string"):
            agent_service.extract_repo_from_github(123)
    
    def test_extract_repo_empty_url(self, agent_service):
        """Test with empty URL."""
        with pytest.raises(ValueError, match="github_url must be a non-empty string"):
            agent_service.extract_repo_from_github("")
    
    def test_extract_repo_invalid_url_format(self, agent_service):
        """Test with invalid GitHub URL."""
        with pytest.raises(ValueError, match="Invalid GitHub URL"):
            agent_service.extract_repo_from_github("https://gitlab.com/test/repo.git")
    
    @patch('subprocess.run')
    def test_extract_repo_success(self, mock_run, agent_service):
        """Test successful repository cloning."""
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        with patch('tempfile.mkdtemp', return_value='/tmp/test_repo'):
            result = agent_service.extract_repo_from_github("https://github.com/test/repo.git")
            assert result == '/tmp/test_repo'
            mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_extract_repo_git_failure(self, mock_run, agent_service):
        """Test git clone failure."""
        mock_run.return_value = MagicMock(returncode=1, stderr="Permission denied")
        
        with pytest.raises(Exception, match="Git clone failed"):
            agent_service.extract_repo_from_github("https://github.com/test/repo.git")


class TestExtractZipFromData:
    """Tests for _extract_zip_from_data method."""
    
    def test_extract_zip_invalid_type(self, agent_service):
        """Test with non-bytes data."""
        with pytest.raises(TypeError, match="zip_data must be bytes"):
            agent_service._extract_zip_from_data("not bytes")
    
    def test_extract_zip_invalid_data(self, agent_service):
        """Test with invalid zip data."""
        with pytest.raises(ValueError, match="Invalid zip data"):
            agent_service._extract_zip_from_data(b"not a zip file")
    
    def test_extract_zip_success(self, agent_service, sample_zip_data):
        """Test successful zip extraction."""
        result = agent_service._extract_zip_from_data(sample_zip_data)
        
        assert os.path.exists(result)
        assert os.path.isdir(result)
        
        # Cleanup
        shutil.rmtree(result)


class TestFindFileInRepo:
    """Tests for _find_file_in_repo method."""
    
    def test_find_file_exact_match(self, agent_service, temp_repo_dir):
        """Test finding file with exact path."""
        result = agent_service._find_file_in_repo(temp_repo_dir, "test.py")
        assert result == os.path.join(temp_repo_dir, "test.py")
    
    def test_find_file_not_found(self, agent_service, temp_repo_dir):
        """Test when file doesn't exist."""
        result = agent_service._find_file_in_repo(temp_repo_dir, "nonexistent.py")
        assert result is None
    


class TestLoadCodeFiles:
    """Tests for _load_code_files method."""
    
    def test_load_code_files_success(self, agent_service, temp_repo_dir):
        """Test loading existing files."""
        result = agent_service._load_code_files(temp_repo_dir, ["test.py"])
        
        assert "test.py" in result
        assert "def hello():" in result["test.py"]
    
    def test_load_code_files_not_found(self, agent_service, temp_repo_dir):
        """Test loading non-existent files."""
        with pytest.raises(Exception, match="No code files could be loaded"):
            agent_service._load_code_files(temp_repo_dir, ["nonexistent.py"])
    
    def test_load_code_files_limit(self, agent_service, temp_repo_dir):
        """Test file limit enforcement."""
        # Create 7 files
        for i in range(7):
            with open(os.path.join(temp_repo_dir, f"file{i}.py"), "w") as f:
                f.write(f"# File {i}")
        
        file_list = [f"file{i}.py" for i in range(7)]
        result = agent_service._load_code_files(temp_repo_dir, file_list)
        
        # Should only load first 5
        assert len(result) == 5


class TestInitializeLLM:
    """Tests for _initialize_llm method."""
    
    @patch('services.agent_service.AzureChatOpenAI')
    def test_initialize_llm(self, mock_azure_chat, agent_service):
        """Test LLM initialization."""
        agent_service._initialize_llm()
        
        mock_azure_chat.assert_called_once()
        call_kwargs = mock_azure_chat.call_args[1]
        assert call_kwargs['temperature'] == 0


class TestFormatCodeContent:
    """Tests for _format_code_content method."""
    
    def test_format_code_content_single_file(self, agent_service):
        """Test formatting single file."""
        code_files = {"test.py": "def hello():\n    pass"}
        result = agent_service._format_code_content(code_files)
        
        assert "File 1: test.py" in result
        assert "def hello():" in result
    
    def test_format_code_content_multiple_files(self, agent_service):
        """Test formatting multiple files."""
        code_files = {
            "file1.py": "# File 1",
            "file2.py": "# File 2"
        }
        result = agent_service._format_code_content(code_files)
        
        assert "File 1:" in result
        assert "File 2:" in result


class TestProcessSingleBatch:
    """Tests for _process_single_batch method."""
    
    @patch.object(AgentService, '_load_code_files')
    @patch.object(AgentService, '_initialize_llm')
    def test_process_single_batch_success(self, mock_init_llm, mock_load_files, agent_service, temp_repo_dir):
        """Test successful batch processing."""
        mock_load_files.return_value = {"test.py": "def test(): pass"}
        
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = '{"rubric_score": "5/6", "hundred_point_score": 83, "review": "Good code."}'
        mock_llm.invoke.return_value = mock_response
        mock_init_llm.return_value = mock_llm
        
        result = agent_service._process_single_batch(
            temp_repo_dir,
            ["test.py"],
            1,
            "Test rubric"
        )
        
        assert result['rubric_score'] == "5/6"
        assert result['hundred_point_score'] == 83
        assert 'file_name' in result


class TestCleanupTempDirectory:
    """Tests for _cleanup_temp_directory method."""
    
    def test_cleanup_success(self, agent_service):
        """Test successful cleanup."""
        temp_dir = tempfile.mkdtemp()
        assert os.path.exists(temp_dir)
        
        agent_service._cleanup_temp_directory(temp_dir)
        assert not os.path.exists(temp_dir)
    
    def test_cleanup_nonexistent(self, agent_service):
        """Test cleanup of non-existent directory."""
        # Should not raise exception
        agent_service._cleanup_temp_directory("/nonexistent/path")


class TestAgentServiceFunction:
    """Tests for agent_service_function."""
    
    @patch.object(AgentService, 'extract_repo_from_github')
    @patch.object(AgentService, '_process_single_batch')
    @patch.object(AgentService, '_cleanup_temp_directory')
    def test_agent_service_function_success(self, mock_cleanup, mock_process, mock_extract):
        """Test main agent service function."""
        mock_extract.return_value = "/tmp/test_repo"
        mock_process.return_value = {
            "rubric_score": "6/6",
            "hundred_point_score": 100,
            "review": "Perfect code.",
            "file_name": ["test.py"]
        }
        
        rubric_json = {
            "batches": [["test.py"]],
            "rubric": "Test rubric"
        }
        
        result = agent_service_function("https://github.com/test/repo.git", rubric_json)
        
        assert isinstance(result, list)
        assert len(result) == 1
        mock_extract.assert_called_once()
        mock_process.assert_called_once()
        mock_cleanup.assert_called_once()
