from agents import (
    MainAgent,
    CreativeAgent,
    DesignAgent,
    DevelopmentAgent,
    TestingAgent
)


def main():
    print("=" * 70)
    print("     AI智能体协同系统 - 待办事项列表项目开发演示")
    print("=" * 70)

    main_agent = MainAgent()
    creative_agent = CreativeAgent()
    design_agent = DesignAgent()
    development_agent = DevelopmentAgent()
    testing_agent = TestingAgent()

    main_agent.register_agent(creative_agent)
    main_agent.register_agent(design_agent)
    main_agent.register_agent(development_agent)
    main_agent.register_agent(testing_agent)

    print("\n[系统] 所有智能体已注册完成")
    print(f"[系统] 已注册 {len(main_agent.agents)} 个专业智能体")

    for agent_id, agent in main_agent.agents.items():
        print(f"  - {agent.name} ({agent.agent_id})")

    main_agent.start()
    creative_agent.start()
    design_agent.start()
    development_agent.start()
    testing_agent.start()

    print("\n[系统] 所有智能体已启动")
    print("=" * 60)

    workflow = [
        {
            "name": "待办事项需求分析",
            "description": "分析待办事项列表应用需求：添加任务、标记完成、删除任务、任务列表展示",
            "agent_type": "creative",
            "priority": 10,
            "metadata": {"project": "待办事项列表"}
        },
        {
            "name": "待办系统架构设计",
            "description": "设计待办事项系统三层架构：前端展示、API服务、数据存储",
            "agent_type": "design",
            "priority": 9,
            "metadata": {"project": "待办事项列表"}
        },
        {
            "name": "待办UI界面设计",
            "description": "设计待办事项界面：输入框、任务列表、完成状态切换、删除按钮",
            "agent_type": "design",
            "priority": 8,
            "metadata": {"project": "待办事项列表"}
        },
        {
            "name": "待办代码实现",
            "description": "实现待办事项核心功能：Task类、任务管理逻辑",
            "agent_type": "development",
            "priority": 7,
            "metadata": {"project": "待办事项列表"}
        },
        {
            "name": "待办API开发",
            "description": "开发待办事项RESTful API：GET/POST/PUT/DELETE /api/todos",
            "agent_type": "development",
            "priority": 6,
            "metadata": {"project": "待办事项列表"}
        },
        {
            "name": "待办单元测试",
            "description": "编写待办事项核心功能单元测试用例",
            "agent_type": "testing",
            "priority": 5,
            "metadata": {"project": "待办事项列表"}
        },
        {
            "name": "待办集成测试",
            "description": "编写待办事项API集成测试用例",
            "agent_type": "testing",
            "priority": 4,
            "metadata": {"project": "待办事项列表"}
        }
    ]

    print("\n[系统] 开始执行工作流...")
    print("=" * 60)

    main_agent.execute_workflow(workflow)

    print("\n" + "=" * 70)
    print("     待办事项列表项目 - 开发流程执行完成")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("     演示: 问题反馈与修复流程")
    print("=" * 70)

    print("\n[系统] 测试智能体发现问题，向主智能体报告...")
    print("=" * 60)
    
    todo_code_task_id = next(
        (t.task_id for t in main_agent.task_registry.values() if "待办代码实现" in t.name),
        None
    )
    
    if todo_code_task_id:
        testing_agent.report_issue(
            title="删除任务功能异常",
            description="测试发现删除任务后，任务列表没有正确更新，已删除的任务仍显示在列表中",
            related_task_id=todo_code_task_id,
            severity="high"
        )

    print("\n" + "=" * 70)
    print("     待办事项列表项目 - 完整流程执行完成")
    print("=" * 70)

    status = main_agent.get_system_status()
    
    print("\n[系统状态摘要]")
    print(f"  总任务数: {status['task_summary']['total']}")
    print(f"  待处理: {status['task_summary']['pending']}")
    print(f"  已调度: {status['task_summary']['dispatched']}")
    print(f"  已完成: {status['task_summary']['completed']}")
    print(f"  待处理问题: {status['open_issues']}")

    print("\n[执行历史]")
    for record in status['execution_history']:
        print(f"  - {record['task_name']}: 已完成")

    print("\n[系统] 工作流执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()