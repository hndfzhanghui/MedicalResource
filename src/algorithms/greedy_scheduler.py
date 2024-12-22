# greedy_scheduler.py

from typing import Dict, Tuple, List
from src.algorithms.base_scheduler import BaseScheduler
from src.models.base import Patient, Hospital, Vehicle, PatientSeverity, VehicleStatus

class GreedyScheduler(BaseScheduler):
    def schedule(self) -> Dict[str, Tuple[Vehicle, Hospital]]:
        """
        使用贪心策略进行调度：
        1. 按优先级对病人排序
        2. 对每个病人，找到最佳的车辆-医院组合
        """
        # 获取未分配的病人
        unassigned_patients = [
            p for p in self.patients 
            if p.id not in self.assignments
        ]
        
        # 按优先级排序
        unassigned_patients.sort(
            key=lambda p: self.calculate_priority_score(p),
            reverse=True
        )
        
        new_assignments = {}
        
        for patient in unassigned_patients:
            best_assignment = self._find_best_assignment(patient)
            if best_assignment:
                vehicle, hospital = best_assignment
                new_assignments[patient.id] = best_assignment
                # 更新车辆状态
                vehicle.status = VehicleStatus.BUSY
                vehicle.current_patients.append(patient)
                # 更新医院资源
                hospital.available_beds -= 1
        
        # 更新总体分配方案
        self.assignments.update(new_assignments)
        return new_assignments
    
    def _find_best_assignment(
        self,
        patient: Patient
    ) -> Tuple[Vehicle, Hospital]:
        """
        为指定病人找到最佳的车辆-医院组合
        """
        available_vehicles = self.get_available_vehicles()
        suitable_hospitals = self.get_suitable_hospitals(patient)
        
        if not available_vehicles or not suitable_hospitals:
            return None
        
        best_score = float('inf')
        best_assignment = None
        
        for vehicle in available_vehicles:
            if not vehicle.can_accommodate(patient):
                continue
                
            for hospital in suitable_hospitals:
                score = self.evaluate_assignment(patient, vehicle, hospital)
                
                if score < best_score:
                    best_score = score
                    best_assignment = (vehicle, hospital)
        
        return best_assignment
    
    def get_assignment_details(self, patient_id: str) -> dict:
        """
        获取特定病人的分配方案详情
        """
        assignment = self.assignments.get(patient_id)
        if not assignment:
            return None
            
        vehicle, hospital = assignment
        patient = next(p for p in self.patients if p.id == patient_id)
        
        # 计算时间估计
        pickup_time = self.distance_calculator.calculate_travel_time(
            vehicle.location,
            patient.location
        )
        transport_time = self.distance_calculator.calculate_travel_time(
            patient.location,
            hospital.location
        )
        
        return {
            "patient_id": patient_id,
            "patient_severity": patient.severity,
            "vehicle_id": vehicle.id,
            "hospital_id": hospital.id,
            "estimated_pickup_time": pickup_time,
            "estimated_transport_time": transport_time,
            "total_estimated_time": pickup_time + transport_time
        } 