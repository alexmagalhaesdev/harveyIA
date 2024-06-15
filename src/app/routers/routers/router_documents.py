from fastapi import APIRouter, Request, File, UploadFile, status, HTTPException
from core.ui_config import templates
from utils.storage import Storage

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def list_all_documents(request: Request):
    documents = Storage.list_objects_in_bucket()
    return templates.TemplateResponse(
        "pages/documents.html", {"request": request, "documents": documents}
    )


@router.post("/")
async def upload_document(request: Request, file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        Storage.upload_to_s3(
            object_data=file_content,
            file_path=file.filename,
        )
        return templates.TemplateResponse(
            "pages/documents.html",
            {
                "request": request,
                "message": f"File '{file.filename}' uploaded successfully.",
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
def delete_document(document_id: str, request: Request):
    try:
        Storage.delete_from_s3(file_path=document_id)
        return templates.TemplateResponse(
            "pages/documents.html",
            {
                "request": request,
                "message": f"Document with ID '{id}' deleted successfully.",
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
