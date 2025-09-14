from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from cognitive_substrate import EnvironmentalSignal, MindState, AriaCore 
from datetime import datetime
import asyncio
import boto3

# Global Aria instance
aria = AriaCore()

# FastAPI app
app = FastAPI(title="Aria Mind API", description="API for Aria's autonomous reasoning system")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Start Aria's mind when the server starts"""
    asyncio.create_task(aria.mind_loop())

@app.on_event("shutdown")
async def shutdown_event():
    """Gracefully stop Aria's mind"""
    aria.stop_mind()

@app.post("/environmental_signal")
async def add_environmental_signal(signal: EnvironmentalSignal):
    """Add a signal to Aria's environment - she'll notice when ready"""
    signal_id = aria.add_environmental_signal(signal)
    return {
        "message": "Signal added to environment",
        "signal_id": signal_id,
        "pending_signals": len(aria.environmental_signals)
    }

@app.get("/mind_state", response_model=MindState)
async def get_mind_state():
    """Get current snapshot of Aria's mind"""
    return aria.get_mind_state()

@app.get("/stream")
async def stream_mind_state():
    """Real-time stream of Aria's mind state changes"""
    async def generate():
        last_state = None
        while True:
            current_state = aria.get_mind_state()
            if current_state != last_state:
                yield f"data: {current_state.json()}\n\n"
                last_state = current_state
            await asyncio.sleep(1)  # Check for updates every second
    
    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/")
async def root():
    return {
        "message": "Aria Mind API",
        "status": "Aria is thinking..." if aria.running else "Aria is sleeping",
        "pending_signals": len(aria.environmental_signals),
    }

# Additional debugging endpoints
@app.post("/debug/wake_aria")
async def wake_aria():
    if not aria.running:
        asyncio.create_task(aria.mind_loop())
        return {"message": "Aria is waking up..."}
    return {"message": "Aria is already awake"}

@app.post("/debug/aria_sleep")
async def aria_sleep():
    if aria.running:
        aria.stop_mind()
        return {"message": "Aria is going to sleep..."}
    return {"message": "Aria is already asleep"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        
        # Check AWS connectivity (simple test)
        aws_accessible = True
        try:
            # Try to create a Bedrock client as a connectivity test
            boto3.client("bedrock-runtime")
        except Exception as e:
            aws_accessible = False
            aws_error = str(e)
        
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "aws_connectivity": "ok" if aws_accessible else "failed",
                "mind_loop_running": aria.running,
                "environmental_signals_pending": len(aria.environmental_signals)
            }
        }
        
        status_code = 200 if health_status["status"] == "healthy" else 503
        return JSONResponse(content=health_status, status_code=status_code)
        
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            },
            status_code=500
        )

@app.get("/metrics")
async def get_metrics():
    """Basic metrics endpoint"""
    try:
        return {
            "mind_cycles_completed": aria.step,
            "environmental_signals_pending": len(aria.environmental_signals),
            "mind_loop_running": aria.running,
            "last_updated": aria.last_updated.isoformat(),
            "uptime_seconds": (datetime.now() - aria.last_updated).total_seconds()
        }
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )