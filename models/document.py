from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timedelta
from typing import List, Optional

class LegalDocument(BaseModel):
    """Модель процессуального документа с валидацией"""
    
    # Основные поля
    document_type: str = Field(..., description="Тип: исковое, ходатайство, жалоба")
    court_name: str = Field(..., description="Наименование суда")
    plaintiff: str = Field(..., description="Истец/Заявитель")
    defendant: str = Field(..., description="Ответчик")
    
    # Даты и сроки
    incident_date: datetime = Field(..., description="Дата события (нарушения)")
    filing_date: datetime = Field(default_factory=datetime.now, description="Дата подачи")
    
    # Содержание
    claims: List[str] = Field(..., description="Требования")
    legal_basis: List[str] = Field(..., description="Ссылки на статьи закона")
    
    # Результаты проверки
    risk_flags: List[str] = Field(default_factory=list, description="Предупреждения")
    is_valid: bool = False
    
    @field_validator("incident_date")
    def check_limitation_period(cls, v):
        """Проверка срока исковой давности (ГК РФ ст. 196: 3 года)"""
        limitation_end = v + timedelta(days=3*365)
        if datetime.now() > limitation_end:
            # Не блокируем, но добавляем флаг
            return v  # Возвращаем дату, но флаг добавим позже
        return v
    
    def validate_full(self) -> dict:
        """Полная проверка документа"""
        errors = []
        warnings = []
        
        # 1. Проверка срока исковой давности
        if datetime.now() > self.incident_date + timedelta(days=3*365):
            warnings.append("⚠️ Срок исковой давности (3 года) может быть истёк. Требуется обоснование перерыва/приостановления (ст. 202-205 ГК РФ)")
        
        # 2. Проверка реквизитов суда
        if "арбитражный" in self.court_name.lower() and "гражданин" in self.plaintiff.lower():
            warnings.append("⚠️ Проверьте подсудность: споры с участием граждан часто в судах общей юрисдикции (ГПК), а не арбитражных (АПК)")
        
        # 3. Минимальный чек-лист по ст. 131 ГПК
        required_fields = ["court_name", "plaintiff", "defendant", "claims"]
        for field in required_fields:
            if not getattr(self, field):
                errors.append(f"❌ Отсутствует обязательное поле: {field}")
        
        # Итог
        self.is_valid = len(errors) == 0
        self.risk_flags = warnings
        
        return {
            "valid": self.is_valid,
            "errors": errors,
            "warnings": warnings,
            "checklist": {
                "✅ Срок давности": "проверен",
                "✅ Подсудность": "проверена", 
                "✅ Реквизиты": "проверены"
            }
        }