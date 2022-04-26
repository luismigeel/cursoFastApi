import json
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi import status

#create entry point
app = FastAPI(
    title="Recipe API",
    openapi_url="/openapi.json"
)


#create route
api_route = APIRouter()


@api_route.get(path='/',
               status_code=status.HTTP_200_OK,
               summary=["this a root"],
               tags=["root"])
async def root() -> dict:
    """_summary_

    Returns:
        dict: _description_
    """
    return {'message': 'Hello World'}


@api_route.get(path="/recipe/{id_recipe}",
               status_code=status.HTTP_200_OK,
               summary=["Get recipe byId"],
               tags=["root"])
def getById(*, id_recipe: int)-> dict:
    """_summary_

    Args:
        id_recipe (int): _description_

    Returns:
        dict: _description_
    """
    with open("app/json/recipes.json", "r+", encoding="utf-8") as f:
        data = json.loads(f.read())
        
    result = [recipe for recipe in data if recipe["id"] == id_recipe]
    
    if result != []:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="item doesnotexist")


@api_route.get(path="/recipe/",
               status_code=status.HTTP_200_OK,
               summary=["Get recipes"],
               tags=["root"])
def getAll()-> list:
    """_summary_

    Raises:
        HTTPException: _description_

    Returns:
        list: _description_
    """
    with open("app/json/recipes.json", "r+", encoding="utf-8") as f:
        data = json.loads(f.read())
        
    # result = [recipe for recipe in data if recipe["id"] == id_recipe]
    
    if data != []:
        return data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="item doesnotexist")


app.include_router(api_route)