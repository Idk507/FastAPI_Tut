from fastapi import APIRouter,FastAPI,status,Response
from typing import Optional
from enum import Enum
from router.blog_post import required_functionality
from pydantic import BaseModel


app = FastAPI()

router = APIRouter(prefix = '/blog',
                   tags = ['blog'])

# @app.get('/all')
# def get_all_blogs():
#   return {'message': 'All blogs provided'}

@router.get('/all',summary = "Retrieve all blogs",description = "This api call simulates fetching all blogs",response_description = "The list of available blogs")
def get_blogs(page = 1, page_size: Optional[int] = None,req_parameter: dict = Depends(required-functioanlity)):
  return {'message': f'All {page_size} blogs on page {page}','req': req_parameter'} '}

@router.get('/{id}/comments/{comment_id}',tags = ['comment'])
def get_comment(id :int, comment_id : int,valid:bool = True, username: Optional[str] = None):
  """Simulates retrieving a comment of a blog
  - **id**: The blog id
  - **comment_id**: The comment id
  -**bool** optional query parameter
  - **username** optional query parameter
  """
  return {'message' : f'blog{id},comment_id {comment_id},valid {valid},username {username}'}

class BlogType(str,Enum):
  short = 'short'
  story = 'story'
  howto = 'howto'


@router.get('/type/{type}')
def get_blog_type(type : BlogType):
  return {'message': f'BlogType{type}'}

@router.get('/{id}',status_code = status.HTTP_200_OK)
def get_blog(id : int, response: Response):
  if id > 5:
    response.statust_Code = status.HTTP_404_NOT_FOUND
    return {'error': 'Blog not found'}
  else:
    response.status_code = status.HTTP_200_OK
    return {'message': f'Blog {id}'}         
  