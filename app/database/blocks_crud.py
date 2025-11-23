from fastapi import HTTPException, status
from sqlmodel import Session, select
from .models import Block


def get_all_blocks(session: Session):
    """Hae kaikki lohkot"""
    blocks = session.exec(select(Block)).all()
    return blocks


def create_block(session: Session, block_name: str):
    """Luo uusi lohko"""
    existing = session.exec(select(Block).where(Block.name == block_name)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{block_name} nimi on jo käytössä."
        )
    
    block = Block(name=block_name)
    session.add(block)
    session.commit()
    session.refresh(block)
    return block


def get_block_by_id(session: Session, block_id: int):
    """Hae lohko id:llä"""
    block = session.get(Block, block_id)
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lohko id:llä {block_id} ei löydy."
        )
    return block
