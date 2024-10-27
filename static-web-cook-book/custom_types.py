from pydantic import BaseModel, HttpUrl
from typing import Dict


class PagePaths(BaseModel):
    root: HttpUrl
    home: str
    about: str
    contact: str
    login: str
    dashboard: str


class Selectors(BaseModel):
    cssSelectors: Dict[str, str]
    xPaths: Dict[str, str]
    ids: Dict[str, str]
    names: Dict[str, str]
    linkTexts: Dict[str, str]
    partialLinkTexts: Dict[str, str]
    tagNames: Dict[str, str]
    classNames: Dict[str, str]


class ScrapingConfig(BaseModel):
    pages: PagePaths
    selectors: Selectors
