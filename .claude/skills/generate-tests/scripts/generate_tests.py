#!/usr/bin/env python3
"""Generate xUnit tests for C#/.NET ABP Framework code.

Usage:
    python generate_tests.py <source_file> [--type unit|integration|both] [--dry-run]

Examples:
    python generate_tests.py src/UserAppService.cs
    python generate_tests.py src/UserAppService.cs --type integration
    python generate_tests.py src/CreateUserValidator.cs --dry-run
"""

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# Test output directories follow ABP Framework conventions
UNIT_TEST_DIR = "api/test/{module}.Application.Tests"
INTEGRATION_TEST_DIR = "api/test/{module}.HttpApi.Tests"


@dataclass
class MethodInfo:
    """Extracted method information."""
    name: str
    return_type: str
    parameters: list[tuple[str, str]]  # [(type, name), ...]
    is_async: bool
    has_authorize: bool


@dataclass
class ClassInfo:
    """Extracted class information."""
    name: str
    namespace: str
    base_class: Optional[str]
    dependencies: list[tuple[str, str]]  # [(type, name), ...]
    methods: list[MethodInfo]
    class_type: str  # 'appservice', 'validator', 'controller'


def detect_class_type(class_name: str, base_class: Optional[str]) -> str:
    """Determine class type from naming conventions."""
    if class_name.endswith("AppService"):
        return "appservice"
    if class_name.endswith("Validator"):
        return "validator"
    if class_name.endswith("Controller"):
        return "controller"
    if base_class and "AppService" in base_class:
        return "appservice"
    return "appservice"  # Default to most common


def extract_module_name(namespace: str) -> str:
    """Extract module name from namespace (e.g., 'MyApp.Users' -> 'Users')."""
    parts = namespace.split(".")
    # Skip common prefixes like company name
    for part in parts:
        if part not in ("Application", "Domain", "HttpApi", "EntityFrameworkCore"):
            return part
    return parts[-1] if parts else "Module"


def parse_source_file(file_path: Path) -> Optional[ClassInfo]:
    """Parse C# source file and extract class information."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        print("Hint: Check the file path and try again.")
        return None
    except PermissionError:
        print(f"Error: Permission denied reading: {file_path}")
        return None

    # Extract namespace
    ns_match = re.search(r"namespace\s+([\w.]+)", content)
    namespace = ns_match.group(1) if ns_match else "Unknown"

    # Extract class declaration
    class_match = re.search(
        r"public\s+(?:sealed\s+)?class\s+(\w+)(?:\s*:\s*([\w<>,\s]+))?",
        content
    )
    if not class_match:
        print(f"Error: No public class found in {file_path}")
        return None

    class_name = class_match.group(1)
    base_class = class_match.group(2)

    # Extract constructor dependencies
    ctor_match = re.search(
        rf"public\s+{class_name}\s*\(([^)]*)\)",
        content,
        re.DOTALL
    )
    dependencies = []
    if ctor_match:
        params = ctor_match.group(1)
        for param in re.findall(r"(I?\w+(?:<[\w,\s]+>)?)\s+(\w+)", params):
            dependencies.append(param)

    # Extract public methods
    methods = []
    method_pattern = re.compile(
        r"(\[Authorize[^\]]*\])?\s*"
        r"public\s+(virtual\s+)?(async\s+)?"
        r"(Task<[\w<>,\s]+>|Task|[\w<>,\s]+)\s+"
        r"(\w+)\s*\(([^)]*)\)",
        re.MULTILINE
    )
    for match in method_pattern.finditer(content):
        has_authorize = match.group(1) is not None
        is_async = match.group(3) is not None
        return_type = match.group(4)
        method_name = match.group(5)
        params_str = match.group(6)

        # Skip common base class methods
        if method_name in ("Dispose", "ToString", "GetHashCode", "Equals"):
            continue

        parameters = []
        if params_str.strip():
            for param in re.findall(r"([\w<>,\s]+)\s+(\w+)", params_str):
                parameters.append(param)

        methods.append(MethodInfo(
            name=method_name,
            return_type=return_type,
            parameters=parameters,
            is_async=is_async,
            has_authorize=has_authorize
        ))

    return ClassInfo(
        name=class_name,
        namespace=namespace,
        base_class=base_class,
        dependencies=dependencies,
        methods=methods,
        class_type=detect_class_type(class_name, base_class)
    )


def generate_unit_test(info: ClassInfo) -> str:
    """Generate unit test class for AppService."""
    module = extract_module_name(info.namespace)

    # Build mock fields
    mock_fields = []
    mock_init = []
    ctor_args = []
    for dep_type, dep_name in info.dependencies:
        field_name = f"_{dep_name}"
        mock_fields.append(f"    private readonly {dep_type} {field_name};")
        mock_init.append(f"        {field_name} = Substitute.For<{dep_type}>();")
        ctor_args.append(field_name)

    # Build test methods
    test_methods = []
    for method in info.methods:
        async_prefix = "async Task" if method.is_async else "void"
        await_prefix = "await " if method.is_async else ""

        # Happy path test
        test_methods.append(f'''
    [Fact]
    public {async_prefix} {method.name}_ValidInput_Succeeds()
    {{
        // Arrange
        // TODO: Set up valid input and mock returns

        // Act
        var result = {await_prefix}_sut.{method.name}();

        // Assert
        result.ShouldNotBeNull();
    }}''')

        # Not found test for methods with Guid parameter
        if any(p[0] == "Guid" for p in method.parameters):
            test_methods.append(f'''
    [Fact]
    public {async_prefix} {method.name}_NotFound_ThrowsEntityNotFoundException()
    {{
        // Arrange
        var id = Guid.NewGuid();

        // Act & Assert
        {await_prefix}Should.ThrowAsync<EntityNotFoundException>(
            () => _sut.{method.name}(id));
    }}''')

        # Authorization test
        if method.has_authorize:
            test_methods.append(f'''
    [Fact]
    public {async_prefix} {method.name}_Unauthorized_ThrowsAbpAuthorizationException()
    {{
        // Arrange
        // TODO: Set up unauthorized context

        // Act & Assert
        {await_prefix}Should.ThrowAsync<AbpAuthorizationException>(
            () => _sut.{method.name}());
    }}''')

    return f'''using Shouldly;
using Xunit;
using NSubstitute;
using Volo.Abp;
using Volo.Abp.Domain.Entities;

namespace {info.namespace}.Tests;

public class {info.name}Tests : {module}ApplicationTestBase
{{
    private readonly {info.name} _sut;
{chr(10).join(mock_fields)}

    public {info.name}Tests()
    {{
{chr(10).join(mock_init)}
        _sut = new {info.name}({", ".join(ctor_args)});
    }}
{"".join(test_methods)}
}}
'''


def generate_validator_test(info: ClassInfo) -> str:
    """Generate unit test class for Validator."""
    # Extract DTO type from class name (e.g., CreateUserDtoValidator -> CreateUserDto)
    dto_type = info.name.replace("Validator", "")

    return f'''using FluentValidation.TestHelper;
using Xunit;

namespace {info.namespace}.Tests;

public class {info.name}Tests
{{
    private readonly {info.name} _validator = new();

    [Fact]
    public void Validate_ValidModel_Passes()
    {{
        // Arrange
        var model = new {dto_type}
        {{
            // TODO: Set valid properties
        }};

        // Act
        var result = _validator.TestValidate(model);

        // Assert
        result.ShouldNotHaveAnyValidationErrors();
    }}

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void Name_Empty_Fails(string value)
    {{
        // Arrange
        var model = new {dto_type} {{ Name = value }};

        // Act
        var result = _validator.TestValidate(model);

        // Assert
        result.ShouldHaveValidationErrorFor(x => x.Name);
    }}

    // TODO: Add tests for other validation rules
}}
'''


def generate_integration_test(info: ClassInfo) -> str:
    """Generate integration test class for Controller."""
    module = extract_module_name(info.namespace)
    # Convert PascalCase to kebab-case for URL
    entity = re.sub(r"Controller$", "", info.name)
    url_path = re.sub(r"(?<!^)(?=[A-Z])", "-", entity).lower()

    return f'''using System.Net;
using System.Net.Http.Json;
using Shouldly;
using Xunit;

namespace {info.namespace}.Tests;

public class {info.name}Tests : {module}HttpApiTestBase
{{
    private const string BaseUrl = "/api/app/{url_path}";

    [Fact]
    public async Task GetList_ReturnsOk()
    {{
        // Act
        var response = await Client.GetAsync(BaseUrl);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.OK);
    }}

    [Fact]
    public async Task Get_ExistingId_ReturnsOk()
    {{
        // Arrange
        var id = TestData.{entity}Id;

        // Act
        var response = await Client.GetAsync($"{{BaseUrl}}/{{id}}");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.OK);
    }}

    [Fact]
    public async Task Get_NonExistingId_ReturnsNotFound()
    {{
        // Act
        var response = await Client.GetAsync($"{{BaseUrl}}/{{Guid.NewGuid()}}");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.NotFound);
    }}

    [Fact]
    public async Task Create_ValidInput_ReturnsCreated()
    {{
        // Arrange
        var input = new Create{entity}Dto
        {{
            // TODO: Set valid properties
        }};

        // Act
        var response = await Client.PostAsJsonAsync(BaseUrl, input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.Created);
    }}

    [Fact]
    public async Task Create_InvalidInput_ReturnsBadRequest()
    {{
        // Arrange
        var input = new Create{entity}Dto(); // Missing required fields

        // Act
        var response = await Client.PostAsJsonAsync(BaseUrl, input);

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.BadRequest);
    }}

    [Fact]
    public async Task Delete_Unauthorized_ReturnsForbidden()
    {{
        // Arrange
        await AuthenticateAsAsync("readonly-user");

        // Act
        var response = await Client.DeleteAsync($"{{BaseUrl}}/{{TestData.{entity}Id}}");

        // Assert
        response.StatusCode.ShouldBe(HttpStatusCode.Forbidden);
    }}
}}
'''


def get_output_path(info: ClassInfo, test_type: str) -> Path:
    """Determine output path for test file."""
    module = extract_module_name(info.namespace)

    if test_type == "integration":
        base_dir = INTEGRATION_TEST_DIR.format(module=module)
        suffix = "IntegrationTests"
    else:
        base_dir = UNIT_TEST_DIR.format(module=module)
        suffix = "Tests"

    return Path(base_dir) / f"{info.name}{suffix}.cs"


def main():
    parser = argparse.ArgumentParser(
        description="Generate xUnit tests for C#/.NET ABP Framework code"
    )
    parser.add_argument("source", help="Source file path")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "both"],
        default="unit",
        help="Test type to generate (default: unit)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated code without writing files"
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    info = parse_source_file(source_path)
    if not info:
        sys.exit(1)

    print(f"Analyzed: {info.name} ({info.class_type})")
    print(f"  Methods: {len(info.methods)}")
    print(f"  Dependencies: {len(info.dependencies)}")

    generators = {
        "appservice": generate_unit_test,
        "validator": generate_validator_test,
        "controller": generate_integration_test,
    }

    # Determine what to generate
    if args.type == "both":
        types_to_generate = ["unit", "integration"]
    elif args.type == "integration" or info.class_type == "controller":
        types_to_generate = ["integration"]
    else:
        types_to_generate = ["unit"]

    for test_type in types_to_generate:
        if test_type == "integration":
            generator = generate_integration_test
        elif info.class_type == "validator":
            generator = generate_validator_test
        else:
            generator = generate_unit_test

        code = generator(info)
        output_path = get_output_path(info, test_type)

        if args.dry_run:
            print(f"\n--- {output_path} ---")
            print(code)
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(code, encoding="utf-8")
            print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
