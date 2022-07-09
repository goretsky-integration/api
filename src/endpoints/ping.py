from fastapi import APIRouter, status, Response

router = APIRouter(tags=['Utils'])


@router.get(path='/ping')
async def ping():
    return Response(status_code=status.HTTP_200_OK)
