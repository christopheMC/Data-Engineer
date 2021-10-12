from pydantic import BaseModel
from enum import Enum
from pydantic import BaseModel


class Source(str, Enum):
    seo = "SEO"
    ads = "Ads"
    direct = "Direct"


class Browser(str, Enum):
    chrome = "Chrome"
    opera = "Opera"
    safari = "Safari"
    ie = "IE"
    firefox = "FireFox"


class Sex(str, Enum):
    male = "M"
    female = "F"


class Features(BaseModel):
    user_id: int
    signup_time: str
    purchase_time: str
    purchase_value: int
    device_id: str
    source: Source
    browser: Browser
    sex: Sex
    age: int
    ip_address: float

    class Config:
        use_enum_values = True
        extra = "forbid"


class Prediction(BaseModel):
    prediction: int
    proba: float