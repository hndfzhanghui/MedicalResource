# example.py

from datetime import datetime
from src.models.base import (
    Patient, Hospital, Vehicle, Location,
    PatientSeverity, PatientType, VehicleStatus
)
from src.algorithms.greedy_scheduler import GreedyScheduler

def main():
    # 创建调度器
    scheduler = GreedyScheduler()
    
    # 创建一些医院
    hospital1 = Hospital(
        id="H001",
        location=Location(x=0, y=0),
        resources={
            "呼吸机": 5,
            "手术室": 3,
            "ICU": 2
        },
        specialties=["外科", "内科"],
        capacity=100,
        available_beds=20
    )
    
    hospital2 = Hospital(
        id="H002",
        location=Location(x=10, y=10),
        resources={
            "呼吸机": 3,
            "手术室": 2,
            "烧伤科": 1
        },
        specialties=["烧伤科", "外科"],
        capacity=80,
        available_beds=15
    )
    
    # 注册医院
    scheduler.register_hospital(hospital1)
    scheduler.register_hospital(hospital2)
    
    # 创建一些救护车
    vehicle1 = Vehicle(
        id="V001",
        location=Location(x=5, y=5),
        capacity={
            PatientSeverity.RED: 1,
            PatientSeverity.YELLOW: 2,
            PatientSeverity.GREEN: 3
        },
        equipment=["呼吸机", "担架"],
        status=VehicleStatus.IDLE
    )
    
    vehicle2 = Vehicle(
        id="V002",
        location=Location(x=15, y=15),
        capacity={
            PatientSeverity.RED: 1,
            PatientSeverity.YELLOW: 1,
            PatientSeverity.GREEN: 2
        },
        equipment=["担架"],
        status=VehicleStatus.IDLE
    )
    
    # 注册车辆
    scheduler.register_vehicle(vehicle1)
    scheduler.register_vehicle(vehicle2)
    
    # 创建一些伤员
    patient1 = Patient(
        id="P001",
        location=Location(x=3, y=4),
        severity=PatientSeverity.RED,
        injury_type=PatientType.TRAUMA,
        discovery_time=datetime.now(),
        special_equipment_needed=["呼吸机"]
    )
    
    patient2 = Patient(
        id="P002",
        location=Location(x=12, y=12),
        severity=PatientSeverity.YELLOW,
        injury_type=PatientType.BURN,
        discovery_time=datetime.now(),
        special_equipment_needed=[]
    )
    
    # 添加伤员并触发调度
    print("添加第一个伤员（重伤）...")
    scheduler.add_patient(patient1)
    print_assignment_details(scheduler, patient1.id)
    
    print("\n添加第二个伤员（中度烧伤）...")
    scheduler.add_patient(patient2)
    print_assignment_details(scheduler, patient2.id)
    
    # 模拟交通状况变化
    print("\n交通状况发生变化（拥堵）...")
    scheduler.update_traffic_condition(1.5)
    print("更新后的分配方案：")
    print_assignment_details(scheduler, patient1.id)
    print_assignment_details(scheduler, patient2.id)

def print_assignment_details(scheduler: GreedyScheduler, patient_id: str):
    """打印分配方案详情"""
    details = scheduler.get_assignment_details(patient_id)
    if details:
        print(f"\n病人 {details['patient_id']} ({details['patient_severity'].name}) 的分配方案：")
        print(f"- 分配的救护车: {details['vehicle_id']}")
        print(f"- 分配的医院: {details['hospital_id']}")
        print(f"- 预计接诊时间: {details['estimated_pickup_time']:.2f} 小时")
        print(f"- 预计运送时间: {details['estimated_transport_time']:.2f} 小时")
        print(f"- 总预计时间: {details['total_estimated_time']:.2f} 小时")
    else:
        print(f"\n病人 {patient_id} 暂未分配方案")

if __name__ == "__main__":
    main() 