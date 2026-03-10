
import time
import random
import pandas as pd
import numpy as np
from datetime import datetime

class DigitalTwinController:
    """
    High-Fidelity Digital Twin Controller for Virtual Data Centers.
    
    Features:
    - Bi-Directional Sync (Redfish/IPMI Mock)
    - Spatial 3D Physics Simulation (Thermal CFD approximation)
    - Predictive Multi-Node Optimization
    """
    
    def __init__(self):
        self.connected = False
        self.sync_active = False
        self.rack_state = {
            f"Server_{i}": {
                "id": f"srv_{i:02d}",
                "u_position": i*4,
                "status": "active", # active, sleep, maintenance
                "cpu_temp": 45.0 + random.uniform(-2, 2),
                "fan_speed": 3500 + random.randint(-100, 100),
                "power_draw": 300 + random.randint(-20, 20),
                "workload": random.randint(30, 80),
                "airflow_cfm": 60.0,
                "health_score": 100.0,
                "vibration_mm_s": 0.2
            } for i in range(1, 11)
        }
        self.physics_engine_enabled = False
        self.thermal_history = []
        self.auto_tune_active = False
        
    def connect_infrastructure(self):
        time.sleep(1.5)
        self.connected = True
        self.sync_active = True
        return True, "Connected to IPMI/Redfish Spatial Bridge (Latency: 8ms)"

    def toggle_physics_engine(self, state: bool):
        self.physics_engine_enabled = state
        return f"Spatial Physics (NVIDIA Omniverse) {'ENABLED' if state else 'DISABLED'}"

    def update_physics_simulation(self):
        if not self.physics_engine_enabled:
            return self.rack_state, []

        alerts = []
        for name, server in self.rack_state.items():
            if server['status'] == 'active':
                # Advanced Thermal Formula
                target_temp = 22 + (server['workload'] ** 1.3) * (6000 / server['fan_speed']) * 0.4
                
                # Apply Auto-Tune dampening if enabled
                if self.auto_tune_active:
                     target_temp -= 5.0
                
                server['cpu_temp'] = (server['cpu_temp'] * 0.7) + (target_temp * 0.3)
                server['vibration_mm_s'] = (server['fan_speed'] / 15000) + random.uniform(0, 0.1)
                server['power_draw'] = (server['workload'] * 5) + (server['fan_speed'] / 10)
                
                # Health Decay simulation
                if server['cpu_temp'] > 80:
                    server['health_score'] = max(0, server['health_score'] - 0.1)
                    if server['health_score'] < 50:
                        alerts.append(f"⚠️ PREDICTIVE FAILURE: {name} (Health: {server['health_score']:.1f}%)")
                
                if server['cpu_temp'] > 85:
                    alerts.append(f"🔥 CRITICAL: {name} Thermal Runaway ({server['cpu_temp']:.1f}°C)")
                    server['fan_speed'] = min(server['fan_speed'] + 800, 15000)
            
            elif server['status'] == 'sleep':
                server['cpu_temp'] = (server['cpu_temp'] * 0.95) + (21.0 * 0.05)
                server['power_draw'] = 12
                server['fan_speed'] = 0
                server['vibration_mm_s'] = 0
                
        return self.rack_state, alerts

    def execute_action(self, asset_id, action):
        target_server = None
        target_key = ""
        for k, v in self.rack_state.items():
            if v['id'] == asset_id:
                target_server = v
                target_key = k
                break
        
        if not target_server: return False, "Asset not found"

        # Normalize action
        cmd = action.upper()
        if cmd == "SHIFT": cmd = "MIGRATE_OUT"

        if cmd == "SLEEP":
            target_server['status'] = 'sleep'
            target_server['workload'] = 0
            return True, f"IPMI Command 0x1A: SLEEP sent to {target_key}."
        elif cmd == "WAKE":
            target_server['status'] = 'active'
            target_server['workload'] = 25
            return True, f"IPMI Command 0x1B: WAKE sent to {target_key}."
        elif cmd == "MIGRATE_OUT":
            target_server['workload'] = 0
            target_server['status'] = 'maintenance'
            return True, f"vMotion Evacuation: {target_key} workloads moved to Cluster-Omega."
        return False, f"Unknown Command: {action}"

    def get_spatial_thermal_data(self, selected_id=None):
        """Returns 3D point data for spatial visualization (X, Y, Z, Temp, Size)."""
        data = []
        for i in range(1, 11):
            key = f"Server_{i}"
            srv = self.rack_state[key]
            temp = srv['cpu_temp']
            is_selected = (srv['id'] == selected_id)
            
            # Map to 3D grid: X=Slot Depth, Y=Width, Z=Height (U-Pos)
            for x in range(3): 
                for y in range(3):
                    data.append({
                        'X': x, 'Y': y, 'Z': i * 4,
                        'Temperature': temp + random.uniform(-0.5, 0.5),
                        'Status': srv['status'].upper(),
                        'Highlight': 'TARGET' if is_selected else 'NORMAL',
                        'Point_Size': 15 if is_selected else 5
                    })
        return pd.DataFrame(data)

    def get_thermal_matrix(self):
        matrix = []
        for i in range(1, 11):
            key = f"Server_{11-i}"
            if 11-i < 1: key = "Server_1"
            temp = self.rack_state.get(key, {}).get('cpu_temp', 22)
            row = [temp + random.uniform(-1,1) for _ in range(4)]
            matrix.append(row)
        return pd.DataFrame(matrix, columns=["Intake", "Core_A", "Core_B", "Exhaust"])
