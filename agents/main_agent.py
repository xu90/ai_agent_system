from typing import Any, Dict, Optional, List
import uuid
from .base_agent import BaseAgent, Task, AgentMessage


class Issue:
    def __init__(self, issue_id: str, title: str, description: str, 
                 reporter_id: str, related_task_id: str, severity: str = "medium"):
        self.issue_id = issue_id
        self.title = title
        self.description = description
        self.reporter_id = reporter_id
        self.related_task_id = related_task_id
        self.severity = severity
        self.status = "open"
        self.assigned_developer_id = None
        self.fix_task_id = None
        self.review_task_id = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "title": self.title,
            "description": self.description,
            "reporter_id": self.reporter_id,
            "related_task_id": self.related_task_id,
            "severity": self.severity,
            "status": self.status,
            "assigned_developer_id": self.assigned_developer_id,
            "fix_task_id": self.fix_task_id,
            "review_task_id": self.review_task_id
        }


class MainAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="main_agent",
            name="主智能体",
            agent_type="main"
        )
        self.agents: Dict[str, BaseAgent] = {}
        self.task_registry: Dict[str, Task] = {}
        self.execution_history: List[Dict[str, Any]] = []
        
        self.task_agent_map: Dict[str, str] = {}
        self.issues: Dict[str, Issue] = {}

    def register_agent(self, agent: BaseAgent):
        if agent.agent_id not in self.agents:
            self.agents[agent.agent_id] = agent
            agent.subscribe(self.agent_id)
            agent.agent_manager = self
            print(f"[主智能体] 已注册智能体: {agent.name} ({agent.agent_id})")

    def unregister_agent(self, agent_id: str):
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            agent.unsubscribe(self.agent_id)
            print(f"[主智能体] 已注销智能体: {agent.name} ({agent_id})")

    def get_agent_by_type(self, agent_type: str) -> Optional[BaseAgent]:
        for agent in self.agents.values():
            if agent.agent_type == agent_type:
                return agent
        return None

    def get_agent_by_id(self, agent_id: str) -> Optional[BaseAgent]:
        return self.agents.get(agent_id)

    def create_task(self, name: str, description: str, agent_type: str, 
                    priority: int = 0, dependencies: List[str] = None, 
                    metadata: Dict[str, Any] = None) -> Task:
        task_id = str(uuid.uuid4())
        task = Task(
            task_id=task_id,
            name=name,
            description=description,
            agent_type=agent_type,
            priority=priority,
            dependencies=dependencies or [],
            metadata=metadata or {}
        )
        self.task_registry[task_id] = task
        print(f"[主智能体] 创建任务: {name} ({task_id})")
        return task

    def dispatch_task(self, task: Task) -> bool:
        target_agent = self.get_agent_by_type(task.agent_type)
        if not target_agent:
            print(f"[主智能体] 错误: 未找到类型为 {task.agent_type} 的智能体")
            return False

        if not self._check_dependencies(task):
            print(f"[主智能体] 任务 {task.name} 依赖未满足，暂不调度")
            return False

        task.update_status("dispatched")
        task.assignee = target_agent.agent_id
        
        self.task_agent_map[task.task_id] = target_agent.agent_id
        
        message = self.send_message(
            receiver_id=target_agent.agent_id,
            content=task.to_dict(),
            message_type="task",
            task_id=task.task_id
        )
        
        target_agent.add_task(task)
        print(f"[主智能体] 任务 {task.name} 已分配给 {target_agent.name}")
        
        target_agent.process_task(task)
        
        return True

    def _check_dependencies(self, task: Task) -> bool:
        for dep_task_id in task.dependencies:
            dep_task = self.task_registry.get(dep_task_id)
            if not dep_task or dep_task.status != "completed":
                return False
        return True

    def process_task(self, task: Task) -> Any:
        print(f"[主智能体] 处理任务: {task.name}")
        return {"status": "processed", "task_id": task.task_id}

    def handle_message(self, message: AgentMessage):
        self.message_history.append(message)
        
        if message.message_type == "task_result":
            self._handle_task_result(message)
        elif message.message_type == "status":
            self._handle_status_update(message)
        elif message.message_type == "broadcast":
            self._handle_broadcast(message)
        elif message.message_type == "issue_report":
            self._handle_issue_report(message)
        elif message.message_type == "fix_complete":
            self._handle_fix_complete(message)

    def _handle_task_result(self, message: AgentMessage):
        task_id = message.task_id
        if task_id in self.task_registry:
            task = self.task_registry[task_id]
            task.set_result(message.content)
            
            execution_record = {
                "task_id": task_id,
                "task_name": task.name,
                "assignee": task.assignee,
                "completed_at": task.updated_at.isoformat(),
                "result": message.content
            }
            self.execution_history.append(execution_record)
            
            print(f"[主智能体] 收到任务结果: {task.name} - 状态: 已完成")
            
            self._check_and_dispatch_pending_tasks()

    def _handle_status_update(self, message: AgentMessage):
        print(f"[主智能体] 收到状态更新: {message.sender_id} - {message.content}")

    def _handle_broadcast(self, message: AgentMessage):
        print(f"[主智能体] 收到广播消息: {message.sender_id} - {message.content}")

    def _handle_issue_report(self, message: AgentMessage):
        issue_data = message.content
        issue_id = str(uuid.uuid4())
        
        issue = Issue(
            issue_id=issue_id,
            title=issue_data["title"],
            description=issue_data["description"],
            reporter_id=message.sender_id,
            related_task_id=issue_data["related_task_id"],
            severity=issue_data.get("severity", "medium")
        )
        self.issues[issue_id] = issue
        
        print(f"[主智能体] 收到问题报告: {issue.title} (严重程度: {issue.severity})")
        
        self._resolve_issue(issue)

    def _resolve_issue(self, issue: Issue):
        related_task_id = issue.related_task_id
        
        if related_task_id in self.task_agent_map:
            original_developer_id = self.task_agent_map[related_task_id]
            issue.assigned_developer_id = original_developer_id
            
            print(f"[主智能体] 找到原开发智能体: {original_developer_id}")
            print(f"[主智能体] 分配修复任务给开发智能体")
            
            fix_task = self.create_task(
                name=f"修复问题: {issue.title}",
                description=issue.description,
                agent_type="development",
                priority=10 if issue.severity == "high" else 5,
                metadata={"issue_id": issue.issue_id, "related_task_id": related_task_id}
            )
            issue.fix_task_id = fix_task.task_id
            
            self.dispatch_task(fix_task)
        else:
            print(f"[主智能体] 无法找到相关任务的开发智能体: {related_task_id}")

    def _handle_fix_complete(self, message: AgentMessage):
        issue_id = message.content.get("issue_id")
        if issue_id in self.issues:
            issue = self.issues[issue_id]
            issue.status = "fixed"
            
            print(f"[主智能体] 问题 {issue.title} 已修复，安排复测")
            
            review_task = self.create_task(
                name=f"复测问题: {issue.title}",
                description=f"对问题'{issue.title}'进行回归测试验证修复效果",
                agent_type="testing",
                priority=8,
                metadata={"issue_id": issue_id, "reporter_id": issue.reporter_id}
            )
            issue.review_task_id = review_task.task_id
            
            self.dispatch_task(review_task)

    def _check_and_dispatch_pending_tasks(self):
        pending_tasks = [t for t in self.task_registry.values() if t.status == "pending"]
        for task in sorted(pending_tasks, key=lambda t: t.priority, reverse=True):
            if self._check_dependencies(task):
                self.dispatch_task(task)

    def execute_workflow(self, workflow: List[Dict[str, Any]]):
        print("[主智能体] 开始执行工作流...")
        
        tasks = []
        for task_def in workflow:
            task = self.create_task(
                name=task_def["name"],
                description=task_def["description"],
                agent_type=task_def["agent_type"],
                priority=task_def.get("priority", 0),
                dependencies=task_def.get("dependencies", []),
                metadata=task_def.get("metadata", {})
            )
            tasks.append(task)
        
        for task in tasks:
            self.dispatch_task(task)

    def get_system_status(self) -> Dict[str, Any]:
        return {
            "main_agent": self.get_status(),
            "registered_agents": {
                agent_id: agent.get_status() for agent_id, agent in self.agents.items()
            },
            "task_summary": {
                "total": len(self.task_registry),
                "pending": sum(1 for t in self.task_registry.values() if t.status == "pending"),
                "dispatched": sum(1 for t in self.task_registry.values() if t.status == "dispatched"),
                "completed": sum(1 for t in self.task_registry.values() if t.status == "completed")
            },
            "open_issues": len([i for i in self.issues.values() if i.status == "open"]),
            "execution_history": self.execution_history
        }