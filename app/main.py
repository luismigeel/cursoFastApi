import json
from typing import Optional, Any

from fastapi import APIRouter, FastAPI, HTTPException, status, Request
from fastapi.templating import Jinja2Templates

from pathlib import Path


#local imports
from app.schemas import Recipe, RecipeSearchResults, RecipeCreate
from app.recipes import RECIPES


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

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
async def root( request : Request) -> dict:
    """_summary_

    Returns:
        dict: _description_
    """
    context={
        "request" : request,
        "recipes": RECIPES
    }
    return TEMPLATES.TemplateResponse("index.html",
                                      context)


@api_route.get(path="/recipe/{id_recipe}",
               status_code=status.HTTP_200_OK,
               response_model=Recipe,
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
        return result[0]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="item doesnotexist")


@api_route.get(path="/recipe/",
               status_code=status.HTTP_200_OK,
               summary=["Get all Recipes"],
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

@api_route.post(path="/recipe/",
                status_code=status.HTTP_201_CREATED,
                response_model=Recipe,
                summary=["Create new recipe"],
                tags=["root"])
def createRecipe(*, recipe_in: RecipeCreate) ->dict:
    """_summary_

    Args:
        recipe_in (RecipeCreate): _description_

    Returns:
        dict: _description_
    """
    with open("app/json/recipes.json", "r+", encoding="utf-8") as f:
        data = json.loads(f.read())
        
    new_entry_id = len(data) + 1
    
    #recipe entry 
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source = recipe_in.source,
        url=recipe_in.url
    )
    data.append(recipe_entry.dict())
    return recipe_entry
    

#new addition, query parameter
@api_route.get(path="/search/",
               status_code=status.HTTP_200_OK,
               response_model=RecipeSearchResults,
               summary=["Search a recipe"],
               tags=["root"])
def getByQuery(keyword: Optional[str] = None,
               max_results: Optional[int] = 10)-> dict:
    """_summary_

    Args:
        keyword (Optional[str], optional): _description_. Defaults to None.
        max_results (Optional[int], optional): _description_. Defaults to 10.

    Returns:
        dict: _description_
    """
    with open("app/json/recipes.json", "r+", encoding="utf-8") as f:
        data = json.loads(f.read())
    
    if not keyword:
        return {"results": data[:max_results]}
    else:
        results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), data)  # 7
        return {"results": list(results)[:max_results]}  


app.include_router(api_route)