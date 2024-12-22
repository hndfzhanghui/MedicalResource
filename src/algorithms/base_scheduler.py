# base_scheduler.py

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional
from datetime import datetime

from src.models.base import Patient, Hospital, Vehicle, PatientSeverity, VehicleStatus
from src.utils.distance_calculator import DistanceCalculator

class BaseScheduler(ABC):
    def __init__(self):
        self.distance_calculator = DistanceCalculator()
        self.hospitals: List[Hospital] = []
        self.vehicles: List[Vehicle] = []
        self.patients: List[Patient] = []
        self.assignments: Dict[str, Tuple[Vehicle, Hospital]] = {}  # patient_id -> (vehicle, hospital)
    
    def register_hospital(self, hospital: Hospital):
        """注册医院"""
        self.hospitals.append(hospital)
    
    def register_vehicle(self, vehicle: Vehicle):
        """注册车辆"""
        self.vehicles.append(vehicle)
    
    def add_patient(self, patient: Patient):
        """添加新的伤员"""
        self.patients.append(patient)
        # 触发重新调度
        self.schedule()
    
    def get_available_vehicles(self) -> List[Vehicle]:
        """获取可用车辆列表"""
        return [v for v in self.vehicles if v.status == VehicleStatus.IDLE]
    
    def get_suitable_hospitals(self, patient: Patient) -> List[Hospital]:
        """获取适合的医院列表"""
        return [h for h in self.hospitals if h.can_accept_patient(patient)]
    
    def calculate_priority_score(self, patient: Patient) -> float:
        """计算伤员优先级分数"""
        severity_scores = {
            PatientSeverity.RED: 100,
            PatientSeverity.YELLOW: 50,
            PatientSeverity.GREEN: 10
        }
        
        base_score = severity_scores[patient.severity]
        wait_time = (datetime.now() - patient.discovery_time).total_seconds() / 3600.0
        
        # 等待时间越长，分数越高
        return base_score * (1 + 0.1 * wait_time)
    
    def evaluate_assignment(
        self,
        patient: Patient,
        vehicle: Vehicle,
        hospital: Hospital
    ) -> float:
        """
        评估一个分配方案的得分
        返回值越小越好
        """
        # 计算总时间成本
        pickup_time = self.distance_calculator.calculate_travel_time(
            vehicle.location,
            patient.location
        )
        transport_time = self.distance_calculator.calculate_travel_time(
            patient.location,
            hospital.location
        )
        total_time = pickup_time + transport_time
        
        # 根据伤员严重程度调整时间权重
        severity_weights = {
            PatientSeverity.RED: 3.0,
            PatientSeverity.YELLOW: 2.0,
            PatientSeverity.GREEN: 1.0
        }
        
        weighted_time = total_time * severity_weights[patient.severity]
        
        return weighted_time
    
    @abstractmethod
    def schedule(self) -> Dict[str, Tuple[Vehicle, Hospital]]:
        """
        执行调度算法
        返回：病人ID -> (分配的车辆, 分配的医院) 的字典
        """
        pass
    
    def update_traffic_condition(self, traffic_factor: float):
        """更新交通状况"""
        self.distance_calculator.update_traffic_factor(traffic_factor)
        # 触发重新调度
        self.schedule()
    
    def get_patient_status(self, patient_id: str) -> Optional[Tuple[Vehicle, Hospital]]:
        """获取病人的分配状态"""
        return self.assignments.get(patient_id)