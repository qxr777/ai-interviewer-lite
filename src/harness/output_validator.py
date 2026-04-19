# src/harness/output_validator.py

import yaml
from typing import Dict, Any, Tuple, List


class OutputValidator:
    """Harness：输出验证器"""
    
    def __init__(self, schema_path: str):
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = yaml.safe_load(f)
    
    def validate(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """验证数据是否符合 Schema"""
        errors = []
        
        # 检查必填字段
        for field in self.schema.get("required", []):
            if field not in data:
                errors.append(f"缺少必填字段：{field}")
        
        # 检查类型
        for field, spec in self.schema.get("properties", {}).items():
            if field in data:
                value = data[field]
                expected_type = spec.get("type")
                
                if expected_type == "string" and not isinstance(value, str):
                    errors.append(f"{field} 应该是字符串")
                elif expected_type == "array" and not isinstance(value, list):
                    errors.append(f"{field} 应该是数组")
                elif expected_type == "integer" and not isinstance(value, int):
                    errors.append(f"{field} 应该是整数")
                
                # 最小长度/数量检查
                if expected_type == "string" and "min_length" in spec:
                    if len(value) < spec["min_length"]:
                        errors.append(f"{field} 长度不能小于 {spec['min_length']}")
                
                if expected_type == "array" and "min_items" in spec:
                    if len(value) < spec["min_items"]:
                        errors.append(f"{field} 至少需要 {spec['min_items']} 项")
        
        return len(errors) == 0, errors
