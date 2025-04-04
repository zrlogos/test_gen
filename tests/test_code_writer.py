import pytest
from code_writer import CodeWriter

@pytest.fixture
def code_writer():
    """Fixture to create a CodeWriter instance for each test."""
    return CodeWriter()

def test_write_code_success(code_writer):
    """Test writing code successfully."""
    code = "print('Hello, World!')"
    result = code_writer.write_code(code)
    assert result == "Code written successfully."

def test_write_code_empty(code_writer):
    """Test writing empty code."""
    code = ""
    result = code_writer.write_code(code)
    assert result == "Error: Code cannot be empty."

def test_write_code_invalid_type(code_writer):
    """Test writing code with invalid type."""
    code = 12345
    with pytest.raises(TypeError):
        code_writer.write_code(code)

def test_write_code_long(code_writer):
    """Test writing long code."""
    code = "a" * 1001
    result = code_writer.write_code(code)
    assert result == "Error: Code exceeds maximum length."

def test_write_code_with_special_chars(code_writer):
    """Test writing code with special characters."""
    code = "print('Hello, @World!')"
    result = code_writer.write_code(code)
    assert result == "Code written successfully."

def test_write_code_with_whitespace(code_writer):
    """Test writing code with leading/trailing whitespace."""
    code = "   print('Hello, World!')   "
    result = code_writer.write_code(code)
    assert result == "Code written successfully."

def test_write_code_multiline(code_writer):
    """Test writing multiline code."""
    code = """def foo():
    print('Hello, World!')"""
    result = code_writer.write_code(code)
    assert result == "Code written successfully."

def test_write_code_with_comments(code_writer):
    """Test writing code with comments."""
    code = "# This is a comment\nprint('Hello, World!')"
    result = code_writer.write_code(code)
    assert result == "Code written successfully."

def test_write_code_with_unicode(code_writer):
    """Test writing code with unicode characters."""
    code = "print('こんにちは')"
    result = code_writer.write_code(code)
    assert result == "Code written successfully."

def test_write_code_with_newlines(code_writer):
    """Test writing code with newlines."""
    code = "print('Hello, World!')\nprint('Goodbye, World!')"
    result = code_writer.write_code(code)
    assert result == "Code written successfully."