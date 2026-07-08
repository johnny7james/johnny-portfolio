from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

app = FastAPI(
    title="Johnny Dietz Portfolio",
    description="Personal portfolio server for Johnny Dietz.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/health")
async def health_check():
    return JSONResponse(
        {
            "status": "online",
            "project": "Johnny Dietz Portfolio",
            "server": "FastAPI",
        }
    )


@app.get("/")
async def home():
    return FileResponse(TEMPLATES_DIR / "index.html")


@app.get("/resume")
async def resume_page():
    return FileResponse(TEMPLATES_DIR / "resume.html")


@app.get("/projects/{project_slug}")
async def project_detail(project_slug: str):
    project_path = TEMPLATES_DIR / "projects" / f"{project_slug}.html"

    if not project_path.exists():
        return JSONResponse(
            {
                "message": "Project page not found.",
                "project": project_slug,
            },
            status_code=404,
        )

    return FileResponse(project_path)



@app.get("/robots.txt")
async def robots_txt():
    return FileResponse(STATIC_DIR / "robots.txt")


@app.get("/sitemap.xml")
async def sitemap_xml():
    return FileResponse(STATIC_DIR / "sitemap.xml")


@app.exception_handler(404)
async def custom_404_handler(request, exc):
    return FileResponse(TEMPLATES_DIR / "404.html", status_code=404)


@app.get("/checklist")
async def checklist_page():
    return FileResponse(TEMPLATES_DIR / "checklist.html")
