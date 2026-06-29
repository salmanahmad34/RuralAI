import uvicorn
from api.main import app
from config.settings import settings

if __name__ == "__main__":
    # Servers MUST listen on localhost (127.0.0.1) when testing.
    # Servers MUST NOT listen on 0.0.0.0.
    # TODO(security): Bind only to secure interfaces.
    host_ip = "127.0.0.1" if settings.environment == "development" else settings.host
    
    uvicorn.run(
        "api.main:app",
        host=host_ip,
        port=settings.port,
        reload=(settings.environment == "development")
    )
