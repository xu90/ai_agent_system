from typing import Any, Dict, List
from .base_agent import BaseAgent, Task, AgentMessage


class DevelopmentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="development_agent",
            name="开发智能体",
            agent_type="development"
        )
        self.code_repository: List[Dict[str, Any]] = []
        self.deployment_history: List[Dict[str, Any]] = []

    def write_code(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[开发智能体] 编写代码: {requirements.get('summary', '')[:30]}...")
        
        code_modules = []
        features = requirements.get("features", [])
        
        for feature in features:
            module = {
                "name": f"{feature['name'].lower().replace(' ', '_')}.py",
                "type": "module",
                "description": feature["description"],
                "functions": [
                    {"name": f"create_{feature['name'].lower().replace(' ', '_')}", "purpose": f"创建{feature['name']}"},
                    {"name": f"get_{feature['name'].lower().replace(' ', '_')}", "purpose": f"获取{feature['name']}"},
                    {"name": f"update_{feature['name'].lower().replace(' ', '_')}", "purpose": f"更新{feature['name']}"},
                    {"name": f"delete_{feature['name'].lower().replace(' ', '_')}", "purpose": f"删除{feature['name']}"}
                ],
                "lines_of_code": 150,
                "status": "completed"
            }
            code_modules.append(module)
        
        code_result = {
            "id": "code_001",
            "project_name": "系统后端服务",
            "modules": code_modules,
            "tech_stack": ["Python", "FastAPI", "SQLAlchemy"],
            "api_endpoints": [
                {"method": "GET", "path": "/api/v1/items", "description": "获取列表"},
                {"method": "POST", "path": "/api/v1/items", "description": "创建资源"},
                {"method": "GET", "path": "/api/v1/items/{id}", "description": "获取详情"},
                {"method": "PUT", "path": "/api/v1/items/{id}", "description": "更新资源"},
                {"method": "DELETE", "path": "/api/v1/items/{id}", "description": "删除资源"}
            ],
            "total_lines": sum(m["lines_of_code"] for m in code_modules),
            "status": "completed",
            "estimated_hours": 24
        }
        
        self.code_repository.append(code_result)
        print("[开发智能体] 代码编写完成")
        return code_result

    def create_api_endpoints(self, design: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[开发智能体] 创建API端点: {design.get('name', '')}")
        
        endpoints = []
        layers = design.get("layers", [])
        
        for layer in layers:
            for component in layer.get("components", []):
                endpoint = {
                    "name": component.lower().replace(" ", "_"),
                    "path": f"/api/v1/{component.lower().replace(' ', '_')}",
                    "methods": ["GET", "POST", "PUT", "DELETE"],
                    "layer": layer["name"],
                    "description": f"{layer['name']}层的{component}服务接口"
                }
                endpoints.append(endpoint)
        
        api_result = {
            "id": "api_001",
            "name": "系统API设计",
            "endpoints": endpoints,
            "version": "1.0.0",
            "authentication": "JWT",
            "rate_limit": "100 requests/minute",
            "status": "completed",
            "estimated_hours": 8
        }
        
        print("[开发智能体] API端点创建完成")
        return api_result

    def deploy_application(self, configuration: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[开发智能体] 部署应用: {configuration.get('name', '')}")
        
        deployment = {
            "id": "deploy_001",
            "name": "应用部署",
            "environment": configuration.get("environment", "production"),
            "status": "deploying",
            "steps": [
                {"step": "构建镜像", "status": "completed", "duration": "5分钟"},
                {"step": "推送镜像", "status": "completed", "duration": "2分钟"},
                {"step": "部署到K8s", "status": "completed", "duration": "3分钟"},
                {"step": "健康检查", "status": "completed", "duration": "1分钟"}
            ],
            "kubernetes": {
                "replicas": 3,
                "namespace": "default",
                "service_type": "LoadBalancer"
            },
            "status": "completed",
            "deployment_time": "11分钟",
            "url": "https://api.example.com"
        }
        
        self.deployment_history.append(deployment)
        print("[开发智能体] 应用部署完成")
        return deployment

    def fix_issue(self, issue_id: str, description: str) -> Dict[str, Any]:
        print(f"[开发智能体] 修复问题: {issue_id}")
        
        fix_result = {
            "issue_id": issue_id,
            "status": "fixed",
            "description": description,
            "fix_details": {
                "changed_files": ["todo_service.py", "api_handler.py"],
                "changes_made": ["修复了任务状态更新逻辑", "修复了API响应格式"],
                "tests_passed": True
            },
            "timestamp": "2024-01-01T12:00:00"
        }
        
        print("[开发智能体] 问题修复完成")
        return fix_result

    def notify_fix_complete(self, issue_id: str):
        if self.subscribers:
            self.send_message(
                receiver_id=self.subscribers[0],
                content={"issue_id": issue_id},
                message_type="fix_complete"
            )
        print(f"[开发智能体] 通知主智能体: 问题 {issue_id} 已修复")

    def process_task(self, task: Task) -> Any:
        print(f"[开发智能体] 处理任务: {task.name}")
        
        task.update_status("processing")
        
        if "修复" in task.name or "fix" in task.name.lower():
            issue_id = task.metadata.get("issue_id", "unknown")
            result = self.fix_issue(issue_id, task.description)
            
            self.notify_fix_complete(issue_id)
        elif "代码" in task.name or "code" in task.name.lower():
            result = self.write_code(task.metadata.get("requirements", {}))
        elif "API" in task.name or "endpoint" in task.name.lower():
            result = self.create_api_endpoints(task.metadata.get("design", {}))
        elif "部署" in task.name or "deploy" in task.name.lower():
            result = self.deploy_application(task.metadata.get("configuration", {}))
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