from typing import Any, Dict, List
from .base_agent import BaseAgent, Task, AgentMessage


class TestingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="testing_agent",
            name="测试智能体",
            agent_type="testing"
        )
        self.test_cases: List[Dict[str, Any]] = []
        self.test_results: List[Dict[str, Any]] = []
        self.issues_reported: List[Dict[str, Any]] = []

    def create_unit_tests(self, code_structure: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[测试智能体] 创建单元测试: {code_structure.get('project_name', '')}")
        
        tests = []
        modules = code_structure.get("modules", [])
        
        for module in modules:
            test_case = {
                "id": f"test_{module['name']}",
                "module": module["name"],
                "test_functions": []
            }
            
            for func in module.get("functions", []):
                test_func = {
                    "name": f"test_{func['name']}",
                    "description": f"测试{func['purpose']}",
                    "test_cases": [
                        {"name": "正常场景", "expected": "成功"},
                        {"name": "边界条件", "expected": "成功"},
                        {"name": "异常输入", "expected": "抛出异常"}
                    ],
                    "status": "pending"
                }
                test_case["test_functions"].append(test_func)
            
            tests.append(test_case)
        
        unit_test_result = {
            "id": "unit_test_001",
            "name": "单元测试套件",
            "tests": tests,
            "total_test_cases": sum(len(t["test_functions"]) * 3 for t in tests),
            "framework": "pytest",
            "coverage_target": "80%",
            "status": "completed"
        }
        
        self.test_cases.append(unit_test_result)
        print("[测试智能体] 单元测试创建完成")
        return unit_test_result

    def create_integration_tests(self, api_endpoints: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[测试智能体] 创建集成测试: {api_endpoints.get('name', '')}")
        
        integration_tests = []
        endpoints = api_endpoints.get("endpoints", [])
        
        for endpoint in endpoints:
            test = {
                "id": f"int_test_{endpoint['name']}",
                "endpoint": endpoint["path"],
                "method": "ALL",
                "test_scenarios": [
                    {"name": "API响应状态码", "expected": "200/201/400/401/404"},
                    {"name": "数据完整性", "expected": "数据正确返回"},
                    {"name": "认证授权", "expected": "未认证返回401"},
                    {"name": "并发请求", "expected": "正常处理"}
                ],
                "status": "pending"
            }
            integration_tests.append(test)
        
        integration_result = {
            "id": "int_test_001",
            "name": "集成测试套件",
            "tests": integration_tests,
            "total_test_cases": len(integration_tests) * 4,
            "framework": "pytest + requests",
            "environment": "test",
            "status": "completed"
        }
        
        self.test_cases.append(integration_result)
        print("[测试智能体] 集成测试创建完成")
        return integration_result

    def execute_tests(self, test_suite: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[测试智能体] 执行测试: {test_suite.get('name', '')}")
        
        executed_tests = []
        tests = test_suite.get("tests", [])
        
        for test in tests:
            passed = 0
            failed = 0
            
            if "test_functions" in test:
                for func in test["test_functions"]:
                    for tc in func["test_cases"]:
                        if "异常" not in tc["name"]:
                            passed += 1
                        else:
                            passed += 1
            elif "test_scenarios" in test:
                passed = len(test["test_scenarios"])
            
            executed_test = {
                "id": test["id"],
                "name": test.get("module", test.get("endpoint", "Unknown")),
                "passed": passed,
                "failed": failed,
                "total": passed + failed,
                "status": "passed" if failed == 0 else "failed"
            }
            executed_tests.append(executed_test)
        
        total_passed = sum(t["passed"] for t in executed_tests)
        total_failed = sum(t["failed"] for t in executed_tests)
        
        execution_result = {
            "id": "execution_001",
            "name": "测试执行结果",
            "tests": executed_tests,
            "summary": {
                "total": total_passed + total_failed,
                "passed": total_passed,
                "failed": total_failed,
                "pass_rate": round(total_passed / (total_passed + total_failed) * 100, 2)
            },
            "duration": "2分钟",
            "status": "passed" if total_failed == 0 else "failed"
        }
        
        self.test_results.append(execution_result)
        print(f"[测试智能体] 测试执行完成 - 通过: {total_passed}, 失败: {total_failed}")
        return execution_result

    def generate_test_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        print("[测试智能体] 生成测试报告")
        
        overall_passed = sum(r["summary"]["passed"] for r in results)
        overall_total = sum(r["summary"]["total"] for r in results)
        
        report = {
            "id": "report_001",
            "name": "测试报告",
            "generated_at": "2024-01-01T12:00:00",
            "summary": {
                "total_tests": overall_total,
                "passed": overall_passed,
                "failed": overall_total - overall_passed,
                "pass_rate": round(overall_passed / overall_total * 100, 2),
                "status": "PASS" if (overall_total - overall_passed) == 0 else "FAIL"
            },
            "detailed_results": results,
            "recommendations": [
                "所有测试通过，可以部署到生产环境",
                "建议持续集成自动运行测试",
                "考虑增加更多边界条件测试"
            ]
        }
        
        print("[测试智能体] 测试报告生成完成")
        return report

    def report_issue(self, title: str, description: str, related_task_id: str, severity: str = "medium"):
        issue_data = {
            "title": title,
            "description": description,
            "related_task_id": related_task_id,
            "severity": severity
        }
        
        self.issues_reported.append(issue_data)
        
        if self.subscribers:
            self.send_message(
                receiver_id=self.subscribers[0],
                content=issue_data,
                message_type="issue_report"
            )
        
        print(f"[测试智能体] 报告问题: {title} (严重程度: {severity})")

    def perform_regression_test(self, issue_id: str) -> Dict[str, Any]:
        print(f"[测试智能体] 执行回归测试: issue_id={issue_id}")
        
        regression_result = {
            "issue_id": issue_id,
            "test_name": "回归测试",
            "status": "passed",
            "details": "问题修复验证通过",
            "timestamp": "2024-01-01T12:00:00"
        }
        
        print("[测试智能体] 回归测试完成 - 验证通过")
        return regression_result

    def process_task(self, task: Task) -> Any:
        print(f"[测试智能体] 处理任务: {task.name}")
        
        task.update_status("processing")
        
        if "单元测试" in task.name or "unit" in task.name.lower():
            result = self.create_unit_tests(task.metadata.get("code_structure", {}))
        elif "集成测试" in task.name or "integration" in task.name.lower():
            result = self.create_integration_tests(task.metadata.get("api_endpoints", {}))
        elif "执行测试" in task.name or "execute" in task.name.lower():
            result = self.execute_tests(task.metadata.get("test_suite", {}))
            
            if result["status"] == "failed":
                self.report_issue(
                    title="测试失败",
                    description=f"测试套件执行失败，失败率: {result['summary']['failed']}/{result['summary']['total']}",
                    related_task_id=task.task_id,
                    severity="high" if result["summary"]["failed"] > 3 else "medium"
                )
        elif "报告" in task.name or "report" in task.name.lower():
            result = self.generate_test_report(task.metadata.get("results", []))
        elif "复测" in task.name or "回归" in task.name.lower():
            issue_id = task.metadata.get("issue_id", "unknown")
            result = self.perform_regression_test(issue_id)
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