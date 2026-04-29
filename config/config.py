from typing import Dict, Any


class Config:
    AGENTS = {
        "main": {
            "agent_id": "main_agent",
            "name": "主智能体",
            "description": "负责任务调度和协调各智能体"
        },
        "creative": {
            "agent_id": "creative_agent",
            "name": "创意智能体",
            "description": "负责创意生成和需求分析"
        },
        "design": {
            "agent_id": "design_agent",
            "name": "设计智能体",
            "description": "负责UI/UX设计和架构设计"
        },
        "development": {
            "agent_id": "development_agent",
            "name": "开发智能体",
            "description": "负责代码实现和开发任务"
        },
        "testing": {
            "agent_id": "testing_agent",
            "name": "测试智能体",
            "description": "负责测试用例编写和验证"
        }
    }

    WORKFLOW_DEFAULTS = {
        "max_concurrent_tasks": 5,
        "default_priority": 0,
        "task_timeout": 300
    }

    LOGGING = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }

    @classmethod
    def get_agent_config(cls, agent_type: str) -> Dict[str, Any]:
        return cls.AGENTS.get(agent_type, {})

    @classmethod
    def get_all_agent_types(cls) -> list:
        return list(cls.AGENTS.keys())