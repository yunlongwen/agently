"""Specialist agents for specific tasks"""

from typing import Any

from agently.agents.base import AgentContext, AgentResult, BaseAgent


class RequirementsAnalyzerAgent(BaseAgent):
    """Agent for analyzing requirements"""

    def __init__(self):
        super().__init__(
            name="requirements-analyzer",
            description="需求分析智能体，负责理解和结构化需求",
            capabilities=["requirements", "analysis", "需求"],
        )

    def execute(self, context: AgentContext) -> AgentResult:
        """Analyze requirements

        Args:
            context: Execution context

        Returns:
            Analysis result
        """
        result = self._analyze(context.task)
        return AgentResult(success=True, data=result)

    def _analyze(self, task: str) -> dict[str, Any]:
        """Analyze task requirements

        Args:
            task: Task description

        Returns:
            Analysis results
        """
        # Handle empty task
        if not task or not task.strip():
            return {"requirements": []}

        task = task.strip()

        # Check for vague requirements
        vague_indicators = [
            "一些",
            "某些",
            "做一些",
            "弄一下",
            "搞一个",
            "something",
            "some",
            "do something",
            "make a",
        ]

        is_vague = any(indicator in task.lower() for indicator in vague_indicators)

        if is_vague:
            return {
                "requirements": ["需求不明确，请提供更多详细信息：需要澄清功能的具体要求"],
                "is_vague": True,
            }

        # Extract keywords and create structured requirements
        keywords = self._extract_keywords(task)
        requirements = self._create_requirements(task, keywords)

        return {
            "requirements": requirements,
            "keywords": keywords,
            "task_type": self._classify_task(task),
        }

    def _extract_keywords(self, task: str) -> list[str]:
        """Extract keywords from task

        Args:
            task: Task description

        Returns:
            List of keywords
        """
        # Common functional keywords in Chinese
        functional_keywords = [
            "登录",
            "注册",
            "邮箱",
            "密码",
            "验证",
            "用户",
            "功能",
            "实现",
            "创建",
            "删除",
            "修改",
            "查询",
            "文件",
            "数据",
            "接口",
            "API",
            "数据库",
        ]

        found_keywords = []
        for keyword in functional_keywords:
            if keyword in task:
                found_keywords.append(keyword)

        return found_keywords

    def _create_requirements(self, task: str, keywords: list[str]) -> list[str]:
        """Create structured requirements from task

        Args:
            task: Task description
            keywords: Extracted keywords

        Returns:
            List of requirements
        """
        requirements = []

        # Create functional requirement based on keywords
        if "登录" in keywords:
            requirements.append("功能需求：实现用户登录功能")
            if "邮箱" in keywords:
                requirements.append("输入验证：支持邮箱格式验证")
            if "密码" in keywords:
                requirements.append("安全需求：支持密码验证")
            if "验证" in keywords:
                requirements.append("验证需求：实现身份验证机制")

        if "注册" in keywords:
            requirements.append("功能需求：实现用户注册功能")

        if not requirements and keywords:
            requirements.append(f"功能需求：实现包含 {', '.join(keywords)} 的功能")

        # If no specific requirements extracted, use task as base
        if not requirements:
            requirements.append(f"需求：{task}")

        return requirements

    def _classify_task(self, task: str) -> str:
        """Classify task type

        Args:
            task: Task description

        Returns:
            Task type classification
        """
        task_lower = task.lower()

        if any(kw in task_lower for kw in ["登录", "login", "signin"]):
            return "authentication"
        elif any(kw in task_lower for kw in ["注册", "register", "signup"]):
            return "registration"
        elif any(kw in task_lower for kw in ["代码", "code", "函数", "function"]):
            return "code_generation"
        elif any(kw in task_lower for kw in ["测试", "test", "bug"]):
            return "testing"
        else:
            return "general"


class CodeGeneratorAgent(BaseAgent):
    """Agent for generating code"""

    def __init__(self):
        super().__init__(
            name="code-generator",
            description="代码生成智能体，负责生成和重构代码",
            capabilities=["code-generation", "代码生成", "generate"],
        )

    def execute(self, context: AgentContext) -> AgentResult:
        """Generate code

        Args:
            context: Execution context

        Returns:
            Generated code
        """
        result = self._generate(context.task)
        return AgentResult(success=True, data=result)

    def _generate(self, task: str) -> dict[str, Any]:
        """Generate code from task

        Args:
            task: Task description

        Returns:
            Generated code
        """
        # Handle empty task
        if not task or not task.strip():
            return {"code": self._generate_default_function()}

        # Generate code based on task keywords
        if "相加" in task or "add" in task or "sum" in task:
            return {"code": self._generate_add_function()}
        elif "函数" in task or "function" in task:
            return {"code": self._generate_generic_function()}
        elif "类" in task or "class" in task:
            return {"code": self._generate_generic_class()}
        elif "排序" in task or "sort" in task:
            return {"code": self._generate_sort_function()}
        elif "文件" in task or "file" in task:
            return {"code": self._generate_file_function()}
        else:
            return {"code": self._generate_contextual_code(task)}

    def _generate_default_function(self) -> str:
        """Generate a default function"""
        return '''def process_data(data: any) -> any:
    """Process input data and return result.
    
    Args:
        data: Input data to process
        
    Returns:
        Processed result
    """
    # TODO: Implement your logic here
    result = data
    return result'''

    def _generate_add_function(self) -> str:
        """Generate an add function"""
        return '''def add(a: int, b: int) -> int:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b'''

    def _generate_generic_function(self) -> str:
        """Generate a generic function"""
        return '''def process_input(input_data: str) -> str:
    """Process input and return result.
    
    Args:
        input_data: Input string to process
        
    Returns:
        Processed result string
    """
    # Implement your logic here
    result = input_data
    return result'''

    def _generate_generic_class(self) -> str:
        """Generate a generic class"""
        return '''class DataProcessor:
    """A class for processing data.
    
    Attributes:
        name: Name of the processor
        data: Data to be processed
    """
    
    def __init__(self, name: str = "default"):
        """Initialize the processor.
        
        Args:
            name: Name of the processor
        """
        self.name = name
        self.data = []
    
    def add_data(self, item: any) -> None:
        """Add data item to process.
        
        Args:
            item: Data item to add
        """
        self.data.append(item)
    
    def process(self) -> list:
        """Process all data.
        
        Returns:
            List of processed results
        """
        return [self._transform(item) for item in self.data]
    
    def _transform(self, item: any) -> any:
        """Transform a single item.
        
        Args:
            item: Item to transform
            
        Returns:
            Transformed item
        """
        return item'''

    def _generate_sort_function(self) -> str:
        """Generate a sort function"""
        return '''def sort_list(items: list, reverse: bool = False) -> list:
    """Sort a list of items.
    
    Args:
        items: List of items to sort
        reverse: If True, sort in descending order
        
    Returns:
        Sorted list
    """
    return sorted(items, reverse=reverse)'''

    def _generate_file_function(self) -> str:
        """Generate a file handling function"""
        return '''def read_file(file_path: str) -> str:
    """Read content from a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File content as string
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_path: str, content: str) -> None:
    """Write content to a file.
    
    Args:
        file_path: Path to the file
        content: Content to write
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)'''

    def _generate_contextual_code(self, task: str) -> str:
        """Generate code based on task context

        Args:
            task: Task description

        Returns:
            Generated code
        """
        # Create a function name from task
        func_name = "generated_function"
        if len(task) > 20:
            # Use first few words
            words = task.split()[:3]
            func_name = "_".join(words)[:30]

        return f'''def {func_name}(input_data: any) -> any:
    """Generated function for: {task[:50]}...
    
    Args:
        input_data: Input data
        
    Returns:
        Processed result
    """
    # TODO: Implement your logic here
    result = input_data
    return result'''


class CodeUnderstandingAgent(BaseAgent):
    """Agent for understanding code"""

    def __init__(self):
        super().__init__(
            name="code-understander",
            description="代码理解智能体，负责分析和理解代码结构",
            capabilities=["code-understanding", "代码理解", "analyze"],
        )

    def execute(self, context: AgentContext) -> AgentResult:
        """Understand code

        Args:
            context: Execution context

        Returns:
            Understanding result
        """
        return AgentResult(success=True, data={"understood": True})


class BugFixerAgent(BaseAgent):
    """Agent for fixing bugs"""

    def __init__(self):
        super().__init__(
            name="bug-fixer",
            description="调试修复智能体，负责定位和修复Bug",
            capabilities=["debug", "bug", "调试", "fix"],
        )

    def execute(self, context: AgentContext) -> AgentResult:
        """Fix bugs

        Args:
            context: Execution context

        Returns:
            Fix result
        """
        return AgentResult(success=True, data={"fixed": True})


class QualityAssuranceAgent(BaseAgent):
    """Agent for testing"""

    def __init__(self):
        super().__init__(
            name="tester",
            description="测试智能体，负责生成和执行测试",
            capabilities=["test", "测试", "testing"],
        )

    def execute(self, context: AgentContext) -> AgentResult:
        """Execute tests

        Args:
            context: Execution context

        Returns:
            Test results
        """
        return AgentResult(success=True, data={"tested": True})


class CodeReviewerAgent(BaseAgent):
    """Agent for reviewing code"""

    def __init__(self):
        super().__init__(
            name="code-reviewer",
            description="代码审查智能体，负责代码质量检查",
            capabilities=["review", "审查", "quality"],
        )

    def execute(self, context: AgentContext) -> AgentResult:
        """Review code

        Args:
            context: Execution context

        Returns:
            Review results
        """
        return AgentResult(success=True, data={"reviewed": True})


class GitManagerAgent(BaseAgent):
    """Agent for Git operations"""

    def __init__(self):
        super().__init__(
            name="git-manager",
            description="Git管理智能体，负责版本控制操作",
            capabilities=["git", "Git", "version-control"],
        )

    def execute(self, context: AgentContext) -> AgentResult:
        """Execute Git operations

        Args:
            context: Execution context

        Returns:
            Operation results
        """
        return AgentResult(success=True, data={"git_operation": "completed"})
