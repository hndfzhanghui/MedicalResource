# 医疗资源动态调度系统

这是一个用于突发事件后的医疗资源动态调度系统，可以根据伤员情况、医院资源和交通状况，实时优化救护车调度和医院分配方案。

## 功能特点

- 支持多级别伤员优先级（红、黄、绿）
- 考虑医院特殊资源和专科能力
- 考虑救护车容量和设备限制
- 实时响应交通状况变化
- 动态调整调度方案

## 安装

1. 克隆项目：
```bash
git clone [项目地址]
cd medical-resource-scheduler
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 基本使用示例：

```python
from src.models.base import Patient, Hospital, Vehicle, Location
from src.algorithms.greedy_scheduler import GreedyScheduler

# 创建调度器
scheduler = GreedyScheduler()

# 注册医院和车辆
scheduler.register_hospital(hospital)
scheduler.register_vehicle(vehicle)

# 添加伤员并触发调度
scheduler.add_patient(patient)

# 获取调度结果
assignment = scheduler.get_assignment_details(patient.id)
```

2. 运行示例程序：

```bash
python src/example.py
```

## 项目结构

```
medical-resource-scheduler/
├── src/
│   ├── models/          # 数据模型定义
│   ├── algorithms/      # 调度算法实现
│   ├── utils/          # 工具函数
│   └── example.py      # 使用示例
├── tests/              # 测试文件
├── requirements.txt    # 项目依赖
└── README.md          # 项目文档
```

## 配置说明

1. 伤员优先级：
- RED（红）：危重伤员，最高优先级
- YELLOW（黄）：中度伤员，中等优先级
- GREEN（绿）：轻度伤员，低优先级

2. 医院资源：
- 可配置不同类型的医疗资源（床位、设备等）
- 可设置专科能力
- 支持动态更新资源状态

3. 救护车配置：
- 可设置不同等级伤员的运载容量
- 可配置车载医疗设备
- 支持实时位置更新

## 开发计划

- [ ] 添加更多调度算法（遗传算法、强化学习等）
- [ ] 支持多目标优化
- [ ] 添加可视化界面
- [ ] 支持历史数据分析
- [ ] 添加预测模型

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License 