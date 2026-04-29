from typing import Any, Dict, List
from .base_agent import BaseAgent, Task, AgentMessage


class DesignAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="design_agent",
            name="设计智能体",
            agent_type="design"
        )
        self.designs: List[Dict[str, Any]] = []
        self.style_guides: Dict[str, Any] = {
            "colors": {"primary": "#3B82F6", "secondary": "#6366F1", "accent": "#F59E0B"},
            "typography": {"font": "Inter", "sizes": {"xs": "12px", "sm": "14px", "md": "16px", "lg": "20px", "xl": "24px"}},
            "spacing": {"xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px"}
        }

    def create_ui_design(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[设计智能体] 创建UI设计: {requirements.get('summary', '')[:30]}...")
        
        design = {
            "id": "ui_design_001",
            "name": "系统界面设计",
            "type": "UI设计",
            "components": [
                {"name": "Header", "description": "顶部导航栏", "status": "设计中"},
                {"name": "Sidebar", "description": "侧边菜单栏", "status": "设计中"},
                {"name": "Dashboard", "description": "主仪表盘", "status": "待设计"},
                {"name": "Modal", "description": "弹窗组件", "status": "待设计"}
            ],
            "wireframes": ["首页线框图", "详情页线框图", "表单页线框图"],
            "mockups": ["移动端预览", "桌面端预览"],
            "style_guide": self.style_guides,
            "design_tokens": {
                "colors": self.style_guides["colors"],
                "typography": self.style_guides["typography"],
                "spacing": self.style_guides["spacing"]
            },
            "status": "completed",
            "estimated_hours": 16
        }
        
        self.designs.append(design)
        print("[设计智能体] UI设计创建完成")
        return design

    def create_system_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[设计智能体] 创建系统架构: {requirements.get('summary', '')[:30]}...")
        
        architecture = {
            "id": "arch_001",
            "name": "系统架构设计",
            "type": "架构设计",
            "layers": [
                {"name": "表现层", "components": ["前端框架", "UI组件库", "状态管理"]},
                {"name": "业务层", "components": ["API网关", "业务服务", "工作流引擎"]},
                {"name": "数据层", "components": ["数据库", "缓存", "消息队列"]}
            ],
            "diagram_type": "分层架构图",
            "tech_stack": ["Python", "FastAPI", "React", "PostgreSQL", "Redis"],
            "scalability": "支持水平扩展",
            "security": ["JWT认证", "RBAC权限控制", "数据加密"],
            "deployment": "容器化部署(Docker/K8s)",
            "estimated_hours": 8
        }
        
        self.designs.append(architecture)
        print("[设计智能体] 系统架构设计完成")
        return architecture

    def create_database_schema(self, entities: List[str]) -> Dict[str, Any]:
        print(f"[设计智能体] 创建数据库Schema: {entities}")
        
        schema = {
            "id": "schema_001",
            "name": "数据库设计",
            "type": "数据设计",
            "tables": []
        }
        
        for entity in entities:
            table = {
                "name": entity.lower().replace(" ", "_"),
                "columns": [
                    {"name": "id", "type": "UUID", "primary_key": True},
                    {"name": "created_at", "type": "TIMESTAMP", "nullable": False},
                    {"name": "updated_at", "type": "TIMESTAMP", "nullable": False}
                ],
                "relationships": []
            }
            schema["tables"].append(table)
        
        self.designs.append(schema)
        print("[设计智能体] 数据库Schema创建完成")
        return schema

    def process_task(self, task: Task) -> Any:
        print(f"[设计智能体] 处理任务: {task.name}")
        
        task.update_status("processing")
        
        if "UI" in task.name or "界面" in task.name:
            result = self.create_ui_design(task.metadata.get("requirements", {}))
        elif "架构" in task.name or "architecture" in task.name.lower():
            result = self.create_system_architecture(task.metadata.get("requirements", {}))
        elif "数据库" in task.name or "schema" in task.name.lower():
            result = self.create_database_schema(task.metadata.get("entities", []))
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