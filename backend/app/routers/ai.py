from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.ai_generator_service import (
    generate_content,
    get_available_templates,
)

router = APIRouter(prefix="/ai", tags=["AI Content Generation"])


class GenerateRequest(BaseModel):
    template_type: str
    context: Dict[str, Any] = {}


class GenerateResponse(BaseModel):
    success: bool
    template_type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    generated_at: Optional[str] = None


@router.post("/generate", response_model=GenerateResponse, summary="生成AI内容")
async def generate_ai_content(request: GenerateRequest):
    result = await generate_content(request.template_type, request.context)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "生成失败"))
    
    return result


@router.get("/templates", summary="获取可用模板列表")
async def get_templates():
    templates = get_available_templates()
    return {
        "success": True,
        "templates": templates,
        "total": len(templates),
    }


@router.get("/templates/{template_type}", summary="获取模板详情")
async def get_template_detail(template_type: str):
    templates = get_available_templates()
    template = next((t for t in templates if t["type"] == template_type), None)
    
    if not template:
        raise HTTPException(status_code=404, detail=f"模板不存在: {template_type}")
    
    return {
        "success": True,
        "template": template,
    }
