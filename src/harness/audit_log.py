# src/harness/audit_log.py

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class AuditLogger:
    """Harness：审计日志器"""
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id
        self.logs: List[Dict[str, Any]] = []
    
    def log(self, event: str, data: Dict[str, Any]):
        """记录事件"""
        entry = {
            "session_id": self.session_id,
            "event": event,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.logs.append(entry)
    
    def get_trail(self) -> List[Dict[str, Any]]:
        """获取完整审计轨迹"""
        return sorted(self.logs, key=lambda x: x["timestamp"])
