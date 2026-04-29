from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import uuid
from datetime import datetime


class Task:
    def __init__(self, task_id: str, name: str, description: str, 
                 agent_type: str, priority: int = 0, 
                 dependencies: List[str] = None, metadata: Dict[str, Any] = None):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.agent_type = agent_type
        self.priority = priority
        self.dependencies = dependencies or []
        self.metadata = metadata or {}
        self.status = "pending"
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.assignee = None
        self.result = None

    def update_status(self, status: str):
        self.status = status
        self.updated_at = datetime.now()

    def set_result(self, result: Any):
        self.result = result
        self.status = "completed"
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "agent_type": self.agent_type,
            "priority": self.priority,
            "dependencies": self.dependencies,
            "metadata": self.metadata,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "assignee": self.assignee,
            "result": self.result
        }


class AgentMessage:
    def __init__(self, sender_id: str, receiver_id: str, content: Any, 
                 message_type: str = "task", task_id: Optional[str] = None):
        self.message_id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.message_type = message_type
        self.task_id = task_id
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "message_type": self.message_type,
            "task_id": self.task_id,
            "timestamp": self.timestamp.isoformat()
        }


class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, agent_type: str):
        self.agent_id = agent_id
        self.name = name
        self.agent_type = agent_type
        self.is_running = False
        self.task_queue: List[Task] = []
        self.message_history: List[AgentMessage] = []
        self.subscribers: List[str] = []
        self.agent_manager = None

    @abstractmethod
    def process_task(self, task: Task) -> Any:
        pass

    @abstractmethod
    def handle_message(self, message: AgentMessage):
        pass

    def add_task(self, task: Task):
        self.task_queue.append(task)

    def remove_task(self, task_id: str):
        self.task_queue = [t for t in self.task_queue if t.task_id != task_id]

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        return next((t for t in self.task_queue if t.task_id == task_id), None)

    def send_message(self, receiver_id: str, content: Any, 
                     message_type: str = "task", task_id: Optional[str] = None):
        message = AgentMessage(
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            content=content,
            message_type=message_type,
            task_id=task_id
        )
        self.message_history.append(message)
        
        receiver_agent = None
        
        if self.agent_manager:
            if receiver_id in self.agent_manager.agents:
                receiver_agent = self.agent_manager.agents[receiver_id]
            elif self.agent_manager.agent_id == receiver_id:
                receiver_agent = self.agent_manager
        
        if receiver_agent:
            receiver_agent.handle_message(message)
        
        return message

    def subscribe(self, agent_id: str):
        if agent_id not in self.subscribers:
            self.subscribers.append(agent_id)

    def unsubscribe(self, agent_id: str):
        if agent_id in self.subscribers:
            self.subscribers.remove(agent_id)

    def broadcast(self, content: Any, message_type: str = "broadcast"):
        messages = []
        for subscriber_id in self.subscribers:
            message = self.send_message(subscriber_id, content, message_type)
            messages.append(message)
        return messages

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "agent_type": self.agent_type,
            "is_running": self.is_running,
            "queue_size": len(self.task_queue),
            "subscribers_count": len(self.subscribers)
        }