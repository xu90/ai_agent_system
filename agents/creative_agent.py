from typing import Any, Dict, List
from .base_agent import BaseAgent, Task, AgentMessage


class CreativeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="creative_agent",
            name="创意智能体",
            agent_type="creative"
        )
        self.idea_bank: List[Dict[str, Any]] = []
        self.requirements_history: List[Dict[str, Any]] = []

    def generate_ideas(self, prompt: str, count: int = 5) -> List[Dict[str, Any]]:
        print(f"[创意智能体] 正在生成创意: {prompt}")
        
        ideas = []
        for i in range(count):
            idea = {
                "id": f"idea_{i+1}",
                "title": f"{prompt} - 创意方案 {i+1}",
                "description": f"针对'{prompt}'的第{i+1}个创意解决方案，包含创新性的实现思路和独特价值主张。",
                "keywords": ["创新", "用户体验", "技术突破", "市场需求"],
                "feasibility": (count - i) * 20,
                "impact_score": 80 + i * 4,
                "category": "产品创意"
            }
            ideas.append(idea)
            self.idea_bank.append(idea)
        
        print(f"[创意智能体] 生成了 {len(ideas)} 个创意方案")
        return ideas

    def analyze_requirements(self, raw_requirements: str) -> Dict[str, Any]:
        print(f"[创意智能体] 正在分析需求: {raw_requirements[:50]}...")
        
        requirements = {
            "summary": raw_requirements,
            "features": [
                {"name": "核心功能", "description": "系统的主要业务能力"},
                {"name": "用户界面", "description": "用户交互和视觉设计"},
                {"name": "数据管理", "description": "数据存储和处理"},
                {"name": "安全性", "description": "数据保护和访问控制"}
            ],
            "user_stories": [
                {"as": "用户", "want": "能够完成核心操作", "reason": "实现业务目标"},
                {"as": "管理员", "want": "能够管理系统配置", "reason": "维护系统运行"}
            ],
            "constraints": ["技术栈限制", "时间周期", "预算约束"],
            "success_criteria": ["功能完整性", "性能指标", "用户满意度"]
        }
        
        self.requirements_history.append(requirements)
        print("[创意智能体] 需求分析完成")
        return requirements

    def brainstorm(self, topic: str, participants: int = 3) -> Dict[str, Any]:
        print(f"[创意智能体] 正在进行头脑风暴: {topic}")
        
        brainstorm_result = {
            "topic": topic,
            "participants": participants,
            "duration": "30分钟",
            "ideas_generated": 12,
            "top_ideas": [
                {"title": "方案A", "votes": 8, "description": "创新性解决方案"},
                {"title": "方案B", "votes": 6, "description": "稳健可靠方案"},
                {"title": "方案C", "votes": 4, "description": "低成本方案"}
            ],
            "action_items": [
                {"item": "深入研究方案A", "owner": "设计智能体"},
                {"item": "评估技术可行性", "owner": "开发智能体"}
            ]
        }
        
        print("[创意智能体] 头脑风暴完成")
        return brainstorm_result

    def process_task(self, task: Task) -> Any:
        print(f"[创意智能体] 处理任务: {task.name}")
        
        task.update_status("processing")
        
        if "创意" in task.name or "idea" in task.name.lower():
            result = self.generate_ideas(
                task.description,
                task.metadata.get("count", 5)
            )
        elif "需求" in task.name or "requirement" in task.name.lower():
            result = self.analyze_requirements(task.description)
        elif "头脑风暴" in task.name or "brainstorm" in task.name.lower():
            result = self.brainstorm(
                task.description,
                task.metadata.get("participants", 3)
            )
        else:
            result = {"status": "completed", "message": "任务已处理", "task_name": task.name}
        
        task.set_result(result)
        self.remove_task(task.task_id)
        
        if self.subscribers:
            self.send_message(
                receiver_id=self.subscribers[0],
                content=result,
                message_type="task_result",
                task_id=task.task_id
            )
        
        return result

    def handle_message(self, message: AgentMessage):
        self.message_history.append(message)
        
        if message.message_type == "task":
            task_data = message.content
            task = Task(
                task_id=task_data["task_id"],
                name=task_data["name"],
                description=task_data["description"],
                agent_type=task_data["agent_type"],
                priority=task_data["priority"],
                dependencies=task_data["dependencies"],
                metadata=task_data["metadata"]
            )
            self.add_task(task)
            self.process_task(task)
        elif message.message_type == "status_request":
            self.send_message(
                receiver_id=message.sender_id,
                content=self.get_status(),
                message_type="status"
            )