# base.py
# 基础模型，定义了伤员、医院、车辆、位置等基本概念

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Tuple
import numpy as np
from datetime import datetime

class PatientSeverity(Enum):
    RED = 3    # 危重伤员
    YELLOW = 2 # 中度伤员
    GREEN = 1  # 轻度伤员

class PatientType(Enum):
    TRAUMA = "外伤"
    BURN = "烧伤"
    INTERNAL = "内科"
    OTHER = "其他"

class VehicleStatus(Enum):
    IDLE = "空闲"
    BUSY = "任务中"
    RETURNING = "返回中"

@dataclass
class Location:
    x: float  # 经度
    y: float  # 纬度
    
    def distance_to(self, other: 'Location') -> float:
        """计算两点之间的欧氏距离"""
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

@dataclass
class Patient:
    id: str
    location: Location
    severity: PatientSeverity
    injury_type: PatientType
    discovery_time: datetime
    special_equipment_needed: List[str] = None
    estimated_treatment_time: float = 0.0  # 预计治疗时间（小时）
    
    def __post_init__(self):
        if self.special_equipment_needed is None:
            self.special_equipment_needed = []

@dataclass
class Hospital:
    id: str
    location: Location
    resources: Dict[str, int]  # 资源类型：数量
    specialties: List[str]     # 专科类型
    capacity: int             # 总床位数
    available_beds: int       # 可用床位数
    
    def has_required_equipment(self, equipment_list: List[str]) -> bool:
        """检查是否具备所需的特殊设备"""
        return all(self.resources.get(equip, 0) > 0 for equip in equipment_list)
    
    def can_accept_patient(self, patient: Patient) -> bool:
        """检查是否能接收特定伤员"""
        if self.available_beds <= 0:
            return False
        if patient.special_equipment_needed:
            return self.has_required_equipment(patient.special_equipment_needed)
        return True

@dataclass
class Vehicle:
    id: str
    location: Location
    capacity: Dict[PatientSeverity, int]  # 不同等级伤员的容量
    equipment: List[str]                  # 车载设备
    status: VehicleStatus = VehicleStatus.IDLE
    current_patients: List[Patient] = None
    
    def __post_init__(self):
        if self.current_patients is None:
            self.current_patients = []
    
    def can_accommodate(self, patient: Patient) -> bool:
        """检查是否能容纳新的伤员"""
        if self.status != VehicleStatus.IDLE:
            return False
            
        current_count = sum(1 for p in self.current_patients 
                          if p.severity == patient.severity)
        max_capacity = self.capacity.get(patient.severity, 0)
        
        if current_count >= max_capacity:
            return False
            
        if patient.special_equipment_needed:
            return all(equip in self.equipment 
                      for equip in patient.special_equipment_needed)
        
        return True 