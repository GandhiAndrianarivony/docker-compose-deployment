from pydantic import BaseModel
from datetime import datetime, date


class EisaModel(BaseModel):
    daty: date
    start_date: datetime
    end_date: datetime
    submission_date: date
    anarana: str
    fanampiny: str
    lahy_sa_vavy: str
    taona: str
    asa: str
    asa_anarana: str
    distrika: str
    fokotany: str
    kaominina: str
    adiresy: str
    nisoratra_anaty_lisitra: str
    antony_nisoratra_anaty_lisitra_tsia: str
    efa_nifidy: str
    antony_efa_nifidy_tsia: str
    hamporisika_tanora_hifidy: str
    hamporisika_vehivavy_hifidy: str
    anarana_fanilo: list
    instanceID: str
    form_id: str
    userform_id: str
    attachments: list
    geolocation: list
    kuser: str


    class Config:
        arbitrary_types_allowed = True
