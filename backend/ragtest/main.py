#!/usr/bin/env python3
"""
GraphRAG API - Versión Híbrida Robusta
Emula la estructura profesional pero con fallbacks CLI para evitar bugs
Ejecutar desde: ~/proyectos/interno/graphrag/graphragnew/graphrag-main/ragtest
"""

import asyncio
import subprocess
import json
import time
from pathlib import Path
from typing import Union, List, Dict, Any, Optional
import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configuración
PROJECT_DIRECTORY = "."  # Ya estamos en ragtest
COMMUNITY_LEVEL = 2
CLAIM_EXTRACTION_ENABLED = False
RESPONSE_TYPE = "Multiple Paragraphs"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Intentar importar GraphRAG API
try:
    import graphrag.api as api
    from graphrag.config.load_config import load_config
    GRAPHRAG_API_AVAILABLE = True
    logger.info("✅ GraphRAG API imports exitosos")
except ImportError as e:
    GRAPHRAG_API_AVAILABLE = False
    logger.warning(f"⚠️ GraphRAG API no disponible: {e}")
    logger.info("🔄 Usando fallback CLI")

# Utilidades para procesar context data
def convert_response_to_string(response: Union[str, Dict[str, Any], List[Dict[str, Any]]]) -> str:
    """Convert a response to string format"""
    if isinstance(response, (dict, list)):
        return json.dumps(response, indent=2)
    elif isinstance(response, str):
        return response
    else:
        return str(response)

def recursively_convert(obj: Any) -> Any:
    """Recursively convert pandas objects to serializable format"""
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict(orient="records")
    elif isinstance(obj, list):
        return [recursively_convert(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: recursively_convert(value) for key, value in obj.items()}
    return obj

def process_context_data(context_data: Union[str, List[pd.DataFrame], Dict, pd.DataFrame]) -> Any:
    """Process context data for JSON serialization"""
    if isinstance(context_data, str):
        return context_data
    if isinstance(context_data, pd.DataFrame):
        return context_data.to_dict(orient="records")
    if isinstance(context_data, (list, dict)):
        return recursively_convert(context_data)
    return None

# Fallback CLI functions
async def execute_cli_search(query: str, method: str, **kwargs) -> Dict[str, Any]:
    """Execute GraphRAG search via CLI as fallback"""
    start_time = time.time()
    
    cmd = [
        "graphrag", "query",
        "--root", ".",
        "--method", method,
        "--query", query
    ]
    
    if "community_level" in kwargs:
        cmd.extend(["--community_level", str(kwargs["community_level"])])
    if "response_type" in kwargs:
        cmd.extend(["--response_type", kwargs["response_type"]])
    
    logger.info(f"🔄 CLI Fallback: {' '.join(cmd[:6])}...")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd="."
        )
        
        execution_time = time.time() - start_time
        
        if result.returncode == 0:
            response_text = result.stdout.strip()
            
            # Extract clean response
            if "SUCCESS:" in response_text:
                response_parts = response_text.split("SUCCESS:")
                if len(response_parts) > 1:
                    response_text = response_parts[-1].strip()
                    if response_text.startswith(("Local Search Response:", "Global Search Response:")):
                        response_text = "\n".join(response_text.split("\n")[1:]).strip()
            
            return {
                "response": response_text,
                "context_data": {"method": "cli_fallback", "execution_time": execution_time},
                "success": True,
                "method_used": "cli"
            }
        else:
            return {
                "response": f"CLI Error: {result.stderr}",
                "context_data": {"error": result.stderr},
                "success": False,
                "method_used": "cli"
            }
            
    except Exception as e:
        return {
            "response": f"CLI Exception: {str(e)}",
            "context_data": {"error": str(e)},
            "success": False,
            "method_used": "cli"
        }

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("🚀 Iniciando GraphRAG API...")
    
    # Cargar datos
    try:
        if GRAPHRAG_API_AVAILABLE:
            logger.info("📋 Cargando configuración GraphRAG...")
            app.state.config = load_config(Path(PROJECT_DIRECTORY))
            
            logger.info("📊 Cargando archivos parquet...")
            app.state.entities = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/entities.parquet")
            app.state.communities = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/communities.parquet")
            app.state.community_reports = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/community_reports.parquet")
            app.state.text_units = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/text_units.parquet")
            app.state.relationships = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/relationships.parquet")
            
            # Covariates (opcional)
            try:
                app.state.covariates = pd.read_parquet(f"{PROJECT_DIRECTORY}/output/covariates.parquet") if CLAIM_EXTRACTION_ENABLED else None
            except:
                app.state.covariates = None
                logger.info("ℹ️ Covariates no disponibles")
            
            logger.info(f"✅ Datos cargados: {len(app.state.entities)} entidades, {len(app.state.relationships)} relaciones")
            app.state.data_loaded = True
        else:
            logger.info("⚠️ GraphRAG API no disponible, usando solo CLI fallback")
            app.state.data_loaded = False
            
    except Exception as e:
        logger.error(f"❌ Error cargando datos: {e}")
        app.state.data_loaded = False
    
    yield
    
    logger.info("👋 Cerrando GraphRAG API...")

app = FastAPI(
    title="GraphRAG API",
    description="API robusta para GraphRAG con fallbacks CLI",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search/global")
async def global_search(query: str = Query(..., description="Global Search")):
    """Global search with API + CLI fallback"""
    logger.info(f"🌍 Global search: {query}")
    
    # Intentar con API primero
    if GRAPHRAG_API_AVAILABLE and app.state.data_loaded:
        try:
            logger.info("🔄 Intentando GraphRAG API...")
            response, context = await api.global_search(
                config=app.state.config,
                entities=app.state.entities,
                communities=app.state.communities,
                community_reports=app.state.community_reports,
                community_level=COMMUNITY_LEVEL,
                dynamic_community_selection=False,
                response_type=RESPONSE_TYPE,
                query=query,
            )
            
            response_dict = {
                "response": response,
                "context_data": process_context_data(context),
                "method_used": "api",
                "success": True
            }
            logger.info("✅ Global search API exitosa")
            return JSONResponse(content=response_dict)
            
        except Exception as e:
            logger.warning(f"⚠️ GraphRAG API falló: {e}")
            logger.info("🔄 Usando CLI fallback...")
    
    # Fallback CLI
    result = await execute_cli_search(
        query=query, 
        method="global",
        community_level=COMMUNITY_LEVEL,
        response_type=RESPONSE_TYPE
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["response"])
    
    return JSONResponse(content=result)

@app.get("/search/local")
async def local_search(query: str = Query(..., description="Local Search")):
    """Local search with API + CLI fallback"""
    logger.info(f"🎯 Local search: {query}")
    
    # Intentar con API primero
    if GRAPHRAG_API_AVAILABLE and app.state.data_loaded:
        try:
            logger.info("🔄 Intentando GraphRAG API...")
            response, context = await api.local_search(
                config=app.state.config,
                entities=app.state.entities,
                communities=app.state.communities,
                community_reports=app.state.community_reports,
                text_units=app.state.text_units,
                relationships=app.state.relationships,
                covariates=app.state.covariates,
                community_level=COMMUNITY_LEVEL,
                response_type=RESPONSE_TYPE,
                query=query,
            )
            
            response_dict = {
                "response": response,
                "context_data": process_context_data(context),
                "method_used": "api",
                "success": True
            }
            logger.info("✅ Local search API exitosa")
            return JSONResponse(content=response_dict)
            
        except Exception as e:
            logger.warning(f"⚠️ GraphRAG API falló: {e}")
            logger.info("🔄 Usando CLI fallback...")
    
    # Fallback CLI
    result = await execute_cli_search(
        query=query, 
        method="local",
        community_level=COMMUNITY_LEVEL,
        response_type=RESPONSE_TYPE
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["response"])
    
    return JSONResponse(content=result)

@app.get("/search/drift")
async def drift_search(query: str = Query(..., description="DRIFT Search")):
    """DRIFT search with API + CLI fallback"""
    logger.info(f"🌊 DRIFT search: {query}")
    
    # Intentar con API primero
    if GRAPHRAG_API_AVAILABLE and app.state.data_loaded:
        try:
            logger.info("🔄 Intentando GraphRAG API...")
            response, context = await api.drift_search(
                config=app.state.config,
                entities=app.state.entities,
                communities=app.state.communities,
                community_reports=app.state.community_reports,
                text_units=app.state.text_units,
                relationships=app.state.relationships,
                community_level=COMMUNITY_LEVEL,
                response_type=RESPONSE_TYPE,
                query=query,
            )
            
            response_dict = {
                "response": response,
                "context_data": process_context_data(context),
                "method_used": "api",
                "success": True
            }
            logger.info("✅ DRIFT search API exitosa")
            return JSONResponse(content=response_dict)
            
        except Exception as e:
            logger.warning(f"⚠️ GraphRAG API falló: {e}")
            logger.info("🔄 Usando CLI fallback...")
    
    # DRIFT no tiene equivalente CLI directo, usar local como fallback
    result = await execute_cli_search(
        query=query, 
        method="local",  # Fallback a local
        community_level=COMMUNITY_LEVEL,
        response_type=RESPONSE_TYPE
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["response"])
    
    result["method_used"] = "cli_local_fallback"
    return JSONResponse(content=result)

@app.get("/search/basic")
async def basic_search(query: str = Query(..., description="Basic Search")):
    """Basic search with API + CLI fallback"""
    logger.info(f"📄 Basic search: {query}")
    
    # Intentar con API primero
    if GRAPHRAG_API_AVAILABLE and app.state.data_loaded:
        try:
            logger.info("🔄 Intentando GraphRAG API...")
            response, context = await api.basic_search(
                config=app.state.config,
                text_units=app.state.text_units,
                query=query,
            )
            
            response_dict = {
                "response": response,
                "context_data": process_context_data(context),
                "method_used": "api",
                "success": True
            }
            logger.info("✅ Basic search API exitosa")
            return JSONResponse(content=response_dict)
            
        except Exception as e:
            logger.warning(f"⚠️ GraphRAG API falló: {e}")
            logger.info("🔄 Usando CLI fallback...")
    
    # Basic search CLI fallback (usar local)
    result = await execute_cli_search(
        query=query, 
        method="local",
        community_level=COMMUNITY_LEVEL,
        response_type=RESPONSE_TYPE
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["response"])
    
    result["method_used"] = "cli_basic_fallback"
    return JSONResponse(content=result)

@app.get("/status")
async def status():
    """Status endpoint with detailed information"""
    return JSONResponse(content={
        "status": "Server is up and running",
        "graphrag_api_available": GRAPHRAG_API_AVAILABLE,
        "data_loaded": getattr(app.state, 'data_loaded', False),
        "fallback_mode": "CLI available" if not GRAPHRAG_API_AVAILABLE else "API + CLI fallback",
        "project_directory": PROJECT_DIRECTORY,
        "community_level": COMMUNITY_LEVEL,
        "response_type": RESPONSE_TYPE
    })

@app.get("/")
async def root():
    """Root endpoint"""
    return await status()

@app.get("/health")
async def health():
    """Simple health check"""
    return {"status": "healthy"}

# Endpoints adicionales para compatibilidad con tu API anterior
@app.get("/query")
async def query_get(
    q: str = Query(..., description="Query"),
    method: str = Query("global", description="Search method")
):
    """Query endpoint for backward compatibility"""
    if method == "global":
        return await global_search(q)
    elif method == "local":
        return await local_search(q)
    elif method == "drift":
        return await drift_search(q)
    elif method == "basic":
        return await basic_search(q)
    else:
        raise HTTPException(status_code=400, detail="Invalid method. Use: global, local, drift, or basic")

if __name__ == "__main__":
    print("🚀 GraphRAG API - Versión Híbrida")
    print("=================================")
    print("📍 http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("🔍 Endpoints:")
    print("  • /search/global")
    print("  • /search/local") 
    print("  • /search/drift")
    print("  • /search/basic")
    print("  • /status")
    print("")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )