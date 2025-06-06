from schemas.base import MyBaseModel


class ExcBaseS(MyBaseModel):
    msg: str
    code: int
