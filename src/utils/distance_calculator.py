# distance_calculator.py

from typing import Dict, Tuple
import numpy as np
from datetime import datetime, timedelta
from src.models.base import Location, PatientSeverity

class DistanceCalculator:
    def __init__(self, traffic_factor: float = 1.0):
        """
        初始化距离计算器
        :param traffic_factor: 交通系数，>1表示拥堵，<1表示通畅
        """
        self.traffic_factor = traffic_factor
        self.average_speed = 50.0  # 平均速度（公里/小时）
        
        # 不同伤情等级的装卸时间（分钟）
        self.loading_times = {
            PatientSeverity.RED: 10,
            PatientSeverity.YELLOW: 7,
            PatientSeverity.GREEN: 5
        }
    
    def calculate_travel_time(self, start: Location, end: Location) -> float:
        """
        计算两点间的预计行驶时间（小时）
        """
        distance = start.distance_to(end)  # 假设返回的是公里数
        return (distance / self.average_speed) * self.traffic_factor
    
    def estimate_total_transport_time(
        self,
        pickup_location: Location,
        hospital_location: Location,
        severity: PatientSeverity
    ) -> float:
        """
        估算总运输时间（小时），包括装卸时间
        """
        travel_time = self.calculate_travel_time(pickup_location, hospital_location)
        loading_time = self.loading_times[severity] / 60.0  # 转换为小时
        
        return travel_time + loading_time
    
    def update_traffic_factor(self, new_factor: float):
        """
        更新交通系数
        """
        self.traffic_factor = new_factor
    
    def get_estimated_arrival_time(
        self,
        start_time: datetime,
        start_location: Location,
        end_location: Location
    ) -> datetime:
        """
        计算预计到达时间
        """
        travel_time = self.calculate_travel_time(start_location, end_location)
        travel_delta = timedelta(hours=travel_time)
        return start_time + travel_delta 