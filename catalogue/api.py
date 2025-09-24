import math
from . import database as db
from . import schemas
from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session

db.Base.metadata.create_all(bind=db.engine, checkfirst=True)

app = FastAPI()


@app.get("/manufacturers", response_model=schemas.ManufacturersResponse)
async def fetch_manufacturers(
    *,
    q: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1, le=100),
    session: Session = Depends(db.get_session),
) -> schemas.ManufacturersResponse:
    filtered = db.select_manufacturers(session, q=q)
    paginated = db.paginate(filtered, page=page, per_page=per_page)

    return schemas.ManufacturersResponse(
        meta=schemas.Meta(
            current_page=page,
            page_count=math.ceil(filtered.count() / per_page) + 1,
        ),
        manufacturers=paginated.all(),
    )


@app.get("/manufacturers/{manufacturer_id}/categories", response_model=schemas.CategoriesResponse)
async def fetch_manufacturer_categories(
    manufacturer_id: int,
    *,
    q: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1, le=100),
    session: Session = Depends(db.get_session),
) -> schemas.CategoriesResponse:
    filtered = db.select_categories(session, manufacturer_id=manufacturer_id, q=q)
    paginated = db.paginate(filtered, page=page, per_page=per_page)

    return schemas.CategoriesResponse(
        meta=schemas.Meta(
            current_page=page,
            page_count=math.ceil(filtered.count() / per_page) + 1,
        ),
        categories=paginated.all(),
    )


@app.get("/categories/{category_id}/models", response_model=schemas.ModelsResponse)
async def fetch_category_models(
    category_id: int,
    *,
    q: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1, le=100),
    session: Session = Depends(db.get_session),
) -> schemas.ModelsResponse:
    filtered = db.select_models(session, category_id=category_id, q=q)
    paginated = db.paginate(filtered, page=page, per_page=per_page)

    return schemas.ModelsResponse(
        meta=schemas.Meta(
            current_page=page,
            page_count=math.ceil(filtered.count() / per_page) + 1,
        ),
        models=paginated.all(),
    )


@app.get("/models/{model_id}/parts", response_model=schemas.PartsResponse)
async def fetch_model_parts(
    model_id: int,
    *,
    q: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1, le=100),
    session: Session = Depends(db.get_session),
) -> schemas.PartsResponse:
    filtered = db.select_parts(session, model_id=model_id, q=q)
    paginated = db.paginate(filtered, page=page, per_page=per_page)

    return schemas.PartsResponse(
        meta=schemas.Meta(
            current_page=page,
            page_count=math.ceil(filtered.count() / per_page) + 1,
        ),
        parts=paginated.all(),
    )
