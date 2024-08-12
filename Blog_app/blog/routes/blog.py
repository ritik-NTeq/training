from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from ..models import Blog
from ..database import get_db
from typing import List
from ..oauth2 import get_current_user

router = APIRouter(prefix="/blog", tags=["Blogs"], dependencies=[Depends(get_current_user)])

@router.get("/", status_code=200, response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body, user_id=1)
    try:
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
    except Exception as e:
        print("Unable to add new blog to DB!")
    return new_blog

@router.get("/{blog_id}", status_code=200, response_model=schemas.ShowBlog)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {blog_id} not found!")
    return blog

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {blog_id} not found!")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'Done'}


@router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {blog_id} not found!")
    blog.update(request)
    db.commit()
    return {'detail':f'Updated {blog_id}!'}